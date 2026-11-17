"""Budget gateway: the ONLY path from any agent to the model.

Runs as root on the host, outside every agent-editable tree. Agents reach it through a unix socket
(agents run in network-less sandboxes), presenting a per-scope token.

Fixed here and nowhere else (agents cannot edit this file):
  * model = gpt-6-luna (Responses API)
  * reasoning effort per role: task=high, meta=high (user changed it from max), task_xhigh=xhigh (one check pass)
  * per-token caps: task tokens -> at most 2 model calls (one token per test input);
    meta tokens -> at most 600k total tokens (one token per meta-agent iteration). Worst-case usage of a call
    is reserved before it starts, and calls on one token are serialized, so caps cannot be exceeded.
  * tokens are revoked by the host as soon as their sandbox exits (no reuse/stashing)
  * global hard stop: refuse every call once settled spend + reserved worst case would exceed $150
  * token & dollar ledger by role (append-only JSONL)
"""
import http.server
import json
import os
import socketserver
import threading
import time

import requests

MODEL = "gpt-6-luna"
EFFORT = {"task": "high", "meta": "high", "task_xhigh": "xhigh", "probe": "high"}
PRICE_IN = 0.10 / 1e6
PRICE_CACHED = 0.01 / 1e6
PRICE_OUT = 0.50 / 1e6
GLOBAL_CAP_USD = 200.0  # raised from 150 by the user (instruction C)
TASK_MAX_CALLS = 2
META_MAX_TOKENS = 600_000
MAX_OUTPUT_TOKENS = {"task": 64000, "task_xhigh": 64000, "meta": 64000, "probe": 2000}
REQUEST_TIMEOUT = 3600

RUN_DIR = os.environ.get("ARCGW_RUN_DIR", "/run/arcgw")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.environ.get("ARCGW_LEDGER", os.path.join(REPO, "exp", "ledger", "calls.jsonl"))
TOKENS_FILE = os.path.join(REPO, "exp", "ledger", "tokens.jsonl")

lock = threading.Lock()
state = {"spent": 0.0, "reserved": 0.0, "by_role": {}, "tokens": {}}


def new_tok():
    return {"calls": 0, "tokens_used": 0, "reserved_tokens": 0, "busy": False, "revoked": False,
            "upstream_errors": 0, "refusals": 0, "refused_global": 0, "possibly_billed_failures": 0}


def cost_of(usage):
    inp = usage.get("input_tokens", 0) or 0
    cached = (usage.get("input_tokens_details") or {}).get("cached_tokens", 0) or 0
    out = usage.get("output_tokens", 0) or 0
    return (inp - cached) * PRICE_IN + cached * PRICE_CACHED + out * PRICE_OUT


def load_state():
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("event") == "revoke":
                    state["tokens"].setdefault(r["token"], new_tok())["revoked"] = True
                    continue
                t = state["tokens"].setdefault(r["token"], new_tok())
                t.update({k: v for k, v in r.items() if k in ("role", "scope", "effort_role")})
    if os.path.exists(LEDGER):
        with open(LEDGER) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                c = r.get("cost", 0.0)
                state["spent"] += c
                role = r.get("role", "?")
                state["by_role"][role] = state["by_role"].get(role, 0.0) + c
                tok = r.get("token")
                if not tok:
                    continue
                t = state["tokens"].setdefault(tok, new_tok())
                if r.get("error"):
                    if r.get("client_error"):
                        t["calls"] += 1
                        t["client_errors"] = t.get("client_errors", 0) + 1
                        continue
                    t["upstream_errors"] += 1
                    if r.get("possibly_billed"):
                        t["calls"] += 1
                        t["possibly_billed_failures"] += 1
                else:
                    t["calls"] += 1
                t["tokens_used"] += r.get("total_tokens", 0)
    # a restarted gateway has no live sandboxes from before: tokens registered earlier are dead
    for t in state["tokens"].values():
        if not t["revoked"]:
            t["revoked"] = True
            t["restart_revoked"] = True


def ledger_write(rec):
    with open(LEDGER, "a") as f:
        f.write(json.dumps(rec) + "\n")


class UpstreamError(Exception):
    """client=True: a 4xx the caller's own request caused (e.g. prompt too long, flagged). It consumes the
    call slot and is NOT an infrastructure failure. Otherwise (5xx, network, timeout) it is infrastructure."""
    def __init__(self, msg, possibly_billed=False, client=False):
        super().__init__(msg)
        self.possibly_billed = possibly_billed
        self.client = client


