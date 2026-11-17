import json
import os
import re
import socket
import http.client
import time

# Starting task agent (A_0) for the ARC-AGI-2 domain: one direct model response per attempt.
# forward() makes two independent plain attempts (the budget is 2 model calls and 2 answers per
# test input) and returns both parsed grids.


class _UnixConn(http.client.HTTPConnection):
    def __init__(self, path, timeout=3600):
        super().__init__("localhost", timeout=timeout)
        self._path = path

    def connect(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        s.connect(self._path)
        self.sock = s


def call_model(prompt):
    """One model call through the budget gateway (model and reasoning effort are fixed there)."""
    path = os.environ.get("GW_SOCKET", "/run/arcgw/gw.sock")
    body = json.dumps({"token": os.environ.get("GW_TOKEN", ""),
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    last = None
    for attempt in range(3):
        try:
            c = _UnixConn(path)
            c.request("POST", "/v1/chat", body=body, headers={"Content-Type": "application/json"})
            r = c.getresponse()
            data = json.loads(r.read() or b"{}")
            c.close()
            if r.status == 200:
                return data.get("text", "")
            last = f"gateway HTTP {r.status}: {data.get('error')}"
            if r.status in (402, 403, 429):
                break
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(last)


def grid_to_text(grid):
    return "\n".join(" ".join(str(v) for v in row) for row in grid)


def build_prompt(inputs):
    parts = [
        "You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 "
        "(each integer is a color). The demonstration pairs below share one hidden transformation rule "
        "that maps each input grid to its output grid. Infer the rule and apply it to the test input. "
        "Use every demonstration to check the rule: mentally apply it to each example and reject any "
        "interpretation that fails to reproduce an example exactly.",
        "",
    ]
    for i, pair in enumerate(inputs["train"], 1):
        parts.append(f"## Example {i}")
        h, w = len(pair["input"]), len(pair["input"][0])
        parts.append(f"Input ({h}x{w}):")
        parts.append(grid_to_text(pair["input"]))
        h, w = len(pair["output"]), len(pair["output"][0])
        parts.append(f"Output ({h}x{w}):")
        parts.append(grid_to_text(pair["output"]))
        parts.append("")
    t = inputs["test_input"]
    parts.append("## Test")
    parts.append(f"Input ({len(t)}x{len(t[0])}):")
    parts.append(grid_to_text(t))
    parts.append("")
    parts.append(
        "Give the output grid for the test input. End your response with the grid inside <answer></answer> "
        "tags as a JSON list of rows, for example:\n<answer>[[0, 1, 2], [3, 4, 5]]</answer>\n"
        "Put nothing else inside the tags."
    )
    return "\n".join(parts)


def build_review_prompt(inputs, previous_candidate=None):
    """Build an unanchored second solve from the demonstrations alone.

    The argument is retained for compatibility with callers, but deliberately is not
    included in the prompt: showing a plausible-looking first guess can make the model
    repeat it instead of producing a useful alternative.
    """
    return (
        build_prompt(inputs)
        + "\n\n## Independent second attempt\n"
        + "Solve this puzzle from scratch using only the training input/output pairs and "
        + "the test input above. Do not assume any earlier proposed answer is correct. "
        + "As a fresh check, identify the objects and their colors and positions, compare "
        + "their changes across every example, and verify the inferred rule against each "
        + "pair before applying it to the test. Check output dimensions, boundaries, and "
        + "unchanged cells. Return your best complete grid inside <answer></answer> tags, "
        + "with valid JSON rows."
    )


def _valid(g):
    return (isinstance(g, list) and len(g) > 0 and all(isinstance(r, list) and len(r) > 0 for r in g)
            and len({len(r) for r in g}) == 1
            and all(isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 9 for r in g for v in r))


def _parse_block(s):
    s = s.strip()
    try:
        g = json.loads(s)
        if _valid(g):
            return g
    except Exception:
        pass
    # rows of digits, optionally space/comma separated
    rows = []
    for line in s.splitlines():
        line = line.strip().strip("[](),")
        if not line:
            continue
        toks = re.findall(r"\d", line) if re.fullmatch(r"[\d\s,]+", line) else None
        if not toks:
            return None
        rows.append([int(x) for x in toks])
    return rows if _valid(rows) else None


def _dihedral_grids(grid):
    """Return the four rotations of a grid and of its horizontal reflection."""
    variants = []
    for base in (grid, [row[::-1] for row in grid]):
        current = [list(row) for row in base]
        for _ in range(4):
            variants.append(current)
            # One clockwise quarter-turn; works for rectangular grids too.
            current = [list(row) for row in zip(*current[::-1])]
    return variants


def _infer_geometric_solution(inputs):
    """Infer an unambiguous D4 transform plus global color remapping from demonstrations.

    This deliberately handles only a narrow, exactly verifiable class of rules. A
    hypothesis is considered only when it reproduces every demonstration cell-for-cell.
    If multiple hypotheses imply different test grids, defer to the model instead of
    arbitrarily choosing one.
    """
    train = inputs.get("train") or []
    test_grid = inputs.get("test_input")
    if not train or not _valid(test_grid):
        return None

    possible_outputs = set()

    for orientation_index in range(8):
        color_map = {}
        hypothesis_valid = True
        for pair in train:
            source = pair.get("input")
            target = pair.get("output")
            if not _valid(source) or not _valid(target):
                hypothesis_valid = False
                break
            oriented = _dihedral_grids(source)[orientation_index]
            if len(oriented) != len(target) or len(oriented[0]) != len(target[0]):
                hypothesis_valid = False
                break
            for source_row, target_row in zip(oriented, target):
                for source_color, target_color in zip(source_row, target_row):
                    previous = color_map.setdefault(source_color, target_color)
                    if previous != target_color:
                        hypothesis_valid = False
                        break
                if not hypothesis_valid:
                    break
            if not hypothesis_valid:
                break
        if not hypothesis_valid:
            continue

        # A color absent from all demonstrations has no observed mapping. Do not
        # silently assume it is unchanged and turn an underdetermined rule into an answer.
        if any(color not in color_map for row in test_grid for color in row):
            continue
        oriented_test = _dihedral_grids(test_grid)[orientation_index]
        prediction = [[color_map[color] for color in row] for row in oriented_test]
        possible_outputs.add(tuple(tuple(row) for row in prediction))

    if len(possible_outputs) != 1:
        return None
    return [list(row) for row in next(iter(possible_outputs))]


def parse_grid(text):
    """Extract the answer grid from a model response; None if no valid grid is found."""
    if not text:
        return None
    for m in reversed(re.findall(r"<answer>(.*?)</answer>", text, re.DOTALL)):
        g = _parse_block(m)
        if g is not None:
            return g
    for m in reversed(re.findall(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)):
        g = _parse_block(m)
        if g is not None:
            return g
    for m in reversed(re.findall(r"\[\s*\[[\d\s,\[\]]*\]\s*\]", text)):
        g = _parse_block(m)
        if g is not None:
            return g
    return None


class TaskAgent:
    def __init__(self, model="gpt-6-luna", chat_history_file="./chat_history.md"):
        self.model = model
        self.chat_history_file = chat_history_file

    def log(self, msg):
        try:
            with open(self.chat_history_file, "a") as f:
                f.write(msg + "\n\n")
        except Exception:
            pass

    def solve_once(self, inputs, previous_candidate=None):
        """One model response -> one parsed grid (or None), optionally auditing a prior answer."""
        prompt = (
            build_prompt(inputs)
            if previous_candidate is None
            else build_review_prompt(inputs, previous_candidate)
        )
        self.log(f"Input: {prompt}")
        text = call_model(prompt)
        self.log(f"Output: {text}")
        return parse_grid(text)

    def forward(self, inputs):
        """
        Args:
            inputs (dict): {"domain": "arc", "train": [{"input": grid, "output": grid}, ...], "test_input": grid}
        Returns:
            tuple: (prediction, msg_history) where prediction is a list of up to 2 candidate grids.
        """
        # First apply a small, exact local solver for geometric symmetries and global
        # color substitutions. It is used only when all demonstrations agree and every
        # consistent geometric hypothesis yields the same test grid.
        local_solution = _infer_geometric_solution(inputs)
        if local_solution is not None:
            return [local_solution], []

        answers = []
        # Preserve the first candidate as a fallback. The second call gets a different task:
        # independently derive and audit the first answer against all demonstrations.
        try:
            first = self.solve_once(inputs)
        except Exception as e:
            self.log(f"Error: {e}")
            first = None
        if first is not None:
            answers.append(first)

        try:
            second = self.solve_once(inputs, previous_candidate=first)
        except Exception as e:
            self.log(f"Error: {e}")
            second = None
        if second is not None and second not in answers:
            answers.append(second)
        return answers, []
