"""Code-execution sandbox helper for task agents (installed read-only at /opt/arc_runner, on PYTHONPATH).

Task agents may run model-written code with:
    from arc_sandbox import run_python
    result = run_python(code_string, stdin_text="")   # -> dict(returncode, stdout, stderr, timed_out)

Guarantees: no network (the whole task-agent process already runs in a network-less namespace),
a fresh temp directory holding only this task's example pairs and test input (task.json), and a
wall-clock budget of 30 seconds per test input in total across all run_python calls.
"""
import os
import shutil
import subprocess
import tempfile
import time

TOTAL_BUDGET_S = 30.0
_used = {"s": 0.0}


def remaining_seconds():
    return max(0.0, TOTAL_BUDGET_S - _used["s"])


def run_python(code, stdin_text="", timeout=None):
    left = remaining_seconds()
    if left <= 0:
        return {"returncode": None, "stdout": "", "stderr": "code-execution budget (30s per test input) exhausted", "timed_out": True}
    t = left if timeout is None else min(timeout, left)
    d = tempfile.mkdtemp(prefix="arcsbx_")
    try:
        src = "/tmp/task/task.json"
        if os.path.exists(src):
            shutil.copy(src, os.path.join(d, "task.json"))
        with open(os.path.join(d, "main.py"), "w") as f:
            f.write(code)
        env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": d, "LANG": "C.UTF-8"}
        t0 = time.time()
        try:
            p = subprocess.run(["python3", "-I", "main.py"], cwd=d, input=stdin_text, capture_output=True,
                               text=True, timeout=t, env=env)
            out = {"returncode": p.returncode, "stdout": p.stdout[-100000:], "stderr": p.stderr[-20000:], "timed_out": False}
        except subprocess.TimeoutExpired as e:
            out = {"returncode": None, "stdout": (e.stdout or "")[-100000:] if isinstance(e.stdout, str) else "",
                   "stderr": "timed out", "timed_out": True}
        _used["s"] += time.time() - t0
        return out
    finally:
        shutil.rmtree(d, ignore_errors=True)
