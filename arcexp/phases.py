"""Phase commands (all resumable; results append to exp/results/<phase>.jsonl).

  python -m arcexp.phases screen                 # A_0 single calls x3 on the 100 screen tasks
  python -m arcexp.phases b0 --reps 3            # A_0 on the 120 held-out tasks, standard budget
  python -m arcexp.phases xhigh                  # one held-out pass of A_0 at xhigh effort
  python -m arcexp.phases final --run <name>     # final scoring of a pay-off run
  python -m arcexp.phases status
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

from arcexp import arc_data
from arcexp.arc_eval import evaluate_set
from arcexp.common import EXP, REPO, append_jsonl, chown_agent, gw_status, read_jsonl
from arcexp.safeio import extract_snapshot

sys.path.insert(0, REPO)
from utils.gl_utils import load_archive_data  # noqa: E402

TEMPLATE = os.path.join(REPO, "agent_template")
WORKERS = int(os.environ.get("ARC_WORKERS", "24"))


def splits():
    return json.load(open(os.path.join(REPO, "splits.json")))


def materialize(run_dir, genid, dest):
    """The exact code of node `genid` of a loop run: its evaluation snapshot (regular files, taken right before
    the loop evaluated it). The initial node is the run's root commit (root-owned repo; git archive runs no hooks)."""
    if os.path.exists(dest):
        shutil.rmtree(dest)
    if str(genid) == "initial":
        cfg = json.load(open(os.path.join(run_dir, "config.json")))
        root = os.path.join(run_dir, f"generate_{cfg['name']}", "gen_initial", "hyperagents")
        os.makedirs(dest)
        p1 = subprocess.Popen(["git", "-C", root, "archive", cfg["root_commit"]], stdout=subprocess.PIPE)
        subprocess.run(["tar", "-x", "-C", dest], stdin=p1.stdout, check=True)
        p1.wait()
    else:
        snap = os.path.join(run_dir, "snapshots", f"gen_{genid}.tar.gz")
        if not os.path.exists(snap):
            raise FileNotFoundError(f"no snapshot for {run_dir} gen {genid}")
        extract_snapshot(snap, dest)
    return dest


def cmd_screen(a):
    ids = splits()["screen"]
    for call in range(3):
        s = evaluate_set(TEMPLATE, ids, {"phase": "screen", "arm": "A0", "seed": "-", "iteration": call},
                         workers=WORKERS, single=True)
        print(f"screen call {call}: {s['score']:.3f} missing={s['missing']} infra_rows={s['infra_error_rows']} fmt_fail={s['format_failures']}")


def cmd_b0(a):
    ids = splits()["heldout"]
    for rep in ([a.only] if a.only is not None else range(a.reps)):
        s = evaluate_set(TEMPLATE, ids, {"phase": "b0", "arm": "A0", "seed": "-", "iteration": rep}, workers=WORKERS)
        append_jsonl(os.path.join(EXP, "results", "b0_summary.jsonl"), {"rep": rep, **{k: v for k, v in s.items() if k != "per_task"}})
        print(f"B0 rep {rep}: {s['score']:.4f} missing={s['missing']} fmt_fail={s['format_failures']}")
        if s["missing"]:
            raise SystemExit("B0 incomplete; rerun")


def cmd_xhigh(a):
    ids = splits()["heldout"]
    s = evaluate_set(TEMPLATE, ids, {"phase": "xhigh", "arm": "A0", "seed": "-", "iteration": 0}, workers=WORKERS,
                     effort_role="task_xhigh")
    print(f"xhigh pass: {s['score']:.4f} missing={s['missing']}")


def node_scores(out_dir):
    """Pay-off-set score of every evaluated node of a run (as the loop records it)."""
    arch = load_archive_data(os.path.join(out_dir, "archive.jsonl"), last_only=True)["archive"]
    res = {}
    for g in arch:
        rp = os.path.join(out_dir, f"gen_{g}", "arc_eval", "report.json")
        if os.path.exists(rp):
            md = os.path.join(out_dir, f"gen_{g}", "metadata.json")
            valid = True if g in ("initial", 0) else json.load(open(md)).get("valid_parent", False) if os.path.exists(md) else False
            if valid:
                res[g] = json.load(open(rp))["overall_accuracy"]
    return res


def cmd_final(a):
    run_dir = os.path.join(EXP, "runs", a.run)
    cfg = json.load(open(os.path.join(run_dir, "config.json")))
    out_dir = os.path.join(run_dir, f"generate_{cfg['name']}")
    sc = node_scores(out_dir)
    order = sorted(sc, key=lambda g: (-sc[g], str(g)))  # ties: deterministic
    cands = order[:2]
    ids = splits()[cfg["task_set"]]
    combined = {}
    for g in cands:
        d = materialize(run_dir, g, os.path.join(run_dir, "final_agents", f"gen_{g}"))
        s = evaluate_set(d, ids, {"phase": "rescore", "arm": cfg["arm"], "seed": cfg["seed"], "iteration": g}, workers=WORKERS)
        if s["missing"]:
            raise SystemExit(f"{a.run}: rescore of gen_{g} incomplete ({s['missing']} missing); rerun later")
        combined[g] = (sc[g] + s["score"]) / 2
        print(f"{a.run} cand gen_{g}: loop score {sc[g]:.3f} rescore {s['score']:.3f} combined {combined[g]:.3f}")
    best = sorted(cands, key=lambda g: (-combined[g], order.index(g)))[0]
    d = os.path.join(run_dir, "final_agents", f"gen_{best}")
    h = evaluate_set(d, splits()["heldout"], {"phase": "heldout", "arm": cfg["arm"], "seed": cfg["seed"], "iteration": best},
                     workers=WORKERS)
    if h["missing"]:
        raise SystemExit(f"{a.run}: held-out scoring incomplete ({h['missing']} missing); rerun later")
    rec = {"run": a.run, "arm": cfg["arm"], "seed": cfg["seed"], "source_seed": cfg.get("source_seed"),
           "node_scores": {str(k): v for k, v in sc.items()}, "candidates": [str(c) for c in cands],
           "combined": {str(k): v for k, v in combined.items()}, "final_node": str(best), "heldout": h["score"],
           "heldout_missing": h["missing"], "n_accepted": sum(1 for g in sc if g not in ("initial", 0))}
    append_jsonl(os.path.join(EXP, "results", "final_runs.jsonl"), rec)
    print(json.dumps(rec))


def cmd_status(a):
    print(gw_status())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--run")
    ap.add_argument("--only", type=int, default=None)
    a = ap.parse_args()
    {"screen": cmd_screen, "b0": cmd_b0, "xhigh": cmd_xhigh, "final": cmd_final, "status": cmd_status}[a.cmd](a)
