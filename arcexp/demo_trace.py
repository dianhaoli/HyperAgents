"""Traced demo runs (DECISIONS 41). NOT part of the experiment's results; everything goes to exp/demo/.

Reuses the real machinery unchanged (sandbox per test input, gateway tokens with the same per-token caps,
host-side scoring of arc_eval, run_loop's LocalContainer + generate_loop for one coaching generation, the
same freeze rules). The only differences: every scope phase starts with "demo_" so the gateway traces each
model call (exp/demo/traces.jsonl: input as sent, visible output, reasoning summary, usage, cost) and charges
it to the combined $8 demo budget; and arc_eval's result file is redirected to exp/demo/results/<phase>.jsonl
so nothing is ever written to exp/results/.

Usage (root, from the repo; gateway must be up: bash arcexp/start_gateway.sh):

  python3 -m arcexp.demo_trace eval --code A0 --tasks source --reps 1 --tag a0
      Run a player on tasks N times, traced. --code: A0 (agent_template) or a directory whose root holds
      task_agent.py (e.g. exp/demo/coach_<tag>/player_code). --tasks: a split name from splits.json
      (source [default], payoff, smoke) or comma-separated task ids. --reps N: independent repetitions
      (phase demo_eval_<tag>, iteration rep<r>). Writes exp/demo/eval_<tag>.jsonl, one row per
      (rep, task, test_input, attempt): pred, correct, token (gateway token, joins traces.jsonl), and
      exp/demo/eval_<tag>/rep<r>/ (the agent-visible report: report.json, predictions.json,
      agent_evals/chat_history_*.md of unsolved inputs, exactly as a coach would see it).

  python3 -m arcexp.demo_trace coach --from A0 --tag c1 [--baseline <eval_tag>]
      ONE generation of the original coach I_0 (agent_template's meta agent incl. the DECISIONS 14-15
      adaptations; meta files frozen as in the pay-off runs) on the source practice set, starting from A_0.
      The coach sees A_0's practice results exactly as in the real loop (gen_initial/arc_eval): by default a
      fresh traced baseline eval of A_0 on the source set (phase demo_coachbase_<tag>); with --baseline <t>
      the rep1 visible dir of `eval --code A0 --tasks source --tag <t>` is reused. Then the produced player is
      practice-evaluated (traced) like any generation. Saves under exp/demo/coach_<tag>/:
      meta_agent_chat_history.md, model_patch.diff, player_code/ (the produced repo; task_agent.py at root),
      baseline_eval/, child_eval/, summary.json, run/ (the generate_loop output dir).

  python3 -m arcexp.demo_trace status        # demo spend vs the $8 demo cap, global spend

Long jobs: bash arcexp/run_bg.sh demo_<name> python3 -m arcexp.demo_trace ...   (log: exp/logs/demo_<name>.log;
note run_bg.sh registers the job in exp/logs/jobs.tsv, so `orchestrate resume` would relaunch it if unfinished).
Find a test input's model calls: traces.jsonl rows whose "token" equals the eval row's token.
"""
import argparse
import json
import os
import shutil
import sys
import time

from arcexp import arc_data, arc_eval
from arcexp.common import EXP, REPO, _admin, gw_status, read_jsonl

DEMO = os.path.join(EXP, "demo")
TEMPLATE = os.path.join(REPO, "agent_template")


def _demo_results_path(phase):
    assert phase.startswith("demo"), phase
    return os.path.join(DEMO, "results", f"{phase}.jsonl")


# never write demo rows into exp/results/
arc_eval.results_path = _demo_results_path

_TOKENS = {}
_orig_register = arc_eval.register_token


def _register(role, scope, effort_role=None):
    assert str(scope.get("phase", "")).startswith("demo"), scope
    tok = _orig_register(role, scope, effort_role=effort_role)
    _TOKENS.setdefault((str(scope.get("iteration")), scope.get("task"), scope.get("test_input")), []).append(tok)
    return tok


arc_eval.register_token = _register


def task_ids_of(spec):
    splits = json.load(open(os.path.join(REPO, "splits.json")))
    if spec in splits and isinstance(splits[spec], list):
        return list(splits[spec])
    return [t.strip() for t in spec.split(",") if t.strip()]


