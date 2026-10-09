"""The index is a derived view of the source.

Upsert by a stable chunk key. Tombstone hides a dead id from retrieve.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

import numpy as np

from rag.embed import ToyEmbedder


def span_hash(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()[:12]


def stable_chunk_key(doc_id: str, text: str) -> str:
    return f"{doc_id}:{span_hash(text)}"


@dataclass
class DerivedRow:
    chunk_id: str
    doc_id: str
    text: str
    vector: np.ndarray
    live: bool = True


class DerivedIndex:
    def __init__(self, embedder: ToyEmbedder | None = None) -> None:
        self.embedder = embedder or ToyEmbedder(semantic_mode=False)
        self.rows: dict[str, DerivedRow] = {}
        self.tombstones: set[str] = set()
        self.embed_calls = 0

    def upsert(self, doc_id: str, text: str) -> str:
        cid = stable_chunk_key(doc_id, text)
        vec = self.embedder.embed(text)
        self.embed_calls += 1
        self.rows[cid] = DerivedRow(cid, doc_id, text, vec, True)
        self.tombstones.discard(cid)
        return cid

    def tombstone(self, chunk_id: str) -> None:
        self.tombstones.add(chunk_id)
        row = self.rows.get(chunk_id)
        if row is not None:
            row.live = False

    def retrieve(self, query: str, k: int = 3) -> list[tuple[str, str, float]]:
        q = self.embedder.embed(query)
        scored: list[tuple[str, str, float]] = []
        for row in self.rows.values():
            if not row.live or row.chunk_id in self.tombstones:
                continue
            denom = float(np.linalg.norm(q) * np.linalg.norm(row.vector)) or 1.0
            score = float(np.dot(q, row.vector) / denom)
            scored.append((row.chunk_id, row.text, score))
        scored.sort(key=lambda item: item[2], reverse=True)
        return scored[:k]
