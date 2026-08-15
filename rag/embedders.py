"""Embedding models used in this project.

Lab default (no download): HashEmbedder. Same idea as a tiny local model so
pytest and first clone stay offline.

Monday swap (real semantic model, no API key): Chroma's ONNX MiniLM
(all-MiniLM-L6-v2) or sentence-transformers. That is what most Python RAG
apps use locally.

Hosted swap: OpenAI text-embedding-3-small, Voyage voyage-3-lite.
Those need a key. We name them. We do not require them.
"""

from __future__ import annotations

import hashlib

import numpy as np

from rag.text import tokenize

DIM = 64

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


class HashEmbedder:
    """Offline stand-in. semantic_mode=True hides rare IDs (the TS-999 lesson)."""

    name = "HashEmbedder"
    dim = DIM

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
                acc += 0.05 * _hash_vec(tok, salt="id")
            else:
                acc += _hash_vec(tok, salt="lex")
        n = np.linalg.norm(acc)
        return acc / n if n else acc

    def encode(self, texts: list[str]) -> np.ndarray:
        return np.vstack([self.embed(t) for t in texts])


# Old name used in earlier tests and labs.
ToyEmbedder = HashEmbedder


def get_embedder(name: str | None = None):
    """Resolve an embedder from a settings name. Offline default is HashEmbedder."""
    from rag.settings import Settings

    raw = (name or Settings.embed_model or "hash").strip()
    key = raw.lower()
    if key in {"hash", "hashembedder", "toy", "toyembedder"}:
        return HashEmbedder(semantic_mode=True)
    if key in {"hash-lexical", "lexical", "hashembedder-lexical"}:
        return HashEmbedder(semantic_mode=False)
    if key in {"nomic-embed-text", "nomic-embed-text:v1.5", "mxbai-embed-large", "all-minilm"}:
        # Named local models. The lab stand-in stays HashEmbedder so clone stays offline.
        emb = HashEmbedder(semantic_mode=True)
        emb.name = raw
        return emb
    if "minilm" in key:
        return MiniLMEmbedder()
    emb = HashEmbedder(semantic_mode=True)
    emb.name = raw
    return emb


class MiniLMEmbedder:
    """Real local semantic model via Chroma ONNX (all-MiniLM-L6-v2). First call may download."""

    name = "all-MiniLM-L6-v2"
    dim = 384

    def __init__(self) -> None:
        from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

        self._fn = DefaultEmbeddingFunction()

    def embed(self, text: str) -> np.ndarray:
        return np.array(self._fn([text])[0], dtype=np.float64)

    def encode(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float64)
        return np.array(self._fn(texts), dtype=np.float64)


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


PRODUCTION_EMBEDDERS = [
    {
        "name": "all-MiniLM-L6-v2",
        "where": "local ONNX / sentence-transformers",
        "key": False,
        "used_in_this_repo": "MiniLMEmbedder and Chroma DefaultEmbeddingFunction",
    },
    {
        "name": "OpenAI text-embedding-3-small",
        "where": "hosted API",
        "key": True,
        "used_in_this_repo": "named swap only",
    },
    {
        "name": "Voyage voyage-3-lite",
        "where": "hosted API",
        "key": True,
        "used_in_this_repo": "named swap only",
    },
    {
        "name": "HashEmbedder",
        "where": "this repo, offline tests",
        "key": False,
        "used_in_this_repo": "pytest and the TS-999 miss demo",
    },
]
