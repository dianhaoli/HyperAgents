"""Answer-isolation check. Run before each phase; exits non-zero on any failure.

1. As the agent user, inside the same sandbox agents run in: the private stores (/opt/arc_private,
   /home/user, /root) and the gateway admin socket must be unreadable, and the network must be down.
2. As the agent user: every file readable on the filesystem outside system dirs is scanned for any
   test output (and any held-out task grid).
3. On the host: every agent-visible tree (agent template, transplant dirs, every run's workspace, the
   run output folders that are copied to the meta agent, sandbox /tmp dirs, initial evals, staging,
   /opt/arc_runner) is scanned for any test output (JSON, compact JSON, digit rows) and held-out grid.
"""
import glob
import json
import os
import sys

from arcexp import arc_data
from arcexp.common import EXP, REPO, RUNNER_DIR
from arcexp.sandbox import run_sandboxed

MAX_FILE = 5_000_000


def grid_forms(g, rows_ok=True):
    yield json.dumps(g)
    yield json.dumps(g, separators=(",", ":"))
    if rows_ok and len(g) >= 3:
        yield "\n".join(" ".join(str(v) for v in r) for r in g)
        yield "\n".join("".join(str(v) for v in r) for r in g)


def build_patterns():
    s = json.load(open(os.path.join(REPO, "splits.json")))
    used = set(s.get("heldout", [])) | set(s.get("screen", [])) | set(s.get("smoke", [])) | set(s.get("source", [])) | set(s.get("payoff", []))
    pats = {}
    for tid in sorted(used):
        t = arc_data.load_task(arc_data.split_of(tid), tid)
        visible = [p["input"] for p in t["train"]] + [p["output"] for p in t["train"]] + [x["input"] for x in t["test"]]
        for i, x in enumerate(t["test"]):
            g = x["output"]
            if sum(len(r) for r in g) < 6 or g in visible:
                continue
            for f in grid_forms(g, rows_ok=sum(len(r) for r in g) >= 9):
                pats[f] = f"test output {tid}[{i}]"
    for tid in s.get("heldout", []):  # held-out task files must never be agent-visible either
        t = arc_data.load_task("evaluation", tid)
        for j, p in enumerate(t["train"]):
            g = p["input"]
            if sum(len(r) for r in g) >= 16:
                pats[json.dumps(g)] = f"held-out grid {tid} train[{j}]"
    return pats


SCANNER = r'''
import os, sys, json
pats = json.load(open(sys.argv[1]))
skip = ("/proc", "/sys", "/dev/pts", "/usr", "/lib", "/lib64", "/lib32", "/bin", "/sbin", "/boot", "/var/lib", "/snap", "/etc", "/var/cache", "/var/log", "/tmp/scan")
hits = []; n = 0
for root, dns, fns in os.walk("/", onerror=lambda e: None):
    if root.startswith(skip) and root != "/":
        dns[:] = []; continue
    for fn in fns:
        p = os.path.join(root, fn)
        try:
            if not os.path.isfile(p) or os.path.getsize(p) > 5000000: continue
            txt = open(p, errors="ignore").read()
        except Exception:
            continue
        n += 1
        for k, v in pats.items():
            if k in txt:
                hits.append([p, v]); break
print(json.dumps({"files": n, "hits": hits}))
'''

PROBE = r'''
import os, json, socket, subprocess
res = {}
for p in ["/opt/arc_private", "/opt/arc_private/ARC-AGI-2/data/evaluation", "/home/user", "/home/user/HyperAgents", "/root"]:
    try:
        os.listdir(p); res[p] = "READABLE"
    except Exception as e:
        res[p] = "blocked"
try:
    s = socket.socket(socket.AF_UNIX); s.connect("/run/arcgw/admin.sock"); res["admin.sock"] = "READABLE"
except Exception:
    res["admin.sock"] = "blocked"
try:
    socket.create_connection(("1.1.1.1", 443), timeout=3); res["net"] = "UP"
except Exception:
    res["net"] = "down"
res["env_proxy"] = [k for k in os.environ if "proxy" in k.lower()]
print(json.dumps(res))
'''


