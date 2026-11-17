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


def _enclosed_cells(grid, background):
    """Return background cells in 4-connected components that do not touch an edge."""
    h, w = len(grid), len(grid[0])
    seen = set()
    enclosed = set()
    for r in range(h):
        for c in range(w):
            if grid[r][c] != background or (r, c) in seen:
                continue
            stack = [(r, c)]
            seen.add((r, c))
            component = []
            touches_edge = False
            while stack:
                y, x = stack.pop()
                component.append((y, x))
                touches_edge |= y == 0 or x == 0 or y == h - 1 or x == w - 1
                for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                    if (0 <= ny < h and 0 <= nx < w and grid[ny][nx] == background
                            and (ny, nx) not in seen):
                        seen.add((ny, nx))
                        stack.append((ny, nx))
            if not touches_edge:
                enclosed.update(component)
    return enclosed


def infer_enclosed_fill(inputs):
    """Infer a globally consistent ARC rule that fills enclosed background regions.

    A candidate is used only when one background/fill-color pair reproduces every
    training output exactly. This gives a deterministic candidate for common
    hollow-object tasks without overriding the model on merely approximate fits.
    """
    train = inputs.get("train", [])
    if not train:
        return None
    for background in range(10):
        for fill in range(10):
            if background == fill:
                continue
            fits = True
            changed_anywhere = False
            for pair in train:
                src, target = pair["input"], pair["output"]
                if (not _valid(src) or not _valid(target) or len(src) != len(target)
                        or len(src[0]) != len(target[0])):
                    fits = False
                    break
                cells = _enclosed_cells(src, background)
                if not cells:
                    fits = False
                    break
                expected = [row[:] for row in src]
                for r, c in cells:
                    expected[r][c] = fill
                if expected != target:
                    fits = False
                    break
                changed_anywhere = True
            if fits and changed_anywhere:
                test = inputs.get("test_input")
                if _valid(test):
                    result = [row[:] for row in test]
                    for r, c in _enclosed_cells(test, background):
                        result[r][c] = fill
                    return result
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
        # Use a small exact-by-demonstrations solver for enclosed-region fill tasks.
        # If it finds a rule that reproduces every training output cell-for-cell,
        # retain it as one candidate and use one model answer as a diverse fallback.
        # Otherwise spend the full two-call budget on independent model attempts.
        rule_candidate = infer_enclosed_fill(inputs)
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
