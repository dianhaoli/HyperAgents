"""Export the full archive of every loop run: each agent's code, scores, parent and children, and the
archive as it stood after every generation.

  python -m arcexp.export_archive          -> exp/archive_export/<run>/
    nodes.json                 per node: generation, parent, children, loop score (or null), valid, patch file,
                               snapshot (exact evaluated code, tar.gz of regular files) and coach-code change vs I_0
    archive_by_generation.json for every g: the archive (node ids) as it stood after generation g
    code/gen_<g>/              extracted evaluated code of each node (initial = root commit)
"""
import json
import os
import shutil
import sys

from arcexp.common import EXP
from arcexp.evolved import _SIG_CACHE_P, archive_at
from arcexp.phases import materialize

sys.path.insert(0, os.path.dirname(EXP))
from utils.gl_utils import get_parent_genid, load_archive_data  # noqa: E402


def export_run(name):
    run_dir = os.path.join(EXP, "runs", name)
    out_dir = os.path.join(run_dir, f"generate_{name}")
    if not os.path.exists(os.path.join(out_dir, "archive.jsonl")):
        return
    dst = os.path.join(EXP, "archive_export", name)
    os.makedirs(os.path.join(dst, "code"), exist_ok=True)
    arch = load_archive_data(os.path.join(out_dir, "archive.jsonl"), last_only=True)["archive"]
    parent = {g: get_parent_genid(out_dir, g) for g in arch}
    sig = json.load(open(_SIG_CACHE_P)) if os.path.exists(_SIG_CACHE_P) else {}
    nodes = {}
    for g in arch:
        gd = os.path.join(out_dir, f"gen_{g}")
        md = json.load(open(os.path.join(gd, "metadata.json"))) if os.path.exists(os.path.join(gd, "metadata.json")) else {}
        rp = os.path.join(gd, "arc_eval", "report.json")
        score = json.load(open(rp))["overall_accuracy"] if os.path.exists(rp) else None
        snap = os.path.join(run_dir, "snapshots", f"gen_{g}.tar.gz")
        code_dir = os.path.join(dst, "code", f"gen_{g}")
        if not os.path.exists(code_dir) and (g == "initial" or os.path.exists(snap)):
            materialize(run_dir, g, code_dir)
            shutil.rmtree(os.path.join(code_dir, "domains", "arc", "data"), ignore_errors=True)  # visible task data, large
        nodes[str(g)] = {
            "generation": g, "parent": parent.get(g), "children": [c for c in arch if parent.get(c) == g],
            "loop_score_on_set": score, "valid_parent": md.get("valid_parent", True if g == "initial" else None),
            "patch_file": os.path.relpath(os.path.join(gd, "agent_output", "model_patch.diff"), EXP)
            if os.path.exists(os.path.join(gd, "agent_output", "model_patch.diff")) else None,
            "snapshot": os.path.relpath(snap, EXP) if os.path.exists(snap) else None,
            "code_dir": os.path.relpath(code_dir, EXP) if os.path.exists(code_dir) else None,
            "coach_files_changed_vs_I0": sig.get(f"{name}:{g}"),
        }
    by_gen = {}
    max_g = max([g for g in arch if isinstance(g, int)] or [0])
    for k in range(0, max_g + 1):
        by_gen[str(k)] = [str(x) for x in archive_at(out_dir, k)]
    json.dump(nodes, open(os.path.join(dst, "nodes.json"), "w"), indent=1)
    json.dump(by_gen, open(os.path.join(dst, "archive_by_generation.json"), "w"))
    print(name, len(nodes), "nodes exported")


if __name__ == "__main__":
    names = sys.argv[1:] or sorted(n for n in os.listdir(os.path.join(EXP, "runs"))
                                   if os.path.exists(os.path.join(EXP, "runs", n, "config.json")) and n != "smoke")
    for n in names:
        export_run(n)
