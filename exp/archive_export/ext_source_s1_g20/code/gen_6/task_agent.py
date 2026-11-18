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


def _expected_output_shape(inputs):
    """Infer a likely test-output shape only when demonstrations agree on it."""
    pairs = inputs.get("train", [])
    if len(pairs) < 2:
        return None

    output_shapes = [(len(pair["output"]), len(pair["output"][0])) for pair in pairs]
    if len(set(output_shapes)) == 1:
        return output_shapes[0]

    # Some tasks preserve a consistent size change rather than a fixed output size.
    deltas = []
    for pair in pairs:
        in_shape = (len(pair["input"]), len(pair["input"][0]))
        out_shape = (len(pair["output"]), len(pair["output"][0]))
        deltas.append((out_shape[0] - in_shape[0], out_shape[1] - in_shape[1]))
    if len(set(deltas)) == 1:
        test = inputs["test_input"]
        return len(test) + deltas[0][0], len(test[0]) + deltas[0][1]
    return None


def build_prompt(inputs, candidate=None, independent_check=False):
    parts = [
        "You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 "
        "(each integer is a color). The demonstration pairs below share one hidden transformation rule "
        "that maps each input grid to its output grid. Infer the rule and apply it to the test input.",
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
    expected_shape = _expected_output_shape(inputs)
    if expected_shape is not None:
        parts.append(
            f"Shape check: the demonstrations consistently imply an output of "
            f"{expected_shape[0]} rows by {expected_shape[1]} columns for this test. "
            "Use that dimension as a verification constraint; count rows and cells per row "
            "before finalizing, and only depart from it if the demonstrated rule requires it."
        )
    if candidate is not None:
        actual_shape = (len(candidate), len(candidate[0]))
        if expected_shape is not None and actual_shape != expected_shape:
            parts.append(
                f"The previous candidate has {actual_shape[0]} rows by {actual_shape[1]} columns, "
                f"which conflicts with the demonstrated {expected_shape[0]}x{expected_shape[1]} shape. "
                "Re-solve the task and return a corrected grid with the consistent dimensions."
            )
        else:
            parts.append(
                "Audit the previous candidate against the rule: independently derive the test output, "
                "then compare its exact rows and columns with the candidate before returning the result."
            )
        parts.append("Previous candidate: " + json.dumps(candidate, separators=(",", ":")))
    if independent_check:
        parts.extend([
            "SECOND-PASS VERIFICATION: Treat the previous candidate as untrusted. First infer the "
            "transformation afresh from the demonstrations, and check that the same concrete "
            "operations reproduce every demonstrated output. Derive the test output from the test "
            "input, then compare it cell by cell with the previous candidate. Keep the candidate "
            "only if it follows the verified rule exactly; otherwise return your independently "
            "derived correction. Check dimensions and row/column order before responding.",
            "",
        ])
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

    def solve_once(self, inputs, candidate=None, independent_check=False):
        """One model response -> one parsed grid (or None)."""
        prompt = build_prompt(inputs, candidate=candidate, independent_check=independent_check)
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
        for attempt in range(2):
            candidate = answers[0] if attempt == 1 and answers else None
            try:
                # Use the second call as both an independent re-derivation and an audit of
                # the first grid. This preserves diversity while making cell-level errors
                # and incorrect rules explicit; it does not increase the two-call budget.
                g = self.solve_once(
                    inputs,
                    candidate=candidate,
                    independent_check=(attempt == 1 and candidate is not None),
                )
            except Exception as e:
                self.log(f"Error: {e}")
                g = None
            if g is not None:
                answers.append(g)
        return answers, []
