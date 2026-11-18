"""Extract all reader-facing text of the explorer page into one editable file, and apply edits back.

  python3 -m arcexp.page_text extract     -> explorer/PAGE_TEXT.md  (+ explorer/.page_text_map.json)
  python3 -m arcexp.page_text apply [FILE] -> writes changed blocks back into explorer/index.html and js/*.js
  python3 -m arcexp.page_text check       -> extract, apply unchanged text, verify the page is byte-identical

PAGE_TEXT.md format
- Part 1 (page prose, from index.html): one block per paragraph / heading / list item / caption / table cell,
  each under a line `[[ID]]`. Footnotes are separate blocks `[[fn-N]]`, referenced in text as `[^N]`.
  Numbers bound to data are locked placeholders `{{kind:key}}` and must be kept as written.
  Inline formatting: **bold**, *italic*, `code`, [text](link). Anything else appears as raw HTML: leave it.
- Part 2 (text inside figures, from js/fig-*.js and js/core.js): one block per string literal
  `[[js:FILE:LINE:N]]`. Some are fragments joined with numbers in code: keep leading/trailing spaces
  and punctuation that join them.
"""
import hashlib
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(ROOT, "explorer")
INDEX = os.path.join(EXP, "index.html")
OUT = os.path.join(EXP, "PAGE_TEXT.md")
MAP = os.path.join(EXP, ".page_text_map.json")
JS_FILES = ["core.js", "fig-setup.js", "fig-puzzle.js", "fig-results.js", "fig-extension.js", "fig-watch.js",
            "fig-demo.js", "fig-tree.js", "fig-replay.js", "fig-transcripts.js", "fig-audit.js"]

BLOCK_RE = re.compile(
    r'<(h1|h2|h3|p|li|figcaption|summary|td|th|caption|div class="fig-title")(\s[^>]*)?>(.*?)</(h1|h2|h3|p|li|figcaption|summary|td|th|caption|div)>',
    re.S)
FN_RE = re.compile(r'<sup class="fn" id="fnref-(\d+)"><a href="#fn-\1">\1</a></sup>'
                   r'<span class="sidenote" id="fn-\1"><span class="sn-num">\1</span>(.*?)</span>(?=[\s\S])', re.S)
DV_RE = re.compile(r'<span data-v="([^"]+)">(.*?)</span>', re.S)


# ---------------- inline html <-> light markdown ----------------
def _fn_spans(s):
    """Footnote = <sup..>..</sup><span class="sidenote" id="fn-N">...</span> with balanced inner spans."""
    out, i = [], 0
    pat = re.compile(r'<sup class="fn" id="fnref-(\d+)"><a href="#fn-\d+">\d+</a></sup><span class="sidenote" id="fn-\d+"><span class="sn-num">\d+</span>')
    while True:
        m = pat.search(s, i)
        if not m:
            break
        depth, j = 1, m.end()
        while depth and j < len(s):
            o = s.find("<span", j)
            c = s.find("</span>", j)
            if o != -1 and o < c:
                depth += 1
                j = o + 5
            else:
                depth -= 1
                j = c + 7
        out.append((m.start(), j, m.group(1), s[m.end():j - 7], s[m.start():j]))
        i = j
    return out


def to_md(inner, dvmap):
    s = inner
    s = DV_RE.sub(lambda m: dvmap.setdefault("{{%s}}" % m.group(1), m.group(0)) and "{{%s}}" % m.group(1), s)
    s = re.sub(r'<a class="cite" href="(#[^"]+)">(.*?)</a>', r'[\2](\1 "cite")', s)
    s = re.sub(r'<a href="([^"]+)">(.*?)</a>', r'[\2](\1)', s)
    s = re.sub(r'<b>(.*?)</b>', r'**\1**', s, flags=re.S)
    s = re.sub(r'<i>(.*?)</i>', r'*\1*', s, flags=re.S)
    s = re.sub(r'<code>(.*?)</code>', r'`\1`', s, flags=re.S)
    s = html.unescape(s)
    return re.sub(r'\s*\n\s*', ' ', s).strip()


