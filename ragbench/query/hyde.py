"""HyDE: invent a fake document, retrieve neighbors of that document.

The fake text is allowed to be wrong. Retrieval must ground it. Cost: one extra generate.
"""

from __future__ import annotations

from ragbench.chunkers import chunk_corpus
from ragbench.corpus import load_documents
from ragbench.embed import ToyEmbedder
from ragbench.generate import generate_answer
from ragbench.retrieve import dense_search


def hypothetical_document(question: str) -> str:
    # Intentionally specific and possibly wrong. That is the paper.
    return (
        f"A technical note that answers: {question}. "
        "It names the company, the quarter, the error id, or the table cell the question wants."
    )


def run_hyde(question: str, k: int = 4) -> dict:
    docs = load_documents()
    chunks = chunk_corpus(docs, "recursive")
    fake = hypothetical_document(question)
    hits = dense_search(fake, chunks, embedder=ToyEmbedder(semantic_mode=False), k=k)
    answer, gen = generate_answer(question, [h.chunk for h in hits])
    return {
        "pipeline": "hyde",
        "question": question,
        "hypothetical": fake,
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
