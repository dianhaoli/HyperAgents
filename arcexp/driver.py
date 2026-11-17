"""Unattended driver: advances parts A and B as their prerequisites appear. Idempotent; safe to restart.

  python3 -m arcexp.driver          (launched via run_bg.sh as job "driver"; one tick every 5 min)

Each tick:
  * every finished pay-off / extension test run without a final exam -> launch `phases final` for it
  * every extension seed (source_s1..s4) that reached generation 6/20/30/40 -> pick (DESIGN_v2 rule), transplant,
    import-check; for generations 20 and 40 also launch the frozen test run
  * commit + push after any action
"""
import json
import os
import subprocess
import time

from arcexp.common import EXP, REPO, read_jsonl
from arcexp.evolved import archive_at

EXT_RUNS = ["source_s1", "source_s2", "source_s3", "source_s4"]
STORE_GENS = [6, 30]
TEST_GENS = [20, 40]


def sh(*cmd, env=None):
    return subprocess.run(list(cmd), cwd=REPO, capture_output=True, text=True, env=env)


def log(msg):
    with open(os.path.join(EXP, "logs", "driver_actions.log"), "a") as f:
        f.write(time.strftime("%H:%M:%S ") + msg + "\n")
    print(msg, flush=True)


def job_alive(name):
    p = os.path.join(EXP, "logs", f"{name}.pid")
    if not os.path.exists(p):
        return False
    try:
        os.kill(int(open(p).read().strip()), 0)
        return True
    except Exception:
        return False


def job_done(name):
    p = os.path.join(EXP, "logs", f"{name}.log")
    return os.path.exists(p) and "__JOB_DONE__" in open(p, errors="replace").read()[-500:]


def tick():
    acted = False
    finals = {r["run"] for r in read_jsonl(os.path.join(EXP, "results", "final_runs.jsonl"))}
    runs = os.path.join(EXP, "runs")
    for name in sorted(os.listdir(runs)):
        p = os.path.join(runs, name, "config.json")
        if not os.path.exists(p):
            continue
        c = json.load(open(p))
        if c.get("phase") not in ("payoff", "ext_payoff") or not c.get("done") or name in finals:
            continue
        j = f"final_{name}"
        if job_alive(j) or job_done(j):
            continue
        env = dict(os.environ, ARC_WORKERS="16")
        sh("bash", "arcexp/run_bg.sh", j, "python3", "-m", "arcexp.phases", "final", "--run", name, env=env)
        log(f"launched final exam for {name}")
        acted = True
    # resume runs that stopped on an infrastructure abort (resumable), at most 15 times each
    for name in sorted(os.listdir(runs)):
        p = os.path.join(runs, name, "config.json")
        if not os.path.exists(p) or name == "smoke":
            continue
        c = json.load(open(p))
        if c.get("done") or job_alive(f"run_{name}"):
            continue
        n_abort = len(read_jsonl(os.path.join(runs, name, "infra_aborts.jsonl")))
        if n_abort >= 15:
            continue
        sh("python3", "-c", f"from arcexp.orchestrate import launch; launch({name!r})")
        log(f"resumed {name} (infra aborts so far: {n_abort})")
        acted = True
    picks_p = os.path.join(EXP, "results", "ext_picks.json")
    for run in EXT_RUNS:
        out_dir = os.path.join(runs, run, f"generate_{run}")
        reached = len(archive_at(out_dir, None)) - 1  # generations completed (archive minus initial)
        for g in STORE_GENS + TEST_GENS:
            if reached < g:
                continue
            picks = json.load(open(picks_p)) if os.path.exists(picks_p) else {}
            key = f"{run}:g{g}"
            if key not in picks:
                r = sh("python3", "-m", "arcexp.evolved", "ext_pick", run, str(g))
                log(f"pick {key}: {r.stdout.strip()[-300:]} {r.stderr.strip()[-300:]}")
                acted = True
                picks = json.load(open(picks_p)) if os.path.exists(picks_p) else {}
            if g in TEST_GENS and picks.get(key, {}).get("pick") and picks[key].get("transplant_check", {}).get("ok"):
                tname = f"ext_{run}_g{g}"
                if not os.path.exists(os.path.join(runs, tname, "config.json")):
                    r = sh("python3", "-m", "arcexp.orchestrate", "ext", run, str(g))
                    log(f"launched extension test {tname}: {r.stdout.strip()[-200:]}")
                    acted = True
    if acted:
        sh("bash", "arcexp/checkpoint.sh", "driver: progress")
    return acted


def main():
    while True:
        try:
            tick()
        except Exception as e:
            log(f"driver error: {type(e).__name__}: {e}")
        time.sleep(300)


if __name__ == "__main__":
    main()
