"""Build the traced-demo bundle (DECISIONS 41; NOT part of the results).

Reads only exp/demo/ (traces.jsonl, eval_<tag>.jsonl, coach_<round>/) and the ARC task files. Writes
exp/demo/demo_bundle.json (full) and explorer/data/demo.json (same content, compact).

  python3 -m arcexp.build_demo_bundle --round c4 --fixed <tid> --still <tid> \
      --before base --after c4_eval --rep-before rpA0 --rep-after rpC4 --edit-summary "..."
"""
import argparse
import datetime
import json
import os
import re
import sys

from arcexp import arc_data
from arcexp.common import EXP, REPO

DEMO = os.path.join(EXP, "demo")
sys.path.insert(0, os.path.join(REPO, "agent_template"))
from task_agent import parse_grid  # noqa: E402  (A_0's parser; the chosen edit leaves it unchanged)

TOOL_PROMPT_END = "DO NOT HALLUCINATE OR MAKE UP ANYTHING."
GRID_RE = re.compile(r"\[\s*\[[\d\s,\[\]]*\]\s*\]")


def jl(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def traces_by_token():
    out = {}
    for r in jl(os.path.join(DEMO, "traces.jsonl")):
        out.setdefault(r["token"], []).append(r)
    for v in out.values():
        v.sort(key=lambda r: (r["call_index"], r["ts"]))
    return out


def clip(s, n=3000):
    if s is None or len(s) <= n:
        return s, False
    head, tail = s[: n * 2 // 3], s[-n // 3:]
    return f"{head}\n[... {len(s) - len(head) - len(tail)} characters omitted ...]\n{tail}", True


def shape(g):
    return f"{len(g)}x{len(g[0])}" if g and isinstance(g, list) and g[0] else "?"


def prompt_summary(text):
    """The prompt with every grid replaced by a placeholder (grid rows and JSON grids)."""
    out, rows = [], 0
    for line in text.splitlines():
        if re.fullmatch(r"[\d ]+", line.strip()) and line.strip():
            rows += 1
            continue
        if rows:
            out.append(f"[grid: {rows} rows]")
            rows = 0

        def rep(m):
            try:
                g = json.loads(m.group(0))
                return f"[grid {shape(g)}]"
            except Exception:
                return "[grid]"
        out.append(GRID_RE.sub(rep, line))
    if rows:
        out.append(f"[grid: {rows} rows]")
    return "\n".join(out)


def task_block(tid):
    t = arc_data.load_task(arc_data.split_of(tid), tid)
    return {"task": tid, "train": t["train"], "test": [{"input": x["input"], "output": x["output"]} for x in t["test"]]}


def rollout(row_group, traces, truth):
    """row_group: eval rows (attempts) of one (tag, rep, task, test_input)."""
    r0 = row_group[0]
    toks = r0.get("all_tokens") or ([r0["token"]] if r0.get("token") else [])
    tok = toks[-1] if toks else None
    calls = []
    for i, t in enumerate(traces.get(tok, []), 1):
        prompt = t["input"][-1]["content"] if t["input"] else ""
        g = parse_grid(t["output_text"] or "")
        calls.append({
            "call": i, "call_index": t["call_index"], "status": t["status"],
            "prompt_chars": len(prompt), "prompt_summary": prompt_summary(prompt),
            "reasoning_summary": t.get("reasoning_summary") or "",
            "answer_text": t["output_text"],
            "parsed_grid": g, "parsed_correct": (g == truth) if g is not None else None,
            "reasoning_tokens": (t.get("usage") or {}).get("output_tokens_details", {}).get("reasoning_tokens"),
            "cost_usd": round(t.get("cost") or 0, 5), "seconds": round(t.get("dur") or 0, 1),
        })
    answers = []
    for x in sorted(row_group, key=lambda x: x["attempt"]):
        if x["pred"] is not None:
            ok = x["pred"] == truth
            assert ok == bool(x["correct"]), ("scoring mismatch", r0["task"], r0["tag"])
            answers.append({"attempt": x["attempt"], "grid": x["pred"], "correct": ok})
    return {"tag": r0["tag"], "rep": r0["rep"], "token": tok, "retried_tokens": toks[:-1],
            "submitted": answers, "solved": any(a["correct"] for a in answers),
            "agent_error": r0.get("agent_error"), "calls": calls,
            "cost_usd": round(sum(c["cost_usd"] for c in calls), 5)}


def eval_groups(tag):
    g = {}
    for r in jl(os.path.join(DEMO, f"eval_{tag}.jsonl")):
        g.setdefault((r["rep"], r["task"], r["test_input"]), []).append(r)
    return g


def short_rollout(ro):
    return {"tag": ro["tag"], "rep": ro["rep"], "solved": ro["solved"],
            "submitted_correct": [a["correct"] for a in ro["submitted"]],
            "calls": [{"call": c["call"], "reasoning_summary": clip(c["reasoning_summary"], 1200)[0],
                       "parsed_correct": c["parsed_correct"]} for c in ro["calls"]]}


def coach_round(rnd, traces):
    cdir = os.path.join(DEMO, f"coach_{rnd}")
    summ = json.load(open(os.path.join(cdir, "summary.json")))
    rs = traces[summ["meta_token"]]
    turns = []
    for i, t in enumerate(rs):
        out = t["output_text"] or ""
        cmd = None
        m = re.search(r"\{.*\}", out, re.DOTALL)
        if m:
            try:
                obj = json.JSONDecoder().raw_decode(out, m.start())[0]
                if "tool_name" in obj:
                    cmd = obj.get("tool_input", {}).get("command", json.dumps(obj.get("tool_input")))
            except Exception:
                pass
        visible = out if cmd is None else out[: m.start()].strip()
        nxt = rs[i + 1]["input"][-1]["content"] if i + 1 < len(rs) else None
        tool_out, kind = None, None
        if nxt is not None:
            if TOOL_PROMPT_END in nxt:
                kind = "tool_output"
                tool_out = nxt.split(TOOL_PROMPT_END, 1)[1].strip()
                mm = re.search(r'"tool_output": "(.*)"\s*}\s*</json>\s*$', tool_out, re.DOTALL)
                if mm:
                    tool_out = mm.group(1)
            else:
                kind = "harness_nudge"
                tool_out = nxt
        to, trunc = clip(tool_out, 3000)
        turns.append({"turn": i + 1, "reasoning_summary": t.get("reasoning_summary") or "",
                      "visible_message": visible, "tool_command": cmd,
                      "next_input_kind": kind, "tool_output": to,
                      "tool_output_note": (f"truncated from {len(tool_out)} characters to ~3 KB" if trunc else None),
                      "cost_usd": round(t.get("cost") or 0, 5)})
    first_in = rs[0]["input"][0]["content"]
    instr = first_in.split(TOOL_PROMPT_END, 1)[1].strip() if TOOL_PROMPT_END in first_in else first_in
    return summ, turns, instr


def other_rounds(chosen, notes):
    out = []
    for d in sorted(os.listdir(DEMO)):
        if d.startswith("coach_") and d != f"coach_{chosen}" and os.path.exists(os.path.join(DEMO, d, "summary.json")):
            sm = json.load(open(os.path.join(DEMO, d, "summary.json")))
            out.append({"round": sm["tag"], "coach_calls": sm["meta_calls"], "patch_bytes": sm["patch_bytes"],
                        "practice_score_after_child_eval": sm["child_score"], "note": notes.get("round:" + sm["tag"])})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", required=True)
    ap.add_argument("--fixed", required=True)
    ap.add_argument("--still", required=True)
    ap.add_argument("--before", default="base")
    ap.add_argument("--after", required=True)
    ap.add_argument("--rep-before", required=True)
    ap.add_argument("--rep-after", required=True)
    ap.add_argument("--edit-summary", required=True)
    ap.add_argument("--choice-notes", default="{}")
    a = ap.parse_args()
    traces = traces_by_token()
    summ, turns, instr = coach_round(a.round, traces)
    cdir = os.path.join(DEMO, f"coach_{a.round}")
    base_rep = json.load(open(os.path.join(cdir, "baseline_eval", "report.json")))
    shown = sorted(f[len("chat_history_"):-3] for f in os.listdir(os.path.join(cdir, "baseline_eval", "agent_evals")))
    cmds = " ".join(t["tool_command"] or "" for t in turns)
    read = sorted({tid.rsplit("_", 1)[0] for tid in shown if tid.rsplit("_", 1)[0] in cmds})
    gb, ga = eval_groups(a.before), eval_groups(a.after)
    rb, ra = eval_groups(a.rep_before), eval_groups(a.rep_after)
    notes = json.loads(a.choice_notes)
    puzzles = []
    for kind, tid in (("fixed", a.fixed), ("still_wrong", a.still)):
        tb = task_block(tid)
        assert len(tb["test"]) == 1, "single test input expected"
        truth = arc_data.truth(tid, 0)
        assert truth == tb["test"][0]["output"]
        before = rollout(gb[(1, tid, 0)], traces, truth)
        after = rollout(ga[(1, tid, 0)], traces, truth)
        rep_b = [rollout(v, traces, truth) for k, v in sorted(rb.items()) if k[1] == tid]
        rep_a = [rollout(v, traces, truth) for k, v in sorted(ra.items()) if k[1] == tid]
        puzzles.append({
            "kind": kind, **tb, "why_chosen": notes.get(tid),
            "before": before, "after": after,
            "repeats": {
                "A0_solved": sum(r["solved"] for r in rep_b), "A0_runs": len(rep_b),
                "edited_solved": sum(r["solved"] for r in rep_a), "edited_runs": len(rep_a),
                "A0_incl_main": f"{sum(r['solved'] for r in rep_b) + before['solved']}/{len(rep_b) + 1}",
                "edited_incl_main": f"{sum(r['solved'] for r in rep_a) + after['solved']}/{len(rep_a) + 1}",
                "A0_runs_detail": [short_rollout(r) for r in rep_b],
                "edited_runs_detail": [short_rollout(r) for r in rep_a],
            },
        })
    # spend from the ledger (all demo phases)
    spend = {}
    for r in jl(os.path.join(EXP, "ledger", "calls.jsonl")):
        p = (r.get("scope") or {}).get("phase", "")
        if p.startswith("demo"):
            spend[p] = spend.get(p, 0) + (r.get("cost") or 0)
    some = next(iter(traces.values()))[0]
    efforts = sorted({(t[0]["role"], t[0].get("effort")) for t in traces.values()})
    diff = open(os.path.join(cdir, "model_patch.diff")).read()
    bundle = {
        "meta": {
            "built": datetime.date.today().isoformat(), "model": some["model"],
            "effort_by_role": {r: e for r, e in efforts},
            "summary_mode": "detailed",
            "demo_cost_usd_total": round(sum(spend.values()), 4),
            "demo_cost_usd_by_phase": {k: round(v, 4) for k, v in sorted(spend.items())},
            "caveats": [
                "Reasoning summaries are short summaries the model writes about its hidden reasoning, not the raw thoughts. "
                "The API returns them for only some reasoning steps, so some calls have none.",
                "Runs are not deterministic: the same player on the same puzzle can succeed one time and fail the next.",
                "This is a separate illustrative run made after the experiment. It is not part of the experiment's results.",
                "Tool calls are not separate events in the trace: the coach writes each tool call as text in its reply, "
                "and the tool's output comes back as text in its next input.",
            ],
        },
        "coach_round": {
            "round": a.round, "instruction": instr, "turns": turns, "diff": diff,
            "editor_summary": a.edit_summary,
            "practice_score_before": summ["baseline_score"], "practice_score_after_child_eval": summ["child_score"],
            "baseline_failures_shown": sorted({x.rsplit('_', 1)[0] for x in shown}),
            "baseline_failures_read": read,
            "baseline_failures_read_note": ("Task ids whose failure log (chat_history_<task>_0.md) the coach named in a tool command. "
                                            "It did not read them in full: see that turn's command for exactly what it printed."),
            "baseline_report": {"overall_accuracy": base_rep.get("overall_accuracy"),
                                "per_task_score": base_rep.get("per_task_score")},
        },
        "puzzles": puzzles,
        "other_rounds": other_rounds(a.round, notes),
    }
    # validation
    for p in puzzles:
        for tr in p["train"]:
            assert all(arc_data.valid_grid(g) for g in (tr["input"], tr["output"]))
        for ro in [p["before"], p["after"]]:
            for s in ro["submitted"]:
                assert s["correct"] == (s["grid"] == p["test"][0]["output"])
    os.makedirs(DEMO, exist_ok=True)
    json.dump(bundle, open(os.path.join(DEMO, "demo_bundle.json"), "w"), indent=1)
    dst = os.path.join(REPO, "explorer", "data", "demo.json")
    json.dump(bundle, open(dst, "w"), separators=(",", ":"))
    print(os.path.getsize(dst), "bytes ->", dst)


if __name__ == "__main__":
    main()
