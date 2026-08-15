"""Five canaries. No API key. Retrieval stays local."""

from rag.eval.golden import REQUIRED_CATEGORIES, canaries, confirm_tags
from rag.gov import denied_absent, prefilter
from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.loops.retrieve_gate import needs_corpus
from rag.multimodal import multimodal_chunks
from rag.pipelines.hybrid import run_hybrid
from rag.retrieve import bm25_search


def test_golden_has_required_canaries():
    report = confirm_tags()
    assert report["ok"], report
    assert report["n_canaries"] >= 5
    cats = {row["category"] for row in canaries()}
    for name in REQUIRED_CATEGORIES:
        assert name in cats


def test_canary_id_ts999_hybrid():
    result = run_hybrid("What does error code TS-999 mean?")
    blob = " ".join(h["text"] for h in result["hits"]).lower()
    assert "ts-999" in blob


def test_canary_paraphrase_revenue_exists():
    docs = load_documents()
    chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
    assert any("revenue grew by 3%" in c.text.lower() for c in chunks)


def test_canary_table_12420():
    chunks = multimodal_chunks()
    hits = bm25_search("How many paid seats did ACME have in Q2?", chunks, k=3)
    assert any("12420" in h.chunk.text for h in hits)


def test_canary_abstention_chitchat():
    assert needs_corpus("Good morning, how are you?") is False


def test_canary_acl_deny_west_misses_faq():
    docs = load_documents()
    chunks = chunk_corpus(docs, "recursive")
    west = prefilter(chunks, "helix-west")
    denied = [c.chunk_id for c in chunks if c.doc_id == "faq"]
    fake_audit = {"chunk_ids": [c.chunk_id for c in west]}
    assert denied
    assert denied_absent(fake_audit, denied)
