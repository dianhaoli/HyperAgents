"""Evolved meta agents: meta-code closure, I_g selection, transplant onto A_0, self-edit stats.

  python -m arcexp.evolved select            # pick I_g per source seed -> exp/results/ig_selection.json
  python -m arcexp.evolved transplant        # build pay-off templates for each I_g -> exp/transplants/<seed>/
  python -m arcexp.evolved stats             # self-edit rate etc. -> exp/results/source_stats.json
"""
import ast
import json
import os
import shutil
import sys

from arcexp.common import EXP, REPO, chown_agent
from arcexp.sandbox import run_sandboxed

sys.path.insert(0, REPO)
from utils.gl_utils import load_archive_data, get_parent_genid, get_patch_files  # noqa: E402

TEMPLATE = os.path.join(REPO, "agent_template")
ENTRY = ["run_meta_agent.py", "meta_agent.py"]
EXCLUDE_PREFIX = ("domains/",)
EXCLUDE_FILES = ("task_agent.py",)
BASE_FREEZE = ["meta_agent.py", "run_meta_agent.py", "agent", "utils"]


def _mod_to_file(repo, mod):
    parts = mod.split(".")
    for cand in (os.path.join(repo, *parts) + ".py", os.path.join(repo, *parts, "__init__.py")):
        if os.path.isfile(cand):
            return os.path.relpath(cand, repo)
    return None


def static_closure(repo, entries=ENTRY):
    """Repo-local Python files reachable by imports (anywhere in each module) from the entry files."""
    seen, stack = set(), [e for e in entries if os.path.isfile(os.path.join(repo, e))]
    while stack:
        f = stack.pop()
        if f in seen:
            continue
        seen.add(f)
        try:
            tree = ast.parse(open(os.path.join(repo, f)).read())
        except Exception:
            continue
        pkg = os.path.dirname(f).replace(os.sep, ".")
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level:
                    up = pkg.split(".") if pkg else []
                    up = up[: len(up) - (node.level - 1)] if node.level > 1 else up
                    base = ".".join([p for p in up if p] + ([base] if base else []))
                mods = [base] + [f"{base}.{a.name}" if base else a.name for a in node.names]
            elif isinstance(node, ast.Call) and getattr(node.func, "attr", getattr(node.func, "id", "")) in ("import_module", "__import__"):
                if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                    mods = [node.args[0].value]
            for m in mods:
                parts = m.split(".")
                for i in range(1, len(parts) + 1):  # parent packages are loaded too
                    p = _mod_to_file(repo, ".".join(parts[:i]))
                    if p and p not in seen:
                        stack.append(p)
    # tools are loaded dynamically by globbing agent/tools/*.py
    tdir = os.path.join(repo, "agent", "tools")
    if "agent/llm_withtools.py" in seen and os.path.isdir(tdir):
        for fn in os.listdir(tdir):
            if fn.endswith(".py"):
                seen.add(f"agent/tools/{fn}")
    return seen


TRACE = r'''
import sys, os, json, runpy
sys.path.insert(0, "/hyperagents"); os.chdir("/hyperagents")
opened = set()
def hook(ev, args):
    if ev == "open" and args and isinstance(args[0], str):
        p = os.path.abspath(args[0])
        if p.startswith("/hyperagents/"):
            opened.add(os.path.relpath(p, "/hyperagents"))
sys.addaudithook(hook)
err = None
try:
    import importlib
    for m in ["meta_agent", "run_meta_agent"]:
        try:
            importlib.import_module(m)
        except Exception as e:
            err = f"{m}: {e!r}"
    try:
        from agent.tools import load_tools
        load_tools(names="all")
    except Exception as e:
        err = (err or "") + f" tools: {e!r}"
except Exception as e:
    err = repr(e)
mods = set()
for m in list(sys.modules.values()):
    f = getattr(m, "__file__", None) or ""
    if f.startswith("/hyperagents/"):
        mods.add(os.path.relpath(f, "/hyperagents"))
print("TRACE_JSON " + json.dumps({"modules": sorted(mods), "opened": sorted(opened), "err": err}))
'''


def dynamic_closure(repo):
    rc, out = run_sandboxed(["python3", "-c", TRACE], binds=[(repo, "/hyperagents", True)], cwd="/hyperagents", timeout=300)
    for line in out.decode(errors="replace").splitlines():
        if line.startswith("TRACE_JSON "):
            return json.loads(line[len("TRACE_JSON "):])
    return {"modules": [], "opened": [], "err": out.decode(errors="replace")[-1000:]}


def is_excluded(f):
    return f in EXCLUDE_FILES or f.startswith(EXCLUDE_PREFIX)


def meta_code_files(repo):
    files = set(static_closure(repo))
    dyn = dynamic_closure(repo)
    files |= {m for m in dyn["modules"] if m.endswith(".py")}
    code = sorted(f for f in files if f.endswith(".py") and not is_excluded(f) and os.path.isfile(os.path.join(repo, f)))
    return code, dyn


