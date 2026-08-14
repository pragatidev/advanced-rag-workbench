"""Naive RAG: fixed chunks, semantic-only embedder, top-k cosine, stuffed prompt."""

from __future__ import annotations

from ragbench.chunkers import chunk_corpus
from ragbench.corpus import load_documents
from ragbench.embed import ToyEmbedder
from ragbench.generate import generate_answer
from ragbench.retrieve import dense_search


def run_naive(question: str, k: int = 3) -> dict:
    docs = load_documents()
    chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
    hits = dense_search(question, chunks, embedder=ToyEmbedder(semantic_mode=True), k=k)
    answer, gen = generate_answer(question, [h.chunk for h in hits])
    return {
        "pipeline": "naive",
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
