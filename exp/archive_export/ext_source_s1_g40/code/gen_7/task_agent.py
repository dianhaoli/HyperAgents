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
    # Surface a mechanical diff so the solver has an exact checklist for validating
    # its inferred rule instead of relying only on visual comparison of large grids.
    parts.append("Mechanical demonstration audit (zero-based coordinates):")
    for i, pair in enumerate(inputs["train"], 1):
        source, target = pair["input"], pair["output"]
        sh, sw, th, tw = len(source), len(source[0]), len(target), len(target[0])
        changes = []
        for r in range(max(sh, th)):
            for c in range(max(sw, tw)):
                before = source[r][c] if r < sh and c < sw else None
                after = target[r][c] if r < th and c < tw else None
                if before != after:
                    changes.append((r, c, before, after))
        parts.append(f"Example {i}: {sh}x{sw} -> {th}x{tw}; {len(changes)} changed cells.")
        if len(changes) <= 80:
            parts.append("; ".join(f"({r},{c}) {a if a is not None else 'outside'}->{b if b is not None else 'outside'}" for r, c, a, b in changes) or "No changed cells.")
        else:
            # Compress large diffs into contiguous row-runs with a consistent color
            # transition. This keeps the audit useful for large fills/recolors without
            # dumping hundreds of individual coordinates into the model prompt.
            by_row = {}
            for r, c, before, after in changes:
                by_row.setdefault(r, []).append((c, before, after))
            runs = []
            for r, cells in by_row.items():
                start = previous = cells[0][0]
                before, after = cells[0][1:]
                for c, old_color, new_color in cells[1:]:
                    if c == previous + 1 and (old_color, new_color) == (before, after):
                        previous = c
                        continue
                    span = str(start) if start == previous else f"{start}-{previous}"
                    runs.append(f"row {r}, col {span}: {before}->{after}")
                    start = previous = c
                    before, after = old_color, new_color
                span = str(start) if start == previous else f"{start}-{previous}"
                runs.append(f"row {r}, col {span}: {before}->{after}")
            parts.append("Compressed changed-cell runs: " + "; ".join(runs))
    parts.append("Use the audit to check that the inferred rule explains every demonstrated edit and output dimension.")
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

    def refine_once(self, inputs, candidate):
        """Use the second budgeted call to check a candidate against all demonstrations."""
        prompt = build_prompt(inputs)
        prompt += (
            "\n\nA first solver proposed this test output candidate (treat it as untrusted):\n"
            + json.dumps(candidate)
            + "\nIndependently infer the transformation from the demonstrations. Check it against "
              "EVERY input/output pair, including dimensions, row and column ordering, and cell "
              "values. Compare the resulting rule with the candidate; correct any disagreement, "
              "then apply the validated rule to the test input. Return the final grid in the required "
              "<answer> JSON format. Do not merely repeat the candidate without checking it."
        )
        self.log(f"Refinement input: {prompt}")
        text = call_model(prompt)
        self.log(f"Refinement output: {text}")
        return parse_grid(text)

    def forward(self, inputs):
        """
        Args:
            inputs (dict): {"domain": "arc", "train": [{"input": grid, "output": grid}, ...], "test_input": grid}
        Returns:
            tuple: (prediction, msg_history) where prediction is a list of up to 2 candidate grids.
        """
        answers = []
        try:
            first = self.solve_once(inputs)
        except Exception as e:
            self.log(f"Error: {e}")
            first = None
        if first is not None:
            answers.append(first)

        # Spend the existing second-call allowance on verification rather than a fully
        # independent guess. If the first response could not be parsed, use it for a retry.
        try:
            second = self.refine_once(inputs, first) if first is not None else self.solve_once(inputs)
        except Exception as e:
            self.log(f"Error: {e}")
            second = None
        if second is not None and second != first:
            answers.append(second)
        return answers, []
