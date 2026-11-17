import json
import os
import socket
import http.client
import time
from typing import Tuple

# NOTE (experiment infrastructure): every model call goes through the budget gateway at the unix
# socket $GW_SOCKET using the token in $GW_TOKEN. The gateway fixes the model (gpt-6-luna) and the
# reasoning effort for the caller's role, and enforces the per-test-input / per-iteration budgets.
# The `model`, `temperature` and `max_tokens` arguments below are accepted for compatibility only.

MAX_TOKENS = 16384

CLAUDE_MODEL = "gpt-6-luna"
CLAUDE_HAIKU_MODEL = "gpt-6-luna"
CLAUDE_35NEW_MODEL = "gpt-6-luna"
OPENAI_MODEL = "gpt-6-luna"
OPENAI_MINI_MODEL = "gpt-6-luna"
OPENAI_O3_MODEL = "gpt-6-luna"
OPENAI_O3MINI_MODEL = "gpt-6-luna"
OPENAI_O4MINI_MODEL = "gpt-6-luna"
OPENAI_GPT52_MODEL = "gpt-6-luna"
OPENAI_GPT5_MODEL = "gpt-6-luna"
OPENAI_GPT5MINI_MODEL = "gpt-6-luna"
GEMINI_3_MODEL = "gpt-6-luna"
GEMINI_MODEL = "gpt-6-luna"
GEMINI_FLASH_MODEL = "gpt-6-luna"


class _UnixConn(http.client.HTTPConnection):
    def __init__(self, path, timeout=3600):
        super().__init__("localhost", timeout=timeout)
        self._path = path

    def connect(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        s.connect(self._path)
        self.sock = s


def _gateway_chat(messages):
    path = os.environ.get("GW_SOCKET", "/run/arcgw/gw.sock")
    token = os.environ.get("GW_TOKEN", "")
    body = json.dumps({"token": token, "messages": messages}).encode()
    last = None
    for attempt in range(4):
        try:
            c = _UnixConn(path)
            c.request("POST", "/v1/chat", body=body, headers={"Content-Type": "application/json"})
            r = c.getresponse()
            data = json.loads(r.read() or b"{}")
            c.close()
            if r.status == 200:
                return data.get("text", "")
            last = f"gateway HTTP {r.status}: {data.get('error')}"
            if r.status in (402, 403, 429):
                break  # budget refusals are final
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        time.sleep(5 * (attempt + 1))
    raise RuntimeError(last)


def get_response_from_llm(
    msg: str,
    model: str = OPENAI_MODEL,
    temperature: float = 0.0,
    max_tokens: int = MAX_TOKENS,
    msg_history=None,
) -> Tuple[str, list, dict]:
    if msg_history is None:
        msg_history = []

    # Convert text to content
    msg_history = [
        {**m, "content": m.pop("text")} if "text" in m else m
        for m in msg_history
    ]

    new_msg_history = msg_history + [{"role": "user", "content": msg}]

    response_text = _gateway_chat([{"role": m["role"], "content": m["content"]} for m in new_msg_history])
    new_msg_history.append({"role": "assistant", "content": response_text})

    # Convert content to text, compatible with MetaGen API
    new_msg_history = [
        {**m, "text": m.pop("content")} if "content" in m else m
        for m in new_msg_history
    ]

    return response_text, new_msg_history, {}


if __name__ == "__main__":
    print(get_response_from_llm("Hello there!")[0])