def code_dir_of(code):
    d = TEMPLATE if code == "A0" else os.path.abspath(code)
    if not os.path.isfile(os.path.join(d, "task_agent.py")):
        sys.exit(f"no task_agent.py in {d}")
    return d


def demo_status():
    return _admin("GET", "/demo_status", tries=2)


def cmd_eval(a):
    code = code_dir_of(a.code)
    tids = task_ids_of(a.tasks)
    phase = f"demo_eval_{a.tag}"
    out = os.path.join(DEMO, f"eval_{a.tag}.jsonl")
    os.makedirs(DEMO, exist_ok=True)
    summ, rows = [], []
    for r in range(1, a.reps + 1):
        scope = {"phase": phase, "arm": "demo", "seed": a.tag, "iteration": f"rep{r}"}
        vis = os.path.join(DEMO, f"eval_{a.tag}", f"rep{r}")
        s = arc_eval.evaluate_set(code, tids, scope, workers=a.workers, visible_dir=vis, retries=2)
        done = arc_eval.load_done(phase, s["code_hash"])
        for tid in tids:
            for ti in range(arc_data.n_test(tid)):
                rs = done.get((phase, "demo", a.tag, f"rep{r}", tid, ti)) or []
                toks = _TOKENS.get((f"rep{r}", tid, ti), [])
                for x in rs:
                    rows.append({"tag": a.tag, "rep": r, "code": a.code, "code_hash": s["code_hash"],
                                       "task": tid, "test_input": ti, "attempt": x["attempt"], "pred": x["pred"],
                                       "correct": x["correct"], "n_answers": x.get("n_answers"), "calls": x.get("calls"),
                                       "agent_error": x.get("agent_error"),
                                       "token": toks[-1] if toks else None, "all_tokens": toks})
        summ.append({"rep": r, "score": s["score"], "missing": s["missing"], "per_task": s["per_task"]})
        print(f"[demo eval {a.tag}] rep {r}: score {s['score']:.3f} on {len(tids)} tasks (missing {s['missing']})", flush=True)
    with open(out, "w") as f:  # rewritten from the (cached) demo results on every invocation
        f.writelines(json.dumps(x) + "\n" for x in rows)
    json.dump({"tag": a.tag, "code": a.code, "tasks": tids, "reps": summ, "finished": time.time()},
              open(os.path.join(DEMO, f"eval_{a.tag}.summary.json"), "w"), indent=2)
    print(demo_status())


