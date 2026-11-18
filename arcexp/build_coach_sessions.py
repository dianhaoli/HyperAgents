#!/usr/bin/env python3
"""Build structured coach (meta-agent) session data for the explorer.

Reads every non-crashed coaching transcript
    exp/runs/<run>/generate_<run>/gen_<k>/agent_output/meta_agent_chat_history.md
plus the round's model_patch.diff, and writes
    explorer/data/coach/index.json       one summary row per session
    explorer/data/coach/<run>.json       full step-by-step sessions for one run

Stdlib only. Read-only with respect to exp/ (never writes there).

Transcript format (written by agent/llm_withtools.py): one turn per line,
"<Prefix>: <python repr of a str>", Prefix in {Input, Output, Tool output, Nudge};
the harness may also log bare "Error: ..." lines.
"""
import ast
import collections
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(ROOT, "exp")
DATA = os.path.join(ROOT, "explorer", "data")
OUT = os.path.join(DATA, "coach")

# ---------------------------------------------------------------- budgets
OUTPUT_CAP = 2500          # tool output: head+tail chars kept (default)
OUTPUT_CAP_MIN = 900       # hardest trim if a run file is over budget
CMD_CAP = 4000             # bash command / editor payload (default)
CMD_CAP_MIN = 1200
BRIEF_TRACE_CAP = 2400     # shared by all failure-trace blocks inside the brief
BRIEF_CAP = 12000          # whole brief after grid compression (safety net)
DIFF_CAP = 40 * 1024
RUN_FILE_CAP = 1.2 * 1024 * 1024
TOTAL_CAP = 6_000_000      # bytes, decimal (stricter than 6 MiB)
INDEX_RESERVE = 200_000

# ---------------------------------------------------------------- redaction
REDACTIONS = collections.Counter()
_SECRET_PATTERNS = [
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}"), "sk-key"),
    (re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-]{16,}"), "bearer"),
    (re.compile(r"(?i)((?:api[_-]?key|access[_-]?token|auth[_-]?token|secret|password)[\"']?\s*[=:]\s*['\"]?)[A-Za-z0-9._\-]{12,}"), "kv-secret"),
    (re.compile(r"(?<![0-9A-Fa-f])[0-9a-fA-F]{32}(?![0-9A-Fa-f])"), "32hex-token"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "github-token"),
    (re.compile(r"/home/[A-Za-z0-9_.\-]+/HyperAgents/"), "local-path"),
]


LOCAL_MARK = "[local]/HyperAgents/"


def scrub(text):
    if not text:
        return text
    for pat, name in _SECRET_PATTERNS:
        def rep(m, name=name):
            REDACTIONS[name] += 1
            if name == "kv-secret":
                return m.group(1) + "[REDACTED]"
            if name == "local-path":
                return LOCAL_MARK
            return "[REDACTED]"
        text = pat.sub(rep, text)
    return text


# ---------------------------------------------------------------- helpers
def lj(path):
    with open(path) as f:
        return json.load(f)


def maybe_json(v):
    """trees.json fields are sometimes JSON-encoded strings."""
    if isinstance(v, str) and v[:1] in "[{":
        try:
            return json.loads(v)
        except ValueError:
            return v
    return v


def head_tail(text, cap, what="chars"):
    """Keep head (~65%) and tail (~35%) of text; returns (text, truncated)."""
    if text is None or len(text) <= cap:
        return text, False
    h = int(cap * 0.65)
    t = cap - h
    cut = len(text) - h - t
    # snap to line boundaries when cheap
    hs = text[:h]
    nl = hs.rfind("\n")
    if nl > h * 0.7:
        hs = hs[:nl]
    ts = text[-t:]
    nl = ts.find("\n")
    if 0 <= nl < t * 0.3:
        ts = ts[nl + 1:]
    cut = len(text) - len(hs) - len(ts)
    return f"{hs}\n[... {cut:,} {what} cut ...]\n{ts}", True


def first_sentence(text, n=160):
    t = " ".join((text or "").split())
    if not t:
        return ""
    m = re.search(r"(?<=[.!?])\s", t)
    s = t[: m.start()] if m else t
    if len(s) > n:
        s = s[: n - 1].rstrip() + "…"
    return s


# ---------------------------------------------------------------- transcript decoding
LINE_RE = re.compile(r"^(Input|Output|Tool output|Nudge): (.*)$", re.S)


def decode_repr(s):
    try:
        v = ast.literal_eval(s)
        if isinstance(v, str):
            return v
    except Exception:
        pass
    # fallback: strip quotes, decode escapes
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "'\"":
        s = s[1:-1]
    try:
        return s.encode("latin-1", "backslashescape").decode("unicode_escape")
    except Exception:
        return s.replace("\\n", "\n").replace("\\'", "'").replace('\\"', '"')


