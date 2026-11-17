"""Score any player (agent repo with task_agent.py) once on the 120 held-out tasks.

  python3 -m arcexp.score_player <agent_dir> <label>
"""
import json
import os
import shutil
import sys

from arcexp.arc_eval import evaluate_set
from arcexp.common import EXP, REPO, chown_agent


def main():
    src, label = os.path.abspath(sys.argv[1]), sys.argv[2]
    work = os.path.join(EXP, "stage", f"_player_{label}")
    if os.path.exists(work):
        shutil.rmtree(work)
    shutil.copytree(src, work, ignore=shutil.ignore_patterns(".git", "__pycache__"), symlinks=False)
    chown_agent(work)
    ids = json.load(open(os.path.join(REPO, "splits.json")))["heldout"]
    s = evaluate_set(work, ids, {"phase": f"exam_{label}", "arm": "player", "seed": "-", "iteration": label},
                     workers=int(os.environ.get("ARC_WORKERS", "24")))
    shutil.rmtree(work, ignore_errors=True)
    print(f"exam score {s['score']:.4f} on {len(ids)} tasks ({s['n_test_inputs']} test inputs), missing={s['missing']}")


if __name__ == "__main__":
    main()
