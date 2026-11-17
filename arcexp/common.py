"""Shared host-side helpers (root only; never copied into an agent tree)."""
import hashlib
import http.client
import json
import os
import secrets
import socket
import threading

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP = os.path.join(REPO, "exp")
PRIVATE = "/opt/arc_private"
ARC_DIR = os.path.join(PRIVATE, "ARC-AGI-2", "data")
RUNNER_DIR = "/opt/arc_runner"  # read-only helper code visible to sandboxes (no answers)
GW_RUN = "/run/arcgw"
GW_SOCK = os.path.join(GW_RUN, "gw.sock")
ADMIN_SOCK = os.path.join(GW_RUN, "admin.sock")
AGENT_UID = 30033
AGENT_GID = 30033

_jsonl_lock = threading.Lock()


class UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, path, timeout=3600):
        super().__init__("localhost", timeout=timeout)
        self._path = path

    def connect(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        s.connect(self._path)
        self.sock = s


def unix_request(path, method, url, body=None, timeout=3600):
    c = UnixHTTPConnection(path, timeout=timeout)
    data = json.dumps(body).encode() if body is not None else None
    c.request(method, url, body=data, headers={"Content-Type": "application/json"})
    r = c.getresponse()
    out = r.read()
    c.close()
    return r.status, json.loads(out or b"{}")


def _admin(method, url, body=None, tries=6):
    import time as _t
    last = None
    for i in range(tries):
        try:
            st, d = unix_request(ADMIN_SOCK, method, url, body, timeout=60)
            if st == 200:
                return d
            last = f"HTTP {st}: {d}"
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        _t.sleep(min(30, 2 ** i))
    raise RuntimeError(f"gateway admin {url} failed: {last}")


def revoke_token(tok):
    d = _admin("POST", "/revoke", {"token": tok})
    if "calls" not in d or not d.get("revoked"):
        raise RuntimeError(f"revoke did not confirm: {d}")
    return d


def register_token(role, scope, effort_role=None):
    tok = secrets.token_hex(16)
    body = {"token": tok, "role": role, "scope": scope}
    if effort_role:
        body["effort_role"] = effort_role
    _admin("POST", "/register", body)
    return tok


def token_info(tok):
    return _admin("GET", f"/token/{tok}")


def gw_status():
    return _admin("GET", "/status", tries=2)


def append_jsonl(path, rec):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with _jsonl_lock:
        with open(path, "a") as f:
            f.write(json.dumps(rec) + "\n")


def read_jsonl(path):
    out = []
    if not os.path.exists(path):
        return out
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out


def tree_hash(root, exclude_dirs=(".git", "__pycache__")):
    """Hash of the regular files of a tree (links and special files are skipped, never followed/opened)."""
    from arcexp.safeio import safe_read_bytes
    h = hashlib.sha256()
    for dp, dns, fns in os.walk(root, followlinks=False):
        dns[:] = sorted(d for d in dns if d not in exclude_dirs and not os.path.islink(os.path.join(dp, d)))
        for fn in sorted(fns):
            if fn.endswith(".pyc"):
                continue
            p = os.path.join(dp, fn)
            b = safe_read_bytes(p)
            if b is None:
                continue
            h.update(os.path.relpath(p, root).encode())
            h.update(hashlib.sha256(b).digest())
    return h.hexdigest()[:16]


def chown_agent(path):
    for dp, dns, fns in os.walk(path, followlinks=False):
        os.lchown(dp, AGENT_UID, AGENT_GID)
        for fn in dns + fns:
            try:
                os.lchown(os.path.join(dp, fn), AGENT_UID, AGENT_GID)
            except FileNotFoundError:
                pass
