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
        "that maps each input grid to its output grid. Infer the rule and apply it to the test input.",
        "Work out the rule from all demonstration pairs, not just one. Check that it reproduces every "
        "demonstration exactly before applying it. Track object shapes, positions, colors, and grid "
        "dimensions carefully; the output dimensions may differ from the input. Do not copy a "
        "demonstration output or assume that background cells should all be zero.",
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
        "Give exactly one candidate output grid for the test input. Check that it is rectangular and "
        "that every cell is an integer from 0 to 9. End your response with the grid inside "
        "<answer></answer> tags as a JSON list of rows, for example:\n"
        "<answer>[[0, 1, 2], [3, 4, 5]]</answer>\nPut nothing else inside the tags."
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

    def _solve_prompt(self, prompt):
        """Make one model call and return both its parsed grid and raw response."""
        self.log(f"Input: {prompt}")
        text = call_model(prompt)
        self.log(f"Output: {text}")
        return parse_grid(text), text

    def solve_once(self, inputs):
        """One direct model response -> one parsed grid (or None)."""
        return self._solve_prompt(build_prompt(inputs))[0]

    def forward(self, inputs):
        """
        Args:
            inputs (dict): {"domain": "arc", "train": [{"input": grid, "output": grid}, ...], "test_input": grid}
        Returns:
            tuple: (prediction, msg_history) where prediction is a list of up to 2 candidate grids.
        """
        answers = []
        try:
            first_grid, _ = self._solve_prompt(build_prompt(inputs))
            if first_grid is not None:
                answers.append(first_grid)
        except Exception as e:
            self.log(f"Error on first attempt: {e}")

        # The gateway permits two calls. Use the second for a fresh verification pass rather than
        # wasting it on the same prompt: explicitly test the first hypothesis against the examples
        # and ask for a corrected (or independently derived) second candidate.
        review_prompt = build_prompt(inputs)
        if answers:
            candidate = json.dumps(answers[0], separators=(",", ":"))
            review_prompt += (
                "\n\nA previous attempt proposed this test grid: " + candidate + "\n"
                "Independently infer the rule again and verify whether this candidate follows from "
                "every training pair. Look especially for a missed object, color, or dimension "
                "change. If the candidate is supported, it is fine to return it again; otherwise "
                "return a corrected or better alternative in the required answer tags."
            )
        else:
            review_prompt += (
                "\n\nThis is a fresh attempt. Carefully infer and verify the rule using all "
                "training pairs, then return the best test grid in the required answer tags."
            )
        try:
            second_grid, _ = self._solve_prompt(review_prompt)
            if second_grid is not None and second_grid not in answers:
                answers.append(second_grid)
        except Exception as e:
            self.log(f"Error on second attempt: {e}")
        return answers, []
