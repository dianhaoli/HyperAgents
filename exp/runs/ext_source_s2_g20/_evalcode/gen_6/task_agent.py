import json
import os
import re
import socket
import http.client
import time
from collections import deque

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


def grid_inventory(grid):
    """Return compact color counts and 4-connected component bounds for a grid."""
    height, width = len(grid), len(grid[0])
    seen = set()
    by_color = {}
    for r in range(height):
        for c in range(width):
            color = grid[r][c]
            by_color.setdefault(color, []).append((r, c))

    lines = []
    for color in sorted(by_color):
        cells = by_color[color]
        components = []
        for start in cells:
            if start in seen:
                continue
            seen.add(start)
            queue = deque([start])
            component = []
            while queue:
                r, c = queue.popleft()
                component.append((r, c))
                for neighbor in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                    nr, nc = neighbor
                    if (0 <= nr < height and 0 <= nc < width
                            and grid[nr][nc] == color and neighbor not in seen):
                        seen.add(neighbor)
                        queue.append(neighbor)
            components.append(component)
        parts = [f"color {color}: {len(cells)} cells, {len(components)} four-connected component(s)"]
        if len(components) <= 8:
            bounds = []
            for component in components:
                rows = [r for r, _ in component]
                cols = [c for _, c in component]
                bounds.append(
                    f"{len(component)}@r{min(rows)}-{max(rows)},c{min(cols)}-{max(cols)}"
                )
            parts.append("[" + "; ".join(bounds) + "]")
        else:
            largest = sorted((len(component) for component in components), reverse=True)[:5]
            parts.append("(largest component sizes: " + ", ".join(map(str, largest)) + ")")
        lines.append(" ".join(parts))
    return "; ".join(lines)


def build_prompt(inputs):
    parts = [
        "You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 "
        "(each integer is a color). The demonstration pairs below share one hidden transformation rule "
        "that maps each input grid to its output grid. Infer the rule and apply it to the test input.",
        "First identify a precise rule that explains every demonstration pair, then check that rule "
        "against each pair before using it. Account for changes in grid dimensions, cell positions, "
        "colors, and cells that stay unchanged. Use all examples to distinguish plausible rules; "
        "do not assume the test output has the same dimensions as its input or guess by visual similarity.",
        "Mechanical inventories follow each grid: color counts and four-connected component sizes/bounds (coordinates start at 0). "
        "Use them only as aids, not as assumptions about which cells form a semantic object; verify the proposed rule on the exact grids.",
        "",
    ]
    for i, pair in enumerate(inputs["train"], 1):
        parts.append(f"## Example {i}")
        h, w = len(pair["input"]), len(pair["input"][0])
        parts.append(f"Input ({h}x{w}):")
        parts.append(grid_to_text(pair["input"]))
        parts.append("Inventory: " + grid_inventory(pair["input"]))
        h, w = len(pair["output"]), len(pair["output"][0])
        parts.append(f"Output ({h}x{w}):")
        parts.append(grid_to_text(pair["output"]))
        parts.append("Inventory: " + grid_inventory(pair["output"]))
        parts.append("")
    t = inputs["test_input"]
    parts.append("## Test")
    parts.append(f"Input ({len(t)}x{len(t[0])}):")
    parts.append(grid_to_text(t))
    parts.append("Inventory: " + grid_inventory(t))
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
        """One model response -> one parsed grid (or None)."""
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
        # Keep attempts independent: the evaluation comparison showed that replacing
        # the second attempt with candidate verification had mixed task-level results.
        for _ in range(2):
            try:
                grid = self.solve_once(inputs)
            except Exception as e:
                self.log(f"Error: {e}")
                grid = None
            if grid is not None:
                answers.append(grid)
        return answers, []
