"""Compose RESULTS.md from analysis.py output and the experiment logs.  Usage: python -m arcexp.make_results"""
import glob
import json
import os
import subprocess

from arcexp.common import EXP, REPO, read_jsonl


def pct(x):
    return "n/a" if x is None else f"{100 * x:.1f}%"


def pts(x):
    return "n/a" if x is None or x != x else f"{100 * x:+.1f}"


def main():
    out = subprocess.run(["python3", os.path.join(REPO, "analysis.py")], capture_output=True, text=True, cwd=REPO).stdout
    a = json.load(open(os.path.join(EXP, "results", "analysis.json")))
    L = ["# RESULTS", ""]
    L += [f"## Headline", "", f"**{a['headline']}**", ""]

    def ci(k):
        v = a.get(k)
        if not v:
            return "n/a"
        if v.get("lo") != v.get("lo"):
            return f"{pts(v['est'])} points (interval n/a: fewer than 2 units)"
        return f"{pts(v['est'])} points, 95% Welch CI [{pts(v['lo'])}, {pts(v['hi'])}] (df {v['df']:.1f})"
    L += ["## Main estimates (held-out ARC-AGI-2 public evaluation, 120 tasks, 167 test inputs)", "",
          f"- B0 (A_0, two plain attempts): {pct(a.get('B0'))} (reps: {', '.join(pct(x) for x in a.get('B0_reps', []))})",
          f"- **G** (I_0-built agents minus B0): {ci('G')}",
          f"- **Delta** (evolved-improver agents minus I_0-built agents): {ci('Delta')}",
          f"- Evolved arm gain over B0: {ci('Ig_gain_over_B0')}",
          f"- Qualifying evolved improvers: {a.get('n_qualifying_Ig')} of {a.get('n_source_seeds')} source seeds", ""]
    L += ["## Per-run held-out scores", "", "| run | arm | seed | final node | held-out | accepted candidates in run |", "|---|---|---|---|---|---|"]
    for r in sorted(a.get("final_runs", []), key=lambda r: (r["arm"], str(r["seed"]))):
        L.append(f"| {r['run']} | {r['arm']} | {r['seed']} | {r['final_node']} | {pct(r['heldout'])} | {r.get('n_accepted')} |")
    L += ["", f"Run-to-run SD: B0 {pct(a['sd'].get('B0'))}, I_0 arm {pct(a['sd'].get('I0'))}, evolved arm {pct(a['sd'].get('Ig'))}.", ""]
    # secondary
    L += ["## Secondary results", ""]
    xs = [l for l in open(os.path.join(EXP, "logs", "xhigh.log"))] if os.path.exists(os.path.join(EXP, "logs", "xhigh.log")) else []
    xl = [l.strip() for l in xs if l.startswith("xhigh pass")]
    if xl:
        L.append(f"- One held-out pass of A_0 at xhigh effort: {xl[-1].split(':')[1].split()[0]} (same 30-min per-test-input wall-clock limit; many xhigh inputs hit it).")
    if a.get("self_edit"):
        tot = sum(v["gens"] for v in a["self_edit"].values())
        se = sum(v["self_edit_gens"] for v in a["self_edit"].values())
        sp = sum(v["self_edit_parents"] for v in a["self_edit"].values())
        L.append(f"- Self-edit rate in source runs: {se} of {tot} generations changed meta-agent code; {sp} of those became parents.")
        for k, v in sorted(a["self_edit"].items()):
            L.append(f"  - {k}: {v['self_edit_gens']}/{v['gens']} self-edits, {v['self_edit_parents']} became parents")
    sel_p = os.path.join(EXP, "results", "ig_selection.json")
    if os.path.exists(sel_p):
        sel = json.load(open(sel_p))
        L.append("- Selected evolved improvers (I_g):")
        for k, s in sorted(sel.items()):
            if s["qualifying"]:
                g = s["I_g"]
                L.append(f"  - {k}: gen {g['gen']}, {g['n_children']} children ({g['n_scored_children']} scored), mean child improvement "
                         f"{pts(g['mean_child_improvement'])} pts, meta files changed vs I_0: {', '.join(g['meta_files_changed_vs_I0'])}; "
                         f"meta edits in ancestry at generations {g['meta_edit_generations_in_ancestry']}")
            else:
                L.append(f"  - {k}: no qualifying agent (no meta-code change with a scored child) - no pay-off run")
    tb = a.get("tokens_by_arm", {})
    for arm, v in sorted(tb.items()):
        L.append(f"- Tokens, arm {arm}: {v['task_tokens_per_task_eval']:.0f} task-agent tokens per task evaluation "
                 f"({v['n_task_evals']} evaluations); {v['meta_tokens_per_iteration']:.0f} meta tokens per iteration ({v['n_meta_iterations']} iterations)")
    L += ["", "## Spend by role (USD, ledger)", ""]
    for k, v in sorted(a.get("spend_by_role", {}).items()):
        L.append(f"- {k}: ${v:.2f}")
    L.append(f"- **total: ${a.get('spend_total', 0):.2f}** (hard stop at $150)")
    L += ["", "## Crashes, aborts and reruns", ""]
    for d in sorted(glob.glob(os.path.join(EXP, "crashed", "*"))):
        L.append(f"- {os.path.basename(d)} (see DECISIONS.md)")
    for p in sorted(glob.glob(os.path.join(EXP, "runs", "*", "infra_aborts.jsonl"))):
        for r in read_jsonl(p):
            L.append(f"- infra abort (resumed) in {p.split('/')[-2]} at gen {r.get('gen')}: {r.get('error', '')[:160]}")
    L += ["", "## analysis.py output", "", "```", out.strip(), "```", ""]
    open(os.path.join(REPO, "RESULTS.md"), "w").write("\n".join(L))
    print("\n".join(L[:30]))


if __name__ == "__main__":
    main()
