"""Run the repo's generate_loop (unchanged algorithm) on the ARC-AGI-2 domain, without Docker.

Docker "containers" are replaced by LocalContainer. Each container gets a FRESH workspace: a clone of the
run's root-owned pristine repo (gen_initial/hyperagents, never writable by agents), plus a fresh /tmp dir.
Every command runs in a network-less, unprivileged namespace sandbox (sandbox.py), with the workspace at
/hyperagents. Root never runs git in, follows links in, or opens special files in agent-writable trees
(safeio.py). The only other substitution is eval_produced_agent: the produced agent's code is snapshotted
(regular files only) and evaluated host-side, one sandbox per test input, scored against private ground
truth that never enters any agent environment.

Usage: python -m arcexp.run_loop --config exp/runs/<name>/config.json   (resumes automatically)
"""
import argparse
import json
import os
import re
import shlex
import shutil
import stat
import subprocess
import sys
import time
import uuid

from arcexp import arc_data
from arcexp.arc_eval import evaluate_set
from arcexp.common import EXP, REPO, AGENT_UID, AGENT_GID, append_jsonl, chown_agent, gw_status, register_token, revoke_token
from arcexp.safeio import extract_snapshot, inside, lchown_tree, safe_copyfile, safe_copytree, snapshot_tree
from arcexp.sandbox import run_sandboxed

os.chdir(REPO)
sys.path.insert(0, REPO)

import generate_loop as GL  # noqa: E402
import utils.gl_utils as GLU  # noqa: E402

CTX = {}


class InfraAbort(BaseException):
    """Infrastructure failure: stop the whole run (resumable) instead of failing the node.
    BaseException so generate()'s `except Exception` cannot swallow it."""


class _Res:
    def __init__(self, code, out):
        self.exit_code = code
        self.output = out


def filter_frozen(patch_str, frozen):
    """Drop diff blocks whose a/ or b/ path is a frozen path or lies under a frozen directory
    (whole path components; unlike filter_patch_by_files' substring test)."""
    def is_frozen(p):
        return any(p == f.rstrip("/") or p.startswith(f.rstrip("/") + "/") for f in frozen)
    out, include, removed = [], True, []
    for line in patch_str.splitlines():
        if line.startswith("diff --git"):
            m = re.match(r"^diff --git a/(\S+) b/(\S+)", line)
            paths = [m.group(1), m.group(2)] if m else []
            include = not any(is_frozen(p) for p in paths)
            if not include:
                removed.append(paths[-1] if paths else line)
        if include:
            out.append(line)
    return "\n".join(out) + ("\n" if out else ""), removed


def _set_frozen_owner(ws):
    for p in CTX.get("freeze_paths", []):
        fp = os.path.join(ws, p)
        if not os.path.lexists(fp) or not inside(fp, ws):
            continue
        if stat.S_ISDIR(os.lstat(fp).st_mode):
            lchown_tree(fp, 0, 0)
            for root, dirs, files in os.walk(fp, followlinks=False):
                os.chmod(root, 0o755)
                for f in files:
                    if not os.path.islink(os.path.join(root, f)):
                        os.chmod(os.path.join(root, f), 0o644)
        else:
            os.lchown(fp, 0, 0)
            os.chmod(fp, 0o644)