def to_html(md, dvmap):
    s = html.escape(md, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<i>\1</i>', s)
    s = re.sub(r'\[([^\]]+)\]\((#[^ )]+) &quot;cite&quot;\)', r'<a class="cite" href="\2">\1</a>', s)
    s = re.sub(r'\[([^\]]+)\]\((#[^ )]+) "cite"\)', r'<a class="cite" href="\2">\1</a>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', s)
    # raw html the writer kept (was escaped above): restore tags only
    s = re.sub(r'&lt;(/?[a-zA-Z][^&]*?)&gt;', lambda m: '<' + html.unescape(m.group(1)) + '>', s)
    for k, v in dvmap.items():
        s = s.replace(k, v)
    s = s.replace('&lt;', '&lt;')
    return ''.join(c if ord(c) < 128 else '&#%d;' % ord(c) for c in s)


# ---------------- extraction ----------------
def section_of(pos, src):
    m = None
    for m in re.finditer(r'<!-- =+ ([^=]+?) =+ -->', src[:pos]):
        pass
    return m.group(1).strip() if m else "Top"


def extract():
    src = open(INDEX, encoding="utf-8").read()
    dvmap, blocks, fns = {}, [], {}
    seen = {}
    for m in BLOCK_RE.finditer(src):
        tag, attrs, inner = m.group(1), m.group(2) or "", m.group(3)
        if tag.startswith("div") and m.group(4) != "div":
            continue
        if not tag.startswith("div") and m.group(4) != tag:
            continue
        if re.search(r'<(p|li|ul|ol|div|figure|section|table|h\d)[\s>]', inner):
            continue  # container, its children are blocks
        text_only = re.sub(r'<[^>]+>', '', inner).strip()
        if not text_only:
            continue
        work = inner
        for (a, b, n, body, full) in reversed(_fn_spans(work)):
            fns[n] = {"html": body, "md": to_md(body, dvmap)}
            work = work[:a] + "[^%s]" % n + work[b:]
        sec = section_of(m.start(), src)
        base = re.sub(r'[^a-z0-9]+', '-', sec.lower()).strip('-') or 'top'
        kind = "title" if tag.startswith("div") else tag
        seen[(base, kind)] = seen.get((base, kind), 0) + 1
        bid = "%s.%s%d" % (base, kind, seen[(base, kind)])
        blocks.append({"id": bid, "section": sec, "tag": kind, "start": m.start(3), "end": m.end(3),
                       "orig_inner": inner, "md": to_md(work, dvmap)})
    # JS strings
    js = []
    for f in JS_FILES:
        p = os.path.join(EXP, "js", f)
        if not os.path.exists(p):
            continue
        for ln, line in enumerate(open(p, encoding="utf-8").read().split("\n"), 1):
            if line.strip().startswith(("//", "*", "/*")) or "console." in line or "querySelector" in line:
                continue
            for k, sm in enumerate(re.finditer(r"'((?:[^'\\]|\\.)*)'", line)):
                t = sm.group(1)
                words = re.findall(r"[A-Za-z]{2,}", t)
                if len(words) < 3 or re.search(r'[{}<>=]|\b(var|function|return)\b|^[a-z-]+( [a-z-]+)*$|^#|\.json|\.js', t):
                    continue
                js.append({"id": "js:%s:%d:%d" % (f, ln, k), "file": f, "line": ln, "lit": t,
                           "text": t.replace("\\'", "'")})
    lines = ["# Page text: Coaching the Coach", "",
             "Edit the text under each `[[ID]]` line. Do not change or remove the `[[ID]]` lines.",
             "", "Rules for the writer:",
             "- `{{...}}` are numbers read from the data. Keep each one exactly as written; you may move it within its block.",
             "- `[^N]` marks where footnote N attaches; footnote text is in its own `[[fn-N]]` block.",
             "- Formatting: **bold**, *italic*, `code`, [text](link). `[n](#ref-x \"cite\")` is a citation: keep it.",
             "- Raw HTML tags, if any, must stay balanced. Keep blocks to one paragraph (no blank lines inside a block).",
             "- Part 2 strings live in code; some are joined to numbers, so keep their leading/trailing spaces and the",
             "  sense of the fragment. Delete nothing; to drop a sentence, leave its block empty only if it is a whole sentence.",
             "", "---", "", "## Part 1: page prose (index.html)", ""]
    cur = None
    for b in blocks:
        if b["section"] != cur:
            cur = b["section"]
            lines += ["", "### " + cur, ""]
        lines += ["[[%s]]  <!-- %s -->" % (b["id"], b["tag"]), b["md"], ""]
    lines += ["", "### Footnotes", ""]
    for n in sorted(fns, key=int):
        lines += ["[[fn-%s]]" % n, fns[n]["md"], ""]
    lines += ["", "---", "", "## Part 2: text inside the figures (js/*.js)", ""]
    curf = None
    for j in js:
        if j["file"] != curf:
            curf = j["file"]
            lines += ["", "### " + curf, ""]
        lines += ["[[%s]]" % j["id"], j["text"], ""]
    open(OUT, "w", encoding="utf-8").write("\n".join(lines).rstrip() + "\n")
    json.dump({"index_sha": hashlib.sha256(src.encode()).hexdigest(), "dv": dvmap, "blocks": blocks,
               "fns": fns, "js": js}, open(MAP, "w"), indent=0)
    print("wrote %s: %d prose blocks, %d footnotes, %d figure strings" % (OUT, len(blocks), len(fns), len(js)))


# ---------------- apply ----------------
def parse_md(path):
    out, cur, buf = {}, None, []
    for line in open(path, encoding="utf-8").read().split("\n"):
        m = re.match(r'^\[\[([^\]]+)\]\]', line)
        if m:
            if cur:
                out[cur] = "\n".join(buf).strip("\n")
            cur, buf = m.group(1), []
        elif cur is not None:
            if line.startswith("### ") or line.startswith("## ") or line == "---":
                out[cur] = "\n".join(buf).strip("\n")
                cur, buf = None, []
            else:
                buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).strip("\n")
    return out


