"""Host-side evaluation of a task agent on a set of ARC tasks.

Every test input runs in its own sandbox (see sandbox.py) with its own gateway token (cap: 2 model
calls). Scoring happens here, on the host, against private ground truth. Results are appended to a
JSONL keyed by (phase, arm, seed, iteration, task, test_input, attempt); finished keys are skipped
(only if the agent code hash matches, so a rerun iteration with different code is re-evaluated).
"""
import json
import os
import re
import shutil
import time
import uuid
from concurrent.futures import ThreadPoolExecutor

from arcexp import arc_data
from arcexp.common import EXP, RUNNER_DIR, append_jsonl, chown_agent, read_jsonl, register_token, token_info, tree_hash
from arcexp.sandbox import run_sandboxed

STAGE = os.path.join(EXP, "stage")
TEST_INPUT_TIMEOUT = 1800  # whole forward() for one test input (two high-effort calls); code exec has its own 30 s budget
INFRA_MARKERS = ("upstream error", "upstream failed", "GLOBAL BUDGET", "ConnectionRefused", "FileNotFoundError: [Errno 2] No such file or directory: '/run/arcgw")


def results_path(phase):
    return os.path.join(EXP, "results", f"{phase}.jsonl")


def _key(r):
    return (r["phase"], r["arm"], str(r["seed"]), str(r["iteration"]), r["task"], int(r["test_input"]))


def load_done(phase, code_hash=None):
    done = {}
    for r in read_jsonl(results_path(phase)):
        if r.get("infra_error"):
            continue
        if code_hash is not None and r.get("code_hash") != code_hash:
            continue
        done.setdefault(_key(r), []).append(r)
    return {k: v for k, v in done.items() if len(v) >= 2}


def run_test_input(workspace, scope, tid, ti, code_hash, single=False, effort_role=None):
    sid = uuid.uuid4().hex[:12]
    stage = os.path.join(STAGE, sid)
    os.makedirs(stage)
    with open(os.path.join(stage, "task.json"), "w") as f:
        json.dump(arc_data.task_input_for(tid, ti), f)
    chown_agent(stage)
    tok_scope = dict(scope, task=tid, test_input=ti)
    tok = register_token("task", tok_scope, effort_role=effort_role)
    cmd = ["python3", os.path.join(RUNNER_DIR, "run_one.py")] + (["--single"] if single else [])
    t0 = time.time()
    rc, out = run_sandboxed(cmd, binds=[(workspace, "/hyperagents", True), (stage, "/tmp/task", False)],
                            cwd="/tmp/task", env_extra={"GW_TOKEN": tok}, timeout=TEST_INPUT_TIMEOUT)
    dur = time.time() - t0
    res = {"answers": [], "error": None, "raw": None}
    ap = os.path.join(stage, "answer.json")
    if os.path.exists(ap):
        try:
            with open(ap) as f:
                res = json.load(f)
        except Exception as e:
            res["error"] = f"unreadable answer.json: {e}"
    else:
        res["error"] = f"no answer.json (rc={rc}): {out.decode(errors='replace')[-1500:]}"
    chat = ""
    cp = os.path.join(stage, "chat_history.md")
    if os.path.exists(cp):
        try:
            with open(cp, errors="replace") as f:
                chat = f.read()[-60000:]
        except Exception:
            pass
    shutil.rmtree(stage, ignore_errors=True)
    info = {}
    try:
        info = token_info(tok)
    except Exception:
        pass
    calls = info.get("calls", 0)
    err = res.get("error") or ""
    infra = bool(err) and any(m in err for m in INFRA_MARKERS) or (rc == 124 and calls == 0)
    answers = [a for a in (res.get("answers") or []) if arc_data.valid_grid(a)][:2]
    truth = arc_data.truth(tid, ti)
    recs = []
    for a in range(2):
        pred = answers[a] if a < len(answers) else None
        recs.append(dict(scope, task=tid, test_input=ti, attempt=a + 1, code_hash=code_hash,
                         pred=pred, correct=(pred == truth), n_answers=len(answers),
                         agent_error=(err[-1500:] if err else None), infra_error=infra,
                         timeout=(rc == 124), calls=calls, tokens=info.get("tokens_used", 0), dur=round(dur, 1),
                         ts=time.time()))
    return recs, chat


