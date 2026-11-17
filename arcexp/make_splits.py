"""Seeded data splits. Stage 1 (before the screen): held-out, screen, smoke.
Stage 2 (after the screen): source and pay-off sets.  Usage:
  python -m arcexp.make_splits stage1
  python -m arcexp.make_splits stage2 --set_size 25|20
"""
import argparse, json, os, random
from arcexp import arc_data
from arcexp.common import REPO, read_jsonl, EXP

SEED = 20261117
P = os.path.join(REPO, "splits.json")


def stage1():
    tr = arc_data.list_ids("training")
    rng = random.Random(SEED)
    rng.shuffle(tr)
    s = {"seed": SEED, "arc_agi_2_commit": "f3283f727488ad98fe575ea6a5ac981e4a188e49",
         "heldout": arc_data.list_ids("evaluation"), "screen": sorted(tr[:100]), "smoke": sorted(tr[100:110])}
    json.dump(s, open(P, "w"), indent=1)
    print({k: len(v) if isinstance(v, list) else v for k, v in s.items()})


def stage2(n):
    s = json.load(open(P))
    rows = [r for r in read_jsonl(os.path.join(EXP, "results", "screen.jsonl")) if not r.get("infra_error") and r["attempt"] == 1]
    # per (task, call): task solved in that call iff all its test inputs solved by that single call
    by = {}
    for r in rows:
        by.setdefault(r["task"], {}).setdefault(int(r["iteration"]), {})[r["test_input"]] = r["correct"]
    solved_count = {}
    for t in s["screen"]:
        calls = by.get(t, {})
        solved_count[t] = sum(1 for c in calls.values() if len(c) == arc_data.n_test(t) and all(c.values()))
    mid = sorted(t for t, c in solved_count.items() if c in (1, 2))
    always = sorted(t for t, c in solved_count.items() if c == 3)
    never = sorted(t for t, c in solved_count.items() if c == 0)
    rng = random.Random(SEED + 1)
    rng.shuffle(mid); rng.shuffle(always); rng.shuffle(never)
    need = 2 * n
    use_mid = mid[: need - (need - len(mid)) % 2] if len(mid) < need else mid[:need]
    fill = need - len(use_mid)
    if fill % 2:  # keep the fill an even split between always- and never-solved
        use_mid = use_mid[:-1]; fill += 1
    k = fill // 2
    if k > len(always) or k > len(never):
        raise SystemExit(f"not enough always/never tasks: need {k} each, have {len(always)}/{len(never)}")
    src, pay = [], []
    for i, t in enumerate(use_mid):
        (src if i % 2 == 0 else pay).append(t)
    for i, t in enumerate(always[:k]):
        (src if i % 2 == 0 else pay).append(t)
    for i, t in enumerate(never[:k]):
        (pay if i % 2 == 0 else src).append(t)
    s.update(screen_solved_count=solved_count, source=sorted(src), payoff=sorted(pay),
             composition={"intermediate_used": len(use_mid), "always_fill": k, "never_fill": k,
                          "n_intermediate_available": len(mid), "n_always": len(always), "n_never": len(never)})
    assert not set(src) & set(pay) and len(src) == n and len(pay) == n, (len(src), len(pay))
    json.dump(s, open(P, "w"), indent=1)
    print(s["composition"], len(src), len(pay))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("stage"); ap.add_argument("--set_size", type=int, default=25)
    a = ap.parse_args()
    stage1() if a.stage == "stage1" else stage2(a.set_size)
