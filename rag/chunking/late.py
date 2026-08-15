"""Late chunking stand-in.

True late chunking runs a long-context encoder over the document, then
mean-pools the already-contextual token vectors inside each chunk span.
This lab copies that shape with HashEmbedder word vectors: embed the
whole document first, then pool the words that fall inside each chunk.
Labeled as a stand-in. A production swap is a long-context encoder.
"""

from __future__ import annotations

import numpy as np

from rag.chunkers import Chunk, recursive
from rag.corpus import Document
from rag.embedders import HashEmbedder
from rag.text import tokenize


def document_token_vectors(doc: Document, embedder=None) -> tuple[list[str], np.ndarray]:
    embedder = embedder or HashEmbedder(semantic_mode=False)
    tokens = tokenize(doc.text)
    if not tokens:
        return [], np.zeros((0, embedder.dim), dtype=np.float64)
    # Contextual stand-in: mix the document vector into every token vector.
    doc_vec = embedder.embed(doc.text)
    token_vecs = np.vstack([0.65 * embedder.embed(tok) + 0.35 * doc_vec for tok in tokens])
    return tokens, token_vecs


def pool_chunk(chunk: Chunk, tokens: list[str], token_vecs: np.ndarray) -> np.ndarray:
    wanted = set(tokenize(chunk.text))
    if not wanted or token_vecs.size == 0:
        return np.zeros(token_vecs.shape[1] if token_vecs.size else 64, dtype=np.float64)
    rows = [token_vecs[i] for i, tok in enumerate(tokens) if tok in wanted]
    if not rows:
        return np.zeros(token_vecs.shape[1], dtype=np.float64)
    acc = np.mean(np.vstack(rows), axis=0)
    n = np.linalg.norm(acc)
    return acc / n if n else acc


def late_vectors(docs: list[Document], chunks: list[Chunk] | None = None, embedder=None) -> tuple[list[Chunk], np.ndarray]:
    embedder = embedder or HashEmbedder(semantic_mode=False)
    if chunks is None:
        chunks = []
        for doc in docs:
            chunks.extend(recursive(doc))
    by_doc = {d.doc_id: d for d in docs}
    cache: dict[str, tuple[list[str], np.ndarray]] = {}
    vecs = []
    for ch in chunks:
        doc = by_doc.get(ch.doc_id)
        if doc is None:
            vecs.append(embedder.embed(ch.text))
            continue
        if ch.doc_id not in cache:
            cache[ch.doc_id] = document_token_vectors(doc, embedder=embedder)
        tokens, token_vecs = cache[ch.doc_id]
        vecs.append(pool_chunk(ch, tokens, token_vecs))
    return chunks, np.vstack(vecs) if vecs else np.zeros((0, embedder.dim), dtype=np.float64)