class LocalContainer:
    def __init__(self, root_dir, name):
        self.name = name
        base = os.path.join(CTX["run_dir"], "_ctmp", name)
        self.base = base
        self.tmp = os.path.join(base, "tmp")
        self.workspace = os.path.join(base, "ws")
        os.makedirs(self.tmp)
        os.chmod(self.tmp, 0o1777)
        # fresh workspace from the root-owned pristine repo (root never runs git in agent-owned repos)
        subprocess.run(["git", "clone", "-q", "--no-hardlinks", root_dir, self.workspace], check=True,
                       env={**os.environ, "GIT_CONFIG_NOSYSTEM": "1"})
        chown_agent(self.workspace)
        _set_frozen_owner(self.workspace)

    def start(self):
        pass

    def reload(self):
        pass

    def map(self, p):
        p = str(p)
        if p == "/hyperagents" or p.startswith("/hyperagents/"):
            return self.workspace + p[len("/hyperagents"):]
        if p == "/tmp" or p.startswith("/tmp/"):
            return self.tmp + p[len("/tmp"):]
        if p.startswith("/DONOTTOUCH"):
            raise RuntimeError("no_selfimprove baseline not supported")
        return None

    def exec_run(self, cmd, workdir="/hyperagents", **kw):
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
        env = {}
        is_meta = any("run_meta_agent.py" in str(c) for c in cmd)
        ro = []
        tok = None
        if is_meta:
            it = CTX.get("current_genid")
            scope = {"phase": CTX["phase"], "arm": CTX["arm"], "seed": CTX["seed"], "iteration": it, "run": CTX["name"]}
            try:
                tok = register_token("meta", scope)
            except Exception as e:
                raise InfraAbort(f"gateway unavailable for meta step: {e}")
            env["GW_TOKEN"] = tok
            ro = ["/hyperagents/" + p for p in CTX.get("freeze_paths", [])]
            t0 = time.time()
        try:
            rc, out = run_sandboxed(cmd, binds=[(self.workspace, "/hyperagents", False)], cwd=workdir,
                                    env_extra=env, timeout=3 * 3600, ro_paths=ro, tmp_host=self.tmp)
        finally:
            if tok:
                try:
                    info = revoke_token(tok)
                except Exception:
                    info = {}
        if is_meta:
            append_jsonl(os.path.join(CTX["run_dir"], "meta_steps.jsonl"),
                         {"iteration": CTX.get("current_genid"), "rc": rc, "dur": time.time() - t0, "token": tok,
                          "meta_calls": info.get("calls"), "meta_tokens": info.get("tokens_used"),
                          "upstream_errors": info.get("upstream_errors"), "tail": out.decode(errors="replace")[-3000:]})
            if info.get("refused_after_restart") or info.get("refused_global"):
                raise InfraAbort("gateway restarted or global budget refusal during meta step")
        return _Res(rc, out)


def build_container(client, repo_path="./", image_name="", container_name="", force_rebuild=False, domains=None, verbose=True):
    return LocalContainer(os.path.abspath(repo_path), container_name + "-" + uuid.uuid4().hex[:6])


def cleanup_container(container, verbose=True):
    shutil.rmtree(container.base, ignore_errors=True)


def copy_to_container(container, source_path, dest_path, verbose=True):
    dst = container.map(dest_path)
    if dst is None:
        raise RuntimeError(f"unmapped container path {dest_path}")
    base = container.workspace if dst.startswith(container.workspace) else container.tmp
    if os.path.lexists(dst) and os.path.islink(dst):
        os.unlink(dst)
    if not inside(os.path.dirname(dst), base):
        raise RuntimeError(f"unsafe destination {dest_path}")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(source_path):  # source is always root-controlled (output dir / patch files)
        shutil.copytree(source_path, dst, dirs_exist_ok=True, symlinks=True)
        chown_agent(dst)
    else:
        shutil.copyfile(source_path, dst, follow_symlinks=False)
        os.lchown(dst, AGENT_UID, AGENT_GID)


def copy_from_container(container, source_path, dest_path, verbose=True):
    src = container.map(source_path)
    base = container.workspace if src and src.startswith(container.workspace) else container.tmp
    if src is None or not os.path.lexists(src):
        raise FileNotFoundError(f"Source path not found in container: {source_path}")
    if not inside(src, base):
        raise FileNotFoundError(f"refusing unsafe container path {source_path}")
    if stat.S_ISDIR(os.lstat(src).st_mode):
        skipped = safe_copytree(src, dest_path, base)
        if skipped:
            append_jsonl(os.path.join(CTX["run_dir"], "unsafe_skipped.jsonl"), {"src": source_path, "skipped": skipped[:50]})
    else:
        safe_copyfile(src, dest_path, base)
    # freeze mode: any edit to meta-agent files is dropped from the recorded patch
    pf = os.path.join(dest_path, "model_patch.diff") if os.path.isdir(dest_path) else None
    if CTX.get("freeze_paths") and pf and os.path.exists(pf):
        s = open(pf).read()
        f, removed = filter_frozen(s, CTX["freeze_paths"])
        if removed:
            open(pf, "w").write(f if f.strip() else "")
            append_jsonl(os.path.join(CTX["run_dir"], "freeze_resets.jsonl"),
                         {"iteration": CTX.get("current_genid"), "removed_paths": removed})


