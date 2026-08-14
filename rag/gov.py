"""Tenant filter, PII redact, audit row. Retrieved text is data, not instructions."""

from __future__ import annotations

import hashlib
import re

from rag.chunkers import Chunk

_NATIONAL_ID = re.compile(r"\bnational id\b", re.I)


def allowed(chunk: Chunk, tenant: str) -> bool:
    tag = chunk.metadata.get("tenant", "shared")
    return tag in {tenant, "shared"}


def redact(text: str) -> str:
    return _NATIONAL_ID.sub("[REDACTED_PII]", text)


def audit_row(question: str, chunks: list[Chunk], model: str = "extractive") -> dict:
    return {
        "question_hash": hashlib.sha256(question.encode("utf-8")).hexdigest()[:12],
        "chunk_ids": [c.chunk_id for c in chunks],
        "chunk_hashes": [
            hashlib.sha256(c.text.encode("utf-8")).hexdigest()[:12] for c in chunks
        ],
        "model": model,
    }
