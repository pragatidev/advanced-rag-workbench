"""Toy embedder that can reproduce the TS-999 miss without a 400MB model.

semantic_mode=True downweights rare IDs so 'error codes in general' ranks above TS-999.
BM25 still sees the raw token. That is the hybrid lesson.
"""

from __future__ import annotations

import hashlib
import math

import numpy as np

from rag.text import tokenize

DIM = 64

# Words that live in the "error advice" neighborhood.
_SEMANTIC = {
    "error": 0,
    "errors": 0,
    "code": 1,
    "codes": 1,
    "log": 2,
    "logs": 2,
    "retry": 3,
    "transient": 3,
    "worker": 4,
    "ticket": 5,
    "general": 6,
    "guidance": 6,
}


def _hash_vec(token: str, salt: str = "") -> np.ndarray:
    seed = f"{salt}:{token}".encode("utf-8")
    data = hashlib.sha256(seed).digest()
    while len(data) < DIM * 4:
        data += hashlib.sha256(data).digest()
    raw = np.frombuffer(data[: DIM * 4], dtype=np.uint32).copy().astype(np.float64)
    vec = (raw % 1000) / 1000.0 - 0.5
    n = np.linalg.norm(vec)
    return vec / n if n else vec


class ToyEmbedder:
    def __init__(self, semantic_mode: bool = True) -> None:
        self.semantic_mode = semantic_mode

    def embed(self, text: str) -> np.ndarray:
        tokens = tokenize(text)
        if not tokens:
            return np.zeros(DIM, dtype=np.float64)
        acc = np.zeros(DIM, dtype=np.float64)
        for tok in tokens:
            if tok in _SEMANTIC:
                acc += _hash_vec(f"sem:{_SEMANTIC[tok]}", salt="cluster")
            elif self.semantic_mode and any(ch.isdigit() for ch in tok):
                # Rare IDs are almost invisible to the semantic view.
                acc += 0.05 * _hash_vec(tok, salt="id")
            else:
                acc += _hash_vec(tok, salt="lex")
        n = np.linalg.norm(acc)
        return acc / n if n else acc

    def encode(self, texts: list[str]) -> np.ndarray:
        return np.vstack([self.embed(t) for t in texts])


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)
