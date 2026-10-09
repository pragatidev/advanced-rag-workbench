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


# Ingest trust (S16.3). Generate hygiene is the other half. Not an exploit.
ALLOW_LIST = frozenset({"filing", "runbook", "policy", "faq", "table", "figure"})
PLANTED_ID = "plant:email:0"
POISONEDRAG_TEXTS_PER_TARGET = 5
POISONEDRAG_CORPUS_SCALE = "millions"
POISONEDRAG_ASR_PCT = 90
POISONEDRAG_VENUE = "USENIX Security 2025"
POISONEDRAG_PAGES = "3827-3844"
ECHOLEAK_CVE = "CVE-2025-32711"
ECHOLEAK_CVSS = "9.3"
ECHOLEAK_YEAR = 2025


def ingest_ok(chunk: Chunk) -> bool:
    return chunk.metadata.get("doc_type") in ALLOW_LIST


def ingest_filter(chunks: list[Chunk]) -> list[Chunk]:
    """Drop chunks whose doc_type is not on the ingest allow-list."""
    return [c for c in chunks if ingest_ok(c)]


def planted_email() -> Chunk:
    """Labeled untrusted inbound. Ordinary text. Not an exploit payload."""
    return Chunk(
        chunk_id=PLANTED_ID,
        doc_id="inbound_mail",
        title="Inbound mail",
        text="Inbound mail. This message is not in the ACME catalog.",
        metadata={"doc_type": "email", "tenant": "untrusted", "planted": True},
    )


def canary_pass(candidates: list[Chunk], planted_id: str = PLANTED_ID) -> bool:
    """True when the planted id is absent from the retrieve candidate set."""
    return all(c.chunk_id != planted_id for c in candidates)
