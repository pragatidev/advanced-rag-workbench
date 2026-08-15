"""Structured log line for one ask. Shape matches OTel GenAI span fields.

This writes JSONL. It is not an OpenTelemetry SDK install.
Required names: trace_id, span_id, latency_ms, gen_ai.request.model,
tokens, usd, retrieval chunk ids.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_SPAN_FIELDS = (
    "trace_id",
    "span_id",
    "name",
    "latency_ms",
    "gen_ai.request.model",
    "tokens",
    "usd",
    "chunk_ids",
)


def new_trace_id() -> str:
    return uuid.uuid4().hex


def start_span(name: str = "rag.ask", trace_id: str | None = None) -> dict:
    return {
        "trace_id": trace_id or new_trace_id(),
        "span_id": uuid.uuid4().hex[:16],
        "name": name,
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def shape_span(
    *,
    question: str,
    pipeline: str,
    chunk_ids: list[str],
    model: str = "extractive",
    latency_ms: float = 0.0,
    tokens: int = 0,
    usd: float = 0.0,
    cache_status: str = "MISS",
    generate_calls: int = 1,
    extra: dict | None = None,
) -> dict:
    span = start_span(name="rag.ask")
    span.update(
        {
            "question": question,
            "pipeline": pipeline,
            "latency_ms": round(float(latency_ms), 3),
            "gen_ai.request.model": model,
            "gen_ai.operation.name": "chat",
            "tokens": int(tokens),
            "usd": float(usd),
            "chunk_ids": list(chunk_ids),
            "cache_status": cache_status,
            "generate_calls": int(generate_calls),
        }
    )
    if extra:
        span.update(extra)
    return span


def missing_span_fields(row: dict) -> list[str]:
    return [f for f in REQUIRED_SPAN_FIELDS if f not in row]


def log_ask(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row = dict(payload)
    if "ts" not in row:
        row["ts"] = datetime.now(timezone.utc).isoformat()
    if "trace_id" not in row:
        row.update(start_span())
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
