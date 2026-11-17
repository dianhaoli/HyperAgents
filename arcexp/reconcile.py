"""One-off: re-check result rows written before the hardened infra classification existed.

A row with fewer answers than expected is trusted as a genuine agent failure only if the ledger shows the
token(s) for that key made all expected successful model calls, or the test input hit the wall-clock limit.
Otherwise the missing answer may come from an infrastructure failure the old code could not see (e.g. the
gateway's listen backlog overflowing). Such rows are moved to exp/results/<phase>.invalidated.jsonl and
re-run with fresh keys. Rows with all answers present are always kept.

  python -m arcexp.reconcile b0 xhigh screen
"""
import json
import os
import sys

from arcexp.common import EXP, read_jsonl


def main(phases):
    ledger = read_jsonl(os.path.join(EXP, "ledger", "calls.jsonl"))
    ok_calls = {}
    for r in ledger:
        sc = r.get("scope", {})
        if r.get("role") != "task" or r.get("error"):
            continue
        k = (sc.get("phase"), str(sc.get("iteration")), sc.get("task"), int(sc.get("test_input", -1)))
        ok_calls.setdefault(k, {}).setdefault(r["token"], 0)
        ok_calls[k][r["token"]] += 1
    for ph in phases:
        p = os.path.join(EXP, "results", f"{ph}.jsonl")
        rows = read_jsonl(p)
        expected = 1 if ph == "screen" else 2
        keep, bad = [], []
        bad_keys = set()
        for r in rows:
            if r.get("infra_error"):
                keep.append(r)
                continue
            k = (ph, str(r["iteration"]), r["task"], int(r["test_input"]))
            if r.get("n_answers", 0) >= expected or r.get("timeout"):
                continue
            toks = ok_calls.get(k, {})
            if not toks or min(toks.values()) < expected:
                bad_keys.add(k + (r.get("ts"),))
        for r in rows:
            k = (ph, str(r["iteration"]), r["task"], int(r["test_input"]), r.get("ts"))
            (bad if k in bad_keys else keep).append(r)
        if bad:
            with open(p + ".tmp", "w") as f:
                for r in keep:
                    f.write(json.dumps(r) + "\n")
            os.replace(p + ".tmp", p)
            with open(os.path.join(EXP, "results", f"{ph}.invalidated.jsonl"), "a") as f:
                for r in bad:
                    f.write(json.dumps({**r, "invalidated_reason": "missing answers without evidence of completed calls (pre-hardening infra classification)"}) + "\n")
        print(ph, "rows", len(rows), "invalidated", len(bad), "test inputs", len(bad) // 2)


def invalidate_timeouts(phases):
    """Move test inputs that hit the old 30-min limit to <phase>.invalidated.jsonl so they re-run under the new limit."""
    for ph in phases:
        p = os.path.join(EXP, "results", f"{ph}.jsonl")
        rows = read_jsonl(p)
        bad_ts = {(r["iteration"], r["task"], r["test_input"], r.get("ts")) for r in rows if r.get("timeout")}
        keep = [r for r in rows if (r["iteration"], r["task"], r["test_input"], r.get("ts")) not in bad_ts]
        bad = [r for r in rows if (r["iteration"], r["task"], r["test_input"], r.get("ts")) in bad_ts]
        with open(p + ".tmp", "w") as f:
            for r in keep:
                f.write(json.dumps(r) + "\n")
        os.replace(p + ".tmp", p)
        with open(os.path.join(EXP, "results", f"{ph}.invalidated.jsonl"), "a") as f:
            for r in bad:
                f.write(json.dumps({**r, "invalidated_reason": "hit the old 30-min per-test-input limit; re-run under the ~2 h limit"}) + "\n")
        print(ph, "timeout test inputs invalidated:", len(bad) // 2)


if __name__ == "__main__":
    if sys.argv[1] == "--timeouts":
        invalidate_timeouts(sys.argv[2:])
    else:
        main(sys.argv[1:])
