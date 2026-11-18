import json
import os
import re
import socket
import http.client
import time

# Starting task agent (A_0) for the ARC-AGI-2 domain. The first model call proposes a solution;
# the second call independently checks that proposal against the demonstrations.


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


def build_prompt(inputs, prior_response=None):
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
    if prior_response is None:
        parts.append(
            "Solve the task by inferring one precise transformation from the demonstrations. "
            "Before deciding, inspect the grids systematically: compare dimensions, colors, connected "
            "objects and their bounding boxes; look for repeated motifs, symmetry, reflection, rotation, "
            "completion of partial patterns, and changes in object size or position. Do not assume the "
            "output is the input with only a small local edit. Derive the rule from the examples, then "
            "check that it reproduces every demonstrated output exactly. Apply that same rule to the test. "
            "Preserve the full grid and its dimensions unless the examples show a dimension change. "
            "Give a brief explanation outside the answer tags, then end with the complete output grid inside "
            "<answer></answer> tags as a JSON list of rows, for example: "
            "<answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags."
        )
    else:
        parts.append(
            "A previous attempt proposed this solution (it may be wrong):\n"
            + prior_response
            + "\n\nNow act as a careful independent verifier, not a copy editor. Infer the rule afresh from "
            "the demonstrations, check it against every input/output pair, and inspect whether the proposed "
            "grid follows that rule cell by cell. In particular, check repeated motifs and their completion, "
            "symmetry/reflection/rotation, object boundaries, colors, and dimensions. Correct the grid if the "
            "candidate is inconsistent; if it is consistent, return it unchanged. Briefly explain the rule "
            "outside the answer tags. End with the complete output grid inside <answer></answer> tags as a "
            "JSON list of rows, with nothing else inside the tags."
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

    def solve_once(self, inputs, prior_response=None):
        """One model response -> one parsed grid (or None)."""
        prompt = build_prompt(inputs, prior_response=prior_response)
        self.log(f"Input: {prompt}")
        text = call_model(prompt)
        self.log(f"Output: {text}")
        self._last_response = text
        return parse_grid(text)

    def forward(self, inputs):
        """
        Args:
            inputs (dict): {"domain": "arc", "train": [{"input": grid, "output": grid}, ...], "test_input": grid}
        Returns:
            tuple: (prediction, msg_history) where prediction is a list of up to 2 candidate grids.
        """
        answers = []
        first_response = None
        for attempt in range(2):
            try:
                # Spend the second allowed call reviewing the first answer instead of repeating
                # the identical prompt, which commonly produced duplicate predictions.
                prompt_context = first_response if attempt == 1 else None
                g = self.solve_once(inputs, prior_response=prompt_context)
                # Keep the raw response for the second-call review.
                first_response = getattr(self, "_last_response", None) if attempt == 0 else first_response
            except Exception as e:
                self.log(f"Error: {e}")
                g = None
            if g is not None:
                answers.append(g)
        return answers, []
