"""Product door. A chat widget or Slack bot POSTs here the way a real app would."""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from rag.ask import run_ask

DESK_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>ACME support desk</title>
  <style>
    body { font-family: Georgia, serif; max-width: 40rem; margin: 2rem auto; padding: 0 1rem; color: #222; }
    h1 { font-size: 1.25rem; }
    p.note { color: #555; font-size: 0.95rem; }
    textarea { width: 100%; min-height: 5rem; font: inherit; padding: 0.5rem; }
    button { font: inherit; padding: 0.4rem 0.9rem; margin-top: 0.5rem; cursor: pointer; }
    #answer { white-space: pre-wrap; margin-top: 1.25rem; }
    .src { font-size: 0.85rem; color: #444; }
  </style>
</head>
<body>
  <h1>ACME support desk</h1>
  <p class="note">This is a product, not a terminal. Your question hits POST /ask, which calls run_ask. Same function a Slack bot or ticket handler would import.</p>
  <textarea id="q" placeholder="What does error code TS-999 mean?"></textarea>
  <div><button type="button" id="go">Ask</button></div>
  <div id="answer"></div>
  <script>
    document.getElementById("go").onclick = async function () {
      const question = document.getElementById("q").value.trim();
      const box = document.getElementById("answer");
      box.textContent = "Looking up the corpus…";
      const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question, pipeline: "hybrid" })
      });
      const data = await res.json();
      if (!res.ok) { box.textContent = data.error || "request failed"; return; }
      const ids = (data.hits || []).map(function (h) { return h.chunk_id; }).join(", ");
      box.innerHTML = "<p>" + (data.answer || "") + "</p><p class=\\"src\\">sources: " + ids + "</p>";
    };
  </script>
</body>
</html>
"""


class AskHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def _send(self, code: int, payload: dict | None = None, raw: bytes | None = None, content_type: str = "application/json; charset=utf-8") -> None:
        body = raw if raw is not None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        if self.path in {"/", "/desk"}:
            self._send(200, raw=DESK_HTML.encode("utf-8"), content_type="text/html; charset=utf-8")
            return
        if self.path == "/health":
            self._send(200, {"ok": True, "post": "/ask"})
            return
        self._send(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/ask":
            self._send(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self._send(400, {"error": "invalid json"})
            return
        question = (data.get("question") or "").strip()
        if not question:
            self._send(400, {"error": "question required"})
            return
        pipeline = data.get("pipeline") or "hybrid"
        generate = data.get("generate")
        try:
            payload = run_ask(question, pipeline=pipeline, generate=generate)
        except ValueError as exc:
            self._send(400, {"error": str(exc)})
            return
        self._send(200, payload)


def make_server(host: str = "127.0.0.1", port: int = 8787) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), AskHandler)


def serve_forever(host: str = "127.0.0.1", port: int = 8787) -> None:
    httpd = make_server(host, port)
    print(f"rag desk http://{host}:{port}/  POST /ask", flush=True)
    httpd.serve_forever()
