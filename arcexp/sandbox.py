"""Process sandbox for everything an agent runs (meta agent, its shell tool, task agents).

Each call runs in fresh Linux namespaces:
  * network namespace with no interfaces  -> no network at all (not just no proxy vars);
    the only way out is the gateway's unix socket at /run/arcgw/gw.sock
  * mount namespace: /tmp is replaced by a private dir/tmpfs, /hyperagents is the agent repo
  * pid namespace: cannot see/signal host processes or read other processes' env
  * runs as unprivileged uid 'arcagent' with all capabilities dropped and no_new_privs,
    so it cannot undo the mounts and cannot read root-only dirs (/home/user, /opt/arc_private, /root)
  * clean environment: no proxy variables, no credentials
"""
import os
import shlex
import signal
import subprocess

from arcexp.common import AGENT_GID, AGENT_UID, GW_SOCK, RUNNER_DIR


SHARED_WRITABLE = ["/dev/shm", "/var/tmp", "/run/lock", "/var/lib/php/sessions", "/dev/mqueue"]


def run_sandboxed(cmd, binds, cwd="/tmp", env_extra=None, timeout=3600, ro_paths=(), tmp_host=None, stdin_data=None):
    """binds: list of (host_path, target_path, read_only). If tmp_host is given it is bound to /tmp,
    else /tmp is a fresh tmpfs. ro_paths: paths (inside the sandbox) to remount read-only."""
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    lines = ["set -e"]
    if tmp_host:
        lines.append(f"mount --bind {shlex.quote(tmp_host)} /tmp")
    else:
        lines.append("mount -t tmpfs -o size=4g,mode=1777 tmpfs /tmp")
    # every other world-writable location gets a private, empty tmpfs (no cross-sandbox channels)
    for d in SHARED_WRITABLE:
        lines.append(f"if [ -d {d} ]; then mount -t tmpfs -o size=256m,mode=1777 tmpfs {d}; fi")
    for host, target, ro in binds:
        q_t = shlex.quote(target)
        if os.path.isdir(host):
            lines.append(f"mkdir -p {q_t}")
        else:
            lines.append(f"mkdir -p $(dirname {q_t}); [ -e {q_t} ] || touch {q_t}")
        lines.append(f"mount --bind {shlex.quote(host)} {q_t}")
        if ro:
            lines.append(f"mount -o remount,bind,ro {q_t}")
    for p in ro_paths:
        q = shlex.quote(p)
        lines.append(f"if [ -e {q} ]; then mount --bind {q} {q}; mount -o remount,bind,ro {q}; fi")
    env = {
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "HOME": "/tmp",
        "LANG": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONPATH": RUNNER_DIR,
        "GW_SOCKET": GW_SOCK,
        "GIT_CONFIG_NOSYSTEM": "1",
    }
    if env_extra:
        env.update(env_extra)
    env_args = " ".join(shlex.quote(f"{k}={v}") for k, v in env.items())
    lines.append(f"cd {shlex.quote(cwd)}")
    lines.append(
        f"exec setpriv --reuid={AGENT_UID} --regid={AGENT_GID} --clear-groups --inh-caps=-all "
        f"--bounding-set=-all --no-new-privs env -i {env_args} " + " ".join(shlex.quote(c) for c in cmd)
    )
    script = "\n".join(lines)
    full = ["unshare", "-m", "-n", "-p", "-f", "--mount-proc", "--propagation", "private", "bash", "-c", script]
    p = subprocess.Popen(full, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         stdin=subprocess.PIPE if stdin_data is not None else subprocess.DEVNULL,
                         start_new_session=True)
    try:
        out, _ = p.communicate(input=stdin_data, timeout=timeout)
        return p.returncode, out
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except Exception:
            pass
        out, _ = p.communicate()
        return 124, (out or b"") + b"\n[sandbox] TIMEOUT\n"