def cmd_coach(a):
    if a.from_ != "A0":
        sys.exit("only --from A0 is supported (the original coach starting from A_0)")
    from arcexp import run_loop as RL  # chdirs to REPO, imports generate_loop
    from arcexp.evolved import BASE_FREEZE
    cdir = os.path.join(DEMO, f"coach_{a.tag}")
    run_dir = os.path.join(cdir, "run")
    if os.path.exists(run_dir):
        sys.exit(f"{run_dir} exists: pick a new --tag (a demo generation is not resumed)")
    os.makedirs(run_dir)
    tids = task_ids_of("source")
    # 1) A_0's practice results, as the coach sees them in gen_initial/arc_eval
    base_vis = os.path.join(cdir, "baseline_eval")
    if a.baseline:
        src = os.path.join(DEMO, f"eval_{a.baseline}", "rep1")
        meta = json.load(open(os.path.join(DEMO, f"eval_{a.baseline}.summary.json")))
        if meta["code"] != "A0" or sorted(meta["tasks"]) != sorted(tids):
            sys.exit("--baseline must be an `eval --code A0 --tasks source` run")
        shutil.copytree(src, base_vis)
        base_score = meta["reps"][0]["score"]
    else:
        s = arc_eval.evaluate_set(TEMPLATE, tids, {"phase": f"demo_coachbase_{a.tag}", "arm": "A0", "seed": a.tag,
                                                   "iteration": "base"}, workers=a.workers, visible_dir=base_vis, retries=2)
        if s["missing"]:
            sys.exit(f"baseline eval incomplete ({s['missing']} missing)")
        base_score = s["score"]
    print(f"[demo coach {a.tag}] A_0 practice score {base_score:.3f}", flush=True)
    # 2) one generation of the real loop (same code path as run_loop.main, minus the shared initial eval)
    cfg = {"name": f"demo_{a.tag}", "phase": f"demo_coach_{a.tag}", "arm": "I0", "seed": a.tag, "task_set": "source",
           "max_generation": 1, "template_dir": "agent_template", "freeze_paths": BASE_FREEZE, "rng_seed": 0,
           "workers": a.workers}
    cfgp = os.path.join(run_dir, "config.json")
    json.dump(cfg, open(cfgp, "w"), indent=2)
    RL.CTX.update(cfg)
    RL.CTX.update(config_path=cfgp, run_dir=run_dir, task_ids=tids)
    import random
    import numpy as np
    random.seed(0)
    np.random.seed(0)
    RL.patch_all()

    def demo_setup(output_dir, domains, **kw):
        kw["copy_eval"] = False  # never read the real outputs/initial_arc_source_0
        r = RL.arc_setup_initial_gen(output_dir, domains, **kw)
        shutil.copytree(base_vis, os.path.join(output_dir, "gen_initial", "arc_eval"), dirs_exist_ok=True)
        return r

    RL.GL.setup_initial_gen = demo_setup
    out_dir = os.path.join(run_dir, f"generate_{cfg['name']}")
    try:
        RL.GL.generate_loop(domains=["arc"], run_id=cfg["name"], max_generation=1, eval_samples=[-1],
                            eval_workers=a.workers, eval_subsets=["_source"], parent_selection="score_child_prop",
                            resume_from=None, output_dir_parent=run_dir, copy_root_dir="agent_template",
                            skip_staged_eval=True)
    except RL.InfraAbort as e:
        print("INFRA ABORT:", e)
        sys.exit(3)
    # 3) collect
    g1 = os.path.join(out_dir, "gen_1")
    for f in ("meta_agent_chat_history.md", "model_patch.diff"):
        p = os.path.join(g1, "agent_output", f)
        if os.path.exists(p):
            shutil.copyfile(p, os.path.join(cdir, f))
    if os.path.isdir(os.path.join(g1, "arc_eval")):
        shutil.copytree(os.path.join(g1, "arc_eval"), os.path.join(cdir, "child_eval"), dirs_exist_ok=True)
    snap = os.path.join(run_dir, "snapshots", "gen_1.tar.gz")
    if os.path.exists(snap):
        from arcexp.safeio import extract_snapshot
        extract_snapshot(snap, os.path.join(cdir, "player_code"))
    gs = read_jsonl(os.path.join(run_dir, "gen_scores.jsonl"))
    ms = read_jsonl(os.path.join(run_dir, "meta_steps.jsonl"))
    summary = {"tag": a.tag, "baseline_score": base_score, "child_score": gs[-1]["score"] if gs else None,
               "patch_bytes": os.path.getsize(os.path.join(cdir, "model_patch.diff")) if os.path.exists(os.path.join(cdir, "model_patch.diff")) else 0,
               "meta_token": ms[-1]["token"] if ms else None, "meta_calls": ms[-1].get("meta_calls") if ms else None,
               "meta_rc": ms[-1].get("rc") if ms else None, "finished": time.time()}
    json.dump(summary, open(os.path.join(cdir, "summary.json"), "w"), indent=2)
    print(json.dumps(summary))
    print(demo_status())


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("eval")
    e.add_argument("--code", default="A0")
    e.add_argument("--tasks", default="source")
    e.add_argument("--reps", type=int, default=1)
    e.add_argument("--tag", required=True)
    e.add_argument("--workers", type=int, default=8)
    c = sub.add_parser("coach")
    c.add_argument("--from", dest="from_", default="A0")
    c.add_argument("--tag", required=True)
    c.add_argument("--baseline", default=None)
    c.add_argument("--workers", type=int, default=8)
    sub.add_parser("status")
    a = ap.parse_args()
    if a.cmd == "status":
        print(json.dumps({"demo": demo_status(), "global": gw_status()}, indent=2))
        return
    if a.cmd != "status" and getattr(a, "tag", None) and not all(ch.isalnum() or ch in "_-" for ch in a.tag):
        sys.exit("tag: letters, digits, _ and - only")
    {"eval": cmd_eval, "coach": cmd_coach}[a.cmd](a)


if __name__ == "__main__":
    main()