class _DummyDocker:
    def __init__(self, *a, **k):
        pass


def arc_eval_produced_agent(container, container_output_folder, gen_output_dir, domain, eval_samples=-1,
                            eval_workers=10, eval_subset="", eval_test=False):
    genid = os.path.basename(os.path.normpath(gen_output_dir)).split("gen_", 1)[1]
    scope = {"phase": CTX["phase"], "arm": CTX["arm"], "seed": CTX["seed"], "iteration": genid}
    # exact, immutable snapshot of the produced agent; this is what is evaluated and later re-scored
    snap = os.path.join(CTX["run_dir"], "snapshots", f"gen_{genid}.tar.gz")
    skipped = snapshot_tree(container.workspace, snap, container.workspace)
    code_dir = extract_snapshot(snap, os.path.join(CTX["run_dir"], "_evalcode", f"gen_{genid}"))
    vis = os.path.join(gen_output_dir, f"{domain}_eval")
    s = evaluate_set(code_dir, CTX["task_ids"], scope, workers=CTX.get("workers", 16), visible_dir=vis,
                     log=lambda m: GL.safe_log(m))
    shutil.rmtree(code_dir, ignore_errors=True)
    append_jsonl(os.path.join(CTX["run_dir"], "gen_scores.jsonl"),
                 {"iteration": genid, "score": s["score"], "missing": s["missing"], "infra_error_rows": s["infra_error_rows"],
                  "n_test_inputs": s["n_test_inputs"], "code_hash": s["code_hash"], "format_failures": s["format_failures"],
                  "snapshot_skipped": skipped[:20]})
    if s["missing"]:
        raise InfraAbort(f"gen {genid}: {s['missing']} test inputs could not be evaluated (infra)")


_orig_setup = GLU.setup_initial_gen
_orig_generate = GL.generate


