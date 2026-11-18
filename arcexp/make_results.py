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
        L.append(f"- One held-out pass of A_0 at xhigh effort: {xl[-1].split(':')[1].split()[0]} (after re-running the 32 inputs that had hit the old 30-min limit; no final xhigh input timed out).")
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
    L.append(f"- **total: ${a.get('spend_total', 0):.2f}** (hard stop: $150 under DESIGN.md, raised to $200 by the user; projection posted before the extension tests: ~$135-165)")
    L += ["", "## Crashes, aborts and reruns", ""]
    for d in sorted(glob.glob(os.path.join(EXP, "crashed", "*"))):
        L.append(f"- {os.path.basename(d)} (see DECISIONS.md)")
    for p in sorted(glob.glob(os.path.join(EXP, "runs", "*", "infra_aborts.jsonl"))):
        for r in read_jsonl(p):
            L.append(f"- infra abort (resumed) in {p.split('/')[-2]} at gen {r.get('gen')}: {r.get('error', '')[:160]}")
    # timeouts per arm (same 3 h limit for every arm; earlier limits were re-run, see DECISIONS 26)
    L += ["", "## Timeouts per arm (rollouts that hit the per-test-input wall-clock limit)", "",
          "| arm / phase | rollouts | timeouts |", "|---|---|---|"]
    import collections
    cnt = collections.OrderedDict()
    for f in sorted(glob.glob(os.path.join(EXP, "results", "*.jsonl"))):
        ph = os.path.basename(f)[:-6]
        if ph.endswith(".invalidated") or ph in ("b0_summary", "final_runs", "devtest"):
            continue
        for r in read_jsonl(f):
            if r.get("attempt") != 1 or r.get("infra_error"):
                continue
            k = f"{ph} / {r.get('arm')}"
            c = cnt.setdefault(k, [0, 0]); c[0] += 1; c[1] += 1 if r.get("timeout") else 0
    for k, (n, t) in cnt.items():
        L.append(f"| {k} | {n} | {t} |")
    inv = sum(1 for f in glob.glob(os.path.join(EXP, "results", "*.invalidated.jsonl")) for r in read_jsonl(f) if r.get("attempt") == 1)
    L.append(f"\n{inv} rollouts that hit an earlier (30-min) limit were invalidated and re-run under the 3 h limit.")
    # effort and model actually used
    led = read_jsonl(os.path.join(EXP, "ledger", "calls.jsonl"))
    eff = collections.Counter((r.get("role"), r.get("effort_echo")) for r in led if not r.get("error"))
    models = collections.Counter(r.get("model") for r in led if not r.get("error"))
    L += ["", "## Model and reasoning effort actually used", "",
          f"- Model string returned by the API: {', '.join(f'`{m}` ({n} calls)' for m, n in models.items())}; calls from 2026-11-17 to {__import__('time').strftime('%Y-%m-%d')}.",
          f"- Effort echoed by the API, by role: {', '.join(f'{r}={e}: {n}' for (r, e), n in sorted(eff.items(), key=lambda x: str(x)))}."]
    # extension
    ext = subprocess.run(["python3", os.path.join(REPO, "analysis_ext.py")], capture_output=True, text=True, cwd=REPO)
    ea = json.load(open(os.path.join(EXP, "results", "ext_analysis.json"))) if os.path.exists(os.path.join(EXP, "results", "ext_analysis.json")) else {}
    L += ["", "# EXTENSION (DESIGN_v2.md, not pre-registered in f577cc7)", "",
          "Does the coach get better at coaching over generations? Exam score of the player each coach builds, by coach generation.", "",
          "![extension plot](exp/results/extension_plot.png)", "",
          "| generation | runs | mean | 95% t-interval | scores |", "|---|---|---|---|---|"]
    for g, v in sorted(ea.get("per_generation", {}).items(), key=lambda x: int(x[0])):
        L.append(f"| {g} | {v['n']} | {pct(v['mean'])} | [{pct(v['lo']) if v['lo'] == v['lo'] else 'n/a'}, {pct(v['hi']) if v['hi'] == v['hi'] else 'n/a'}] | {', '.join(pct(x) for x in v['scores'])} |")
    if "gen40_minus_gen0" in ea:
        v = ea["gen40_minus_gen0"]
        L.append(f"\n**Generation 40 minus original coach: {pts(v['est'])} points, 95% Welch CI [{pts(v['lo'])}, {pts(v['hi'])}] -> {v['verdict']}.**")
    for k, v in ea.get("paired_changes", {}).items():
        L.append(f"- Paired change {k} (seeds 0-3): " + (", ".join(f"seed {s}: {pts(d)}" for s, d in v["per_seed"].items()) or "n/a")
                 + (f"; mean {pts(v['mean'])}" if v.get("mean") is not None else ""))
    L.append("\n**Caveat (identical coaches).** Several extension picks are the same coach node at several generations (DECISIONS 37). "
             "Seed 0's picks at generations 12, 20 and 40 are all node 1, and seed 2's at 20 and 40 are node 9. For those seeds the 'change' "
             "between generations is run-to-run variation of one coach's 8-round run. Seed 0's identical coach scored "
             + ", ".join(pct(x) for x in [p_["heldout"] for p_ in ea.get("points", []) if p_.get("seed_index") == 0])
             + " (a spread of about 10 points), so the trend cannot be separated from that variation.")
    cmp_p = os.path.join(EXP, "results", "pick_rule_comparison_g12.json")
    if os.path.exists(cmp_p):
        cmp = json.load(open(cmp_p))
        L += ["", "**Pick rules compared at generation 12** (extension rule vs committed rule, same archive):", "",
              "| seed | committed rule | extension rule | same coach? |", "|---|---|---|---|"]
        for run, v in cmp.items():
            L.append(f"| {v['seed_index']} ({run}) | {v['committed_rule_pick'] if v['committed_rule_pick'] is not None else 'none'} | "
                     f"{v['extension_rule_pick'] if v['extension_rule_pick'] is not None else 'none'} | "
                     f"{'yes' if v['committed_rule_pick'] == v['extension_rule_pick'] else 'no'} |")
        L.append("\nSeed 3: the committed rule needs a changed coach with at least one scored child and finds none. The extension "
                 "rule falls back to the changed coach with the most descendants: node 6, with 0 descendants (tied with node 12 and broken by the earlier generation).")
    pc = ea.get("picks_changed_code", {})
    L.append(f"- Picks with changed coach code: generation 12 (part A rule) {pc.get('gen12 (part A rule)')}; extension {pc.get('extension picks with changed coach code')} ({pc.get('extension picks')}).")
    au_p = os.path.join(EXP, "results", "diff_audit.json")
    if os.path.exists(au_p):
        au = json.load(open(au_p))
        L += ["", "## Diff audit of every picked coach (each changed hunk vs I_0; 2 independent judges + tiebreak)", "",
              "| pick | file | hunk | tag | agreement |", "|---|---|---|---|---|"]
        for k, v in sorted(au.items()):
            for h in sorted(v["hunks"], key=lambda h: h["idx"]):
                L.append(f"| {k} | {h['file']} | {h['idx']} | {h['tag']} | {h['agreement']} |")
        tags = [h["tag"] for v in au.values() for h in v["hunks"]]
        L.append(f"\n{tags.count('ARC-specific')} of {len(tags)} hunks ARC-specific, {tags.count('general')} general. Reasons in exp/results/diff_audit.json.")
    L += ["", "## Deviations from f577cc7 and DESIGN_v2.md", "", "Every deviation and harness fix is numbered in DECISIONS.md (items marked DEVIATION; harness bugs and reruns at 23, 24, 26, 28, 33, 35)."]
    L += ["", "## analysis.py output", "", "```", out.strip(), "```", ""]
    open(os.path.join(REPO, "RESULTS.md"), "w").write("\n".join(L))
    print("\n".join(L[:30]))


if __name__ == "__main__":
    main()
