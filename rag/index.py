"""Build a named index to store/<name>/. Production indexes on write. The lab does it on screen."""

from __future__ import annotations

from pathlib import Path

from rag.chunkers import chunk_corpus, contextualize
from rag.corpus import load_documents
from rag.embed import ToyEmbedder
from rag.settings import LAB_EMBEDDER, PROFILES
from rag.store import Index, print_card, save_index


def build_index(name: str, root: Path | None = None) -> Index:
    if name not in PROFILES:
        raise ValueError(f"unknown index profile: {name}")
    profile = PROFILES[name]
    docs = load_documents()
    chunks = chunk_corpus(docs, profile["chunker"], **profile["chunk_kwargs"])
    if profile["contextual"]:
        chunks = [contextualize(c) for c in chunks]
    embedder = ToyEmbedder(semantic_mode=bool(LAB_EMBEDDER["semantic_mode"]))
    vectors = embedder.encode([c.text for c in chunks])
    extra = {
        "chunker": profile["chunker"],
        "chunk_kwargs": profile["chunk_kwargs"],
        "contextual": profile["contextual"],
        "search": profile["search"],
        "doc_ids": [d.doc_id for d in docs],
        "doc_count": len(docs),
    }
    return save_index(name, chunks, vectors, extra=extra, root=root)


__all__ = ["build_index", "print_card"]