def state_files(repo, code):
    """Non-code repo files referenced by string literals in the meta code (memory/state)."""
    out = set()
    for f in code:
        try:
            tree = ast.parse(open(os.path.join(repo, f)).read())
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and 0 < len(node.value) < 200 and "\n" not in node.value:
                v = node.value
                for cand in (v, v.replace("/hyperagents/", "", 1)):
                    cand = cand.lstrip("./")
                    if not cand or cand.endswith(".py") or is_excluded(cand) or cand in ("README.md", "requirements.txt"):
                        continue
                    p = os.path.join(repo, cand)
                    if os.path.exists(p) and os.path.realpath(p).startswith(os.path.realpath(repo) + os.sep) and not cand.startswith(".git"):
                        out.add(cand.rstrip("/") + ("/" if os.path.isdir(p) else ""))
    return sorted(out)


def norm_ast(path):
    try:
        return ast.dump(ast.parse(open(path).read()), annotate_fields=False, include_attributes=False)
    except Exception:
        return "UNPARSEABLE:" + open(path, errors="replace").read()


def _strip_docstrings_dump(path):
    """AST dump with docstrings removed (comments/whitespace are already ignored by ast)."""
    try:
        tree = ast.parse(open(path).read())
    except Exception:
        return "UNPARSEABLE:" + open(path, errors="replace").read()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)) and node.body:
            b = node.body[0]
            if isinstance(b, ast.Expr) and isinstance(getattr(b, "value", None), ast.Constant) and isinstance(b.value.value, str):
                node.body = node.body[1:] or [ast.Pass()]
    return ast.dump(tree, annotate_fields=False, include_attributes=False)


def meta_signature(repo):
    code, _ = meta_code_files(repo)
    return {f: norm_ast(os.path.join(repo, f)) for f in code}


def diff_meta(sig_a, sig_b):
    files = set(sig_a) | set(sig_b)
    return sorted(f for f in files if sig_a.get(f) != sig_b.get(f))


# ---------------------------------------------------------------- selection

def source_runs():
    d = os.path.join(EXP, "runs")
    out = []
    for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        p = os.path.join(d, name, "config.json")
        if os.path.exists(p):
            c = json.load(open(p))
            if c.get("phase") == "source":
                out.append((name, c))
    return out


def node_score(out_dir, g):
    rp = os.path.join(out_dir, f"gen_{g}", "arc_eval", "report.json")
    md = os.path.join(out_dir, f"gen_{g}", "metadata.json")
    if not os.path.exists(rp):
        return None
    if g not in ("initial", 0) and os.path.exists(md) and not json.load(open(md)).get("valid_parent", False):
        return None
    return json.load(open(rp))["overall_accuracy"]


def patch_touches(patch_path, files_or_dirs):
    if not os.path.exists(patch_path):
        return []
    hit = set()
    for line in open(patch_path, errors="replace"):
        if line.startswith("diff --git"):
            p = line.split(" b/")[-1].strip()
            for t in files_or_dirs:
                if p == t or p.startswith(t.rstrip("/") + "/"):
                    hit.add(p)
    return sorted(hit)


def cmd_select():
    from arcexp.phases import materialize
    i0 = meta_signature(TEMPLATE)
    sel = {}
    for name, cfg in source_runs():
        run_dir = os.path.join(EXP, "runs", name)
        out_dir = os.path.join(run_dir, f"generate_{name}")
        arch = load_archive_data(os.path.join(out_dir, "archive.jsonl"), last_only=True)["archive"]
        parent = {g: get_parent_genid(out_dir, g) for g in arch}
        children = {g: [c for c in arch if parent.get(c) == g] for g in arch}
        cands = []
        for g in arch:
            if not children[g]:
                continue
            d = materialize(run_dir, g, os.path.join(run_dir, "nodes", f"gen_{g}"))
            sig = meta_signature(d)
            changed = diff_meta(i0, sig)
            shutil.rmtree(d, ignore_errors=True)
            if not changed:
                continue
            ps = node_score(out_dir, g)
            kid_scores = [node_score(out_dir, c) for c in children[g]]
            scored = [k for k in kid_scores if k is not None]
            if ps is None or not scored:
                continue
            imp = sum(k - ps for k in scored) / len(scored)
            # meta edits along the ancestry (which generations' patches touched meta code)
            anc, x = [], g
            while x not in (None, "initial"):
                anc.append(x)
                x = parent.get(x)
            meta_edit_gens = [a for a in reversed(anc)
                              if patch_touches(os.path.join(out_dir, f"gen_{a}", "agent_output", "model_patch.diff"), list(sig) + BASE_FREEZE)]
            cands.append({"gen": g, "score": ps, "n_children": len(children[g]), "n_scored_children": len(scored),
                          "mean_child_improvement": imp, "meta_files_changed_vs_I0": changed,
                          "meta_edit_generations_in_ancestry": meta_edit_gens})
        cands.sort(key=lambda c: (-c["mean_child_improvement"], int(c["gen"])))
        sel[name] = {"source_seed": cfg["seed"], "qualifying": bool(cands), "I_g": cands[0] if cands else None,
                     "all_candidates": cands}
        print(name, "->", (cands[0]["gen"], round(cands[0]["mean_child_improvement"], 3)) if cands else "NO QUALIFYING AGENT")
    json.dump(sel, open(os.path.join(EXP, "results", "ig_selection.json"), "w"), indent=1)


