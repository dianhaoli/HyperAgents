import json
import os
import re
import socket
import http.client
import time

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


def _change_audit(source, target, max_coordinates=40):
    """Summarize every training edit and the unchanged-cell count compactly."""
    in_h, in_w = len(source), len(source[0])
    out_h, out_w = len(target), len(target[0])
    changes = {}
    unchanged = 0
    # Treat cells outside either grid as absent, so size-changing examples are
    # auditable too. Coordinates use the output/input shared top-left origin.
    for r in range(max(in_h, out_h)):
        for c in range(max(in_w, out_w)):
            before = source[r][c] if r < in_h and c < in_w else None
            after = target[r][c] if r < out_h and c < out_w else None
            if before == after:
                unchanged += 1
            else:
                changes.setdefault((before, after), []).append((r, c))

    if not changes:
        details = "no changed cells"
    else:
        pieces = []
        remaining = max_coordinates
        for (before, after), coords in sorted(
                changes.items(), key=lambda item: (str(item[0][0]), str(item[0][1]))):
            shown = coords[:remaining]
            remaining -= len(shown)
            old = "outside" if before is None else str(before)
            new = "outside" if after is None else str(after)
            piece = f"{old}->{new}: {len(coords)}"
            if shown:
                piece += " at " + ", ".join(f"({r},{c})" for r, c in shown)
            if len(shown) < len(coords):
                piece += f" (+{len(coords) - len(shown)} coordinates omitted)"
            pieces.append(piece)
        details = "; ".join(pieces)
    return (f"Change audit (input {in_h}x{in_w} -> output {out_h}x{out_w}; "
            f"{unchanged} unchanged cell(s)): {details}")


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
        parts.append(_change_audit(pair["input"], pair["output"]))
        parts.append("")
    t = inputs["test_input"]
    parts.append("## Test")
    parts.append(f"Input ({len(t)}x{len(t[0])}):")
    parts.append(grid_to_text(t))
    parts.append("")
    parts.append(
        "Before applying a rule, audit the demonstrations: identify the relevant objects/colors and "
        "describe how the changed cells relate to them. Check the proposed rule against every "
        "input/output pair, including cells that stay unchanged; reject or revise it if even one "
        "pair disagrees. Do not infer a rule from only the endpoints or one example when the "
        "other examples constrain which cells change. Then apply the verified rule to the test, "
        "checking the grid dimensions and changed regions.\n\n"
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
                if attempt == 1 and answers:
                    # The second attempt is a verification opportunity, not just a
                    # duplicate independent solve. ARC failures often come from a
                    # plausible rule that misses a demonstrated change or unchanged
                    # cell. Expose the first grid so the model must check it against
                    # every pair, and retain its corrected grid as the second answer.
                    g = self.solve_once(inputs, candidate=answers[0])
                else:
                    # If the first response did not contain a parseable grid, there
                    # is no candidate to check; use the second call for a fresh solve.
                    g = self.solve_once(inputs, independent=(attempt == 1))
            except Exception as e:
                self.log(f"Error: {e}")
                g = None
            if g is not None:
                answers.append(g)
        return answers, []
