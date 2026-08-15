from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.pipelines.hybrid import run_hybrid
from rag.retrieve import alpha_hybrid, bm25_search, dense_search, rrf_fuse


def test_section_07_rrf_recovers_ts999():
    docs = load_documents()
    chunks = chunk_corpus(docs, "recursive")
    q = "What does error code TS-999 mean?"
    dense = dense_search(q, chunks, embedder=HashEmbedder(semantic_mode=True), k=8)
    sparse = bm25_search(q, chunks, k=8)
    assert "ts-999" not in dense[0].chunk.text.lower()
    assert "ts-999" in sparse[0].chunk.text.lower()
    fused = rrf_fuse([dense, sparse], top_n=16)
    assert any("ts-999" in h.chunk.text.lower() for h in fused)
    alpha_hybrid(dense, sparse, alpha=0.5, top_n=3)
    result = run_hybrid(q)
    blob = " ".join(h["text"] for h in result["hits"]).lower()
    assert "ts-999" in blob