def read_turns(path):
    turns = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln.strip():
                continue
            m = LINE_RE.match(ln)
            if m:
                turns.append((m.group(1), scrub(decode_repr(m.group(2)))))
            else:
                turns.append(("Harness", scrub(ln.strip())))
    return turns


# --- tool-call detection: mirrors agent/llm_withtools.py check_for_tool_uses
TOOL_RE = re.compile(r"<json>\s*(\{.*?\})\s*</json>", re.S)


def find_tool_calls(resp):
    """Returns list of (tool_use, (start, end)) spans in resp, harness-style."""
    calls = []
    for m in TOOL_RE.finditer(resp):
        try:
            tu = json.loads(m.group(1))
        except ValueError:
            continue
        if isinstance(tu, dict) and "tool_name" in tu and "tool_input" in tu:
            calls.append((tu, m.span()))
    if not calls:  # bare JSON fallback (experiment adaptation in the harness)
        dec = json.JSONDecoder()
        i = resp.find("{")
        while i != -1:
            try:
                obj, end = dec.raw_decode(resp, i)
                if isinstance(obj, dict) and "tool_name" in obj and "tool_input" in obj:
                    calls.append((obj, (i, end)))
                    break
            except ValueError:
                pass
            i = resp.find("{", i + 1)
    return calls


def all_call_spans(resp):
    """Spans of every tool-call-shaped JSON object in resp (tagged or bare), non-overlapping.
    Used only to separate narration from (possibly unexecuted) tool calls."""
    spans = []
    for m in TOOL_RE.finditer(resp):
        try:
            tu = json.loads(m.group(1))
        except ValueError:
            continue  # not valid JSON: left in the text (it may be prose or a malformed call)
        if isinstance(tu, dict) and "tool_name" in tu and "tool_input" in tu:
            spans.append(m.span())

    def inside(i):
        return any(a <= i < b for a, b in spans)

    dec = json.JSONDecoder()
    i = resp.find("{")
    while i != -1:
        if not inside(i):
            try:
                obj, end = dec.raw_decode(resp, i)
                if isinstance(obj, dict) and "tool_name" in obj and "tool_input" in obj:
                    spans.append((i, end))
                    i = resp.find("{", end)
                    continue
            except ValueError:
                pass
        i = resp.find("{", i + 1)
    return sorted(spans)


ECHO_RE = re.compile(
    r'^<json>\s*\{\s*"tool_name": "(?P<name>[^"\n]*)",\s*"tool_input": (?P<inp>[^\n]*),\s*\n\s*"tool_output": "(?P<out>.*)"\s*\}\s*</json>\s*$',
    re.S,
)


def parse_echo(text):
    m = ECHO_RE.match(text)
    if not m:
        return None, None, text
    inp = m.group("inp")
    try:
        inp = ast.literal_eval(inp)
    except Exception:
        try:
            inp = json.loads(inp)
        except Exception:
            pass
    return m.group("name"), inp, m.group("out")


def short_path(p):
    p = str(p or "")
    return p[len("/hyperagents/"):] if p.startswith("/hyperagents/") else p


def describe_call(name, inp):
    """Returns (cmd one-liner, text body)."""
    if not isinstance(inp, dict):
        return f"{name}", str(inp)
    if name == "bash":
        c = str(inp.get("command", ""))
        extra = {k: v for k, v in inp.items() if k != "command"}
        body = c + (f"\n# (extra tool_input keys: {json.dumps(extra)})" if extra else "")
        line = next((l for l in c.splitlines() if l.strip()), "")
        if len(line) > 200:
            line = line[:199] + "…"
        return line, body
    if name == "editor":
        op = inp.get("command", "?")
        path = inp.get("path", "")
        cmd = f"editor {op} {short_path(path)}"
        if inp.get("view_range"):
            cmd += f" lines {inp['view_range']}"
        if op == "insert" and "insert_line" in inp:
            cmd += f" after line {inp['insert_line']}"
        parts = []
        if "old_str" in inp:
            parts.append("--- old_str ---\n" + str(inp["old_str"]))
        if "new_str" in inp:
            parts.append("+++ new_str +++\n" + str(inp["new_str"]))
        if "file_text" in inp:
            parts.append("+++ file_text +++\n" + str(inp["file_text"]))
        other = {k: v for k, v in inp.items() if k not in ("command", "path", "view_range", "insert_line", "old_str", "new_str", "file_text")}
        if other:
            parts.append("(other keys: " + json.dumps(other)[:500] + ")")
        return cmd, "\n".join(parts) if parts else cmd
    return f"{name} " + json.dumps(inp)[:180], json.dumps(inp, indent=1)


