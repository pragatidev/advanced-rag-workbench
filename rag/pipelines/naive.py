"""Naive RAG: fixed chunks, HashEmbedder, Chroma cosine, stuffed prompt."""

from __future__ import annotations

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.generate import generate_answer
from rag.stores.chroma_store import ChromaStore


def _hits_payload(hits) -> list[dict]:
    return [
        {
            "chunk_id": h.chunk.chunk_id,
            "score": h.score,
            "text": h.chunk.text,
            "doc_id": h.chunk.doc_id,
        }
        for h in hits
    ]


class NaivePipeline:
    name = "naive"

    def __call__(self, question: str, k: int = 3, persist: bool = False) -> dict:
        return run_naive(question, k=k, persist=persist)


def run_naive(question: str, k: int = 3, persist: bool = False) -> dict:
    docs = load_documents()
    chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
    embedder = HashEmbedder(semantic_mode=True)
    store = ChromaStore("naive", persist=persist)
    if persist:
        store.reset()
    else:
        store.reset()
    store.add(chunks, embedder.encode([c.text for c in chunks]).tolist())
    hits = store.query(embedder.embed(question).tolist(), k=k)
    answer, gen = generate_answer(question, [h.chunk for h in hits])
    return {
        "pipeline": "naive",
        "question": question,
        "answer": answer,
        "answer_source": "retrieved_text",
        "generator": gen,
        "store": store.info().__dict__,
        "hits": _hits_payload(hits),
    }
