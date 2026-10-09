"""Embedder version cutover.

A v3 query against a v1 column returns a cosine number and no error.
Production pattern: side-by-side columns, then a feature-flag flip.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from rag.embed import DIM, _hash_vec, cosine, tokenize


class VersionedEmbedder:
    """Offline stand-in. The salt is the version. v1 and v3 are different spaces."""

    dim = DIM

    def __init__(self, version: str) -> None:
        self.version = version

    def embed(self, text: str) -> np.ndarray:
        tokens = tokenize(text)
        if not tokens:
            return np.zeros(DIM, dtype=np.float64)
        acc = np.zeros(DIM, dtype=np.float64)
        salt = f"ver:{self.version}"
        for tok in tokens:
            acc += _hash_vec(tok, salt=salt)
        n = np.linalg.norm(acc)
        return acc / n if n else acc


@dataclass
class ColumnRow:
    chunk_id: str
    text: str
    vector: np.ndarray


class DualColumnIndex:
    """Two embedding columns and one live flag.

    retrieve never raises on a mixed query. Cosine still returns a number.
    """

    def __init__(self) -> None:
        self.columns: dict[str, dict[str, ColumnRow]] = {"v1": {}, "v3": {}}
        self.live = "v1"
        self.shadow = False
        self.embed_calls = 0

    def fill_column(
        self,
        version: str,
        chunks: list[tuple[str, str]],
        embedder: VersionedEmbedder | None = None,
    ) -> int:
        emb = embedder or VersionedEmbedder(version)
        if emb.version != version:
            raise ValueError(f"embedder version {emb.version} does not match column {version}")
        col = self.columns.setdefault(version, {})
        for chunk_id, text in chunks:
            vec = emb.embed(text)
            self.embed_calls += 1
            col[chunk_id] = ColumnRow(chunk_id, text, vec)
        return len(col)

    def retrieve(
        self,
        query: str,
        query_version: str,
        column: str | None = None,
        k: int = 3,
    ) -> tuple[list[tuple[str, str, float]], dict[str, object]]:
        col_name = self.live if column is None else column
        emb = VersionedEmbedder(query_version)
        q = emb.embed(query)
        scored: list[tuple[str, str, float]] = []
        for row in self.columns.get(col_name, {}).values():
            scored.append((row.chunk_id, row.text, cosine(q, row.vector)))
        scored.sort(key=lambda item: item[2], reverse=True)
        meta: dict[str, object] = {
            "error_raised": False,
            "query_version": query_version,
            "column": col_name,
            "mixed": query_version != col_name,
        }
        return scored[:k], meta

    def flip(self, to_version: str) -> str:
        if to_version not in self.columns:
            raise KeyError(to_version)
        self.live = to_version
        return self.live
