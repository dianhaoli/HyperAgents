"""Fixed per-test-input runner (installed read-only at /opt/arc_runner; not agent-editable).

Runs inside the sandbox with cwd=/tmp/task, which holds ONLY this task's example pairs and
this one test input (task.json). Loads TaskAgent from /hyperagents/task_agent.py, calls
forward(inputs) and writes the returned answers to /tmp/task/answer.json. The host takes at most
the first 2 valid grids and scores them outside the sandbox.
"""
import argparse
import importlib.util
import json
import os
import sys
import traceback


def normalize(pred):
    if isinstance(pred, str):
        s = pred.strip()
        try:
            pred = json.loads(s)
        except Exception:
            return []
    if isinstance(pred, tuple):
        pred = list(pred)
    if isinstance(pred, list) and pred and isinstance(pred[0], list) and pred[0] and isinstance(pred[0][0], int):
        return [pred]  # a single grid
    if isinstance(pred, list):
        out = []
        for p in pred:
            if isinstance(p, str):
                try:
                    p = json.loads(p)
                except Exception:
                    continue
            out.append(p)
        return out
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", default="/hyperagents/task_agent.py")
    ap.add_argument("--task", default="/tmp/task/task.json")
    ap.add_argument("--out", default="/tmp/task/answer.json")
    ap.add_argument("--single", action="store_true", help="screen mode: one direct call (A_0.solve_once)")
    a = ap.parse_args()
    res = {"answers": [], "error": None, "raw": None}
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(a.agent)))
        with open(a.task) as f:
            task = json.load(f)
        inputs = {"domain": "arc", "train": task["train"], "test_input": task["test_input"]}
        spec = importlib.util.spec_from_file_location("task_agent", a.agent)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        agent = mod.TaskAgent(model="gpt-6-luna", chat_history_file="/tmp/task/chat_history.md")
        if a.single:
            pred = [agent.solve_once(inputs)]
        else:
            out = agent.forward(inputs)
            pred = out[0] if isinstance(out, tuple) else out
        res["raw"] = repr(pred)[:20000]
        res["answers"] = normalize(pred)
    except BaseException as e:  # noqa
        res["error"] = "".join(traceback.format_exception(type(e), e, e.__traceback__))[-4000:]
    try:
        with open(a.out, "w") as f:
            json.dump(res, f)
    except Exception:
        print(json.dumps(res))


if __name__ == "__main__":
    main()
