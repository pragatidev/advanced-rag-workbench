from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.gov import (
    ALLOW_LIST,
    DETECTOR,
    ECHOLEAK_CVE,
    PLANTED_ID,
    POISONEDRAG_ASR_PCT,
    POISONEDRAG_TEXTS_PER_TARGET,
    RLS_SQL,
    audit_row,
    canary_pass,
    denied_absent,
    ingest_filter,
    planted_email,
    prefilter,
    redact,
)


def test_section_16_governance():
    assert "ENABLE ROW LEVEL SECURITY" in RLS_SQL
    assert "[REDACTED_PII]" in redact("Do not send a national id to the model.")
    assert DETECTOR
    docs = load_documents()
    chunks = chunk_corpus(docs, "recursive")
    west = prefilter(chunks, "helix-west")
    denied = [c.chunk_id for c in chunks if c.doc_id == "faq"]
    row = audit_row("q", west, tenant="helix-west")
    assert denied_absent(row, denied)
    east = prefilter(chunks, "helix-east")
    assert len(east) > len(west)


def test_section_16_ingest_trust():
    planted = planted_email()
    assert planted.chunk_id == PLANTED_ID
    assert planted.metadata.get("doc_type") == "email"
    docs = load_documents()
    chunks = chunk_corpus(docs, "recursive")
    mixed = list(chunks) + [planted]
    kept = ingest_filter(mixed)
    assert canary_pass(kept)
    assert all(c.metadata.get("doc_type") in ALLOW_LIST for c in kept)
    assert POISONEDRAG_TEXTS_PER_TARGET == 5
    assert POISONEDRAG_ASR_PCT == 90
    assert ECHOLEAK_CVE == "CVE-2025-32711"
