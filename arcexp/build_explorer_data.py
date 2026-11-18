#!/usr/bin/env python3
"""Build the JSON data files for the interactive experiment explorer (explorer/data/).

Read-only on the experiment: it reads exp/ (results, runs, archive_export, ledger), splits.json
and the ARC-AGI-2 task files, and writes only explorer/data/*.json. Stdlib only.

    python3 arcexp/build_explorer_data.py

Every number is derived from the experiment's files; nothing is typed in by hand.
"""
import collections
import glob
import json
import os
import re
import statistics

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(REPO, "exp")
RES = os.path.join(EXP, "results")
OUT = os.path.join(REPO, "explorer", "data")
ARC_DIR = "/opt/arc_private/ARC-AGI-2/data"
SIZE_BUDGET = 9 * 1024 * 1024

DIFF_CAP = 6 * 1024
PLAYER_TX_CAP = 8 * 1024
COACH_TX_CAP = 10 * 1024
HELDOUT_PRED_BUDGET = 4.2 * 1024 * 1024

SOURCE_RUNS = [f"source_s{i}" for i in range(1, 7)]
TRIMMED = []  # human-readable log of every trim, copied into manifest.json
REDACTIONS = collections.Counter()


# ----------------------------------------------------------------------------- helpers
def rj(path):
    out = []
    if not os.path.exists(path):
        return out
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def lj(path):
    with open(path) as f:
        return json.load(f)


_SECRET_PATTERNS = [
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{16,}"), "sk-key"),
    (re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._\-]{16,}"), "bearer"),
    (re.compile(r"(?i)((?:api[_-]?key|access[_-]?token|secret|password)\s*[=:]\s*['\"]?)[A-Za-z0-9._\-]{12,}"), "kv-secret"),
    (re.compile(r"\b[0-9a-f]{32}\b"), "32hex-gateway-token"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "github-token"),
]


def scrub(text):
    if not text:
        return text
    for pat, name in _SECRET_PATTERNS:
        def rep(m, name=name):
            REDACTIONS[name] += 1
            if name == "kv-secret":
                return m.group(1) + "[REDACTED]"
            return "[REDACTED]"
        text = pat.sub(rep, text)
    return text


def r4(x):
    return None if x is None else round(x, 4)


def mean(xs):
    xs = [x for x in xs if x is not None]
    return statistics.mean(xs) if xs else None


def write(name, obj):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        json.dump(obj, f, separators=(",", ":"))
    return os.path.getsize(path)


# ----------------------------------------------------------------------------- ARC data
_task_cache = {}


def load_task(tid):
    if tid not in _task_cache:
        for split in ("evaluation", "training"):
            p = os.path.join(ARC_DIR, split, f"{tid}.json")
            if os.path.exists(p):
                d = lj(p)
                d["_split"] = split
                _task_cache[tid] = d
                break
        else:
            raise FileNotFoundError(tid)
    return _task_cache[tid]


def n_test(tid):
    return len(load_task(tid)["test"])


# ----------------------------------------------------------------------------- results rows
def done_map(rows, key_fn, code_hash_for=None):
    """Mirror arcexp.arc_eval.load_done: skip infra errors, optional code-hash filter, first row per
    attempt wins, keep keys with both attempts. Returns {key: [row_attempt1, row_attempt2]}."""
    slots = {}
    for r in rows:
        if r.get("infra_error"):
            continue
        k = key_fn(r)
        if code_hash_for is not None:
            want = code_hash_for(k)
            if want is not None and r.get("code_hash") != want:
                continue
        slots.setdefault(k, {}).setdefault(r["attempt"], r)
    return {k: [v[1], v[2]] for k, v in slots.items() if 1 in v and 2 in v}


def score_from_done(done, prefix, task_ids):
    """Task-averaged pass@2 score, same as evaluate_set (missing test inputs count as unsolved)."""
    per_task = {}
    for tid in task_ids:
        vals = []
        for ti in range(n_test(tid)):
            rs = done.get(prefix + (tid, ti))
            vals.append(bool(rs and any(x["correct"] for x in rs)))
        per_task[tid] = sum(vals) / len(vals)
    return sum(per_task.values()) / len(per_task), per_task


def run_identity(run):
    """(results phase file, arm, seed-as-str) used for practice-set rows of a run."""
    m = re.match(r"source_s(\d+)$", run)
    if m:
        return "source", "I0src", m.group(1)
    m = re.match(r"payoff_I0_(\d+)$", run)
    if m:
        return "payoff", "I0", "r" + m.group(1)
    m = re.match(r"payoff_Ig_source_s(\d+)$", run)
    if m:
        return "payoff", "Ig", m.group(1)
    m = re.match(r"ext_source_s(\d+)_g(\d+)$", run)
    if m:
        return "ext_payoff", "g" + m.group(2), str(int(m.group(1)) - 1)
    raise ValueError(run)


def run_kind(run):
    if run.startswith("source_"):
        return "source"
    if run.startswith("payoff_I0"):
        return "payoff_I0"
    if run.startswith("payoff_Ig"):
        return "payoff_Ig"
    return "extension_test"


# ----------------------------------------------------------------------------- diffs
COACH_PREFIXES = ("meta_agent.py", "run_meta_agent.py", "agent/", "tests/test_meta_agent")
PLAYER_PREFIXES = ("task_agent.py", "run_task_agent.py", "domains/", "tests/test_task_agent")


def classify_path(p):
    if p.endswith(".pyc") or "__pycache__" in p:
        return "other"
    if p.startswith(COACH_PREFIXES):
        return "coach"
    if p.startswith(PLAYER_PREFIXES):
        return "player"
    return "other"


def parse_diff(path):
    """Return (files[{path, role, added, removed, binary}], cleaned_text_without_binary_sections)."""
    if not path or not os.path.exists(path):
        return [], ""
    raw = open(path, errors="replace").read()
    sections = re.split(r"(?m)^(?=diff --git )", raw)
    files, keep = [], []
    for s in sections:
        m = re.match(r"diff --git a/(\S+) b/(\S+)", s)
        if not m:
            if s.strip():
                keep.append(s)
            continue
        p = m.group(2)
        binary = "GIT binary patch" in s or re.search(r"(?m)^Binary files ", s) is not None
        added = removed = 0
        if not binary:
            for line in s.splitlines():
                if line.startswith("+") and not line.startswith("+++"):
                    added += 1
                elif line.startswith("-") and not line.startswith("---"):
                    removed += 1
        files.append({"path": p, "role": classify_path(p), "added": added, "removed": removed, "binary": binary})
        if binary:
            keep.append(s.split("\n", 1)[0] + "\n[binary diff omitted]\n")
        else:
            keep.append(s)
    return files, "".join(keep)