# ---------------------------------------------------------------- degenerate-loop collapsing
REPEAT_RE = re.compile(r"(.{1,600}?)\1{7,}", re.S)
DEGENERATE_MIN = 8000  # only messages longer than this are checked


def collapse_repeats(text):
    """Lossless-in-spirit compression of degenerate token loops (a fragment repeated many times
    in a row, or long lines repeated verbatim). Ordinary narration is never affected."""
    if not text or len(text) < DEGENERATE_MIN:
        return text, False

    def rep(m):
        frag, whole = m.group(1), m.group(0)
        if len(whole) - len(frag) < 300:
            return whole
        n = len(whole) // len(frag) - 1
        return frag + f" [... degenerate output: the preceding {len(frag)}-char fragment repeats {n} more times; collapsed ...] "

    out = REPEAT_RE.sub(rep, text)
    lines, seen, dup = [], set(), 0
    for l in out.split("\n"):
        if len(l) > 120 and l in seen:
            dup += 1
            if lines and lines[-1].startswith("[... degenerate output: repeated line"):
                lines[-1] = f"[... degenerate output: repeated lines omitted ({dup} so far in this message) ...]"
            else:
                lines.append(f"[... degenerate output: repeated line omitted ({dup} so far in this message) ...]")
            continue
        seen.add(l)
        lines.append(l)
    out = "\n".join(lines)
    return out, len(out) < len(text)


# ---------------------------------------------------------------- brief trimming
GRID_ROW = re.compile(r"^\s*(?:\d[ ,]*){4,}\s*$|^\s*\[?\s*\[[\d,\s]+\]\s*,?\]?\s*$")


def compress_grids(text):
    """Collapse runs of grid rows (keep 2), shorten long inline answer arrays."""
    out, run, rows_cut = [], [], 0

    def flush():
        nonlocal rows_cut
        if len(run) > 3:
            out.extend(run[:2])
            out.append(f"[... {len(run) - 2} more grid rows cut ...]")
            rows_cut += len(run) - 2
        else:
            out.extend(run)
        run.clear()

    for line in text.split("\n"):
        if GRID_ROW.match(line):
            run.append(line)
            continue
        flush()
        if len(line) > 300 and re.search(r"\[\[[\d,\s\]\[]{200,}", line):
            m = re.search(r"\[\[[\d,\s\]\[]{200,}", line)
            seg = m.group(0)
            line = line[: m.start()] + seg[:120] + f" [... {len(seg) - 120} chars of grid cut ...]" + line[m.end():]
        out.append(line)
    flush()
    return "\n".join(out), rows_cut


