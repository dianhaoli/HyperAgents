import json
import os
import re
import socket
import http.client
import time
from collections import Counter

# ARC task agent: two model calls and up to two candidate answers per test input.


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


def _training_change_audit(pair, number, limit=60):
    """Summarize the observed input/output differences, without inferring a rule."""
    a, b = pair["input"], pair["output"]
    h, w = min(len(a), len(b)), min(len(a[0]), len(b[0]))
    changes = [(r, c, a[r][c], b[r][c]) for r in range(h) for c in range(w)
               if a[r][c] != b[r][c]]
    lines = [f"Example {number} change audit (0-based): {len(changes)} changed, "
             f"{h*w-len(changes)} unchanged cells in shared {h}x{w} area."]
    transitions = Counter((old, new) for _, _, old, new in changes)
    for (old, new), count in sorted(transitions.items()):
        cells = [(r, c) for r, c, x, y in changes if (x, y) == (old, new)]
        if len(cells) <= limit:
            locations = ", ".join(f"({r},{c})" for r, c in cells)
            lines.append(f"  {old}->{new} ({count}): {locations}")
        else:
            rows, cols = [r for r, _ in cells], [c for _, c in cells]
            lines.append(f"  {old}->{new} ({count}): rows {min(rows)}-{max(rows)}, "
                         f"columns {min(cols)}-{max(cols)}; coordinates omitted")
    return "\n".join(lines)


def build_prompt(inputs):
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
    parts.append("## Training change audit")
    parts.extend(_training_change_audit(pair, i) for i, pair in enumerate(inputs["train"], 1))
    parts.append(
        "Use this audit as evidence, not as a proposed rule. State what input property selects "
        "the changed cells, and check the rule against every demonstration, including unchanged "
        "cells. Reject any rule that does not explain every listed change. Then apply it to the "
        "test grid and verify dimensions and changed cells.\n\n"
    )
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

    def solve_once(self, inputs, candidate=None, independent=False):
        """Make one model call and parse its output grid, if present.

        ``candidate`` retains the explicit verification mode for callers that use it.
        ``independent`` asks for a fresh derivation without exposing an earlier guess;
        this is useful for a second attempt because candidate-visible checks can anchor
        the model on the same incorrect transformation.
        """
        prompt = build_prompt(inputs)
        if candidate is not None:
            prompt += (
                "\n\nIndependent verification of a previous candidate: "
                f"{json.dumps(candidate)}\n"
                "First infer the transformation from the demonstrations and check that it "
                "accounts for every input/output pair. Compare the candidate with the test "
                "input and that inferred rule; do not copy a demonstration output or accept "
                "the candidate merely because it looks plausible. If the candidate fails "
                "any check, correct it. Return the verified test grid in the required "
                "<answer> tags, with nothing else inside the tags."
            )
        elif independent:
            prompt += (
                "\n\nMake this a fresh, independent solve: do not assume or reuse any "
                "earlier proposed rule or grid. Infer a concrete rule from the training "
                "pairs, check that it reproduces every demonstrated output, then apply it "
                "to the test input. Verify the dimensions and changed cells against that "
                "rule before returning the grid in <answer> tags, with nothing else inside "
                "the tags."
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
        answers = []
        for attempt in range(2):
            try:
                # A fresh second derivation avoids anchoring on a plausible-but-wrong
                # first grid, while preserving the two-call/two-answer budget.
                g = self.solve_once(inputs, independent=(attempt == 1))
            except Exception as e:
                self.log(f"Error: {e}")
                g = None
            if g is not None:
                answers.append(g)
        return answers, []
