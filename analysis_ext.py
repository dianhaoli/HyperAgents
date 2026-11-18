"""EXTENSION analysis (DESIGN_v2.md) - reported separately from the committed analysis.py.

  python analysis_ext.py  -> exp/results/ext_analysis.json, exp/results/extension_plot.png

Generations: 0 = original-coach (I_0) pay-off runs from part A; 12 = evolved-coach (I_g) pay-off runs from part A;
20 and 40 = extension test runs of seeds 0-3 (seed index i = source_s{i+1}).
"""
import json
import math
import os
import statistics as st

from scipy import stats as sps

ROOT = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ROOT, "exp", "results")
SEEDS = [0, 1, 2, 3]
GENS = [0, 12, 20, 40]
COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]   # validated categorical slots 1-4 (light surface)
MARKERS = ["o", "s", "^", "D"]


def rj(p):
    return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []


def tci(xs):
    n = len(xs)
    m = st.mean(xs)
    if n < 2:
        return m, float("nan"), float("nan")
    h = sps.t.ppf(0.975, n - 1) * st.stdev(xs) / math.sqrt(n)
    return m, m - h, m + h


def welch(a, b):
    d = st.mean(a) - st.mean(b)
    if len(a) < 2 or len(b) < 2:
        return d, float("nan"), float("nan")
    va, vb = st.variance(a) / len(a), st.variance(b) / len(b)
    se = math.sqrt(va + vb)
    if se == 0:
        return d, d, d
    df = (va + vb) ** 2 / (va ** 2 / (len(a) - 1) + vb ** 2 / (len(b) - 1))
    t = sps.t.ppf(0.975, df)
    return d, d - t * se, d + t * se