def scan_tree(root, pats, hits, counter):
    from arcexp.safeio import safe_read_text
    for dp, dns, fns in os.walk(root, followlinks=False):
        # .git is scanned too (agents could stash files there); packed/loose objects are zlib-compressed
        dns[:] = [d for d in dns if not (os.path.basename(dp) == ".git" and d == "objects")]
        for fn in fns:
            p = os.path.join(dp, fn)
            txt = safe_read_text(p, MAX_FILE)
            if txt is None:
                continue
            counter[0] += 1
            for k, v in pats.items():
                if k in txt:
                    hits.append((p, v))
                    break


def agent_visible_roots():
    roots = [os.path.join(REPO, "agent_template"), RUNNER_DIR, os.path.join(REPO, "outputs"),
             os.path.join(EXP, "initial"), os.path.join(EXP, "stage"), os.path.join(EXP, "transplants"),
             "/dev/shm", "/var/tmp", "/run/lock", "/var/lib/php/sessions"]
    for d in glob.glob(os.path.join(EXP, "runs", "*")):
        for sub in os.listdir(d):
            if sub.startswith("generate_") or sub in ("_ctmp", "_evalcode", "final_agents", "nodes"):
                roots.append(os.path.join(d, sub))
    return [r for r in roots if os.path.exists(r)]


def main():
    pats = build_patterns()
    ok = True
    report = {"n_patterns": len(pats)}
    # 1. probes as the agent user in the sandbox
    rc, out = run_sandboxed(["python3", "-c", PROBE], binds=[], timeout=120)
    probe = json.loads(out.decode().strip().splitlines()[-1])
    report["probe"] = probe
    if any(v in ("READABLE", "UP") for v in probe.values()) or probe.get("env_proxy"):
        ok = False
    # 2. filesystem scan as the agent user
    pf = os.path.join(EXP, "stage", "_isocheck_patterns.json")
    os.makedirs(os.path.dirname(pf), exist_ok=True)
    scan_dir = os.path.join(EXP, "stage", "_isoscan")
    os.makedirs(scan_dir, exist_ok=True)
    json.dump(pats, open(os.path.join(scan_dir, "p.json"), "w"))
    os.chmod(scan_dir, 0o755); os.chmod(os.path.join(scan_dir, "p.json"), 0o644)
    rc, out = run_sandboxed(["python3", "-c", SCANNER, "/tmp/scan/p.json"], binds=[(scan_dir, "/tmp/scan", True)], timeout=1200)
    try:
        fs = json.loads(out.decode().strip().splitlines()[-1])
    except Exception:
        fs = {"error": out.decode()[-2000:]}
        ok = False
    import shutil
    shutil.rmtree(scan_dir, ignore_errors=True)
    report["agent_fs_scan"] = fs
    if fs.get("hits"):
        ok = False
    # 3. host-side scan of every agent-visible tree
    hits, counter = [], [0]
    roots = agent_visible_roots()
    for r in roots:
        scan_tree(r, pats, hits, counter)
    report["visible_roots"] = roots
    report["visible_files_scanned"] = counter[0]
    report["visible_hits"] = hits[:50]
    if hits:
        ok = False
    report["PASS"] = ok
    os.makedirs(os.path.join(EXP, "logs"), exist_ok=True)
    with open(os.path.join(EXP, "logs", "isolation_checks.jsonl"), "a") as f:
        import time
        f.write(json.dumps({"ts": time.time(), "phase": sys.argv[1] if len(sys.argv) > 1 else "", **{k: v for k, v in report.items() if k != "visible_roots"}}) + "\n")
    print(json.dumps({k: v for k, v in report.items()}, indent=1)[:4000])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