def cap_text(text, cap, tail=1200, label="chars"):
    if text is None or len(text) <= cap:
        return text, False
    head = cap - tail - 80
    return (text[:head] + f"\n\n[... {len(text) - head - tail} {label} truncated ...]\n\n" + text[-tail:]), True


# ----------------------------------------------------------------------------- main build
def main():
    os.makedirs(OUT, exist_ok=True)
    splits = lj(os.path.join(REPO, "splits.json"))
    HELDOUT = splits["heldout"]
    SRC_SET = splits["source"]
    PAY_SET = splits["payoff"]

    analysis = lj(os.path.join(RES, "analysis.json"))
    ext = lj(os.path.join(RES, "ext_analysis.json"))
    ig_sel = lj(os.path.join(RES, "ig_selection.json"))
    ext_picks = lj(os.path.join(RES, "ext_picks.json"))
    diff_audit = lj(os.path.join(RES, "diff_audit.json"))
    final_runs = {r["run"]: r for r in analysis["final_runs"]}
    final_runs_file = {}
    for r in rj(os.path.join(RES, "final_runs.jsonl")):
        final_runs_file[r["run"]] = r  # last write wins
    for k, v in final_runs.items():
        assert abs(final_runs_file[k]["heldout"] - v["heldout"]) < 1e-12, k
    PAYOFF_RUNS = [r["run"] for r in analysis["final_runs"]]
    PAYOFF_RUNS.sort(key=lambda r: (["payoff_I0", "payoff_Ig", "extension_test"].index(run_kind(r)), r))
    ledger = rj(os.path.join(EXP, "ledger", "calls.jsonl"))

    rows_by_phase = {ph: rj(os.path.join(RES, f"{ph}.jsonl"))
                     for ph in ("source", "payoff", "ext_payoff", "heldout", "b0", "xhigh", "initial")}

    def k6(r):
        return (r["phase"], r["arm"], str(r["seed"]), str(r["iteration"]), r["task"], int(r["test_input"]))

    # ------------------------------------------------------------------ ledger aggregations
    led_task = collections.defaultdict(lambda: {"cost": 0.0, "tokens": 0, "calls": 0})
    led_meta = collections.defaultdict(lambda: {"cost": 0.0, "tokens": 0, "calls": 0})
    spend_phase_role = collections.defaultdict(float)
    for c in ledger:
        sc = c.get("scope") or {}
        cost = c.get("cost") or 0.0
        spend_phase_role[(sc.get("phase"), c.get("role"))] += cost
        if c.get("role") == "task":
            k = (sc.get("phase"), sc.get("arm"), str(sc.get("seed")), str(sc.get("iteration")))
            a = led_task[k]
        elif c.get("role") == "meta":
            k = (sc.get("run"), str(sc.get("iteration")))
            a = led_meta[k]
        else:
            continue
        a["cost"] += cost
        a["tokens"] += c.get("total_tokens") or 0
        a["calls"] += 1

    def led_task_sum(phase, arm, seed, iteration=None):
        out = {"cost": 0.0, "tokens": 0, "calls": 0}
        for (ph, ar, se, it), v in led_task.items():
            if ph == phase and ar == arm and se == str(seed) and (iteration is None or it == str(iteration)):
                for kk in out:
                    out[kk] += v[kk]
        return out

    def led_meta_run(run):
        out = {"cost": 0.0, "tokens": 0, "calls": 0}
        for (rn, it), v in led_meta.items():
            if rn == run:
                for kk in out:
                    out[kk] += v[kk]
        return out

    # ================================================================== trees.json
    trees = {}
    practice_done_cache = {}
    meta_lineage_tokens = {}  # (run, node) -> cumulative meta tokens along lineage
    all_runs = SOURCE_RUNS + PAYOFF_RUNS
    for run in all_runs:
        nodes = lj(os.path.join(EXP, "archive_export", run, "nodes.json"))
        cfg = lj(os.path.join(EXP, "runs", run, "config.json"))
        gen_scores = {str(r["iteration"]): r for r in rj(os.path.join(EXP, "runs", run, "gen_scores.jsonl"))}
        meta_steps = {}
        for r in rj(os.path.join(EXP, "runs", run, "meta_steps.jsonl")):
            meta_steps[str(r["iteration"])] = r  # last write wins (resumed iterations)
        phase, arm, seed = run_identity(run)
        task_set = SRC_SET if phase == "source" else PAY_SET
        set_name = "source" if phase == "source" else "payoff"

        rows = [r for r in rows_by_phase[phase] if r["arm"] == arm and str(r["seed"]) == seed]
        done = done_map(rows, k6, lambda k: (gen_scores.get(k[3]) or {}).get("code_hash"))
        init_rows = [r for r in rows_by_phase["initial"] if str(r["iteration"]) == set_name]
        init_done = done_map(init_rows, k6)

        # pick annotations
        ig_gen = None
        ext_pick_labels = collections.defaultdict(list)
        if run in ig_sel and ig_sel[run].get("I_g"):
            ig_gen = str(ig_sel[run]["I_g"]["gen"])
        for key, v in ext_picks.items():
            if v["run"] == run:
                ext_pick_labels[str(v["pick"]["gen"])].append(f"g{v['generation']}")
        fr = final_runs.get(run)

        out_nodes = []
        # order: initial first, then numeric
        order = sorted(nodes.keys(), key=lambda x: (-1 if x == "initial" else int(x)))
        for nid in order:
            n = nodes[nid]
            files, diff_text = parse_diff(os.path.join(EXP, n["patch_file"]) if n.get("patch_file") else None)
            diff_text = scrub(diff_text)
            diff_full_len = len(diff_text or "")
            diff_text, truncated = cap_text(diff_text, DIFF_CAP, tail=800, label="diff chars")
            ms = meta_steps.get(nid)
            # practice-set rollouts of this node's player
            if nid == "initial":
                pre = ("initial", "A0", "-", set_name)
                d = init_done
            else:
                pre = (phase, arm, seed, nid)
                d = done
            have = [k for k in d if k[:4] == pre]
            prac = None
            if have:
                sc, per_task = score_from_done(d, pre, task_set)
                first = [d[k][0] for k in have]
                prac = {
                    "recomputed_score": r4(sc),
                    "n_test_inputs_run": len(have),
                    "tokens_per_test_input": r4(mean([x.get("tokens") for x in first])),
                    "calls_per_test_input": r4(mean([x.get("calls") for x in first])),
                    "seconds_per_test_input": r4(mean([x.get("dur") for x in first])),
                    "per_task": {t: r4(v) for t, v in per_task.items()},
                }
                practice_done_cache[(run, nid)] = (d, pre)
            node = {
                "id": nid,
                "generation": n["generation"],
                "parent": None if n["parent"] is None else str(n["parent"]),
                "children": [str(c) for c in n.get("children", [])],
                "practice_score": n.get("loop_score_on_set"),
                "valid": bool(n.get("valid_parent")),
                "files_changed": files,
                "touched_coach": any(f["role"] == "coach" for f in files),
                "touched_player": any(f["role"] == "player" for f in files),
                "coach_files_changed_vs_I0": n.get("coach_files_changed_vs_I0"),
                "diff": diff_text,
                "diff_truncated": truncated,
                "diff_full_chars": diff_full_len,
                "meta": None if ms is None else {
                    "calls": ms.get("meta_calls"), "tokens": ms.get("meta_tokens"),
                    "seconds": r4(ms.get("dur")), "rc": ms.get("rc"),
                    "ledger_cost": r4(led_meta.get((run, nid), {}).get("cost")),
                },
                "practice": prac,
                "is_Ig_pick": ig_gen == nid,
                "ext_pick_at": ext_pick_labels.get(nid, []),
                "is_final_player": bool(fr and fr["final_node"] == nid),
                "final_candidate": bool(fr and nid in fr["candidates"]),
                "rescore_combined": (fr or {}).get("combined", {}).get(nid),
                "heldout_score": r4(fr["heldout"]) if fr and fr["final_node"] == nid else None,
            }
            out_nodes.append(node)

        # lineage compute
        by_id = {n["id"]: n for n in out_nodes}
        for n in out_nodes:
            tot, calls, cost, cur, depth = 0, 0, 0.0, n, 0
            while cur is not None:
                if cur["meta"]:
                    tot += cur["meta"]["tokens"] or 0
                    calls += cur["meta"]["calls"] or 0
                    cost += cur["meta"]["ledger_cost"] or 0.0
                depth += 1
                cur = by_id.get(cur["parent"]) if cur["parent"] is not None else None
            n["lineage"] = {"depth": depth - 1, "cum_meta_tokens": tot, "cum_meta_calls": calls, "cum_meta_cost": r4(cost)}
            meta_lineage_tokens[(run, n["id"])] = n["lineage"]

        # coach origin for pay-off/extension runs
        coach_origin = None
        if run.startswith("payoff_Ig_source_s"):
            src = "source_s" + run.rsplit("s", 1)[1]
            g = str(ig_sel[src]["I_g"]["gen"])
            coach_origin = {"source_run": src, "source_node": g, "rule": "A_gen12 I_g selection (ig_selection.json)"}
        elif run.startswith("ext_source_s"):
            m = re.match(r"ext_source_s(\d+)_g(\d+)", run)
            key = f"source_s{m.group(1)}:g{m.group(2)}"
            coach_origin = {"source_run": f"source_s{m.group(1)}", "source_node": str(ext_picks[key]["pick"]["gen"]),
                            "rule": ext_picks[key]["rule"]}
        elif run.startswith("payoff_I0"):
            coach_origin = {"source_run": None, "source_node": None, "rule": "original coach I_0 (unchanged)"}

        audit = []
        for key, v in diff_audit.items():
            if key == f"A_gen12:{run}" or key.startswith(f"ext:{run}_g"):
                for h in v["hunks"]:
                    audit.append({"pick": key, "file": h.get("file"), "idx": h.get("idx"), "tag": h.get("tag"),
                                  "agreement": h.get("agreement"), "reason": scrub((h.get("reasons") or [""])[0])})

        trees[run] = {
            "run": run,
            "kind": run_kind(run),
            "arm": arm,
            "seed": seed,
            "task_set": set_name,
            "max_generation": cfg.get("max_generation"),
            "max_generation_committed": cfg.get("max_generation_committed"),
            "frozen_paths": cfg.get("freeze_paths"),
            "coach_origin": coach_origin,
            "final": None if not fr else {
                "final_node": fr["final_node"], "candidates": fr["candidates"], "combined": fr["combined"],
                "heldout": r4(fr["heldout"]), "n_accepted": fr.get("n_accepted"),
            },
            "diff_audit": audit,
            "nodes": out_nodes,
        }
    # attach source-lineage compute to coach origins
    for run, t in trees.items():
        co = t.get("coach_origin")
        if co and co.get("source_run"):
            co["source_lineage"] = meta_lineage_tokens.get((co["source_run"], co["source_node"]))
            co["source_node_practice_score"] = next(
                (n["practice_score"] for n in trees[co["source_run"]]["nodes"] if n["id"] == co["source_node"]), None)

    # sanity: recomputed practice score vs loop score
    mism = []
    for run, t in trees.items():
        for n in t["nodes"]:
            if n["practice"] and n["practice_score"] is not None and n["id"] != "initial":
                if abs(n["practice"]["recomputed_score"] - n["practice_score"]) > 0.011:
                    mism.append((run, n["id"], n["practice_score"], n["practice"]["recomputed_score"]))

    # ================================================================== heldout runs (compute.json + heldout.json)
    hrows = rows_by_phase["heldout"]
    held_runs = []  # (run_id, label, group, prefix, done)
    b0_done = done_map(rows_by_phase["b0"], k6)
    b0_reps = sorted({k[3] for k in b0_done}, key=int)
    for rep in b0_reps:
        held_runs.append((f"B0_rep{rep}", f"B0 rep {rep} (A_0, two plain attempts)", "B0",
                          ("b0", "A0", "-", rep), b0_done, ("b0", "A0", "-", rep)))
    x_done = done_map(rows_by_phase["xhigh"], k6)
    held_runs.append(("xhigh", "A_0 at xhigh effort", "xhigh", ("xhigh", "A0", "-", "0"), x_done, ("xhigh", "A0", "-", None)))
    h_done = done_map(hrows, k6)
    for run in PAYOFF_RUNS:
        fr = final_runs[run]
        _, arm, seed = run_identity(run)
        held_runs.append((run, run, {"I0": "I0", "Ig": "Ig"}.get(arm, arm), ("heldout", arm, seed, fr["final_node"]),
                          h_done, ("heldout", arm, seed, fr["final_node"])))

    b0_by_rep = {}
    for r in rj(os.path.join(RES, "b0_summary.jsonl")):
        b0_by_rep[str(r["rep"])] = r["score"]

    compute = {"runs": [], "notes": {}}
    heldout = {"task_order": HELDOUT, "n_test_inputs": {t: n_test(t) for t in HELDOUT}, "runs": {}}
    score_check = []
    for run_id, label, group, pre, d, ledkey in held_runs:
        sc, per_task = score_from_done(d, pre, HELDOUT)
        keys = [k for k in d if k[:4] == pre]
        first = [d[k][0] for k in keys]
        reported = None
        if group == "B0":
            reported = b0_by_rep.get(pre[3])
        elif group == "xhigh":
            reported = ext.get("xhigh")
        else:
            reported = final_runs[run_id]["heldout"]
        score_check.append((run_id, r4(sc), r4(reported)))
        led = led_task_sum(*ledkey)
        entry = {
            "run": run_id, "label": label, "group": group,
            "generation": {"B0": None, "xhigh": None, "I0": 0, "Ig": 12, "g20": 20, "g40": 40}[group],
            "score": r4(sc), "reported_score": r4(reported),
            "n_test_inputs": len(keys),
            "tokens_per_test_input": r4(mean([x.get("tokens") for x in first])),
            "calls_per_test_input": r4(mean([x.get("calls") for x in first])),
            "seconds_per_test_input": r4(mean([x.get("dur") for x in first])),
            "timeouts": sum(1 for x in first if x.get("timeout")),
            "format_failures": sum(1 for x in first if (x.get("n_answers") or 0) == 0),
            "heldout_eval_cost": r4(led["cost"]), "heldout_eval_ledger_tokens": led["tokens"],
            "heldout_eval_ledger_calls": led["calls"],
        }
        entry["score_per_10k_tokens"] = r4(sc / entry["tokens_per_test_input"] * 1e4) if entry["tokens_per_test_input"] else None
        if group not in ("B0", "xhigh"):
            phase, arm, seed = run_identity(run_id)
            loop_player = led_task_sum(phase, arm, seed)
            rescore = led_task_sum("rescore", arm, seed)
            coach = led_meta_run(run_id)
            co = trees[run_id]["coach_origin"]
            src_lin = (co or {}).get("source_lineage") or {}
            entry.update({
                "final_node": final_runs[run_id]["final_node"],
                "improvement_cost": {
                    "payoff_loop_player_cost": r4(loop_player["cost"]), "payoff_loop_player_tokens": loop_player["tokens"],
                    "payoff_loop_coach_cost": r4(coach["cost"]), "payoff_loop_coach_tokens": coach["tokens"],
                    "rescore_cost": r4(rescore["cost"]),
                    "coach_source_lineage_meta_tokens": src_lin.get("cum_meta_tokens"),
                    "coach_source_lineage_meta_cost": src_lin.get("cum_meta_cost"),
                },
                "final_player_lineage": meta_lineage_tokens.get((run_id, final_runs[run_id]["final_node"])),
            })
        compute["runs"].append(entry)
        # heldout per-task results
        heldout["runs"][run_id] = {"label": label, "group": group, "score": r4(sc), "has_preds": False,
                                   "per_task": {t: r4(v) for t, v in per_task.items()}, "results": {},
                                   "_raw": {t: [d.get(pre + (t, ti)) for ti in range(n_test(t))] for t in HELDOUT}}
    compute["notes"] = {
        "tokens_per_test_input": "mean over test inputs of the player's total model tokens for that test input (both answers come from one execution; rows for attempt 1 and 2 carry the same totals)",
        "heldout_eval_cost": "sum of ledger cost for role=task calls whose scope matches the run's held-out evaluation (includes infra retries)",
        "improvement_cost": "cost/tokens spent producing the final player: pay-off loop player evals (scope phase payoff/ext_payoff), coach calls in the pay-off run (ledger meta scope.run), rescoring of finalists, and the source-run lineage meta tokens/cost of the frozen coach (Ig/g20/g40 only)",
        "score": "recomputed task-averaged pass@2 from result rows (same rule as arcexp/arc_eval.evaluate_set); reported_score is the value in analysis/b0_summary/ext_analysis",
    }

    # choose which runs keep preds
    def pred_size(run_id):
        raw = heldout["runs"][run_id]["_raw"]
        s = 0
        for t, lst in raw.items():
            for rs in lst:
                if not rs:
                    continue
                p1, p2 = rs[0].get("pred"), rs[1].get("pred")
                s += len(json.dumps(p1, separators=(",", ":")))
                if p2 != p1:
                    s += len(json.dumps(p2, separators=(",", ":")))
        return s

    g40_best = max([r for r in PAYOFF_RUNS if r.endswith("_g40")], key=lambda r: final_runs[r]["heldout"])
    ig_best = max([r for r in PAYOFF_RUNS if r.startswith("payoff_Ig")], key=lambda r: final_runs[r]["heldout"])
    priority = ["payoff_I0_1", ig_best, g40_best, f"B0_rep{b0_reps[0]}", "xhigh"]
    priority += [r for r in heldout["runs"] if r not in priority]
    used, keep_preds = 0, []
    for rid in priority:
        s = pred_size(rid)
        if used + s <= HELDOUT_PRED_BUDGET:
            keep_preds.append(rid)
            used += s
    dropped = [r for r in heldout["runs"] if r not in keep_preds]
    if dropped:
        TRIMMED.append(f"heldout.json: predicted grids dropped (correct flags kept) for {len(dropped)} runs: {', '.join(dropped)}")
    for rid, hr in heldout["runs"].items():
        raw = hr.pop("_raw")
        hr["has_preds"] = rid in keep_preds
        for t, lst in raw.items():
            out = []
            for rs in lst:
                if not rs:
                    out.append(None)
                    continue
                rec = {"c": [int(bool(rs[0]["correct"])), int(bool(rs[1]["correct"]))],
                       "n": rs[0].get("n_answers"), "tok": rs[0].get("tokens"), "calls": rs[0].get("calls"),
                       "sec": rs[0].get("dur")}
                if rs[0].get("timeout"):
                    rec["timeout"] = True
                if rs[0].get("agent_error"):
                    rec["err"] = scrub(str(rs[0]["agent_error"])[:200])
                if hr["has_preds"]:
                    p1, p2 = rs[0].get("pred"), rs[1].get("pred")
                    rec["p"] = [p1, "=1" if (p2 == p1 and p1 is not None) else p2]
                out.append(rec)
            hr["results"][t] = out

    # ================================================================== tasks.json
    practice_ids = sorted(set(SRC_SET) | set(PAY_SET))
    tasks = {}
    for tid in HELDOUT + practice_ids:
        t = load_task(tid)
        tasks[tid] = {
            "id": tid,
            "set": "heldout" if tid in HELDOUT else ("source" if tid in SRC_SET else "payoff"),
            "arc_split": t["_split"],
            "train": [{"input": p["input"], "output": p["output"]} for p in t["train"]],
            "test": [{"input": p["input"], "output": p["output"]} for p in t["test"]],
        }
    # solve-rate summary per held-out task (over all held-out runs, pass@2 per test input)
    for tid in HELDOUT:
        vals = [hr["per_task"][tid] for hr in heldout["runs"].values()]
        tasks[tid]["heldout_mean_solve"] = r4(mean(vals))

    # ================================================================== transcripts.json
    def gen_dir(run, nid):
        return os.path.join(EXP, "runs", run, f"generate_{run}", f"gen_{nid}")

    HDR = re.compile(r"(?m)^(Input|Output|Error|Tool output|Nudge|[A-Z][a-z]+ (?:input|output)):")

    def segments(text, cap, kind):
        parts = []
        idx = [(m.start(), m.group(1)) for m in HDR.finditer(text)]
        if not idx or idx[0][0] != 0:
            idx = [(0, "Text")] + idx
        for i, (pos, name) in enumerate(idx):
            end = idx[i + 1][0] if i + 1 < len(idx) else len(text)
            body = text[pos:end]
            body = body[len(name) + 1:].strip() if body.startswith(name + ":") else body.strip()
            parts.append({"role": name, "text": body})
        out = []
        for p in parts:
            t = p["text"]
            if kind == "player":
                if p["role"].lower().endswith("input") or p["role"] == "Input":
                    # prompt: show the instruction head and the closing instructions; grids live in tasks.json
                    if len(t) > 1800:
                        t = t[:1100] + f"\n\n[... {len(t) - 1700} chars of example/test grids elided (see the puzzle view) ...]\n\n" + t[-600:]
                else:
                    if len(t) > 3200:
                        t = t[:2000] + f"\n\n[... {len(t) - 3000} chars elided ...]\n\n" + t[-1000:]
            else:
                if len(t) > 900:
                    t = t[:650] + f"\n[... {len(t) - 900} chars elided ...]\n" + t[-250:]
            out.append({"role": p["role"], "text": scrub(t)})
        # global cap: keep head and tail segments
        total = sum(len(s["text"]) for s in out)
        if total > cap:
            head, tail, hs, ts = [], [], 0, 0
            budget_head, budget_tail = cap * 0.45, cap * 0.45
            for s in out:
                if hs + len(s["text"]) > budget_head:
                    break
                head.append(s)
                hs += len(s["text"])
            for s in reversed(out[len(head):]):
                if ts + len(s["text"]) > budget_tail:
                    break
                tail.insert(0, s)
                ts += len(s["text"])
            skipped = len(out) - len(head) - len(tail)
            if not tail and len(out) > len(head):  # one huge final segment: keep its end
                last = dict(out[-1])
                last["text"] = "[...]\n" + last["text"][-int(budget_tail):]
                tail = [last]
                skipped -= 1
            out = head + ([{"role": "Elided", "text": f"[{skipped} turns elided]"}] if skipped > 0 else []) + tail
        return out, total

    # inventory of player transcripts
    inv = []
    for run in all_runs:
        nodes = {n["id"]: n for n in trees[run]["nodes"]}
        for f in glob.glob(os.path.join(EXP, "runs", run, f"generate_{run}", "gen_*", "arc_eval", "agent_evals", "*.md")):
            gd = f.split("/arc_eval/")[0]
            nid = os.path.basename(gd)[4:]
            if nid not in nodes:
                continue  # aborted gen dirs etc.
            m = re.match(r"chat_history_(\w+)_(\d+)\.md$", os.path.basename(f))
            if not m:
                continue
            inv.append((run, nid, m.group(1), int(m.group(2)), f))
    preds_cache = {}

    def preds_for(run, nid):
        if (run, nid) not in preds_cache:
            p = os.path.join(gen_dir(run, nid), "arc_eval", "predictions.json")
            preds_cache[(run, nid)] = lj(p) if os.path.exists(p) else []
        return preds_cache[(run, nid)]

    # deterministic curated sample
    by_run_task = collections.defaultdict(list)
    for x in inv:
        by_run_task[(x[0], x[2], x[3])].append(x)

    def nkey(nid):
        return -1 if nid == "initial" else int(nid)

    chosen, seen = [], set()

    def take(x, why):
        k = (x[0], x[1], x[2], x[3])
        if k in seen:
            return
        seen.add(k)
        chosen.append((x, why))

    # 1) evolution series: in source_s1 and source_s2, practice tasks failing at many generations
    series_tasks = []
    for run in ("source_s1", "source_s2", "payoff_I0_2"):
        cands = sorted(((len(v), k) for k, v in by_run_task.items() if k[0] == run), reverse=True)
        picked = 0
        for cnt, k in cands:
            if picked >= 2:
                break
            # prefer tasks that the run solves at some generation (fail -> success visible)
            solved_somewhere = any(
                (n.get("practice") or {}).get("per_task", {}).get(k[1], 0) > 0 for n in trees[run]["nodes"])
            if not solved_somewhere and picked == 0 and cnt < 6:
                continue
            xs = sorted(by_run_task[k], key=lambda x: nkey(x[1]))
            step = max(1, len(xs) // 4)
            for x in xs[::step][:4]:
                take(x, f"evolution series: {run} task {k[1]} across generations")
            series_tasks.append({"run": run, "task": k[1], "test_input": k[2]})
            picked += 1
    # 2) multi-call (refinement / verification) players
    multi = [x for x in inv if re.search(r"(?m)^(Refinement|Verification) input:", open(x[4]).read())]
    multi.sort(key=lambda x: (x[0], nkey(x[1]), x[2]))
    for x in multi[:: max(1, len(multi) // 10)][:10]:
        take(x, "player uses a second model call (refine/verify)")
    # 3) error transcripts (broken player code)
    errs = [x for x in inv if open(x[4]).read().lstrip().startswith("Error:")]
    errs.sort(key=lambda x: (x[0], nkey(x[1])))
    for x in errs[:3]:
        take(x, "player crashed (agent error)")
    # 4) fill across all runs
    per_run = collections.defaultdict(list)
    for x in sorted(inv, key=lambda x: (x[0], nkey(x[1]), x[2], x[3])):
        per_run[x[0]].append(x)
    i = 0
    while len(chosen) < 60 and any(per_run.values()):
        for run in all_runs:
            lst = per_run.get(run)
            if lst:
                x = lst.pop((i * 7) % len(lst))
                take(x, "sample across runs")
                if len(chosen) >= 60:
                    break
        i += 1

    player_tx = []
    for x, why in chosen:
        run, nid, tid, ti, f = x
        text = open(f, errors="replace").read()
        segs, full = segments(text, PLAYER_TX_CAP, "player")
        pr = [p for p in preds_for(run, nid) if p["task_id"] == tid and p["test_input"] == ti]
        pr = pr[0] if pr else {}
        node = next(n for n in trees[run]["nodes"] if n["id"] == nid)
        player_tx.append({
            "kind": "player", "run": run, "node": nid, "generation": node["generation"], "task": tid,
            "test_input": ti, "task_set": trees[run]["task_set"],
            "correct": bool(pr.get("solved", False)), "n_answers": pr.get("n_answers_returned"),
            "agent_error": scrub(pr.get("agent_error")) if pr.get("agent_error") else None,
            "answers": pr.get("wrong_answers"), "why": why, "segments": segs, "full_chars": full,
        })
    # solved examples: only failed transcripts were saved by the harness; add pred-only replays of solves
    solved_pred = []
    for s in series_tasks:
        run = s["run"]
        for n in trees[run]["nodes"]:
            dd = practice_done_cache.get((run, n["id"]))
            if not dd:
                continue
            d, pre = dd
            rs = d.get(pre + (s["task"], s["test_input"]))
            if rs and any(r["correct"] for r in rs):
                solved_pred.append({
                    "kind": "pred_only", "run": run, "node": n["id"], "generation": n["generation"],
                    "task": s["task"], "test_input": s["test_input"], "task_set": trees[run]["task_set"],
                    "correct": True, "answers": [rs[0].get("pred"), rs[1].get("pred")],
                    "attempt_correct": [bool(rs[0]["correct"]), bool(rs[1]["correct"])],
                    "tokens": rs[0].get("tokens"), "calls": rs[0].get("calls"),
                    "why": "solved at this generation (no transcript is saved for solved tasks; answer grids from result rows)",
                })
    # thin to <=4 per series
    thin = []
    for s in series_tasks:
        lst = [x for x in solved_pred if x["run"] == s["run"] and x["task"] == s["task"]]
        thin += lst[:: max(1, len(lst) // 4)][:4]
    solved_pred = thin
    # a few more solved replays from varied runs (first solved test input per run, latest node)
    for run in all_runs:
        if sum(1 for x in solved_pred if x["run"] == run) >= 1 or len(solved_pred) >= 30:
            continue
        nodes_sorted = sorted([n for n in trees[run]["nodes"] if (run, n["id"]) in practice_done_cache],
                              key=lambda n: nkey(n["id"]), reverse=True)
        for n in nodes_sorted[:1]:
            d, pre = practice_done_cache[(run, n["id"])]
            for k in sorted(k for k in d if k[:4] == pre):
                rs = d[k]
                if any(r["correct"] for r in rs) and k[4] not in {x["task"] for x in solved_pred}:
                    solved_pred.append({
                        "kind": "pred_only", "run": run, "node": n["id"], "generation": n["generation"],
                        "task": k[4], "test_input": k[5], "task_set": trees[run]["task_set"], "correct": True,
                        "answers": [rs[0].get("pred"), rs[1].get("pred")],
                        "attempt_correct": [bool(rs[0]["correct"]), bool(rs[1]["correct"])],
                        "tokens": rs[0].get("tokens"), "calls": rs[0].get("calls"),
                        "why": "solved example (pred-only replay)"})
                    break

    # coach transcripts
    coach_targets = []
    for run in SOURCE_RUNS:
        g = (ig_sel.get(run, {}).get("I_g") or {}).get("gen")
        if g is not None:
            coach_targets.append((run, str(g), "I_g pick (coach transplanted into the pay-off test)"))
    for key, v in sorted(ext_picks.items()):
        if v["generation"] == 40:
            coach_targets.append((v["run"], str(v["pick"]["gen"]), f"extension pick at generation 40 ({key})"))
    jumps = []
    for run in SOURCE_RUNS:
        nodes = {n["id"]: n for n in trees[run]["nodes"]}
        for n in nodes.values():
            p = nodes.get(n["parent"]) if n["parent"] else None
            if p and n["practice_score"] is not None and p["practice_score"] is not None:
                jumps.append((n["practice_score"] - p["practice_score"], run, n["id"]))
    jumps.sort(reverse=True)
    for dlt, run, nid in jumps[:3]:
        coach_targets.append((run, nid, f"big practice-score jump (+{dlt:.2f} over parent)"))
    jumps.sort()
    coach_targets.append((jumps[0][1], jumps[0][2], f"big practice-score drop ({jumps[0][0]:+.2f} vs parent)"))
    # one pay-off coach edit for contrast
    coach_targets.append(("payoff_I0_1", final_runs["payoff_I0_1"]["final_node"], "I_0 coach edit that produced payoff_I0_1's final player"))
    coach_tx, seen_c = [], set()
    for run, nid, why in coach_targets:
        if (run, nid) in seen_c:
            for c in coach_tx:
                if (c["run"], c["node"]) == (run, nid):
                    c["why"] += "; " + why
            continue
        p = os.path.join(gen_dir(run, nid), "agent_output", "meta_agent_chat_history.md")
        if not os.path.exists(p):
            continue
        seen_c.add((run, nid))
        text = open(p, errors="replace").read()
        segs, full = segments(text, COACH_TX_CAP, "coach")
        node = next(n for n in trees[run]["nodes"] if n["id"] == nid)
        par = next((n for n in trees[run]["nodes"] if n["id"] == node["parent"]), None)
        coach_tx.append({"kind": "coach", "run": run, "node": nid, "generation": node["generation"],
                         "parent": node["parent"], "practice_score": node["practice_score"],
                         "parent_practice_score": par["practice_score"] if par else None,
                         "files_changed": node["files_changed"], "why": why, "segments": segs, "full_chars": full})
    TRIMMED.append(f"transcripts.json: player transcripts sampled {len(player_tx)} of {len(inv)} available; prompt grids elided; capped at ~{PLAYER_TX_CAP} chars")
    TRIMMED.append(f"transcripts.json: coach transcripts sampled {len(coach_tx)}; each turn clipped to 900 chars, whole transcript capped at ~{COACH_TX_CAP} chars")
    TRIMMED.append(f"trees.json: each node diff capped at {DIFF_CAP} chars (head + last 800 chars); binary (.pyc) sections omitted")

    transcripts = {"player": player_tx, "solved_replays": solved_pred, "coach": coach_tx,
                   "evolution_series": series_tasks,
                   "note": "The harness saved player transcripts only for practice-set test inputs the player FAILED; solved examples are given as pred-only replays from the result rows. The model's hidden reasoning is not in the transcripts: each Output is the visible response."}

    # ================================================================== summary.json
    spend_role = collections.defaultdict(float)
    for (ph, role), v in spend_phase_role.items():
        spend_role[role] += v
    xh_entry = next(e for e in compute["runs"] if e["run"] == "xhigh")
    summary = {
        "headline": analysis.get("headline"),
        "model": "gpt-6-luna (effort high; xhigh for the xhigh baseline)",
        "sets": {"heldout_tasks": len(HELDOUT), "heldout_test_inputs": sum(n_test(t) for t in HELDOUT),
                 "source_practice_tasks": len(SRC_SET), "payoff_practice_tasks": len(PAY_SET)},
        "B0": {"reps": analysis["B0_reps"], "mean": analysis["B0"], "sd": analysis["sd"]["B0"]},
        "xhigh": {"score": ext.get("xhigh"), "recomputed": xh_entry["score"]},
        "I0_runs": analysis["I0_runs"], "Ig_runs": analysis["Ig_runs"],
        "I0_mean": mean(analysis["I0_runs"].values()), "Ig_mean": mean(analysis["Ig_runs"].values()),
        "sd": analysis["sd"],
        "G": analysis["G"], "Delta": analysis["Delta"],
        "Ig_gain_over_B0": analysis.get("Ig_gain_over_B0"), "I0_gain_over_B0": analysis.get("I0_gain_over_B0"),
        "n_source_seeds": analysis.get("n_source_seeds"), "n_qualifying_Ig": analysis.get("n_qualifying_Ig"),
        "self_edit": analysis.get("self_edit"), "self_edit_rate": analysis.get("self_edit_rate"),
        "tokens_by_arm": analysis.get("tokens_by_arm"),
        "extension": {
            "label": ext.get("label"), "per_generation": ext.get("per_generation"), "points": ext.get("points"),
            "gen40_minus_gen0": ext.get("gen40_minus_gen0"), "paired_changes": ext.get("paired_changes"),
            "picks_changed_code": ext.get("picks_changed_code"),
        },
        "diff_audit_summary": ext.get("diff_audit_summary"),
        "spend": {
            "total": analysis.get("spend_total"), "by_role": analysis.get("spend_by_role"),
            "by_role_recomputed": {k: r4(v) for k, v in spend_role.items()},
            "by_phase_role": [{"phase": ph, "role": ro, "cost": r4(v)} for (ph, ro), v in
                              sorted(spend_phase_role.items(), key=lambda kv: -kv[1])],
        },
        "final_runs": [{k: final_runs[r][k] for k in ("run", "arm", "seed", "final_node", "heldout", "candidates", "combined")}
                       for r in PAYOFF_RUNS],
    }

    # ================================================================== write + size control
    sizes = {}
    sizes["summary.json"] = write("summary.json", summary)
    sizes["trees.json"] = write("trees.json", {"runs": SOURCE_RUNS + PAYOFF_RUNS, "trees": trees})
    sizes["compute.json"] = write("compute.json", compute)
    sizes["tasks.json"] = write("tasks.json", {"heldout": HELDOUT, "source": SRC_SET, "payoff": PAY_SET, "tasks": tasks})
    sizes["heldout.json"] = write("heldout.json", heldout)
    sizes["transcripts.json"] = write("transcripts.json", transcripts)
    total = sum(sizes.values())
    while total > SIZE_BUDGET - 64 * 1024 and any(heldout["runs"][r]["has_preds"] for r in heldout["runs"]):
        rid = [r for r in priority if heldout["runs"][r]["has_preds"]][-1]
        heldout["runs"][rid]["has_preds"] = False
        for lst in heldout["runs"][rid]["results"].values():
            for rec in lst:
                if rec:
                    rec.pop("p", None)
        TRIMMED.append(f"heldout.json: additionally dropped preds for {rid} to fit the size budget")
        sizes["heldout.json"] = write("heldout.json", heldout)
        total = sum(sizes.values())

    manifest = {
        "generated_by": "arcexp/build_explorer_data.py",
        "sources": ["exp/results/*.json(l)", "exp/runs/<run>/{gen_scores,meta_steps}.jsonl", "exp/archive_export/<run>/nodes.json",
                    "exp/runs/<run>/generate_<run>/gen_<k>/{agent_output,arc_eval}", "exp/ledger/calls.jsonl", "splits.json",
                    "ARC-AGI-2 task JSON (evaluation + training)"],
        "sizes_bytes": sizes, "total_bytes": total, "budget_bytes": SIZE_BUDGET,
        "trimmed": TRIMMED,
        "redactions": dict(REDACTIONS),
        "excluded": ["gateway call tokens ('token' in meta_steps.jsonl / ledger) are never copied",
                     "ledger rows are aggregated, never copied"],
        "heldout_preds_kept_for": [r for r in heldout["runs"] if heldout["runs"][r]["has_preds"]],
        "files": FIELD_DOCS,
        "sanity": {"heldout_score_recomputed_vs_reported": score_check,
                   "practice_score_mismatches_gt_0.011": mism},
    }
    sizes["manifest.json"] = write("manifest.json", manifest)

    # ------------------------------------------------------------------ sanity print
    print("== sizes")
    for k, v in sizes.items():
        print(f"  {k:18s} {v/1024:9.1f} KB")
    print(f"  TOTAL {sum(sizes.values())/1024/1024:.2f} MB (budget 9 MB)")
    print("== heldout score check (run, recomputed, reported)")
    bad = [x for x in score_check if x[2] is not None and abs(x[1] - x[2]) > 0.002]
    for x in score_check:
        print("  ", x, "MISMATCH" if x in bad else "")
    print("== practice-score mismatches (loop vs recomputed):", len(mism), mism[:8])
    print("== trees:", {r: len(t["nodes"]) for r, t in trees.items()})
    print("== transcripts: player", len(player_tx), "solved replays", len(solved_pred), "coach", len(coach_tx))
    print("== tasks:", len(tasks), "heldout preds kept for", manifest["heldout_preds_kept_for"])
    print("== redactions:", dict(REDACTIONS))
    print("== trimmed:", *TRIMMED, sep="\n   ")


FIELD_DOCS = {
    "summary.json": {
        "headline": "one-line verdict from analysis.json",
        "sets": "sizes of the held-out exam and the two practice sets",
        "B0": "A_0 with two plain attempts on the held-out exam: reps (list of scores), mean, sd",
        "xhigh": "A_0 at xhigh effort: score as reported in ext_analysis.json and as recomputed from xhigh.jsonl",
        "I0_runs / Ig_runs": "held-out score of the final player of each pay-off run (I0 = original coach, Ig = evolved coach)",
        "G": "I0 mean minus B0 mean with Welch CI {est, lo, hi, df}",
        "Delta": "Ig mean minus I0 mean with Welch CI",
        "extension.per_generation": "{gen: {n, mean, lo, hi, scores}} for coaches picked at generation 0/12/20/40 (DESIGN_v2 extension)",
        "extension.points": "one point per test run: {generation, seed_index, heldout, run}",
        "spend": "USD: total and by role from analysis.json; by_phase_role recomputed from the ledger",
        "final_runs": "per pay-off/extension run: final_node, held-out score, finalist candidates and combined (loop+rescore)/2 scores",
        "scores": "all scores are fractions in [0,1] (task-averaged pass@2)",
    },
    "trees.json": {
        "runs": "ordered list of run ids",
        "trees[run].kind": "source | payoff_I0 | payoff_Ig | extension_test",
        "trees[run].arm/seed": "arm and seed as they appear in the result rows",
        "trees[run].task_set": "practice set the loop scored on: source (25 tasks) or payoff (25 tasks)",
        "trees[run].frozen_paths": "paths the coach could not change (non-empty for pay-off runs: frozen coach)",
        "trees[run].coach_origin": "for pay-off/extension runs: which source node the frozen coach came from, the selection rule, source_lineage {depth, cum_meta_tokens, cum_meta_calls, cum_meta_cost} of that coach, and its practice score",
        "trees[run].final": "final player selection: final_node, candidates, combined scores, held-out score",
        "trees[run].diff_audit": "audited coach-edit hunks for picks from this source run: {pick, file, idx, tag: general|ARC-specific, agreement, reason}",
        "node.id": "'initial' or generation number as string",
        "node.generation": "same as id ('initial' or int)",
        "node.parent / children": "tree edges (string ids)",
        "node.practice_score": "loop_score_on_set from nodes.json (practice-set score the loop saw; null = not evaluated/invalid)",
        "node.valid": "valid_parent flag (could be selected as a parent)",
        "node.files_changed": "files in this generation's model_patch.diff: {path, role: coach|player|other, added, removed, binary}. coach = meta_agent.py, run_meta_agent.py, agent/**, tests/test_meta_agent*; player = task_agent.py, run_task_agent.py, domains/**, tests/test_task_agent*; other = pyc, .gitignore, generate_loop.py, utils/**, stray files",
        "node.touched_coach / touched_player": "booleans derived from files_changed",
        "node.coach_files_changed_vs_I0": "from nodes.json: coach files that differ from I_0 in this node's code (cumulative), null if unknown",
        "node.diff": "the coach's edit (unified diff) for this generation, binary sections removed, capped ~6 KB; diff_truncated / diff_full_chars tell if/how much was cut",
        "node.meta": "coach work in the step that produced this node (meta_steps.jsonl): {calls, tokens, seconds, rc, ledger_cost}; null for 'initial'",
        "node.lineage": "{depth, cum_meta_tokens, cum_meta_calls, cum_meta_cost}: coach compute summed over this node and all its ancestors",
        "node.practice": "player rollouts on the practice set for this node's code: {recomputed_score, n_test_inputs_run, tokens_per_test_input, calls_per_test_input, seconds_per_test_input, per_task: {task: fraction of test inputs solved}}; null if no rows",
        "node.is_Ig_pick": "this source node is the I_g coach used in payoff_Ig_source_sN",
        "node.ext_pick_at": "list like ['g20','g40']: extension pick labels that chose this node's coach",
        "node.is_final_player / final_candidate / rescore_combined / heldout_score": "pay-off runs: whether this node is the final player (took the exam), a finalist, its (loop+rescore)/2 score, and its held-out score",
    },
    "compute.json": {
        "runs[]": "one entry per held-out evaluation: B0_rep0..2, xhigh, and every pay-off/extension final player",
        "run/label/group": "id, human label, group B0|xhigh|I0|Ig|g20|g40",
        "generation": "coach generation (I0=0, Ig=12, g20=20, g40=40; null for baselines)",
        "score / reported_score": "recomputed and officially reported held-out score",
        "tokens_per_test_input / calls_per_test_input / seconds_per_test_input": "mean player test-time compute per test input",
        "score_per_10k_tokens": "score divided by tokens_per_test_input, x 1e4",
        "heldout_eval_cost": "USD from the ledger for this held-out evaluation",
        "improvement_cost": "pay-off runs: compute spent to produce the final player (see notes)",
        "final_player_lineage": "lineage compute of the final player node inside its pay-off run",
        "notes": "definitions",
    },
    "tasks.json": {
        "heldout/source/payoff": "task id lists",
        "tasks[id]": "{id, set: heldout|source|payoff, arc_split, train: [{input, output}], test: [{input, output}], heldout_mean_solve (held-out only: mean task score over all held-out runs)}; grids are int arrays (0-9 colours)",
    },
    "heldout.json": {
        "task_order": "the 120 held-out task ids",
        "n_test_inputs": "{task: number of test inputs}",
        "runs[run]": "{label, group, score, has_preds, per_task: {task: score}, results: {task: [per test input record or null]}}",
        "record.c": "[attempt1_correct, attempt2_correct] as 0/1; the test input counts as solved if either is 1",
        "record.n / tok / calls / sec": "answers returned, player tokens, model calls, seconds for this test input",
        "record.timeout / err": "present only when the player timed out / raised an error",
        "record.p": "only when has_preds: [pred_attempt1, pred_attempt2]; a grid (int array) or null (no answer); '=1' means attempt 2 equals attempt 1",
    },
    "transcripts.json": {
        "player[]": "{kind:'player', run, node, generation, task, test_input, task_set, correct, n_answers, agent_error, answers (wrong answer grids the player returned), why (selection reason), segments: [{role: Input|Output|Refinement input|...|Error|Elided, text}], full_chars}",
        "solved_replays[]": "{kind:'pred_only', run, node, generation, task, test_input, task_set, correct:true, answers:[grid,grid], attempt_correct, tokens, calls, why}",
        "coach[]": "{kind:'coach', run, node, generation, parent, practice_score, parent_practice_score, files_changed, why, segments: [{role: Input|Output|Tool output|Nudge|Elided, text}], full_chars}",
        "evolution_series[]": "{run, task, test_input}: tasks whose transcripts are included at several generations of the same run",
        "note": "caveats",
    },
}


if __name__ == "__main__":
    main()