def trim_brief(text):
    """Keep instructions + evaluation summary in full; compress grids (long grid-row runs keep 2 rows, long inline
    grids such as answers keep their first 120 chars); share ~BRIEF_TRACE_CAP chars among all failure traces
    (each keeps its header, its start and its end). Returns (text, trim dict or None, original length)."""
    orig = len(text)
    text, rows_cut = compress_grids(text)
    parts = re.split(r"(?m)(?=^Failure trace \()", text)
    traces = [p for p in parts if p.startswith("Failure trace (")]
    per = max(500, BRIEF_TRACE_CAP // max(1, len(traces)))
    traces_trimmed = 0
    new = []
    for p in parts:
        if p.startswith("Failure trace (") and len(p) > per:
            p, _ = head_tail(p, per, "chars of this failure trace")
            p += "\n\n"
            traces_trimmed += 1
        new.append(p)
    text = "".join(new)
    text, capped = head_tail(text, BRIEF_CAP, "chars of brief")
    trim = {}
    if rows_cut:
        trim["grid_rows_cut"] = rows_cut
    if traces_trimmed:
        trim["traces_trimmed"] = traces_trimmed
        trim["traces_total"] = len(traces)
        trim["trace_chars"] = per
    if capped:
        trim["capped"] = True
    if len(text) < orig and not trim:
        trim["grids_shortened"] = True  # only inline grids were shortened
    return text, trim or None, orig


# ---------------------------------------------------------------- diffs
COACH_PREFIXES = ("meta_agent.py", "run_meta_agent.py", "agent/", "tests/test_meta_agent", "utils/")
PLAYER_PREFIXES = ("task_agent.py", "run_task_agent.py", "domains/", "tests/test_task_agent")


def classify_path(p):
    if p.endswith(".pyc") or "__pycache__" in p:
        return "other"
    if p.startswith(COACH_PREFIXES):
        return "coach"
    if p.startswith(PLAYER_PREFIXES):
        return "player"
    return "other"


def parse_patch(text):
    files, cur = [], None
    for line in (text or "").split("\n"):
        if line.startswith("diff --git "):
            m = re.match(r"diff --git a/(.*?) b/(.*)$", line)
            cur = {"path": m.group(2) if m else line[11:], "added": 0, "removed": 0}
            cur["role"] = classify_path(cur["path"])
            files.append(cur)
        elif cur is not None:
            if line.startswith("+") and not line.startswith("+++"):
                cur["added"] += 1
            elif line.startswith("-") and not line.startswith("---"):
                cur["removed"] += 1
    return files


def drop_binary_sections(text):
    out, skip = [], False
    for sec in re.split(r"(?m)(?=^diff --git )", text or ""):
        if "GIT binary patch" in sec:
            head = sec.split("GIT binary patch")[0]
            out.append(head + "[binary patch body omitted]\n")
        else:
            out.append(sec)
    return "".join(out)


# ---------------------------------------------------------------- session parsing
STANDARD_NUDGE = ("No tool call was found in your last response. If you are not finished, make the next tool call now, "
                  "using exactly the <json> format above. If you are finished, reply with the single word DONE.")
NUDGE_SHORT = "No tool call found; make the next tool call or reply DONE."


GATEWAY_PREFIX = "[GATEWAY]"
# Leftovers of tool-call markup once the call itself is taken out: lone tags, braces, fences, chat-template tokens.
DEBRIS_TOKEN = re.compile(r"</?\|?(?:json|assistant|user|analysis|commentary|final|tool_call|im_end|im_start|endoftext)"
                          r"[|a-z_]*>?|<\|[a-z_|]+\|>|\(json\)|```(?:json)?|[{}\[\],]")
CALL_HINT = re.compile(r'"?tool_name"?\s*[:=]|\{\s*"(?:command|name)"\s*:')


def clean_debris(text):
    """Drop lines that hold only tag / brace debris; trim the rest."""
    lines = [l for l in (text or "").split("\n") if DEBRIS_TOKEN.sub("", l).strip(" \t\"'():;.|")]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def readable(text):
    """At least two letters or digits once debris tokens are removed."""
    return len(re.findall(r"[^\W_]", DEBRIS_TOKEN.sub("", text or ""))) >= 2


def think_step(text, **flags):
    t, collapsed = collapse_repeats(text)
    st = {"kind": "think", "text": t}
    if CALL_HINT.search(t):
        st["unparsed_call"] = True  # holds a tool call the harness did not run (malformed or extra)
    st.update(flags)
    if collapsed:
        st["collapsed_repeats"] = True
        st["full_chars"] = len(text)
    return st


def noise_step(raw):
    return {"kind": "think", "text": "(no readable text)", "empty": True, "raw": raw.strip()[:80]}


def build_steps(turns, out_cap, cmd_cap):
    steps = []
    first_input_done = False
    pending_cmd = False  # last step is a command awaiting its output
    for i, (kind, text) in enumerate(turns):
        if kind == "Input":
            if not first_input_done:
                t, trim, full = trim_brief(text)
                st = {"kind": "brief", "text": t,
                      "has_scores": bool(re.search(r"(?i)accuracy=|=\s*[01]\.\d{2}|scored [01]\.\d|\b\d{1,3}(?:\.\d)?%", text)),
                      "n_traces": len(re.findall(r"(?m)^Failure trace \(", text))}
                if trim:
                    st["truncated"] = True
                    st["full_chars"] = full
                    st["trim"] = trim
                steps.append(st)
                first_input_done = True
            else:  # a later Input (should not happen in a single chat): keep as brief-like note
                t, trunc = head_tail(text, out_cap)
                steps.append({"kind": "nudge", "text": "[harness input] " + t})
            continue
        if kind == "Nudge":
            t = text.strip()
            steps.append({"kind": "nudge", "text": "(standard nudge) " + NUDGE_SHORT if t == STANDARD_NUDGE else t})
            pending_cmd = False
            continue
        if kind == "Harness":
            steps.append({"kind": "nudge", "text": "[harness] " + text})
            continue
        if kind == "Output":
            resp = text
            calls = find_tool_calls(resp)
            if calls:
                tu, span = calls[0]
                spans = all_call_spans(resp)
                if span not in spans:
                    spans = sorted([x for x in spans if x[1] <= span[0] or x[0] >= span[1]] + [span])
                # take every well-formed tool-call object out of the text (only the first one was run);
                # text before the executed call is shown before the command, text after it right after.
                def strip_spans(a0, b0):
                    t, pos = [], a0
                    for a, b in spans:
                        if b <= a0 or a >= b0:
                            continue
                        t.append(resp[pos:a])
                        pos = b
                    t.append(resp[pos:b0])
                    return clean_debris("".join(t))
                before, after = strip_spans(0, span[0]), strip_spans(span[1], len(resp))
                n_extra = len(spans) - 1
                if before and readable(before):
                    steps.append(think_step(before))
                cmd, body = describe_call(tu["tool_name"], tu["tool_input"])
                body_t, trunc = head_tail(body, cmd_cap, "chars of command")
                st = {"kind": "command", "tool": tu["tool_name"], "cmd": cmd, "text": body_t}
                if trunc:
                    st["truncated"] = True
                    st["full_chars"] = len(body)
                if n_extra > 0:
                    st["ignored_calls"] = n_extra
                    st["text"] += (f"\n\n[{n_extra} further tool call(s) in this same message were not run "
                                   f"by the harness (it runs only the first); omitted here]")
                steps.append(st)
                if after and readable(after):
                    steps.append(think_step(after, after_call=True))
                pending_cmd = True
            else:
                s = resp.strip()
                if s.startswith(GATEWAY_PREFIX):
                    # the gateway answered in place of the model (token budget spent): not the coach's words
                    steps.append({"kind": "nudge", "gateway": True, "text": "[gateway] " + s[len(GATEWAY_PREFIX):].strip()})
                elif s == "DONE":
                    steps.append({"kind": "done", "text": "DONE"})
                elif re.search(r"\bDONE\s*$", s):
                    body = clean_debris(re.sub(r"\bDONE\s*$", "", s))
                    if body and readable(body):
                        steps.append(think_step(body))
                    steps.append({"kind": "done", "text": "DONE"})
                elif not readable(s):
                    steps.append(noise_step(s))
                else:
                    steps.append(think_step(clean_debris(s) if not CALL_HINT.search(s) else s))
                pending_cmd = False
            continue
        if kind == "Tool output":
            name, inp, out = parse_echo(text)
            if not pending_cmd and name is not None:
                # call not visible in the preceding Output (or not parsed): synthesize from the echo
                cmd, body = describe_call(name, inp)
                body_t, trunc = head_tail(body, cmd_cap, "chars of command")
                st = {"kind": "command", "tool": name, "cmd": cmd, "text": body_t, "from_echo": True}
                if trunc:
                    st["truncated"] = True
                    st["full_chars"] = len(body)
                steps.append(st)
            out_t, trunc = head_tail(out, out_cap, "chars of output")
            st = {"kind": "output", "text": out_t}
            if name:
                st["tool"] = name
            if trunc:
                st["truncated"] = True
                st["full_chars"] = len(out)
            steps.append(st)
            pending_cmd = False
            continue
    return steps


# ---------------------------------------------------------------- main
def main():
    trees_doc = lj(os.path.join(DATA, "trees.json"))
    tree_runs = list(trees_doc["runs"])
    trees = trees_doc["trees"]

    md_files = sorted(glob.glob(os.path.join(EXP, "runs", "*", "generate_*", "gen_*", "agent_output", "meta_agent_chat_history.md")))
    by_run = collections.defaultdict(list)
    for f in md_files:
        rel = os.path.relpath(f, EXP)
        if rel.startswith("crashed"):
            continue
        run = rel.split(os.sep)[1]
        by_run[run].append(f)
    n_crashed = len(glob.glob(os.path.join(EXP, "crashed", "**", "meta_agent_chat_history.md"), recursive=True))
    n_aborted_no_tx = sum(1 for d in glob.glob(os.path.join(EXP, "runs", "*", "generate_*", "gen_*.aborted_*"))
                          if not os.path.exists(os.path.join(d, "agent_output", "meta_agent_chat_history.md")))

    extra_runs = sorted(r for r in by_run if r not in trees)
    run_order = [r for r in tree_runs if r in by_run] + extra_runs

    os.makedirs(OUT, exist_ok=True)
    index_sessions, runs_meta = [], []
    sizes = {}
    trims = []
    all_runs = []

    for run in run_order:
        tree = trees.get(run)
        nodes = {n["id"]: n for n in tree["nodes"]} if tree else {}
        cfg_p = os.path.join(EXP, "runs", run, "config.json")
        cfg = lj(cfg_p) if os.path.exists(cfg_p) else {}

        def report_scores(gdir):
            p = os.path.join(gdir, "arc_eval", "report.json")
            if not os.path.exists(p):
                return None, None
            r = lj(p)
            pts = r.get("per_task_score")
            if isinstance(pts, str):
                try:
                    pts = ast.literal_eval(pts)
                except Exception:
                    pts = None
            return r.get("overall_accuracy"), pts

        def node_scores(nid, gdir_for_fallback=None):
            if nid in nodes:
                n = nodes[nid]
                pr = maybe_json(n.get("practice"))
                per = pr.get("per_task") if isinstance(pr, dict) else None
                return n.get("practice_score"), per, bool(n.get("valid"))
            if gdir_for_fallback and os.path.isdir(gdir_for_fallback):
                sc, per = report_scores(gdir_for_fallback)
                return sc, per, sc is not None
            return None, None, False

        gen_root = os.path.join(EXP, "runs", run, f"generate_{run}")

        def sortkey(f):
            d = f.split(os.sep)[-3][4:]
            m = re.match(r"(\d+)(.*)$", d)
            return (int(m.group(1)), m.group(2)) if m else (10 ** 6, d)

        files = sorted(by_run[run], key=sortkey)
        parsed = []
        for f in files:
            gdir = os.path.dirname(os.path.dirname(f))
            dname = os.path.basename(gdir)[4:]  # e.g. "5" or "5.aborted_1794936889"
            aborted = not dname.isdigit()
            gen = int(re.match(r"\d+", dname).group(0))
            md = {}
            mp = os.path.join(gdir, "metadata.json")
            if os.path.exists(mp):
                try:
                    md = lj(mp)
                except Exception:
                    md = {}
            node = nodes.get(dname)
            nid = dname
            parent = node["parent"] if node else (str(md["parent_genid"]) if md.get("parent_genid") is not None else None)
            patch_p = os.path.join(gdir, "agent_output", "model_patch.diff")
            patch = open(patch_p, encoding="utf-8", errors="replace").read() if os.path.exists(patch_p) else ""
            made_edit = bool(patch.strip())
            if node and maybe_json(node.get("files_changed")) is not None:
                fe = [{"path": x["path"], "role": x["role"], "added": x.get("added", 0), "removed": x.get("removed", 0)}
                      for x in maybe_json(node.get("files_changed")) or []]
            else:
                fe = parse_patch(patch)
            # scores
            if aborted:
                after, per_after, valid = None, None, False
            else:
                after, per_after, valid = node_scores(nid, gdir)
            parent_dir = os.path.join(gen_root, f"gen_{parent}") if parent is not None else None
            before, per_before, _ = node_scores(parent, parent_dir) if parent is not None else (None, None, False)
            gained, lost = [], []
            # only for a scored edit: no-edit / aborted / unscored nodes may carry a partial per_task
            if made_edit and not aborted and after is not None and per_after and per_before:
                for t in sorted(set(per_after) | set(per_before)):
                    a, b = per_after.get(t), per_before.get(t)
                    if a is None or b is None:
                        continue
                    if a > b:
                        gained.append(t)
                    elif a < b:
                        lost.append(t)
            if not made_edit:
                outcome = "no edit"
            elif aborted:
                outcome = "not scored"
            elif (node is not None and not node.get("valid") and after is None) or after == 0:
                outcome = "broke"
            elif after is None or before is None:
                outcome = "not scored"
            elif after > before + 1e-9:
                outcome = "improved"
            elif after < before - 1e-9:
                outcome = "worse"
            else:
                outcome = "same"
            meta = maybe_json(node.get("meta")) if node else None
            coach_tokens = meta.get("tokens") if isinstance(meta, dict) else None

            diff = drop_binary_sections(scrub(patch))
            diff_full = len(diff)
            diff_note = None
            if len(diff) > DIFF_CAP:
                diff, _ = head_tail(diff, DIFF_CAP, "chars of patch")
                diff_note = f"patch capped at {DIFF_CAP // 1024} KB (full {diff_full:,} chars)"
            parsed.append(dict(f=f, gdir=gdir, nid=nid, gen=gen, aborted=aborted, parent=parent, made_edit=made_edit,
                               fe=fe, before=before, after=after, gained=gained, lost=lost, outcome=outcome,
                               coach_tokens=coach_tokens, diff=diff, diff_full=diff_full, diff_note=diff_note,
                               turns=read_turns(f), valid=valid,
                               player_changed=any(x["role"] == "player" for x in fe)))

        all_runs.append((run, tree, cfg, parsed))

    def render(run, parsed, out_cap, cmd_cap):
        sessions = {}
        for p in parsed:
            steps = build_steps(p["turns"], out_cap, cmd_cap)
            if p["made_edit"]:
                fe = p["fe"]
                tot_a = sum(x["added"] for x in fe)
                tot_r = sum(x["removed"] for x in fe)
                lines = [f"Patch: {len(fe)} file(s) changed, +{tot_a} / -{tot_r} lines."]
                for x in fe:
                    lines.append(f"  {x['path']} ({x['role']}) +{x['added']} -{x['removed']}")
                etext = "\n".join(lines)
            else:
                etext = "No edit: the round produced an empty patch."
            steps.append({"kind": "edit", "text": etext})
            sess = {"steps": steps, "diff": p["diff"]}
            if p["diff_note"]:
                sess["diff_note"] = p["diff_note"]
            if p["aborted"]:
                sess["aborted"] = True
            sessions[p["nid"]] = sess
            p["steps"] = steps
        return json.dumps({"run": run, "sessions": sessions}, ensure_ascii=False, separators=(",", ":"))

    # Trim levels (tool-output cap, command cap). A global level is lowered until the total fits;
    # a run whose file is still over the per-run cap is pushed to lower levels on its own.
    LEVELS = [(OUTPUT_CAP, CMD_CAP), (2000, 3200), (1700, 2700), (1500, 2300), (1350, 2000), (1200, 1800),
              (1100, 1600), (1000, 1400), (OUTPUT_CAP_MIN, CMD_CAP_MIN)]
    for g in range(len(LEVELS)):
        blobs, used = {}, {}
        for run, tree, cfg, parsed in all_runs:
            lv = g
            while True:
                blob = render(run, parsed, *LEVELS[lv])
                if len(blob.encode()) <= RUN_FILE_CAP or lv == len(LEVELS) - 1:
                    break
                lv += 1
            blobs[run], used[run] = blob, lv
        total = sum(len(b.encode()) for b in blobs.values())
        print(f"trim level {g} {LEVELS[g]}: run files total {total / 1e6:.2f} MB")
        if total <= TOTAL_CAP - INDEX_RESERVE or g == len(LEVELS) - 1:
            break
    if g:
        trims.append(f"To fit the {TOTAL_CAP / 1e6:.0f} MB budget, tool outputs are capped at {LEVELS[g][0]} chars and "
                     f"commands at {LEVELS[g][1]} chars (head+tail; see truncated/full_chars on each step).")
    for run, tree, cfg, parsed in all_runs:
        blob = blobs[run]
        out_cap, cmd_cap = LEVELS[used[run]]
        if used[run] != g:
            trims.append(f"{run}: tool outputs capped at {out_cap} chars, commands at {cmd_cap} chars (per-run budget)")
        with open(os.path.join(OUT, f"{run}.json"), "w", encoding="utf-8") as fh:
            fh.write(blob)
        sizes[f"{run}.json"] = len(blob.encode())
        for p in parsed:
            steps = p["steps"]
            def prose_part(t):
                return re.split(r"<json>|\{\s*\"tool_name\"", t)[0].strip()
            first_think = next((prose_part(s["text"]) for s in steps if s["kind"] == "think" and not s.get("empty")
                                and prose_part(s["text"])[:1] not in "{[<"
                                and len(re.findall(r"[A-Za-z]", prose_part(s["text"]))) >= 15), "")
            index_sessions.append({
                "run": run,
                "node": p["nid"],
                "generation": p["gen"],
                "parent": p["parent"],
                "aborted": p["aborted"],
                "made_edit": p["made_edit"],
                "player_changed": p["player_changed"],
                "valid": p["valid"],
                "files_edited": p["fe"],
                "practice_before": p["before"],
                "practice_after": p["after"],
                "gained": p["gained"],
                "lost": p["lost"],
                "n_steps": len(steps),
                "n_commands": sum(1 for s in steps if s["kind"] == "command"),
                "n_nudges": sum(1 for s in steps if s["kind"] == "nudge" and not s.get("gateway")),
                "n_gateway": sum(1 for s in steps if s.get("gateway")),
                "coach_tokens": p["coach_tokens"],
                "first_line": first_sentence(first_think),
                "outcome_kind": p["outcome"],
            })
        runs_meta.append({
            "run": run,
            "kind": tree.get("kind") if tree else cfg.get("phase"),
            "arm": tree.get("arm") if tree else cfg.get("arm"),
            "in_trees": bool(tree),
            "n_sessions": len(parsed),
            "n_aborted": sum(1 for p in parsed if p["aborted"]),
            "output_cap_chars": out_cap,
            "command_cap_chars": cmd_cap,
        })
        print(f"{run:24s} sessions={len(parsed):3d} size={sizes[f'{run}.json']/1024:8.1f} KB caps={out_cap}/{cmd_cap}")

    index = {
        "generated_by": "arcexp/build_coach_sessions.py",
        "schema": {
            "runs[]": "{run, kind, arm, in_trees, n_sessions, n_aborted, output_cap_chars, command_cap_chars}",
            "sessions[]": "{run, node, generation, parent, aborted, made_edit, player_changed, valid, files_edited[{path, role, added, removed}], practice_before, practice_after, gained[], lost[], n_steps, n_commands, n_nudges, n_gateway, coach_tokens, first_line, outcome_kind}",
            "gained/lost": "practice tasks whose per-task score rose / fell vs the parent node (per-task scores are fractions of test inputs solved, pass@2)",
            "outcome_kind": "'no edit' (empty patch) | 'not scored' (aborted round or no score) | 'broke' (invalid or score 0) | 'improved' | 'same' | 'worse' (vs parent practice score)",
            "<run>.json": "{run, sessions:{<node>:{steps:[{kind: brief|think|command|output|nudge|edit|done, text, cmd?, tool?, truncated?, full_chars?, trim?, has_scores?, n_traces?, ignored_calls?, from_echo?, collapsed_repeats?, empty?, raw?, after_call?, unparsed_call?, gateway?}], diff, diff_note?, aborted?}}}",
        },
        "notes": [
            "Aborted rounds (gen_<k>.aborted_<ts> dirs, restarted by the harness) that left a transcript are included with node '<k>.aborted_<ts>' and outcome 'not scored' (or 'no edit'). In all of them the coaching session finished; the harness stopped the round while the edited player was being scored (generate.log). Their parent is not recorded (parent=null). Aborted rounds stopped during coaching left no transcript and are not included (see excluded).",
            "gained/lost are filled only for a scored edit (made_edit, not aborted, practice_after not null); no-edit and unscored nodes can carry a partial per_task.",
            "player_changed=false with made_edit=true: only coach or other files changed, so the player is the parent's and any score change is re-evaluation noise.",
            "valid mirrors trees.json node.valid (false: the harness did not accept the node as a parent).",
            "Gateway replies (the model gateway answering '[GATEWAY] ... token budget ... exhausted' in place of a model reply) are 'nudge' steps with gateway=true, not coach messages.",
            "Text the coach wrote after its executed tool call is a separate 'think' step with after_call=true, placed right after the command. Malformed or unrun tool calls stay in the text and set unparsed_call=true. Messages with no readable text are 'think' steps with empty=true (raw: the first 80 chars). Lone tag / brace fragments left by tool-call markup are dropped.",
            "Local paths '/home/<user>/HyperAgents/' are replaced by '" + LOCAL_MARK + "' before any truncation.",
            "Runs not in trees.json (smoke, trial_*) take scores from gen_<k>/arc_eval/report.json and have no coach_tokens.",
            "'command' steps follow the harness's own tool-call detection (first valid <json> block, else a bare JSON object); ignored_calls counts further well-formed calls in the same message that the harness did not run.",
            "Nudge steps with the harness's standard text are shortened to '(standard nudge) " + NUDGE_SHORT + "'; full text: " + STANDARD_NUDGE,
            "Harness lines such as 'Error: Output context exceeded' appear as 'nudge' steps prefixed '[harness]'.",
            "Narration is never trimmed, except that degenerate token loops (a fragment or line repeated verbatim many times) are collapsed with a note and collapsed_repeats=true, and lone tag / brace lines are dropped.",
            "Tool outputs keep head+tail; the brief's grid dumps are collapsed (inline grids, including answers, keep their first 120 chars) and failure traces share a ~2.4 KB budget (start and end of each kept); brief.trim says what was cut; narration ('think') is never trimmed.",
        ] + trims,
        "excluded": {"crashed_transcripts_skipped": n_crashed, "aborted_rounds_without_transcript": n_aborted_no_tx},
        "redactions": dict(REDACTIONS),
        "runs": runs_meta,
        "sessions": index_sessions,
    }
    blob = json.dumps(index, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as fh:
        fh.write(blob)
    sizes["index.json"] = len(blob.encode())
    total = sum(sizes.values())
    print(f"index.json {sizes['index.json']/1024:.1f} KB; total {total/1e6:.3f} MB ({total:,} bytes); sessions {len(index_sessions)}; crashed skipped {n_crashed}")
    print("redactions", dict(REDACTIONS))
    if total > TOTAL_CAP:
        print("WARNING: total over budget", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