def evaluate_set(workspace, task_ids, scope, workers=16, single=False, effort_role=None,
                 visible_dir=None, retries=1, code_hash=None, log=print):
    """scope: dict with phase, arm, seed, iteration (+ anything else). Returns summary dict."""
    phase = scope["phase"]
    code_hash = code_hash or tree_hash(workspace)
    path = results_path(phase)
    jobs = [(tid, ti) for tid in task_ids for ti in range(arc_data.n_test(tid))]
    chats = {}

    def key_of(tid, ti):
        return (phase, scope["arm"], str(scope["seed"]), str(scope["iteration"]), tid, ti)

    for attempt_round in range(retries + 1):
        done = load_done(phase, code_hash)
        todo = [(tid, ti) for tid, ti in jobs if key_of(tid, ti) not in done]
        if not todo:
            break
        log(f"[eval] {scope} round {attempt_round}: {len(todo)} test inputs to run ({len(jobs)-len(todo)} cached)")

        def work(j):
            tid, ti = j
            try:
                recs, chat = run_test_input(workspace, scope, tid, ti, code_hash, single=single, effort_role=effort_role)
            except Exception as e:
                recs = [dict(scope, task=tid, test_input=ti, attempt=a + 1, code_hash=code_hash, pred=None,
                             correct=False, infra_error=True, agent_error=f"host error: {e}", ts=time.time())
                        for a in range(2)]
                chat = ""
            for r in recs:
                append_jsonl(path, r)
            chats[(tid, ti)] = chat
            return recs

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, todo))

    done = load_done(phase, code_hash)
    all_recs = read_jsonl(path)
    n_infra = sum(1 for r in all_recs if r.get("infra_error") and r.get("code_hash") == code_hash
                  and _key(r)[:4] == key_of("", 0)[:4] and r["attempt"] == 1)
    per_ti = {}
    missing = 0
    for tid, ti in jobs:
        rs = done.get(key_of(tid, ti))
        if rs is None:
            missing += 1
            per_ti[(tid, ti)] = None
        else:
            per_ti[(tid, ti)] = any(r["correct"] for r in rs)
    per_task = {}
    for tid in task_ids:
        vals = [per_ti[(tid, ti)] for ti in range(arc_data.n_test(tid))]
        vals = [bool(v) for v in vals]  # missing (infra failure after retries) counts as unsolved
        per_task[tid] = sum(vals) / len(vals)
    score = sum(per_task.values()) / len(per_task) if per_task else 0.0
    summary = {"score": score, "per_task": per_task, "n_test_inputs": len(jobs), "missing": missing,
               "infra_error_rows": n_infra, "code_hash": code_hash,
               "format_failures": sum(1 for k, rs in done.items() if k[:4] == key_of("", 0)[:4] and rs[0].get("n_answers", 0) == 0)}
    if visible_dir:
        write_visible(visible_dir, task_ids, per_task, per_ti, done, key_of, chats)
    return summary


def _grid_strings(g):
    yield json.dumps(g)
    yield json.dumps(g, separators=(",", ":"))
    yield "\n".join(" ".join(str(v) for v in r) for r in g)
    yield "\n".join("".join(str(v) for v in r) for r in g)


def redact(text, truths):
    for g in truths:
        for s in _grid_strings(g):
            if len(s) >= 5 and s in text:
                text = text.replace(s, "[REDACTED]")
    return text


def write_visible(visible_dir, task_ids, per_task, per_ti, done, key_of, chats):
    """Agent-visible results: scores, wrong answers, and chat logs of unsolved test inputs only."""
    os.makedirs(os.path.join(visible_dir, "agent_evals"), exist_ok=True)
    details = []
    for tid in task_ids:
        truths = [arc_data.truth(tid, i) for i in range(arc_data.n_test(tid))]
        for ti in range(arc_data.n_test(tid)):
            rs = done.get(key_of(tid, ti)) or []
            solved = bool(per_ti.get((tid, ti)))
            item = {"task_id": tid, "test_input": ti, "solved": solved,
                    "n_answers_returned": rs[0].get("n_answers") if rs else None,
                    "agent_error": (rs[0].get("agent_error") or None) if rs else "not evaluated"}
            if not solved:
                item["wrong_answers"] = [r["pred"] for r in rs if r.get("pred") is not None and r["pred"] not in truths]
                chat = chats.get((tid, ti))
                if chat:
                    with open(os.path.join(visible_dir, "agent_evals", f"chat_history_{tid}_{ti}.md"), "w") as f:
                        f.write(redact(chat, truths))
            details.append(item)
    report = {"overall_accuracy": sum(per_task.values()) / max(1, len(per_task)),
              "total": len(per_task), "total_test_inputs": len(details),
              "per_task_score": per_task,
              "question_ids_passed": [t for t, s in per_task.items() if s == 1.0],
              "question_ids_failed": [t for t, s in per_task.items() if s < 1.0]}
    with open(os.path.join(visible_dir, "report.json"), "w") as f:
        json.dump(report, f, indent=2)
    with open(os.path.join(visible_dir, "predictions.json"), "w") as f:
        json.dump(details, f)
