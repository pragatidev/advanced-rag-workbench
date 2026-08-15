from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.gov import DETECTOR, RLS_SQL, audit_row, denied_absent, prefilter, redact


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
