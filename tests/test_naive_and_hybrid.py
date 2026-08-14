from ragbench.chunkers import chunk_corpus
from ragbench.corpus import load_documents
from ragbench.embed import ToyEmbedder
from ragbench.loops.retrieve_gate import needs_corpus
from ragbench.pipelines.hybrid import run_hybrid
from ragbench.pipelines.naive import run_naive
from ragbench.retrieve import bm25_search, dense_search


def test_dense_prefers_general_error_advice_for_ts999():
    docs = load_documents()
    chunks = chunk_corpus(docs, "recursive")
    hits = dense_search(
        "What does error code TS-999 mean?",
        chunks,
        embedder=ToyEmbedder(semantic_mode=True),
        k=1,
    )
    assert hits
    assert "ts-999 means" not in hits[0].chunk.text.lower()


def test_bm25_locks_ts999():
    docs = load_documents()
    chunks = chunk_corpus(docs, "recursive")
    hits = bm25_search("What does error code TS-999 mean?", chunks, k=1)
    assert "ts-999" in hits[0].chunk.text.lower()
    assert "duplicate invoice" in hits[0].chunk.text.lower()


def test_hybrid_recovers_ts999():
    result = run_hybrid("What does error code TS-999 mean?")
    blob = " ".join(h["text"] for h in result["hits"]).lower()
    assert "ts-999" in blob
    assert "duplicate invoice" in blob


def test_naive_returns_sources():
    result = run_naive("What was ACME revenue growth in Q2 2023?")
    assert result["pipeline"] == "naive"
    assert result["hits"]
    assert result["answer"]


def test_chitchat_does_not_need_corpus():
    assert needs_corpus("Good morning, how are you?") is False
    assert needs_corpus("What does error code TS-999 mean?") is True
