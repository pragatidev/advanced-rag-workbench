"""Hybrid: recursive chunks, BM25 + Chroma dense, RRF, lexical rerank."""

from __future__ import annotations

from rag.chunkers import chunk_corpus, contextualize
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.generate import generate_answer
from rag.retrieve import bm25_search, rerank_lexical, rrf_fuse
from rag.stores.chroma_store import ChromaStore


def run_hybrid(question: str, k: int = 4, contextual: bool = True, persist: bool = False) -> dict:
    docs = load_documents()
    chunks = chunk_corpus(docs, "recursive")
    if contextual:
        chunks = [contextualize(c) for c in chunks]
    embedder = HashEmbedder(semantic_mode=True)
    store = ChromaStore("hybrid", persist=persist)
    store.reset()
    store.add(chunks, embedder.encode([c.text for c in chunks]).tolist())
    dense = store.query(embedder.embed(question).tolist(), k=max(k, 8))
    sparse = bm25_search(question, chunks, k=max(k, 8))
    fused = rrf_fuse([dense, sparse], top_n=max(k * 2, 10))
    hits = rerank_lexical(question, fused, keep=k)
    answer, gen = generate_answer(question, [h.chunk for h in hits])
    return {
        "pipeline": "hybrid",
        "question": question,
        "answer": answer,
        "generator": gen,
        "store": store.info().__dict__,
        "hits": [
            {
                "chunk_id": h.chunk.chunk_id,
                "score": h.score,
                "text": h.chunk.text,
                "doc_id": h.chunk.doc_id,
            }
            for h in hits
        ],
    }
