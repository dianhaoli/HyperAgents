"""Private ARC-AGI-2 data access (root only). Test outputs never leave this module except for scoring."""
import json
import os
from functools import lru_cache

from arcexp.common import ARC_DIR


@lru_cache(maxsize=None)
def load_task(split, tid):
    with open(os.path.join(ARC_DIR, split, f"{tid}.json")) as f:
        return json.load(f)


def list_ids(split):
    return sorted(f[:-5] for f in os.listdir(os.path.join(ARC_DIR, split)) if f.endswith(".json"))


def split_of(tid):
    if os.path.exists(os.path.join(ARC_DIR, "evaluation", f"{tid}.json")):
        return "evaluation"
    return "training"


def n_test(tid):
    return len(load_task(split_of(tid), tid)["test"])


def visible_task(tid):
    """Example pairs + test inputs only (no test outputs)."""
    t = load_task(split_of(tid), tid)
    return {"id": tid, "train": t["train"], "test": [{"input": x["input"]} for x in t["test"]]}


def task_input_for(tid, test_idx):
    t = load_task(split_of(tid), tid)
    return {"train": t["train"], "test_input": t["test"][test_idx]["input"]}


def truth(tid, test_idx):
    return load_task(split_of(tid), tid)["test"][test_idx]["output"]


def all_test_outputs(tids):
    out = []
    for tid in tids:
        t = load_task(split_of(tid), tid)
        for i, x in enumerate(t["test"]):
            out.append((tid, i, x["output"]))
    return out


def valid_grid(g):
    if not isinstance(g, list) or not g or len(g) > 30:
        return False
    w = None
    for row in g:
        if not isinstance(row, list) or not row or len(row) > 30:
            return False
        for v in row:
            if not isinstance(v, int) or isinstance(v, bool) or v < 0 or v > 9:
                return False
        if w is None:
            w = len(row)
        elif len(row) != w:
            return False
    return True
