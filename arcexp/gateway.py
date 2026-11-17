"""Budget gateway: the ONLY path from any agent to the model.

Runs as root on the host, outside every agent-editable tree. Agents reach it through
a unix socket (agents run in network-less sandboxes), presenting a per-scope token.

Fixed here and nowhere else (agents cannot edit this file):
  * model = gpt-6-luna
  * reasoning effort per role: task=high, meta=high (user changed from max) (task_xhigh=xhigh for the one check pass)
  * per-token caps: task tokens -> at most 2 model calls (one token per test input);
    meta tokens -> at most 600k total tokens (one token per meta-agent iteration)
  * global hard stop: refuse every call once ledger spend >= $150
  * token & dollar ledger by role (append-only JSONL)
"""
import http.client
import http.server
import json
import os
import socket
import socketserver
import sys
import threading
import time
import traceback

import requests

MODEL = "gpt-6-luna"
EFFORT = {"task": "high", "meta": "high", "task_xhigh": "xhigh", "probe": "high"}
PRICE_IN = 0.10 / 1e6
PRICE_CACHED = 0.01 / 1e6
PRICE_OUT = 0.50 / 1e6
GLOBAL_CAP_USD = 150.0
TASK_MAX_CALLS = 2
META_MAX_TOKENS = 600_000
MAX_OUTPUT_TOKENS = {"task": 64000, "task_xhigh": 64000, "meta": 64000, "probe": 2000}
REQUEST_TIMEOUT = 1800

RUN_DIR = os.environ.get("ARCGW_RUN_DIR", "/run/arcgw")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.environ.get("ARCGW_LEDGER", os.path.join(REPO, "exp", "ledger", "calls.jsonl"))
TOKENS_FILE = os.path.join(REPO, "exp", "ledger", "tokens.jsonl")

lock = threading.Lock()
state = {"spent": 0.0, "by_role": {}, "tokens": {}}  # token -> dict


def cost_of(usage):
    inp = usage.get("input_tokens", 0) or 0
    cached = (usage.get("input_tokens_details") or {}).get("cached_tokens", 0) or 0
    out = usage.get("output_tokens", 0) or 0
    return (inp - cached) * PRICE_IN + cached * PRICE_CACHED + out * PRICE_OUT


def load_state():
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    if os.path.exists(LEDGER):
        with open(LEDGER) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                state["spent"] += r.get("cost", 0.0)
                role = r.get("role", "?")
                state["by_role"][role] = state["by_role"].get(role, 0.0) + r.get("cost", 0.0)
                tok = r.get("token")
                if tok:
                    t = state["tokens"].setdefault(tok, {"calls": 0, "tokens_used": 0, "role": role, "scope": r.get("scope", {})})
                    t["calls"] += 1
                    t["tokens_used"] += r.get("total_tokens", 0)
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                t = state["tokens"].setdefault(r["token"], {"calls": 0, "tokens_used": 0})
                t.update({k: v for k, v in r.items() if k not in ("calls", "tokens_used")})


def ledger_write(rec):
    with open(LEDGER, "a") as f:
        f.write(json.dumps(rec) + "\n")


def call_openai(messages, effort, max_out):
    # Convert chat-style messages to Responses API input
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
    body = {"model": MODEL, "input": inp, "reasoning": {"effort": effort},
            "max_output_tokens": max_out, "store": False}
    last_err = None
    for attempt in range(7):
        try:
            r = requests.post("https://api.openai.com/v1/responses", json=body, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                d = r.json()
                return d
            last_err = f"HTTP {r.status_code}: {r.text[:500]}"
            if r.status_code in (400, 401, 403, 404):
                # sporadic false-positive "flagged" 400s: retry those twice, everything else is final
                if not (r.status_code == 400 and "flagged" in r.text and attempt < 2):
                    raise RuntimeError(last_err)
        except RuntimeError:
            raise
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
        time.sleep(min(60, 2 ** attempt * 2))
    raise RuntimeError(f"upstream failed after retries: {last_err}")


def extract_text(d):
    texts = []
    for o in d.get("output", []) or []:
        if o.get("type") == "message":
            for c in o.get("content", []) or []:
                if c.get("type") in ("output_text", "text"):
                    texts.append(c.get("text", ""))
    return "\n".join(t for t in texts if t)


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
        return json.loads(self.rfile.read(n) or b"{}")

    def do_GET(self):
        if self.path == "/status":
            with lock:
                return self._send(200, {"spent": state["spent"], "by_role": state["by_role"], "cap": GLOBAL_CAP_USD})
        if self.admin and self.path.startswith("/token/"):
            tok = self.path.split("/token/")[1]
            with lock:
                return self._send(200, state["tokens"].get(tok, {}))
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
                t = state["tokens"].setdefault(rec["token"], {"calls": 0, "tokens_used": 0})
                t.update(rec)
                with open(TOKENS_FILE, "a") as f:
                    f.write(json.dumps(rec) + "\n")
            return self._send(200, {"ok": True})
        if self.path not in ("/v1/chat", "/chat"):
            return self._send(404, {"error": "not found"})
        tok = body.get("token") or self.headers.get("X-GW-Token")
        with lock:
            t = state["tokens"].get(tok)
            if not t or "role" not in t:
                return self._send(403, {"error": "unknown token"})
            if state["spent"] >= GLOBAL_CAP_USD:
                return self._send(402, {"error": "GLOBAL BUDGET EXHAUSTED ($150). All calls refused."})
            role = t["role"]
            eff_role = t.get("effort_role", role)
            if role == "task" and t["calls"] >= TASK_MAX_CALLS:
                return self._send(429, {"error": f"call budget exhausted: at most {TASK_MAX_CALLS} model calls per test input",
                                        "budget_exhausted": True})
            max_out = MAX_OUTPUT_TOKENS.get(eff_role, 64000)
            msgs = body.get("messages") or []
            est_in = sum(len(str(m.get("content", m.get("text", "")))) for m in msgs) // 3 + 50
            if role == "meta":
                remaining = META_MAX_TOKENS - t["tokens_used"]
                if remaining - est_in < 2000:
                    t["calls"] += 0
                    return self._send(200, {"text": "[GATEWAY] The token budget for this meta-agent iteration (600k tokens) is exhausted. No further model calls are possible in this iteration; finish now.",
                                            "usage": {}, "budget_exhausted": True})
                max_out = max(1000, min(max_out, remaining - est_in))
            t["calls"] += 1  # reserve the call slot
        t0 = time.time()
        try:
            d = call_openai(msgs, EFFORT[eff_role], max_out)
        except Exception as e:
            with lock:
                t["calls"] -= 1  # infra failure does not consume a call slot
            ledger_write({"ts": time.time(), "token": tok, "role": role, "scope": t.get("scope", {}),
                          "error": str(e)[:500], "cost": 0.0, "total_tokens": 0})
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
    serve(os.path.join(RUN_DIR, "gw.sock"), AgentHandler, 0o666)
    serve(os.path.join(RUN_DIR, "admin.sock"), AdminHandler, 0o600)
    with open(os.path.join(RUN_DIR, "gateway.pid"), "w") as f:
        f.write(str(os.getpid()))
    print(f"gateway up; spent so far ${state['spent']:.4f}", flush=True)
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
