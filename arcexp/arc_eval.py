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
from arcexp.common import EXP, RUNNER_DIR, append_jsonl, chown_agent, gw_status, read_jsonl, register_token, revoke_token, tree_hash
from arcexp.safeio import safe_read_text
from arcexp.sandbox import run_sandboxed

STAGE = os.path.join(EXP, "stage")
TEST_INPUT_TIMEOUT = 1800  # whole forward() for one test input (two high-effort calls); code exec has its own 30 s budget


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
        slot = done.setdefault(_key(r), {})
        slot.setdefault(r["attempt"], r)  # first complete execution wins; duplicates never add attempts
    return {k: [v[1], v[2]] for k, v in done.items() if 1 in v and 2 in v}


class HostInfraError(Exception):
    pass


def run_test_input(workspace, scope, tid, ti, code_hash, single=False, effort_role=None):
    sid = uuid.uuid4().hex[:12]
    stage = os.path.join(STAGE, sid)
    os.makedirs(stage)
    with open(os.path.join(stage, "task.json"), "w") as f:
        json.dump(arc_data.task_input_for(tid, ti), f)
    chown_agent(stage)
    tok_scope = dict(scope, task=tid, test_input=ti)
    try:
        tok = register_token("task", tok_scope, effort_role=effort_role)
    except Exception as e:  # nothing ran yet: infrastructure
        shutil.rmtree(stage, ignore_errors=True)
        raise HostInfraError(f"token registration failed: {e}")
    cmd = ["python3", os.path.join(RUNNER_DIR, "run_one.py")] + (["--single"] if single else [])
    t0 = time.time()
    try:
        rc, out = run_sandboxed(cmd, binds=[(workspace, "/hyperagents", True), (stage, "/tmp/task", False)],
                                cwd="/tmp/task", env_extra={"GW_TOKEN": tok}, timeout=TEST_INPUT_TIMEOUT)
    finally:
        try:
            info = revoke_token(tok)  # the sandbox is gone; its token must never work again
        except Exception:
            info = None
    dur = time.time() - t0
    if info is None:
        shutil.rmtree(stage, ignore_errors=True)
        raise HostInfraError("gateway unreachable after the sandbox ran")
    # agent-controlled files: read without following links / opening special files
    res = {"answers": [], "error": None}
    raw = safe_read_text(os.path.join(stage, "answer.json"), 20_000_000)
    if raw is None:
        res["error"] = f"no readable answer.json (rc={rc}): {out.decode(errors='replace')[-1500:]}"
    else:
        try:
            d = json.loads(raw)
            if not isinstance(d, dict):
                raise ValueError("answer.json is not an object")
            res["answers"] = d.get("answers") if isinstance(d.get("answers"), list) else []
            res["error"] = d.get("error") if isinstance(d.get("error"), str) else (None if d.get("error") is None else str(d.get("error")))
        except Exception as e:
            res["error"] = f"malformed answer.json: {e}"
    chat = safe_read_text(os.path.join(stage, "chat_history.md"), 5_000_000) or ""
    chat = chat[-60000:]
    shutil.rmtree(stage, ignore_errors=True)
    calls = info.get("calls", 0)
    billed_ok = calls - info.get("possibly_billed_failures", 0)
    # infrastructure failure = gateway-side facts only (never agent-controlled text or exit codes)
    infra = bool(info.get("upstream_errors", 0) or info.get("refused_global", 0) or info.get("refused_after_restart", 0)) \
        and billed_ok < (1 if single else 2)
    err = res.get("error") or ""
    answers = [a for a in (res.get("answers") or []) if arc_data.valid_grid(a)][:2]
    truth = arc_data.truth(tid, ti)
    recs = []
    for a in range(2):
        pred = answers[a] if a < len(answers) else None
        recs.append(dict(scope, task=tid, test_input=ti, attempt=a + 1, code_hash=code_hash,
                         pred=pred, correct=(pred == truth), n_answers=len(answers),
                         agent_error=(err[-1500:] if err else None), infra_error=infra,
                         timeout=(rc == 124), calls=calls, tokens=info.get("tokens_used", 0),
                         upstream_errors=info.get("upstream_errors", 0), dur=round(dur, 1), ts=time.time()))
    return recs, chat


def evaluate_set(workspace, task_ids, scope, workers=16, single=False, effort_role=None,
                 visible_dir=None, retries=4, code_hash=None, log=print):
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
        if attempt_round > 0:
            time.sleep(min(600, 30 * 2 ** (attempt_round - 1)))
            try:
                gw_status()
            except Exception:
                time.sleep(120)
        log(f"[eval] {scope} round {attempt_round}: {len(todo)} test inputs to run ({len(jobs)-len(todo)} cached)")

        def work(j):
            tid, ti = j
            try:
                recs, chat = run_test_input(workspace, scope, tid, ti, code_hash, single=single, effort_role=effort_role)
            except HostInfraError as e:
                recs = [dict(scope, task=tid, test_input=ti, attempt=a + 1, code_hash=code_hash, pred=None,
                             correct=False, infra_error=True, agent_error=f"host infra error: {e}", ts=time.time())
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


def contains_truth(text, truths):
    """True if any true grid appears in the text in any serialization (digits in row-major order,
    ignoring every non-digit character)."""
    if not text:
        return False
    digits = re.sub(r"\D", "", text)
    for g in truths:
        flat = "".join(str(v) for r in g for v in r)
        if len(flat) >= 4 and flat in digits:
            return True
    return False


def withhold(text, truths):
    return "[withheld: contains a sequence equal to a true output]" if contains_truth(text, truths) else text


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
                    "agent_error": withhold((rs[0].get("agent_error") or None), truths) if rs else "not evaluated"}
            if not solved:
                item["wrong_answers"] = [r["pred"] if not contains_truth(json.dumps(r["pred"]), truths) else "[withheld]"
                                         for r in rs if r.get("pred") is not None and r["pred"] not in truths]
                chat = chats.get((tid, ti))
                if chat:
                    with open(os.path.join(visible_dir, "agent_evals", f"chat_history_{tid}_{ti}.md"), "w") as f:
                        f.write(withhold(chat, truths))
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
