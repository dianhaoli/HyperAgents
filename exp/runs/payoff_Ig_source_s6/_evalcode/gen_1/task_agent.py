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


def build_prompt(inputs, previous_candidate=None):
    """Build a careful ARC prompt, optionally asking for an independent audit."""
    parts = [
        "Solve this ARC-AGI puzzle. The training pairs demonstrate one exact grid transformation. ",
        "Infer a rule that explains every pair, then apply it to the test grid. Do not assume the ",
        "output has the same dimensions as the input: some rules crop, tile, rearrange, or enlarge grids.",
        "\nReason carefully before answering:",
        "1. Identify the relevant objects, colors, repeating patterns, borders, and grid structure.",
        "2. Compare each input with its output and state what changes and what stays unchanged.",
        "3. Check that the proposed rule accounts for every training pair, not just one example.",
        "4. Apply the rule to the test input and check the result's dimensions and every row.",
        "Do not invent details unsupported by the examples. Return one complete rectangular grid of integers 0-9.",
        "",
    ]
    for i, pair in enumerate(inputs["train"], 1):
        parts.append(f"## Training pair {i}")
        for name, grid in (("Input", pair["input"]), ("Output", pair["output"])):
            parts.append(f"{name} ({len(grid)}x{len(grid[0])}):")
            parts.append(grid_to_text(grid))
        parts.append("")
    test = inputs["test_input"]
    parts.extend(["## Test input", f"({len(test)}x{len(test[0])}):", grid_to_text(test), ""])
    if previous_candidate is not None:
        parts.extend([
            "A first independent attempt proposed this test output:",
            json.dumps(previous_candidate),
            "Do not simply copy it. Re-derive the rule from the training pairs, compare the candidate ",
            "against the test grid cell by cell, and correct it if the examples do not support it.",
            "If the candidate is consistent, you may return it.",
            "",
        ])
    parts.append(
        "End your response with the output grid inside <answer></answer> tags as valid JSON, "
        "for example <answer>[[0, 1], [2, 3]]</answer>. Put nothing else inside the tags."
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

    def solve_once(self, inputs):
        """One direct model response -> one parsed grid (or None)."""
        prompt = build_prompt(inputs)
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
        # Spend the two-call budget on complementary attempts rather than submitting the
        # same prompt twice. The second call audits the first against all demonstrations.
        for attempt in range(2):
            try:
                prompt = build_prompt(inputs, answers[0] if attempt and answers else None)
                self.log(f"Input: {prompt}")
                text = call_model(prompt)
                self.log(f"Output: {text}")
                g = parse_grid(text)
            except Exception as e:
                self.log(f"Error: {e}")
                g = None
            if g is not None and g not in answers:
                answers.append(g)
        return answers[:2], []