# ---------------------------------------------------------------- transplant

def transplant(run_name, genid, dest):
    """Copy every code file the I_g improvement step loads (except task-agent and domain code) onto A_0.
    State/memory files it reads are created empty. The meta code itself is copied verbatim."""
    from arcexp.phases import materialize
    run_dir = os.path.join(EXP, "runs", run_name)
    src = materialize(run_dir, genid, os.path.join(run_dir, "nodes", f"gen_{genid}"))
    code, dyn = meta_code_files(src)
    states = state_files(src, code)
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(TEMPLATE, dest)
    for f in code:
        os.makedirs(os.path.dirname(os.path.join(dest, f)) or dest, exist_ok=True)
        shutil.copy2(os.path.join(src, f), os.path.join(dest, f))
    emptied = []
    for s in states:
        p = os.path.join(dest, s)
        if s.endswith("/"):
            if os.path.exists(p):
                shutil.rmtree(p)
            os.makedirs(p, exist_ok=True)
        else:
            os.makedirs(os.path.dirname(p) or dest, exist_ok=True)
            orig = open(os.path.join(src, s), errors="replace").read().strip()
            empty = "{}" if (s.endswith(".json") and orig.startswith("{")) else "[]" if (s.endswith(".json") and orig.startswith("[")) else ""
            open(p, "w").write(empty)
        emptied.append(s)
    # sanity: A_0 task agent untouched
    assert open(os.path.join(dest, "task_agent.py")).read() == open(os.path.join(TEMPLATE, "task_agent.py")).read()
    state_set = {s.rstrip("/") for s in emptied}
    freeze = sorted(set(BASE_FREEZE) | set(code))
    # a frozen directory must not contain a state file the meta agent needs to write
    final_freeze = []
    for p in freeze:
        if any(s == p or s.startswith(p.rstrip("/") + "/") for s in state_set):
            final_freeze += [f for f in code if f.startswith(p.rstrip("/") + "/")]
        else:
            final_freeze.append(p)
    final_freeze = sorted(set(final_freeze) - state_set)
    manifest = {"source_run": run_name, "gen": genid, "code_files": code, "state_files_emptied": emptied,
                "freeze_paths": final_freeze, "dynamic_trace_err": dyn.get("err"),
                "files_differing_from_I0": diff_meta(meta_signature(TEMPLATE), meta_signature(dest))}
    json.dump(manifest, open(os.path.join(os.path.dirname(dest), "manifest.json"), "w"), indent=1)
    # keep a copy of the I_g's full code for the deliverables
    keep = os.path.join(os.path.dirname(dest), "I_g_full_repo")
    if os.path.exists(keep):
        shutil.rmtree(keep)
    shutil.copytree(src, keep, ignore=shutil.ignore_patterns(".git", "__pycache__"))
    shutil.rmtree(src, ignore_errors=True)
    chown_agent(dest)
    return manifest


def cmd_transplant():
    sel = json.load(open(os.path.join(EXP, "results", "ig_selection.json")))
    for name, s in sel.items():
        if not s["qualifying"]:
            continue
        dest = os.path.join(EXP, "transplants", name, "template")
        m = transplant(name, s["I_g"]["gen"], dest)
        print(name, "gen", s["I_g"]["gen"], "code files", len(m["code_files"]), "state", m["state_files_emptied"],
              "diff vs I0", m["files_differing_from_I0"])


def cmd_stats():
    i0_files = set(meta_code_files(TEMPLATE)[0]) | set(BASE_FREEZE)
    stats = {}
    for name, cfg in source_runs():
        out_dir = os.path.join(EXP, "runs", name, f"generate_{name}")
        arch = load_archive_data(os.path.join(out_dir, "archive.jsonl"), last_only=True)["archive"]
        parents = {get_parent_genid(out_dir, g) for g in arch}
        gens = [g for g in arch if g not in ("initial", 0)]
        rows = []
        for g in gens:
            pf = os.path.join(out_dir, f"gen_{g}", "agent_output", "model_patch.diff")
            touched_all = patch_touches(pf, [""]) if os.path.exists(pf) else []
            meta_t = patch_touches(pf, sorted(i0_files))
            rows.append({"gen": g, "parent": get_parent_genid(out_dir, g), "score": node_score(out_dir, g),
                         "files_changed": touched_all, "meta_files_changed": meta_t, "became_parent": g in parents})
        stats[name] = {"generations": rows, "n_gens": len(rows),
                       "n_self_edit": sum(1 for r in rows if r["meta_files_changed"]),
                       "n_self_edit_parents": sum(1 for r in rows if r["meta_files_changed"] and r["became_parent"])}
        print(name, stats[name]["n_self_edit"], "/", len(rows), "self-edits;", stats[name]["n_self_edit_parents"], "became parents")
    json.dump(stats, open(os.path.join(EXP, "results", "source_stats.json"), "w"), indent=1)


if __name__ == "__main__":
    {"select": cmd_select, "transplant": cmd_transplant, "stats": cmd_stats}[sys.argv[1]]()
