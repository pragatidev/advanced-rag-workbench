"""Product door. A real app POSTs here. Run: python app.py"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from rag.ask import run_ask

HOST = "127.0.0.1"
PORT = 8787

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>ACME support desk</title>
  <style>
    body { font-family: Georgia, serif; max-width: 40rem; margin: 2rem auto; padding: 0 1rem; }
    textarea { width: 100%; min-height: 5rem; font: inherit; }
    button { font: inherit; margin-top: 0.5rem; }
    .src { color: #444; font-size: 0.9rem; }
  </style>
</head>
<body>
  <h1>ACME support desk</h1>
  <p>This is the product. Your question hits POST /ask, which calls run_ask. Same function a Slack bot would import.</p>
  <textarea id="q" placeholder="What does error code TS-999 mean?"></textarea>
  <div><button type="button" id="go">Ask</button></div>
  <div id="out"></div>
  <script>
    document.getElementById("go").onclick = async function () {
      const question = document.getElementById("q").value.trim();
      const box = document.getElementById("out");
      box.textContent = "Looking up the corpus…";
      const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question, pipeline: "hybrid" })
      });
      const data = await res.json();
      if (!res.ok) { box.textContent = data.error || "failed"; return; }
      const ids = (data.hits || []).map(function (h) { return h.chunk_id; }).join(", ");
      box.innerHTML = "<p>" + (data.answer || "") + "</p><p class=\\"src\\">sources: " + ids + "</p>";
    };
  </script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        return

    def _send(self, code: int, payload=None, raw: bytes | None = None, ctype: str = "application/json; charset=utf-8") -> None:
        body = raw if raw is not None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
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
            self._send(200, raw=HTML.encode("utf-8"), ctype="text/html; charset=utf-8")
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
        try:
            payload = run_ask(
                question,
                pipeline=data.get("pipeline") or "hybrid",
                generate=data.get("generate"),
            )
        except ValueError as exc:
            self._send(400, {"error": str(exc)})
            return
        self._send(200, payload)


def make_server(host: str = HOST, port: int = PORT) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    httpd = make_server()
    print(f"ACME desk http://{HOST}:{PORT}/  POST /ask", flush=True)
    httpd.serve_forever()
