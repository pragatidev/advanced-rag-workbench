"""Cosine-breakpoint semantic chunking.

Embed consecutive sentences. Cut when similarity drops below a percentile
of the pairwise scores. This is the LlamaIndex SemanticSplitter idea,
implemented here without that dependency.
"""

from __future__ import annotations

import numpy as np

from rag.chunkers import Chunk
from rag.corpus import Document
from rag.embedders import HashEmbedder, cosine
from rag.text import split_sentences


def pairwise_similarities(sentences: list[str], embedder=None) -> list[float]:
    embedder = embedder or HashEmbedder(semantic_mode=False)
    if len(sentences) < 2:
        return []
    vecs = embedder.encode(sentences)
    return [cosine(vecs[i], vecs[i + 1]) for i in range(len(vecs) - 1)]


def cut_mask(sims: list[float], percentile: float = 95.0) -> list[bool]:
    """True means cut AFTER this sentence (between i and i+1)."""
    if not sims:
        return []
    # A 95 percentile breakpoint cuts the most dissimilar 5 percent of joints.
    cutoff = float(np.percentile(np.asarray(sims, dtype=np.float64), 100.0 - percentile))
    return [s <= cutoff for s in sims]


def cosine_breakpoint_chunks(
    doc: Document,
    percentile: float = 95.0,
    embedder=None,
) -> list[Chunk]:
    embedder = embedder or HashEmbedder(semantic_mode=False)
    sentences = split_sentences(doc.text)
    if not sentences:
        return []
    if len(sentences) == 1:
        return [
            Chunk(
                chunk_id=f"{doc.doc_id}:sem:0",
                doc_id=doc.doc_id,
                title=doc.title,
                text=sentences[0],
                metadata={**doc.metadata, "chunker": "semantic_cosine", "sentences": 1},
            )
        ]
    sims = pairwise_similarities(sentences, embedder=embedder)
    cuts = cut_mask(sims, percentile=percentile)
    groups: list[list[str]] = [[sentences[0]]]
    for i, sent in enumerate(sentences[1:], start=0):
        if cuts[i]:
            groups.append([sent])
        else:
            groups[-1].append(sent)
    chunks: list[Chunk] = []
    for n, group in enumerate(groups):
        text = " ".join(group)
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}:sem:{n}",
                doc_id=doc.doc_id,
                title=doc.title,
                text=text,
                metadata={
                    **doc.metadata,
                    "chunker": "semantic_cosine",
                    "sentences": len(group),
                    "percentile": percentile,
                },
            )
        )
    return chunks
