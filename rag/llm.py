"""Chat generate. OpenAI-compatible or Anthropic-compatible (Token Plan / Qwen)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from rag.chunkers import Chunk
from rag.envload import api_backend, api_base, api_key, api_model

SYSTEM = (
    "Answer only from the retrieved sources. Cite chunk ids. "
    "If the sources do not support an answer, say REFUSE."
)


def _source_blob(question: str, chunks: list[Chunk]) -> str:
    sources = []
    for i, ch in enumerate(chunks, start=1):
        sources.append(f"[{i}] {ch.chunk_id}\n{ch.text}")
    context = "\n\n".join(sources) if sources else "(no retrieved chunks)"
    return f"Question: {question}\n\nSources:\n{context}"


def _post(url: str, headers: dict, body: dict, timeout: int) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:400]
        raise RuntimeError(f"model HTTP {exc.code}: {detail}") from exc


def _chat_openai(question: str, chunks: list[Chunk], timeout: int) -> dict:
    url = api_base() + "/chat/completions"
    body = {
        "model": api_model(),
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": _source_blob(question, chunks)},
        ],
        "temperature": 0,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key()}",
    }
    payload = _post(url, headers, body, timeout)
    text = (
        payload.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
        .strip()
    )
    return payload, text


def _chat_anthropic(question: str, chunks: list[Chunk], timeout: int) -> dict:
    url = api_base().rstrip("/") + "/v1/messages"
    body = {
        "model": api_model(),
        "max_tokens": 512,
        "system": SYSTEM,
        "messages": [{"role": "user", "content": _source_blob(question, chunks)}],
        "temperature": 0,
    }
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key(),
        "anthropic-version": "2023-06-01",
    }
    payload = _post(url, headers, body, timeout)
    parts = payload.get("content") or []
    text = "".join(
        p.get("text", "") for p in parts if isinstance(p, dict) and p.get("type") == "text"
    ).strip()
    if not text and isinstance(payload.get("content"), str):
        text = payload["content"].strip()
    return payload, text


def chat(question: str, chunks: list[Chunk], timeout: int = 90) -> dict:
    key = api_key()
    if not key:
        raise RuntimeError(
            "RAGBENCH_GENERATE=api needs a key in .env "
            "(RAGBENCH_API_KEY or ANTHROPIC_API_KEY). Do not commit the key."
        )
    if api_backend() == "anthropic":
        payload, text = _chat_anthropic(question, chunks, timeout)
    else:
        payload, text = _chat_openai(question, chunks, timeout)
    usage = payload.get("usage") or {}
    return {
        "text": text or "REFUSE: empty model response.",
        "model": payload.get("model") or api_model(),
        "usage": usage,
        "endpoint": api_base(),
        "backend": api_backend(),
    }
