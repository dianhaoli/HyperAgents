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


def build_prompt(inputs, independent_attempt=False):
    parts = [
        "You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 "
        "(each integer is a color). The demonstration pairs below share one hidden transformation rule "
        "that maps each input grid to its output grid. Infer the rule and apply it to the test input.",
        "",
    ]
    if independent_attempt:
        parts.extend([
            "Solve this independently using a deliberate grid comparison, not a guess based on one example.",
            "First determine whether the output dimensions change. Compare each training input and output "
            "cell by cell (using row and column positions), noting what stays fixed and what changes. "
            "Look for one simple operation that explains every example, including object shapes, positions, "
            "colors, repetition, symmetry, and boundaries where relevant. Check the operation against all "
            "training pairs before applying it to the test; do not assume unchanged background cells or "
            "the input dimensions without checking.",
            "",
        ])
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


def _valid(g):
    return (isinstance(g, list) and len(g) > 0 and all(isinstance(r, list) and len(r) > 0 for r in g)
            and len({len(r) for r in g}) == 1
            and all(isinstance(v, int) and not isinstance(v, bool) and 0 <= v <= 9 for r in g for v in r))


def infer_exact_grid_transform(inputs):
    """Find an exact geometric/color transform shared by all demonstrations.

    This deliberately covers only the eight rectangle symmetries with an
    optional one-to-one color relabeling. A rule is returned only when every
    demonstration is reproduced exactly and all fitting rules agree on the
    test grid, so uncertain cases remain with the language-model attempts.
    """
    train = inputs.get("train", [])
    test = inputs.get("test_input")
    if not train or not _valid(test):
        return None

    def orientations(grid):
        # Keep dimensions and cell positions exact for non-square grids.
        variants = [grid]
        for _ in range(3):
            prev = variants[-1]
            variants.append([list(row) for row in zip(*prev[::-1])])
        base = list(variants)
        variants.extend([row[::-1] for row in grid] for grid in base)
        # Symmetric inputs may produce duplicate variants; names do not matter.
        return variants

    candidates = set()
    for transform in range(8):
        mapping = {}
        reverse_mapping = {}
        fits = True
        for pair in train:
            src, target = pair.get("input"), pair.get("output")
            if not _valid(src) or not _valid(target):
                fits = False
                break
            oriented = orientations(src)[transform]
            if len(oriented) != len(target) or len(oriented[0]) != len(target[0]):
                fits = False
                break
            for source_row, target_row in zip(oriented, target):
                for source_color, target_color in zip(source_row, target_row):
                    if (source_color in mapping and mapping[source_color] != target_color) or (
                        target_color in reverse_mapping and reverse_mapping[target_color] != source_color
                    ):
                        fits = False
                        break
                    mapping[source_color] = target_color
                    reverse_mapping[target_color] = source_color
                if not fits:
                    break
            if not fits:
                break
        if not fits:
            continue
        oriented_test = orientations(test)[transform]
        if any(color not in mapping for row in oriented_test for color in row):
            continue
        candidates.add(tuple(tuple(mapping[color] for color in row) for row in oriented_test))

    if len(candidates) != 1:
        return None
    return [list(row) for row in next(iter(candidates))]


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

    def solve_once(self, inputs, independent_attempt=False):
        """One model response -> one parsed grid (or None)."""
        prompt = build_prompt(inputs, independent_attempt=independent_attempt)
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
        answers = []
        # Reserve one candidate slot for an exact solver when the demonstrations
        # identify a shared symmetry/color transform unambiguously. Keep one model
        # attempt as a fallback; otherwise use both calls for independent attempts.
        rule_candidate = infer_exact_grid_transform(inputs)
        attempts = (True,) if rule_candidate is not None else (False, True)
        if rule_candidate is not None:
            answers.append(rule_candidate)
        for attempt_number, independent_attempt in enumerate(attempts, start=1):
            try:
                g = self.solve_once(inputs, independent_attempt=independent_attempt)
            except Exception as e:
                self.log(f"Error on attempt {attempt_number}: {e}")
                g = None
            if g is not None:
                answers.append(g)
        return answers, []
