"""Monday default: recursive chunks, BM25 + dense + RRF + lexical rerank."""

from __future__ import annotations

from ragbench.chunkers import chunk_corpus, contextualize
from ragbench.corpus import load_documents
from ragbench.generate import generate_answer
from ragbench.retrieve import hybrid_search


def run_hybrid(question: str, k: int = 4, contextual: bool = True) -> dict:
    from ragbench.store import load_index

    stored = load_index("hybrid") if contextual else None
    if stored is not None:
        hits = stored.hybrid_search(question, k=k, rerank=True)
    else:
        docs = load_documents()
        chunks = chunk_corpus(docs, "recursive")
        if contextual:
            chunks = [contextualize(c) for c in chunks]
        hits = hybrid_search(question, chunks, k=k, rerank=True)
    answer, gen = generate_answer(question, [h.chunk for h in hits])
    return {
        "pipeline": "hybrid",
        "question": question,
        "answer": answer,
        "generator": gen,
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