def call_openai(messages, effort, max_out):
    inp = []
    for m in messages:
        role = m.get("role", "user")
        if role not in ("user", "assistant", "system", "developer"):
            role = "user"
        content = m.get("content")
        if content is None:
            content = m.get("text", "")
        if not isinstance(content, str):
            content = json.dumps(content)
        inp.append({"role": role, "content": content})
    # Streamed, with a reasoning summary requested only so that events keep flowing during long reasoning:
    # non-streamed requests longer than ~25-40 min were being cut by the network path (HTTP 502). The summary
    # is discarded; agents receive exactly the same message text as before.
    body = {"model": MODEL, "input": inp, "reasoning": {"effort": effort, "summary": "auto"},
            "max_output_tokens": max_out, "store": False, "stream": True}
    last_err = None
    for attempt in range(7):
        started = False
        try:
            with requests.post("https://api.openai.com/v1/responses", json=body, stream=True,
                               timeout=(30, 300)) as r:  # read timeout = max silence between events
                if r.status_code != 200:
                    txt = r.text
                    last_err = f"HTTP {r.status_code}: {txt[:500]}"
                    if r.status_code in (400, 401, 403, 404):
                        if not (r.status_code == 400 and "flagged" in txt and attempt < 2):
                            raise UpstreamError(last_err, client=(r.status_code == 400))
                    time.sleep(min(60, 2 ** attempt * 2))
                    continue
                for line in r.iter_lines():
                    if not line or not line.startswith(b"data:"):
                        continue
                    started = True
                    try:
                        ev = json.loads(line[5:])
                    except Exception:
                        continue
                    et = ev.get("type", "")
                    if et in ("response.completed", "response.incomplete"):
                        return ev["response"]
                    if et in ("response.failed", "error"):
                        err = ev.get("response", {}).get("error") or ev.get("error") or ev
                        raise UpstreamError(f"stream failure: {str(err)[:400]}", possibly_billed=True)
                raise UpstreamError("stream ended without completion", possibly_billed=started)
        except UpstreamError:
            raise
        except Exception as e:
            if started:  # generation was under way: may be billed, do not retry
                raise UpstreamError(f"stream broken: {type(e).__name__}: {e}", possibly_billed=True)
            last_err = f"{type(e).__name__}: {e}"
            time.sleep(min(60, 2 ** attempt * 2))
    raise UpstreamError(f"upstream failed after retries: {last_err}")


def extract_text(d):
    texts = []
    for o in d.get("output", []) or []:
        if o.get("type") == "message":
            for c in o.get("content", []) or []:
                if c.get("type") in ("output_text", "text"):
                    texts.append(c.get("text", ""))
    return "\n".join(t for t in texts if t)


def estimate_tokens(msgs):
    # conservative: ~2 characters per token for grids/code
    return sum(len(str(m.get("content", m.get("text", "")))) for m in msgs) // 2 + 200


