"""Run the repo's generate_loop (unchanged algorithm) on the ARC-AGI-2 domain, without Docker.

Docker "containers" are replaced by LocalContainer: the agent repo is bound at /hyperagents and a
per-container dir at /tmp inside a network-less, unprivileged namespace sandbox (sandbox.py). The only
other substitution is eval_produced_agent: the task agent is evaluated host-side, one sandbox per test
input, scored against private ground truth that never enters the agent's environment.

Usage: python -m arcexp.run_loop --config exp/runs/<name>/config.json   (resumes automatically)
"""
import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
import uuid

from arcexp import arc_data
from arcexp.arc_eval import evaluate_set
from arcexp.common import EXP, REPO, chown_agent, register_token, append_jsonl
from arcexp.sandbox import run_sandboxed

os.chdir(REPO)
sys.path.insert(0, REPO)

import generate_loop as GL  # noqa: E402
import utils.gl_utils as GLU  # noqa: E402
from utils.gl_utils import filter_patch_by_files  # noqa: E402

CTX = {}


class _Res:
    def __init__(self, code, out):
        self.exit_code = code
        self.output = out


class LocalContainer:
    def __init__(self, workspace, name):
        self.workspace = os.path.abspath(workspace)
        self.name = name
        self.tmp = os.path.join(CTX["run_dir"], "_ctmp", name)
        os.makedirs(self.tmp, exist_ok=True)
        os.chmod(self.tmp, 0o1777)

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
        timeout = 3 * 3600
        is_meta = any("run_meta_agent.py" in str(c) for c in cmd)
        ro = []
        if is_meta:
            it = CTX.get("current_genid")
            scope = {"phase": CTX["phase"], "arm": CTX["arm"], "seed": CTX["seed"], "iteration": it, "run": CTX["name"]}
            env["GW_TOKEN"] = register_token("meta", scope)
            ro = ["/hyperagents/" + p for p in CTX.get("freeze_paths", [])]
            CTX["last_meta_token"] = env["GW_TOKEN"]
            t0 = time.time()
        rc, out = run_sandboxed(cmd, binds=[(self.workspace, "/hyperagents", False)], cwd=workdir,
                                env_extra=env, timeout=timeout, ro_paths=ro, tmp_host=self.tmp)
        if is_meta:
            append_jsonl(os.path.join(CTX["run_dir"], "meta_steps.jsonl"),
                         {"iteration": CTX.get("current_genid"), "rc": rc, "dur": time.time() - t0,
                          "token": env["GW_TOKEN"], "tail": out.decode(errors="replace")[-3000:]})
            if CTX.get("freeze_paths"):
                self._freeze_reset()
        return _Res(rc, out)

    def _freeze_reset(self):
        """Freeze mode: drop any change to meta-agent files from the produced patch and the workspace."""
        fz = CTX["freeze_paths"]
        pf = os.path.join(self.tmp, "agent_output", "model_patch.diff")
        if os.path.exists(pf):
            s = open(pf).read()
            f = filter_patch_by_files(s, fz)
            if f.strip() != s.strip():
                append_jsonl(os.path.join(CTX["run_dir"], "freeze_resets.jsonl"),
                             {"iteration": CTX.get("current_genid"), "removed_bytes": len(s) - len(f)})
                open(pf, "w").write(f if s.strip() else s)
        subprocess.run(["git", "-C", self.workspace, "checkout", "HEAD", "--"] + fz, capture_output=True)
        subprocess.run(["git", "-C", self.workspace, "clean", "-fdq", "--"] + fz, capture_output=True)


def build_container(client, repo_path="./", image_name="", container_name="", force_rebuild=False, domains=None, verbose=True):
    return LocalContainer(repo_path, container_name + "-" + uuid.uuid4().hex[:6])


def cleanup_container(container, verbose=True):
    shutil.rmtree(container.tmp, ignore_errors=True)


def copy_to_container(container, source_path, dest_path, verbose=True):
    dst = container.map(dest_path)
    if dst is None:
        raise RuntimeError(f"unmapped container path {dest_path}")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(source_path):
        shutil.copytree(source_path, dst, dirs_exist_ok=True, symlinks=True)
        chown_agent(dst)
    else:
        shutil.copy2(source_path, dst)
        os.chown(dst, 30033, 30033)


def copy_from_container(container, source_path, dest_path, verbose=True):
    src = container.map(source_path)
    if src is None or not os.path.exists(src):
        raise FileNotFoundError(f"Source path not found in container: {source_path}")
    os.makedirs(os.path.dirname(os.path.abspath(dest_path)), exist_ok=True)
    if os.path.isdir(src):
        shutil.copytree(src, dest_path, dirs_exist_ok=True, symlinks=True)
    else:
        shutil.copy2(src, dest_path)


