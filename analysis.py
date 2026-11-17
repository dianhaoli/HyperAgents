"""Pre-registered analysis. Usage: python analysis.py  -> prints a report, writes exp/results/analysis.json

Arms (per-run held-out scores; unit = run for I_0, seed for evolved):
  B0    : A_0 on the 120 held-out tasks with the standard budget (one value per B0 repetition)
  I0    : final agents of pay-off runs whose improver is the original meta agent I_0
  Ig    : final agents of pay-off runs whose improver is an evolved meta agent I_g (one per qualifying seed)
G     = mean(I0) - mean(B0)          95% Welch t-interval (I0 runs vs B0 repetitions)
Delta = mean(Ig) - mean(I0)          95% Welch t-interval (Ig seeds vs I0 runs)
"""
import json
import math
import os
import statistics as st

from scipy import stats as sps

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, "exp", "results")


def rj(p):
    out = []
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out


def welch(a, b, conf=0.95):
    """CI for mean(a) - mean(b). Returns (diff, lo, hi, df). Needs len>=2 in each group."""
    na, nb = len(a), len(b)
    d = st.mean(a) - st.mean(b)
    if na < 2 or nb < 2:
        return d, float("nan"), float("nan"), float("nan")
    va, vb = st.variance(a) / na, st.variance(b) / nb
    se = math.sqrt(va + vb)
    if se == 0:
        return d, d, d, float("inf")
    df = (va + vb) ** 2 / ((va ** 2) / (na - 1) + (vb ** 2) / (nb - 1))
    t = sps.t.ppf(0.5 + conf / 2, df)
    return d, d - t * se, d + t * se, df


def fmt(x):
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{100 * x:+.1f}" if abs(x) < 1.5 else f"{x:.2f}"


def pct(x):
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{100 * x:.1f}%"


