"""Reference for exercises/ex_orphan.py."""

from __future__ import annotations

from rag.chunkers import Chunk, chunk_corpus
from rag.corpus import load_documents


def find_orphan() -> Chunk:
    docs = load_documents()
    chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
    return next(c for c in chunks if "revenue grew by 3%" in c.text.lower())


if __name__ == "__main__":
    chunk = find_orphan()
    print(chunk.chunk_id)
    print("acme" in chunk.text.lower())