def main():
    finals = {}
    for r in rj(os.path.join(RES, "final_runs.jsonl")):
        finals[r["run"]] = r
    pts = []  # (gen, seed_index or None, score, run)
    for name, r in finals.items():
        if r["arm"] == "I0":
            pts.append((0, None, r["heldout"], name))
        elif r["arm"] == "Ig":
            si = int(str(r.get("source_seed", r["seed"]))) - 1
            pts.append((12, si, r["heldout"], name))
        elif str(r["arm"]).startswith("g") and name.startswith("ext_"):
            pts.append((int(r["arm"][1:]), int(r["seed"]), r["heldout"], name))
    b0 = {}
    for r in rj(os.path.join(RES, "b0_summary.jsonl")):
        b0[r["rep"]] = r["score"]
    B0 = st.mean(b0.values()) if b0 else None
    xh = None
    for line in open(os.path.join(ROOT, "exp", "logs", "xhigh.log")) if os.path.exists(os.path.join(ROOT, "exp", "logs", "xhigh.log")) else []:
        if line.startswith("xhigh pass:"):
            xh = float(line.split(":")[1].split()[0])
    per_gen = {}
    for g in GENS:
        xs = [p[2] for p in pts if p[0] == g]
        if xs:
            m, lo, hi = tci(xs)
            per_gen[g] = {"n": len(xs), "mean": m, "lo": lo, "hi": hi, "scores": xs}
    out = {"label": "EXTENSION (DESIGN_v2.md) - not part of the pre-registered analysis",
           "points": [{"generation": p[0], "seed_index": p[1], "heldout": p[2], "run": p[3]} for p in pts],
           "per_generation": per_gen, "B0": B0, "xhigh": xh}
    g0 = [p[2] for p in pts if p[0] == 0]
    g40 = [p[2] for p in pts if p[0] == 40]
    if g0 and g40:
        d, lo, hi = welch(g40, g0)
        verdict = "rising" if lo > 0 else "falling" if hi < 0 else "flat within the interval"
        out["gen40_minus_gen0"] = {"est": d, "lo": lo, "hi": hi, "verdict": verdict}
    by = {(p[0], p[1]): p[2] for p in pts if p[1] is not None}
    paired = {}
    for a, b in [(12, 20), (20, 40)]:
        ch = {s: by[(b, s)] - by[(a, s)] for s in SEEDS if (a, s) in by and (b, s) in by}
        paired[f"{a}->{b}"] = {"per_seed": ch, "mean": st.mean(ch.values()) if ch else None}
    out["paired_changes"] = paired
    picks = json.load(open(os.path.join(RES, "ext_picks.json"))) if os.path.exists(os.path.join(RES, "ext_picks.json")) else {}
    sel = json.load(open(os.path.join(RES, "ig_selection.json"))) if os.path.exists(os.path.join(RES, "ig_selection.json")) else {}
    out["picks_changed_code"] = {
        "gen12 (part A rule)": f"{sum(1 for k, v in sel.items() if v.get('qualifying'))} of {len(sel)} seeds",
        "extension picks": {k: (v["pick"]["gen"] if v.get("pick") else None) for k, v in picks.items()},
        "extension picks with changed coach code": f"{sum(1 for v in picks.values() if v.get('pick'))} of {len(picks)}"}
    audit_p = os.path.join(RES, "diff_audit.json")
    if os.path.exists(audit_p):
        a = json.load(open(audit_p))
        tags = [h["tag"] for c in a.values() for h in c.get("hunks", [])]
        out["diff_audit_summary"] = {"hunks": len(tags), "arc_specific": tags.count("ARC-specific"), "general": tags.count("general")}
    json.dump(out, open(os.path.join(RES, "ext_analysis.json"), "w"), indent=1)

    # ---- plot
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ink, ink2, grid = "#0b0b0b", "#52514e", "#e6e5e1"
    fig, ax = plt.subplots(figsize=(7.5, 4.6), dpi=200)
    fig.patch.set_facecolor("#fcfcfb"); ax.set_facecolor("#fcfcfb")
    for s in SEEDS:
        xs = [g for g in GENS if (g, s) in by]
        if xs:
            ys = [100 * by[(g, s)] for g in xs]
            ax.plot(xs, ys, color=COLORS[s], lw=2, marker=MARKERS[s], ms=8, mec="#fcfcfb", mew=2, zorder=3)
            ax.annotate(f"seed {s}", (xs[-1], ys[-1]), xytext=(8, 0), textcoords="offset points", va="center",
                        color=ink2, fontsize=9)
    others = [p for p in pts if p[1] is None or p[1] not in SEEDS]
    if others:
        # small deterministic horizontal jitter so runs with identical scores stay visible
        seen = {}
        xs_j = []
        for p in others:
            k = (p[0], round(p[2], 4))
            seen[k] = seen.get(k, 0) + 1
            xs_j.append(p[0] - 0.6 * (seen[k] - 1))
        ax.scatter(xs_j, [100 * p[2] for p in others], s=40, color="#8a8984", zorder=2,
                   edgecolor="#fcfcfb", linewidth=1.5, label="other runs (gen 0: original coach; gen 12: seeds 4-5)")
    for g, v in per_gen.items():
        if v["n"] >= 2:
            ax.errorbar(g - 1.6, 100 * v["mean"], yerr=[[100 * (v["mean"] - v["lo"])], [100 * (v["hi"] - v["mean"])]],
                        fmt="_", color=ink, ms=12, capsize=3, lw=1.2, zorder=4)
    if B0 is not None:
        ax.axhline(100 * B0, color=ink2, lw=1, ls="--", zorder=1)
        ax.annotate(f"B0 {100 * B0:.1f}%", (2.0, 100 * B0 - 0.25), va="top", ha="left", color=ink2, fontsize=9)
    if xh is not None:
        ax.axhline(100 * xh, color=ink2, lw=1, ls=":", zorder=1)
        ax.annotate(f"A_0 at xhigh {100 * xh:.1f}%", (-1.8, 100 * xh + 0.25), va="bottom", ha="left", color=ink2, fontsize=9)
    ax.set_xticks(GENS)
    ax.set_xlim(-2, 48)
    ax.set_xlabel("Coach generation", color=ink2)
    ax.set_ylabel("Held-out exam score (%)", color=ink2)
    ax.set_title("Extension: exam score of the player built by the coach at each generation", color=ink, fontsize=11, loc="left")
    ax.grid(axis="y", color=grid, lw=0.8); ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(grid)
    ax.tick_params(colors=ink2)
    if others:
        ax.legend(frameon=False, fontsize=8, loc="lower left")
    fig.text(0.01, 0.01, "Black bars: mean and 95% t-interval per generation. Dashed: B0 (A_0, 2 plain attempts). Dotted: one A_0 pass at xhigh.",
             fontsize=7, color=ink2)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(RES, "extension_plot.png"))
    print(json.dumps({k: v for k, v in out.items() if k != "points"}, indent=1, default=str)[:3000])


if __name__ == "__main__":
    main()
