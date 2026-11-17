"""Create run configs and launch loop runs as resumable background jobs.

  python -m arcexp.orchestrate pilot            # payoff_I0_1, payoff_I0_2
  python -m arcexp.orchestrate source           # source_s1..s6 (12 generations on the source set)
  python -m arcexp.orchestrate trial            # one trial iteration per I_g from A_0 (transplant check)
  python -m arcexp.orchestrate payoff           # payoff_Ig_<seed> for qualifying seeds + payoff_I0_3..6
  python -m arcexp.orchestrate status
"""
import json
import os
import subprocess
import sys

from arcexp.common import EXP, REPO
from arcexp.evolved import BASE_FREEZE

RUNS = os.path.join(EXP, "runs")
K = 8
G = 12
N_SEEDS = 6
N_I0 = 6


def make(name, **cfg):
    d = os.path.join(RUNS, name)
    p = os.path.join(d, "config.json")
    os.makedirs(d, exist_ok=True)
    if os.path.exists(p):
        old = json.load(open(p))
        for k in ("root_commit", "done"):
            if k in old:
                cfg[k] = old[k]
    cfg["name"] = name
    json.dump(cfg, open(p, "w"), indent=2)
    return p


def launch(name):
    p = os.path.join(RUNS, name, "config.json")
    if json.load(open(p)).get("done"):
        print(name, "done")
        return
    subprocess.run(["bash", os.path.join(REPO, "arcexp", "run_bg.sh"), f"run_{name}",
                    f"python3 -m arcexp.run_loop --config {p} > {os.path.join(RUNS, name, 'run.log')} 2>&1"])


def payoff_i0(i):
    name = f"payoff_I0_{i}"
    make(name, phase="payoff", arm="I0", seed=f"r{i}", task_set="payoff", max_generation=K,
         template_dir="agent_template", freeze_paths=BASE_FREEZE, rng_seed=(1200 + i if i == 2 else 1100 + i), workers=16)  # reruns after harness bugs, see DECISIONS 23-24
    return name


def cmd_pilot():
    for i in (1, 2):
        launch(payoff_i0(i))


def cmd_source():
    for s in range(1, N_SEEDS + 1):
        name = f"source_s{s}"
        make(name, phase="source", arm="I0src", seed=s, task_set="source", max_generation=G,
             template_dir="agent_template", freeze_paths=[], rng_seed=s, workers=12)
        launch(name)


def _ig_runs():
    sel = json.load(open(os.path.join(EXP, "results", "ig_selection.json")))
    out = []
    for src, s in sel.items():
        if not s["qualifying"]:
            continue
        man = json.load(open(os.path.join(EXP, "transplants", src, "manifest.json")))
        out.append((src, s, man))
    return out


def cmd_trial():
    for src, s, man in _ig_runs():
        name = f"trial_Ig_{src}"
        make(name, phase="trial", arm="Ig", seed=s["source_seed"], source_seed=s["source_seed"], task_set="payoff",
             max_generation=1, template_dir=os.path.relpath(os.path.join(EXP, "transplants", src, "template"), REPO),
             freeze_paths=man["freeze_paths"], rng_seed=500 + int(s["source_seed"]), workers=16)
        launch(name)


def cmd_payoff():
    for src, s, man in _ig_runs():
        name = f"payoff_Ig_{src}"
        make(name, phase="payoff", arm="Ig", seed=s["source_seed"], source_seed=s["source_seed"], task_set="payoff",
             max_generation=K, template_dir=os.path.relpath(os.path.join(EXP, "transplants", src, "template"), REPO),
             freeze_paths=man["freeze_paths"], rng_seed=2000 + int(s["source_seed"]), workers=16)
        launch(name)
    for i in range(3, N_I0 + 1):
        launch(payoff_i0(i))


def cmd_ext(run, gen):
    """DESIGN_v2 extension test run: transplanted coach of `run` at generation `gen`, frozen pay-off rules."""
    seed_index = int(run.replace("source_s", "")) - 1
    tdir = os.path.join(EXP, "transplants_ext", f"{run}_g{gen}")
    man = json.load(open(os.path.join(tdir, "manifest.json")))
    name = f"ext_{run}_g{gen}"
    make(name, phase="ext_payoff", arm=f"g{gen}", seed=seed_index, source_run=run, coach_generation=gen,
         coach_node=man["gen"], task_set="payoff", max_generation=K,
         template_dir=os.path.relpath(os.path.join(tdir, "template"), REPO), freeze_paths=man["freeze_paths"],
         rng_seed=3000 + 100 * gen + seed_index, workers=12)
    launch(name)


def cmd_resume():
    """Relaunch every unfinished loop run and every registered phase job that has not logged __JOB_DONE__."""
    for name in sorted(os.listdir(RUNS)):
        p = os.path.join(RUNS, name, "config.json")
        if os.path.exists(p) and not json.load(open(p)).get("done") and name != "smoke":
            launch(name)
    reg = os.path.join(EXP, "logs", "jobs.tsv")
    seen = {}
    if os.path.exists(reg):
        for line in open(reg):
            parts = line.rstrip("\n").split("\t")
            if len(parts) == 3:
                seen[parts[0]] = parts
    for name, w, cmd in seen.values():
        log = os.path.join(EXP, "logs", f"{name}.log")
        tail = open(log, errors="replace").read()[-3000:] if os.path.exists(log) else ""
        if "__JOB_DONE__" in tail.splitlines()[-1:] or tail.rstrip().endswith("__JOB_DONE__"):
            continue
        env = dict(os.environ, ARC_WORKERS=w or "16")
        subprocess.run(["bash", os.path.join(REPO, "arcexp", "run_bg.sh"), name] + cmd.split(), env=env)


def cmd_status():
    for name in sorted(os.listdir(RUNS)):
        p = os.path.join(RUNS, name, "config.json")
        if not os.path.exists(p):
            continue
        c = json.load(open(p))
        arch = os.path.join(RUNS, name, f"generate_{name}", "archive.jsonl")
        n = len(open(arch).read().splitlines()) if os.path.exists(arch) else 0
        gs = os.path.join(RUNS, name, "gen_scores.jsonl")
        sc = [json.loads(l)["score"] for l in open(gs)] if os.path.exists(gs) else []
        print(f"{name:22s} done={c.get('done', False)!s:5s} archive={n:2d} gen_scores={[round(x, 2) for x in sc]}")


if __name__ == "__main__":
    if sys.argv[1] == "ext":
        cmd_ext(sys.argv[2], int(sys.argv[3]))
    else:
        {"pilot": cmd_pilot, "source": cmd_source, "trial": cmd_trial, "payoff": cmd_payoff, "status": cmd_status,
         "resume": cmd_resume}[sys.argv[1]]()