class AgentHandler(http.server.BaseHTTPRequestHandler):
    admin = False

    def address_string(self):
        return "unix"

    def log_message(self, fmt, *args):
        pass

    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        if n > 50_000_000:
            raise ValueError("too large")
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        if self.path == "/status":
            with lock:
                return self._send(200, {"spent": state["spent"], "reserved": state["reserved"],
                                        "by_role": state["by_role"], "cap": GLOBAL_CAP_USD})
        if self.admin and self.path.startswith("/token/"):
            tok = self.path.split("/token/")[1]
            with lock:
                return self._send(200, {k: v for k, v in state["tokens"].get(tok, {}).items()})
        self._send(404, {"error": "not found"})

    def do_POST(self):
        try:
            body = self._body()
        except Exception:
            return self._send(400, {"error": "bad json"})
        if self.admin and self.path == "/register":
            rec = {"token": body["token"], "role": body["role"], "scope": body.get("scope", {}),
                   "effort_role": body.get("effort_role", body["role"]), "registered_at": time.time()}
            with lock:
                t = state["tokens"].setdefault(rec["token"], new_tok())
                t.update({k: rec[k] for k in ("role", "scope", "effort_role")})
                t["revoked"] = False
                with open(TOKENS_FILE, "a") as f:
                    f.write(json.dumps(rec) + "\n")
            return self._send(200, {"ok": True})
        if self.admin and self.path == "/revoke":
            with lock:
                t = state["tokens"].get(body.get("token"))
                if t is not None:
                    t["revoked"] = True
                    with open(TOKENS_FILE, "a") as f:
                        f.write(json.dumps({"event": "revoke", "token": body["token"], "ts": time.time()}) + "\n")
                info = dict(t) if t else {}
            return self._send(200, info)
        if self.path not in ("/v1/chat", "/chat"):
            return self._send(404, {"error": "not found"})
        tok = body.get("token") or self.headers.get("X-GW-Token")
        msgs = body.get("messages") or []
        with lock:
            t = state["tokens"].get(tok)
            if not t or "role" not in t or t["revoked"]:
                if t is not None and t.get("restart_revoked"):
                    t["refused_after_restart"] = t.get("refused_after_restart", 0) + 1
                return self._send(403, {"error": "unknown or revoked token"})
            if t["busy"]:
                t["refusals"] += 1
                return self._send(429, {"error": "one model call at a time per token"})
            role = t["role"]
            eff_role = t.get("effort_role", role)
            if role == "task" and t["calls"] >= TASK_MAX_CALLS:
                t["refusals"] += 1
                return self._send(429, {"error": f"call budget exhausted: at most {TASK_MAX_CALLS} model calls per test input",
                                        "budget_exhausted": True})
            max_out = MAX_OUTPUT_TOKENS.get(eff_role, 64000)
            est_in = estimate_tokens(msgs)
            if role == "meta":
                remaining = META_MAX_TOKENS - t["tokens_used"]
                if remaining - est_in < 2000:
                    return self._send(200, {"text": "[GATEWAY] The token budget for this meta-agent iteration (600k tokens) is exhausted. No further model calls are possible in this iteration; finish now.",
                                            "usage": {}, "budget_exhausted": True})
                max_out = max(1000, min(max_out, remaining - est_in))
            worst = est_in * PRICE_IN + max_out * PRICE_OUT
            if state["spent"] + state["reserved"] + worst > GLOBAL_CAP_USD:
                t["refused_global"] += 1
                return self._send(402, {"error": "GLOBAL BUDGET EXHAUSTED ($150). All calls refused."})
            t["busy"] = True
            t["calls"] += 1
            state["reserved"] += worst
        t0 = time.time()
        try:
            d = call_openai(msgs, EFFORT[eff_role], max_out)
        except UpstreamError as e:
            with lock:
                t["busy"] = False
                state["reserved"] -= worst
                c = worst if e.possibly_billed else 0.0  # charge worst case if the call may have been billed
                if e.client:
                    t["client_errors"] = t.get("client_errors", 0) + 1  # agent-caused: slot consumed, not infra
                else:
                    t["upstream_errors"] += 1
                    if e.possibly_billed:
                        t["possibly_billed_failures"] += 1
                    else:
                        t["calls"] -= 1  # infra failure that was certainly not billed does not consume a slot
                state["spent"] += c
                state["by_role"][role] = state["by_role"].get(role, 0.0) + c
                ledger_write({"ts": time.time(), "token": tok, "role": role, "scope": t.get("scope", {}),
                              "error": str(e)[:500], "possibly_billed": e.possibly_billed, "client_error": e.client,
                              "cost": c, "total_tokens": 0})
            return self._send(502, {"error": f"upstream error: {e}"})
        usage = d.get("usage") or {}
        c = cost_of(usage)
        text = extract_text(d)
        rec = {"ts": time.time(), "dur": time.time() - t0, "token": tok, "role": role, "effort_role": eff_role,
               "effort_echo": (d.get("reasoning") or {}).get("effort"), "model": d.get("model"),
               "scope": t.get("scope", {}), "status": d.get("status"),
               "input_tokens": usage.get("input_tokens", 0),
               "cached_tokens": (usage.get("input_tokens_details") or {}).get("cached_tokens", 0),
               "output_tokens": usage.get("output_tokens", 0),
               "reasoning_tokens": (usage.get("output_tokens_details") or {}).get("reasoning_tokens", 0),
               "total_tokens": usage.get("total_tokens", 0), "cost": c}
        with lock:
            t["busy"] = False
            state["reserved"] -= worst
            state["spent"] += c
            state["by_role"][role] = state["by_role"].get(role, 0.0) + c
            t["tokens_used"] += usage.get("total_tokens", 0)
            ledger_write(rec)
        return self._send(200, {"text": text, "usage": usage, "status": d.get("status"),
                                "effort": rec["effort_echo"], "model": rec["model"]})


class AdminHandler(AgentHandler):
    admin = True


class UServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True
    request_queue_size = 256

    def get_request(self):
        req, _ = super().get_request()
        return req, ("unix", 0)


def serve(path, handler, mode):
    if os.path.exists(path):
        os.remove(path)
    srv = UServer(path, handler)
    os.chmod(path, mode)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    os.makedirs(RUN_DIR, exist_ok=True)
    os.chmod(RUN_DIR, 0o755)
    load_state()
    serve(os.path.join(RUN_DIR, "admin.sock"), AdminHandler, 0o600)
    serve(os.path.join(RUN_DIR, "gw.sock"), AgentHandler, 0o666)
    with open(os.path.join(RUN_DIR, "gateway.pid"), "w") as f:
        f.write(str(os.getpid()))
    print(f"gateway up; spent so far ${state['spent']:.4f}", flush=True)
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