def apply(path=OUT):
    mp = json.load(open(MAP))
    src = open(INDEX, encoding="utf-8").read()
    if hashlib.sha256(src.encode()).hexdigest() != mp["index_sha"]:
        sys.exit("index.html changed since extract; re-run extract first (or merge by hand).")
    ed = parse_md(path)
    dv = mp["dv"]
    changed, problems = [], []
    new_fn = {}
    for n, f in mp["fns"].items():
        t = ed.get("fn-" + n, f["md"])
        new_fn[n] = f["html"] if t == f["md"] else to_html(t, dv)
        if t != f["md"]:
            changed.append("fn-" + n)
    out = src
    for b in sorted(mp["blocks"], key=lambda b: -b["start"]):
        t = ed.get(b["id"])
        if t is None:
            problems.append("missing block " + b["id"])
            continue
        fn_in_block = re.findall(r'\[\^(\d+)\]', b["md"])
        if t == b["md"] and not any(("fn-" + n) in changed for n in fn_in_block):
            continue
        for k in re.findall(r'\{\{[^}]+\}\}', b["md"]):
            if k not in t:
                problems.append("%s: number placeholder %s was removed" % (b["id"], k))
        h = to_html(t, dv)
        for n in re.findall(r'\[\^(\d+)\]', h):
            h = h.replace("[^%s]" % n, '<sup class="fn" id="fnref-%s"><a href="#fn-%s">%s</a></sup><span class="sidenote" id="fn-%s"><span class="sn-num">%s</span>%s</span>'
                          % (n, n, n, n, n, new_fn.get(n, "")))
        out = out[:b["start"]] + h + out[b["end"]:]
        changed.append(b["id"])
    open(INDEX, "w", encoding="utf-8").write(out)
    # js
    for j in mp["js"]:
        t = ed.get(j["id"])
        if t is None or t == j["text"]:
            continue
        p = os.path.join(EXP, "js", j["file"])
        lines = open(p, encoding="utf-8").read().split("\n")
        L = lines[j["line"] - 1]
        old = "'" + j["lit"] + "'"
        if L.count(old) != 1:
            problems.append("%s: could not place (line changed?)" % j["id"])
            continue
        lines[j["line"] - 1] = L.replace(old, "'" + t.replace("\\", "\\\\").replace("'", "\\'") + "'")
        open(p, "w", encoding="utf-8").write("\n".join(lines))
        changed.append(j["id"])
    print("changed %d blocks" % len(changed))
    for c in changed:
        print("  " + c)
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  " + p)


def check():
    import shutil, tempfile
    tmp = tempfile.mkdtemp()
    shutil.copy(INDEX, os.path.join(tmp, "index.html"))
    jsb = {f: open(os.path.join(EXP, "js", f), encoding="utf-8").read() for f in JS_FILES if os.path.exists(os.path.join(EXP, "js", f))}
    extract()
    before = open(INDEX, encoding="utf-8").read()
    apply(OUT)
    after = open(INDEX, encoding="utf-8").read()
    ok = before == after and all(open(os.path.join(EXP, "js", f), encoding="utf-8").read() == s for f, s in jsb.items())
    if not ok:
        shutil.copy(os.path.join(tmp, "index.html"), INDEX)
        for f, s in jsb.items():
            open(os.path.join(EXP, "js", f), "w", encoding="utf-8").write(s)
        extract()
    print("round trip:", "OK (no change)" if ok else "FAILED (restored originals)")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "extract"
    {"extract": extract, "apply": lambda: apply(sys.argv[2] if len(sys.argv) > 2 else OUT), "check": check}[cmd]()
