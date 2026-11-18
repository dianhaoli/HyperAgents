import json
import os
import re
import socket
import http.client
import time

# Starting task agent for the ARC-AGI-2 domain. The second call uses the first candidate as
# an explicit verification target, while retaining it as a separate answer in case the
# verification attempt makes a different mistake.


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


def _training_change_audit(input_grid, output_grid, max_positions=40):
    """Summarize demonstrated edits with exact coordinates, without bloating prompts."""
    in_h, in_w = len(input_grid), len(input_grid[0])
    out_h, out_w = len(output_grid), len(output_grid[0])
    if (in_h, in_w) != (out_h, out_w):
        return (f"Training change audit (zero-based): dimensions change from "
                f"{in_h}x{in_w} to {out_h}x{out_w}; compare the complete grids above.")

    edits = {}
    for r in range(in_h):
        for c in range(in_w):
            before, after = input_grid[r][c], output_grid[r][c]
            if before != after:
                edits.setdefault((before, after), []).append((r, c))
    if not edits:
        return "Training change audit (zero-based): no cells changed."

    total = sum(len(coords) for coords in edits.values())
    parts = [f"Training change audit (zero-based; {total} changed cell(s)):"]
    remaining = max_positions
    for (before, after), coords in sorted(edits.items()):
        shown = coords[:remaining]
        suffix = f"; first {len(shown)} shown" if len(shown) < len(coords) else ""
        parts.append(f"{before}->{after}: {len(coords)} at {shown}{suffix}")
        remaining -= len(shown)
        if remaining <= 0:
            break
    if total > max_positions:
        parts.append(f"Coordinates capped at {max_positions} total; use the full grids above for omitted edits.")
    return " ".join(parts)



def build_prompt(inputs):
    parts = [
        "You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 "
        "(each integer is a color). The demonstration pairs below share one hidden transformation rule "
        "that maps each input grid to its output grid. Infer the rule and apply it to the test input. "
        "Use each training change audit as evidence: your rule must explain every changed cell and "
        "why the other cells remain unchanged.",
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
        parts.append(_training_change_audit(pair["input"], pair["output"]))
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

    def solve_once(self, inputs, candidate=None):
        """Make one model call and parse its grid, optionally checking a prior candidate."""
        prompt = build_prompt(inputs)
        if candidate is not None:
            prompt += (
                "\n\nIndependently verify this candidate: "
                f"{json.dumps(candidate)}\n"
                "Infer the rule from the demonstrations and check that it explains every "
                "input/output pair. Apply that rule to the test input, then compare the "
                "result with the candidate. Do not accept the candidate just because it "
                "looks plausible, and do not copy a demonstration output. If it is wrong, "
                "correct it. Return the verified test grid in the required <answer> tags; "
                "put nothing else inside the tags."
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
                # Use the existing second-call budget to scrutinize the first candidate;
                # retaining both candidates means a mistaken verification cannot discard
                # a correct first answer.
                candidate = answers[0] if attempt == 1 and answers else None
                g = self.solve_once(inputs, candidate=candidate)
            except Exception as e:
                self.log(f"Error: {e}")
                g = None
            if g is not None:
                answers.append(g)
        return answers, []
