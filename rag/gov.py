"""Tenant filter, PII redact, audit row, pgvector RLS shape.

Retrieved text is data, not instructions. A denied chunk must never enter
the prompt. Pre-filter before search; do not retrieve then drop.
"""

from __future__ import annotations

import hashlib
import re

from rag.chunkers import Chunk
from rag.retrieve import Hit

_NATIONAL_ID = re.compile(r"\bnational id\b", re.I)
DETECTOR = "national_id_phrase"

RLS_SQL = """
-- pgvector row-level security shape. Demo only.
ALTER TABLE rag_chunks ENABLE ROW LEVEL SECURITY;
ALTER TABLE rag_chunks FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_select ON rag_chunks
    FOR SELECT
    USING (
        metadata->>'tenant' = current_setting('app.tenant', true)
        OR metadata->>'tenant' = 'shared'
    );

-- Session: SET app.tenant = 'helix-east';
""".strip()


def allowed(chunk: Chunk, tenant: str) -> bool:
    tag = chunk.metadata.get("tenant", "shared")
    return tag in {tenant, "shared"}


def prefilter(chunks: list[Chunk], tenant: str) -> list[Chunk]:
    """Stencil the allowed set before search. Denied ids never enter ANN."""
    return [c for c in chunks if allowed(c, tenant)]


def prefilter_hits(hits: list[Hit], tenant: str) -> list[Hit]:
    return [h for h in hits if allowed(h.chunk, tenant)]


def redact(text: str) -> str:
    return _NATIONAL_ID.sub("[REDACTED_PII]", text)


def audit_row(question: str, chunks: list[Chunk], model: str = "extractive", tenant: str = "") -> dict:
    return {
        "question_hash": hashlib.sha256(question.encode("utf-8")).hexdigest()[:12],
        "tenant": tenant,
        "chunk_ids": [c.chunk_id for c in chunks],
        "chunk_hashes": [
            hashlib.sha256(c.text.encode("utf-8")).hexdigest()[:12] for c in chunks
        ],
        "model": model,
    }


def denied_absent(audit: dict, denied_ids: list[str]) -> bool:
    seen = set(audit.get("chunk_ids") or [])
    return all(cid not in seen for cid in denied_ids)
