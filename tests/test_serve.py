import json
import threading
from http.client import HTTPConnection

from app import make_server


def _start():
    httpd = make_server("127.0.0.1", 0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd


def _json(conn: HTTPConnection, method: str, path: str, payload: dict | None = None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if body is not None else {}
    conn.request(method, path, body=body, headers=headers)
    resp = conn.getresponse()
    raw = resp.read().decode("utf-8")
    data = json.loads(raw) if raw.startswith("{") or raw.startswith("[") else raw
    return resp.status, data


def test_desk_is_a_product_page():
    httpd = _start()
    try:
        conn = HTTPConnection("127.0.0.1", httpd.server_address[1], timeout=15)
        status, page = _json(conn, "GET", "/")
        assert status == 200
        assert "ACME support desk" in page
        assert "POST /ask" in page
    finally:
        httpd.shutdown()


def test_post_ask_is_how_an_app_invokes_rag():
    httpd = _start()
    try:
        conn = HTTPConnection("127.0.0.1", httpd.server_address[1], timeout=30)
        status, data = _json(
            conn,
            "POST",
            "/ask",
            {
                "question": "What does error code TS-999 mean?",
                "pipeline": "hybrid",
                "generate": "extractive",
            },
        )
        assert status == 200
        blob = " ".join(h["text"] for h in data["hits"]).lower()
        assert "ts-999" in blob
        assert "answer" in data
    finally:
        httpd.shutdown()


def test_post_ask_requires_a_question():
    httpd = _start()
    try:
        conn = HTTPConnection("127.0.0.1", httpd.server_address[1], timeout=15)
        status, data = _json(conn, "POST", "/ask", {"question": ""})
        assert status == 400
        assert data["error"] == "question required"
    finally:
        httpd.shutdown()
