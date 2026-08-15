"""Dense, BM25, RRF, optional rerank. Reciprocal Rank Fusion uses k=60 (Cormack 2009)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from rank_bm25 import BM25Okapi

from rag.chunkers import Chunk
from rag.embed import ToyEmbedder, cosine
from rag.text import tokenize

RRF_K = 60


@dataclass
class Hit:
    chunk: Chunk
    score: float
    source: str


def dense_search(
    query: str,
    chunks: list[Chunk],
    embedder: ToyEmbedder | None = None,
    k: int = 5,
) -> list[Hit]:
    embedder = embedder or ToyEmbedder(semantic_mode=True)
    q = embedder.embed(query)
    scored: list[Hit] = []
    for ch in chunks:
        scored.append(Hit(chunk=ch, score=cosine(q, embedder.embed(ch.text)), source="dense"))
    scored.sort(key=lambda h: h.score, reverse=True)
    return scored[:k]


def bm25_search(query: str, chunks: list[Chunk], k: int = 5) -> list[Hit]:
    corpus = [tokenize(ch.text) for ch in chunks]
    if not any(corpus):
        return []
    model = BM25Okapi(corpus)
    scores = model.get_scores(tokenize(query))
    order = np.argsort(scores)[::-1][:k]
    return [Hit(chunk=chunks[int(i)], score=float(scores[int(i)]), source="bm25") for i in order]


def rrf_fuse(lists: list[list[Hit]], k: int = RRF_K, top_n: int = 8) -> list[Hit]:
    """RRFscore(d) = sum 1 / (k + rank). Ranks are 1-based. Missing docs contribute 0."""
    acc: dict[str, tuple[float, Chunk]] = {}
    for ranked in lists:
        for rank, hit in enumerate(ranked, start=1):
            cid = hit.chunk.chunk_id
            add = 1.0 / (k + rank)
            if cid not in acc:
                acc[cid] = (add, hit.chunk)
            else:
                acc[cid] = (acc[cid][0] + add, acc[cid][1])
    fused = [Hit(chunk=ch, score=score, source="rrf") for score, ch in (
        (v[0], v[1]) for v in acc.values()
    )]
    fused.sort(key=lambda h: h.score, reverse=True)
    return fused[:top_n]


def rerank_lexical(query: str, hits: list[Hit], keep: int = 5) -> list[Hit]:
    """Cheap cross-encoder stand-in: overlap of query tokens with chunk tokens."""
    q = set(tokenize(query))
    scored: list[Hit] = []
    for hit in hits:
        c = set(tokenize(hit.chunk.text))
        overlap = len(q & c) / max(len(q), 1)
        scored.append(Hit(chunk=hit.chunk, score=overlap, source="rerank"))
    scored.sort(key=lambda h: h.score, reverse=True)
    return scored[:keep]


def alpha_hybrid(
    dense: list[Hit],
    sparse: list[Hit],
    alpha: float = 0.5,
    top_n: int = 8,
) -> list[Hit]:
    """alpha * dense + (1-alpha) * sparse after min-max normalize.

    Unbounded BM25 scores swamp cosine unless you scale. That is the lesson.
    """

    def _norm(hits: list[Hit]) -> dict[str, float]:
        if not hits:
            return {}
        scores = [h.score for h in hits]
        lo, hi = min(scores), max(scores)
        span = (hi - lo) or 1.0
        return {h.chunk.chunk_id: (h.score - lo) / span for h in hits}

    dn = _norm(dense)
    sn = _norm(sparse)
    by_id: dict[str, Chunk] = {}
    for h in dense + sparse:
        by_id[h.chunk.chunk_id] = h.chunk
    fused: list[Hit] = []
    for cid, chunk in by_id.items():
        score = alpha * dn.get(cid, 0.0) + (1.0 - alpha) * sn.get(cid, 0.0)
        fused.append(Hit(chunk=chunk, score=score, source=f"alpha:{alpha}"))
    fused.sort(key=lambda h: h.score, reverse=True)
    return fused[:top_n]


def hybrid_search(query: str, chunks: list[Chunk], k: int = 8, rerank: bool = True) -> list[Hit]:
    dense = dense_search(query, chunks, k=max(k, 8))
    sparse = bm25_search(query, chunks, k=max(k, 8))
    fused = rrf_fuse([dense, sparse], top_n=max(k * 2, 10))
    if rerank:
        return rerank_lexical(query, fused, keep=k)
    return fused[:k]