def arc_setup_initial_gen(output_dir, domains, copy_root_dir=None, subsets=[], resume=False, **kw):
    cfgp = CTX["config_path"]
    cfg = json.load(open(cfgp))
    root_dir = os.path.abspath(os.path.join(output_dir, "gen_initial/hyperagents"))
    if resume and cfg.get("root_commit"):
        # root_dir is root-owned and never writable by agents (each generation works in a fresh clone)
        assert os.stat(root_dir).st_uid == 0
        return root_dir, cfg["root_commit"]
    # The template has no .git of its own (the original copies the host repo incl. .git); give the
    # agent repo its own git repo so commits never land in the host repository.
    _orig_commit = GLU.commit_repo

    def _commit_with_init(d, *a2, **k2):
        if not os.path.isdir(os.path.join(d, ".git")):
            subprocess.run(["git", "init", "-q", d], check=True)
        return _orig_commit(d, *a2, **k2)
    GLU.commit_repo = _commit_with_init
    try:
        rd, _ = _orig_setup(output_dir, domains, copy_root_dir=copy_root_dir, subsets=subsets, resume=False, **kw)
    finally:
        GLU.commit_repo = _orig_commit
    assert os.path.isdir(os.path.join(rd, ".git")) and rd == root_dir
    ddir = os.path.join(root_dir, "domains", "arc", "data")
    os.makedirs(ddir, exist_ok=True)
    with open(os.path.join(ddir, "tasks.json"), "w") as f:
        json.dump([arc_data.visible_task(t) for t in CTX["task_ids"]], f)
    from utils.git_utils import commit_repo
    commit = commit_repo(root_dir)
    top = subprocess.run(["git", "-C", root_dir, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(root_dir), f"agent repo git toplevel is {top}"
    full = subprocess.run(["git", "-C", root_dir, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    cfg["root_commit"] = full
    json.dump(cfg, open(cfgp, "w"), indent=2)
    return root_dir, full


def arc_generate(*a, **kw):
    CTX["current_genid"] = kw["current_genid"] if "current_genid" in kw else a[4]
    try:
        st = gw_status()
    except Exception as e:
        raise InfraAbort(f"gateway down before generation {CTX['current_genid']}: {e}")
    if st["spent"] + st.get("reserved", 0) >= 150.0:
        raise InfraAbort("global budget exhausted")
    return _orig_generate(*a, **kw)


def patch_all():
    GL.build_container = build_container
    GL.cleanup_container = cleanup_container
    GL.copy_to_container = copy_to_container
    GL.copy_from_container = copy_from_container
    GL.docker.DockerClient = _DummyDocker
    GL.eval_produced_agent = arc_eval_produced_agent
    GL.setup_initial_gen = arc_setup_initial_gen
    GL.generate = arc_generate
    GLU.copy_to_container = copy_to_container
    # plotting/visualisation only (graphviz etc.); not part of the algorithm
    for n in ["plot_progress_single", "plot_progress_together", "visualize_archive_single", "visualize_archive_together"]:
        setattr(GL, n, lambda *a, **k: None)


def ensure_initial_eval(set_name, task_ids, workers):
    """A_0's score on the run's set (shared by all runs on that set), as the loop's gen_initial eval."""
    dst = os.path.join(REPO, "outputs", f"initial_arc_{set_name}_0")
    keep = os.path.join(EXP, "initial", f"initial_arc_{set_name}_0")
    if os.path.exists(os.path.join(dst, "report.json")):
        return
    if os.path.exists(os.path.join(keep, "report.json")):  # restore after a VM rebuild
        shutil.copytree(keep, dst, dirs_exist_ok=True)
        return
    tmpl = os.path.join(REPO, "agent_template")
    s = evaluate_set(tmpl, task_ids, {"phase": "initial", "arm": "A0", "seed": "-", "iteration": set_name},
                     workers=workers, visible_dir=dst)
    if s["missing"]:
        shutil.rmtree(dst, ignore_errors=True)
        raise InfraAbort(f"initial eval incomplete: {s['missing']} missing")
    shutil.copytree(dst, keep, dirs_exist_ok=True)
    print(f"A_0 on {set_name}: {s['score']:.3f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    a = ap.parse_args()
    cfgp = os.path.abspath(a.config)
    cfg = json.load(open(cfgp))
    run_dir = os.path.dirname(cfgp)
    splits = json.load(open(os.path.join(REPO, "splits.json")))
    task_ids = splits[cfg["task_set"]] if cfg["task_set"] in splits else cfg["task_ids"]
    CTX.update(cfg)
    CTX.update(config_path=cfgp, run_dir=run_dir, task_ids=task_ids)
    shutil.rmtree(os.path.join(run_dir, "_ctmp"), ignore_errors=True)  # leftovers of a killed process
    import random
    import numpy as np
    random.seed(cfg["rng_seed"])
    np.random.seed(cfg["rng_seed"])
    patch_all()
    try:
        ensure_initial_eval(cfg["task_set"], task_ids, cfg.get("workers", 16))
        out_dir = os.path.join(run_dir, f"generate_{cfg['name']}")
        resume = os.path.exists(os.path.join(out_dir, "archive.jsonl"))
        if resume:
            # the parent RNG state is not restorable; reseed deterministically per resume point
            random.seed(cfg["rng_seed"] * 1000 + len(open(os.path.join(out_dir, "archive.jsonl")).read().splitlines()))
        GL.generate_loop(
            domains=["arc"],
            run_id=cfg["name"],
            max_generation=cfg["max_generation"],
            eval_samples=[-1],
            eval_workers=cfg.get("workers", 16),
            eval_subsets=["_" + cfg["task_set"]],
            parent_selection=cfg.get("parent_selection", "score_child_prop"),
            resume_from=out_dir if resume else None,
            output_dir_parent=run_dir,
            copy_root_dir=cfg["template_dir"],
            skip_staged_eval=True,
        )
    except InfraAbort as e:
        append_jsonl(os.path.join(run_dir, "infra_aborts.jsonl"), {"ts": time.time(), "gen": CTX.get("current_genid"), "error": str(e)})
        print("INFRA ABORT (resumable):", e)
        sys.exit(3)
    cfg = json.load(open(cfgp))
    cfg["done"] = True
    json.dump(cfg, open(cfgp, "w"), indent=2)
    print("RUN DONE", cfg["name"])


if __name__ == "__main__":
    main()