class _DummyDocker:
    def __init__(self, *a, **k):
        pass


def arc_eval_produced_agent(container, container_output_folder, gen_output_dir, domain, eval_samples=-1,
                            eval_workers=10, eval_subset="", eval_test=False):
    genid = os.path.basename(os.path.normpath(gen_output_dir)).split("gen_", 1)[1]
    scope = {"phase": CTX["phase"], "arm": CTX["arm"], "seed": CTX["seed"], "iteration": genid}
    vis = os.path.join(gen_output_dir, f"{domain}_eval")
    s = evaluate_set(container.workspace, CTX["task_ids"], scope, workers=CTX.get("workers", 16), visible_dir=vis,
                     log=lambda m: GL.safe_log(m))
    append_jsonl(os.path.join(CTX["run_dir"], "gen_scores.jsonl"),
                 {"iteration": genid, "score": s["score"], "missing": s["missing"], "infra_error_rows": s["infra_error_rows"],
                  "n_test_inputs": s["n_test_inputs"], "code_hash": s["code_hash"], "format_failures": s["format_failures"]})


_orig_setup = GLU.setup_initial_gen
_orig_generate = GL.generate


def arc_setup_initial_gen(output_dir, domains, copy_root_dir=None, subsets=[], resume=False, **kw):
    cfgp = CTX["config_path"]
    cfg = json.load(open(cfgp))
    if resume and cfg.get("root_commit"):
        root_dir = os.path.abspath(os.path.join(output_dir, "gen_initial/hyperagents"))
        # crash recovery: the repo may be mid-generation; return it to the root commit
        subprocess.run(["git", "-C", root_dir, "reset", "-q", "--hard", cfg["root_commit"]], check=True)
        subprocess.run(["git", "-C", root_dir, "clean", "-fdq"], check=True)
        return root_dir, cfg["root_commit"]
    root_dir, _ = _orig_setup(output_dir, domains, copy_root_dir=copy_root_dir, subsets=subsets, resume=False, **kw)
    ddir = os.path.join(root_dir, "domains", "arc", "data")
    os.makedirs(ddir, exist_ok=True)
    with open(os.path.join(ddir, "tasks.json"), "w") as f:
        json.dump([arc_data.visible_task(t) for t in CTX["task_ids"]], f)
    from utils.git_utils import commit_repo
    commit = commit_repo(root_dir)
    chown_agent(root_dir)
    for p in CTX.get("freeze_paths", []):  # frozen meta files: root-owned, read-only to the agent
        fp = os.path.join(root_dir, p)
        if os.path.exists(fp):
            for dp, dns, fns in os.walk(fp) if os.path.isdir(fp) else [(os.path.dirname(fp), [], [os.path.basename(fp)])]:
                if os.path.isdir(fp):
                    os.chown(dp, 0, 0)
                    os.chmod(dp, 0o755)
                for fn in fns:
                    os.chown(os.path.join(dp, fn), 0, 0)
                    os.chmod(os.path.join(dp, fn), 0o644)
    cfg["root_commit"] = commit
    json.dump(cfg, open(cfgp, "w"), indent=2)
    return root_dir, commit


def arc_generate(*a, **kw):
    CTX["current_genid"] = kw.get("current_genid")
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
    if os.path.exists(os.path.join(dst, "report.json")):
        return
    tmpl = os.path.join(REPO, "agent_template")
    s = evaluate_set(tmpl, task_ids, {"phase": "initial", "arm": "A0", "seed": "-", "iteration": set_name},
                     workers=workers, visible_dir=dst)
    keep = os.path.join(EXP, "initial", f"initial_arc_{set_name}_0")
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
    import random
    import numpy as np
    random.seed(cfg["rng_seed"])
    np.random.seed(cfg["rng_seed"])
    patch_all()
    ensure_initial_eval(cfg["task_set"], task_ids, cfg.get("workers", 16))
    # restore cached initial eval if outputs/ was wiped (VM rebuild)
    out_parent = os.path.join(run_dir)
    out_dir = os.path.join(out_parent, f"generate_{cfg['name']}")
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
        output_dir_parent=out_parent,
        copy_root_dir=cfg["template_dir"],
        skip_staged_eval=True,
    )
    cfg = json.load(open(cfgp))
    cfg["done"] = True
    json.dump(cfg, open(cfgp, "w"), indent=2)
    print("RUN DONE", cfg["name"])


if __name__ == "__main__":
    main()
