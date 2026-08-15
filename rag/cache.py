"""Semantic cache with three layers and one skip.

1. Exact string hit.
2. Near-neighbor hit (cosine above a threshold).
3. Personalized skip: do not reuse an answer that names a user or tenant.

A stale or personalized answer must not be amplified.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from rag.embedders import HashEmbedder, cosine


@dataclass
class CacheEntry:
    question: str
    answer: str
    tenant: str = "shared"
    personalized: bool = False
    vector: list[float] = field(default_factory=list)


class SemanticCache:
    def __init__(self, threshold: float = 0.92, embedder=None) -> None:
        self.threshold = threshold
        self.embedder = embedder or HashEmbedder(semantic_mode=False)
        self.entries: list[CacheEntry] = []
        self.hits = 0
        self.misses = 0
        self.skips = 0

    def lookup(self, question: str, tenant: str = "shared", personalized: bool = False) -> dict:
        if personalized:
            self.skips += 1
            return {"status": "SKIP_PERSONALIZED", "answer": None, "generate": True}
        qv = self.embedder.embed(question)
        best: CacheEntry | None = None
        best_sim = -1.0
        for entry in self.entries:
            if entry.tenant != tenant:
                continue
            if entry.question == question:
                self.hits += 1
                return {"status": "HIT", "answer": entry.answer, "generate": False, "sim": 1.0}
            sim = cosine(qv, self.embedder.embed(entry.question))
            if sim > best_sim:
                best_sim = sim
                best = entry
        if best is not None and best_sim >= self.threshold:
            self.hits += 1
            return {"status": "HIT", "answer": best.answer, "generate": False, "sim": best_sim}
        self.misses += 1
        return {"status": "MISS", "answer": None, "generate": True, "sim": best_sim}

    def store(self, question: str, answer: str, tenant: str = "shared", personalized: bool = False) -> None:
        if personalized:
            return
        self.entries.append(
            CacheEntry(
                question=question,
                answer=answer,
                tenant=tenant,
                personalized=personalized,
                vector=self.embedder.embed(question).tolist(),
            )
        )
