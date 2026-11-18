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


def build_prompt(inputs, second_attempt=False):
    """Build a solve prompt; the second attempt uses a distinct, independent check."""
    parts = [
        "Solve this ARC-AGI puzzle. Each grid is a rectangular 2D array of colors 0-9. "
        "All training pairs use the same transformation; infer it and apply it to the test input.",
        "",
    ]
    for i, pair in enumerate(inputs["train"], 1):
        parts.append(f"## Training example {i}")
        grid = pair["input"]
        parts.append(f"Input ({len(grid)}x{len(grid[0])}):")
        parts.append(grid_to_text(grid))
        grid = pair["output"]
        parts.append(f"Output ({len(grid)}x{len(grid[0])}):")
        parts.append(grid_to_text(grid))
        parts.append("")

    test = inputs["test_input"]
    parts.extend([
        "## Test input",
        f"Input ({len(test)}x{len(test[0])}):",
        grid_to_text(test),
        "",
        "Reason carefully before answering: identify what changes and what stays invariant; "
        "check that your proposed rule reproduces EVERY training output exactly; then apply "
        "that same rule to the complete test grid. Do not assume output dimensions equal input "
        "dimensions. Check row/column counts, colors, and every cell of the final grid.",
    ])

    if second_attempt:
        parts.extend([
            "",
            "Solve this independently from the examples; do not assume a first interpretation is correct. "
            "Compare the input-output changes across all examples, consider whether the rule changes "
            "grid size or acts on objects/regions rather than individual cells, and verify your inferred "
            "rule against every training pair before constructing the test output. Check that the final "
            "grid has the correct dimensions and includes every row and cell.",
        ])

    parts.extend([
        "",
        "Return the final output grid inside <answer></answer> tags as a JSON list of integer rows, "
        "for example <answer>[[0, 1], [2, 3]]</answer>. Put nothing else inside the tags.",
    ])
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
    """Extract a valid ARC grid from common tagged, fenced, or plain JSON responses."""
    if not text:
        return None

    # Prefer explicitly marked answers, then fenced blocks. Be tolerant of tag/fence
    # casing and whitespace so harmless formatting differences do not lose a prediction.
    answer_blocks = re.findall(
        r"<\s*answer\s*>(.*?)<\s*/\s*answer\s*>", text, re.DOTALL | re.IGNORECASE
    )
    for block in reversed(answer_blocks):
        grid = _parse_block(block)
        if grid is not None:
            return grid

    fenced_blocks = re.findall(r"```[^\n`]*\n?(.*?)```", text, re.DOTALL)
    for block in reversed(fenced_blocks):
        grid = _parse_block(block)
        if grid is not None:
            return grid

    # Decode JSON arrays at any position rather than relying on a digit-only regex.
    # Advance past each parsed array so nested row arrays are not mistaken for grids;
    # retaining the last valid top-level array preserves the final-answer preference.
    decoder = json.JSONDecoder()
    candidate = None
    index = 0
    while index < len(text):
        if text[index] != "[":
            index += 1
            continue
        try:
            value, end = decoder.raw_decode(text[index:])
        except (json.JSONDecodeError, ValueError):
            index += 1
            continue
        if _valid(value):
            candidate = value
            index += end
        else:
            index += 1
    return candidate


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

    def solve_once(self, inputs, second_attempt=False):
        """One direct model response -> one parsed grid (or None)."""
        prompt = build_prompt(inputs, second_attempt=second_attempt)
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
        # Keep both answers as independent candidates: the grader accepts either, and
        # retaining diversity avoids making the second call depend on a potentially wrong
        # first interpretation. Use a more systematic prompt for the second solve.
        answers = []
        first = None
        try:
            first = self.solve_once(inputs)
        except Exception as e:
            self.log(f"Error on initial solve: {e}")
        if first is not None:
            answers.append(first)

        try:
            second = self.solve_once(inputs, second_attempt=True)
        except Exception as e:
            self.log(f"Error on verification solve: {e}")
            second = None
        if second is not None:
            answers.append(second)
        return answers, []