def main():
    b0_rows = rj(os.path.join(RES, "b0_summary.jsonl"))
    b0_by_rep = {}
    for r in b0_rows:
        b0_by_rep[r["rep"]] = r["score"]  # last write wins (resumed reps re-append the same value)
    B0 = [b0_by_rep[k] for k in sorted(b0_by_rep)]
    finals = {}
    for r in rj(os.path.join(RES, "final_runs.jsonl")):
        finals[r["run"]] = r  # last record per run
    i0 = [r for r in finals.values() if r["arm"] == "I0"]
    ig = [r for r in finals.values() if r["arm"] == "Ig"]
    I0 = [r["heldout"] for r in i0]
    IG = [r["heldout"] for r in ig]
    sel = json.load(open(os.path.join(RES, "ig_selection.json"))) if os.path.exists(os.path.join(RES, "ig_selection.json")) else {}
    n_seeds = len(sel)
    n_qual = sum(1 for s in sel.values() if s.get("qualifying"))
    out = {"B0_reps": B0, "B0": st.mean(B0) if B0 else None, "I0_runs": {r["run"]: r["heldout"] for r in i0},
           "Ig_runs": {r["run"]: r["heldout"] for r in ig}, "n_source_seeds": n_seeds, "n_qualifying_Ig": n_qual}
    if I0 and B0:
        out["G"] = dict(zip(["est", "lo", "hi", "df"], welch(I0, B0)))
    if IG and I0:
        out["Delta"] = dict(zip(["est", "lo", "hi", "df"], welch(IG, I0)))
    if IG and B0:
        out["Ig_gain_over_B0"] = dict(zip(["est", "lo", "hi", "df"], welch(IG, B0)))
    if I0 and B0:
        out["I0_gain_over_B0"] = out["G"]
    out["sd"] = {"B0": st.stdev(B0) if len(B0) > 1 else None, "I0": st.stdev(I0) if len(I0) > 1 else None,
                 "Ig": st.stdev(IG) if len(IG) > 1 else None}

    # headline: first row that applies
    def above0(k):
        return k in out and not math.isnan(out[k]["lo"]) and out[k]["lo"] > 0

    def below0(k):
        return k in out and not math.isnan(out[k]["hi"]) and out[k]["hi"] < 0
    if not I0 or not B0:
        head = "Incomplete: not enough runs to evaluate the headline"
    elif n_seeds and n_qual < n_seeds / 2:
        head = f"Hyperagents rarely put a rewritten improver to use: {n_qual} of {n_seeds} runs"
    elif not above0("I0_gain_over_B0") and not above0("Ig_gain_over_B0"):
        head = "Neither improver beat two plain attempts on ARC-AGI-2"
    elif above0("Delta"):
        head = "An evolved improver improves better"
    elif below0("Delta"):
        head = "Evolving made the improver worse"
    elif "Delta" in out and "G" in out:
        head = (f"The original improver gained {fmt(out['G']['est'])} points; evolving it changed that by between "
                f"{fmt(out['Delta']['lo'])} and {fmt(out['Delta']['hi'])} points")
    else:
        head = "Incomplete: not enough runs to evaluate the headline"
    out["headline"] = head

    # secondary: self-edit rate
    ss = json.load(open(os.path.join(RES, "source_stats.json"))) if os.path.exists(os.path.join(RES, "source_stats.json")) else {}
    out["self_edit"] = {k: {"gens": v["n_gens"], "self_edit_gens": v["n_self_edit"], "self_edit_parents": v["n_self_edit_parents"]} for k, v in ss.items()}
    tot_g = sum(v["n_gens"] for v in ss.values())
    out["self_edit_rate"] = (sum(v["n_self_edit"] for v in ss.values()) / tot_g) if tot_g else None

    # tokens and spend by role / arm
    ledger = rj(os.path.join(ROOT, "exp", "ledger", "calls.jsonl"))
    spend = {}
    for r in ledger:
        spend[r.get("role", "?")] = spend.get(r.get("role", "?"), 0.0) + r.get("cost", 0.0)
    out["spend_by_role"] = spend
    out["spend_total"] = sum(spend.values())
    by_arm = {}
    for r in ledger:
        sc = r.get("scope", {})
        if sc.get("phase") != "payoff":
            continue
        k = sc.get("arm")
        a = by_arm.setdefault(k, {"task_tokens": 0, "meta_tokens": 0, "task_keys": set(), "meta_iters": set()})
        if r.get("role") == "task":
            a["task_tokens"] += r.get("total_tokens", 0)
            a["task_keys"].add((sc.get("seed"), sc.get("iteration"), sc.get("task")))
        elif r.get("role") == "meta":
            a["meta_tokens"] += r.get("total_tokens", 0)
            a["meta_iters"].add((sc.get("run"), sc.get("iteration")))
    out["tokens_by_arm"] = {k: {"task_tokens_per_task_eval": v["task_tokens"] / max(1, len(v["task_keys"])),
                                "meta_tokens_per_iteration": v["meta_tokens"] / max(1, len(v["meta_iters"])),
                                "n_task_evals": len(v["task_keys"]), "n_meta_iterations": len(v["meta_iters"])}
                            for k, v in by_arm.items()}
    out["final_runs"] = list(finals.values())
    os.makedirs(RES, exist_ok=True)
    json.dump(out, open(os.path.join(RES, "analysis.json"), "w"), indent=1, default=str)

    print("HEADLINE:", head)
    print(f"B0 = {pct(out['B0'])} (reps: {', '.join(pct(x) for x in B0)})")
    for k in ["G", "Delta", "I0_gain_over_B0", "Ig_gain_over_B0"]:
        if k in out:
            v = out[k]
            print(f"{k:16s} {fmt(v['est'])} pts  95% CI [{fmt(v['lo'])}, {fmt(v['hi'])}]  df={v['df']:.1f}" if not math.isnan(v['df']) else f"{k:16s} {fmt(v['est'])} pts  (CI n/a: <2 units)")
    print("\n| run | arm | seed | final node | held-out |")
    print("|---|---|---|---|---|")
    for r in sorted(finals.values(), key=lambda r: (r["arm"], str(r["seed"]))):
        print(f"| {r['run']} | {r['arm']} | {r['seed']} | {r['final_node']} | {pct(r['heldout'])} |")
    print("\nrun-to-run SD:", {k: pct(v) for k, v in out["sd"].items()})
    print("self-edit:", out["self_edit"], "rate", out["self_edit_rate"])
    print("tokens by arm:", out["tokens_by_arm"])
    print("spend by role:", {k: round(v, 3) for k, v in spend.items()}, "total", round(out["spend_total"], 3))


if __name__ == "__main__":
    main()
