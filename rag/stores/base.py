"""One interface. Four local backends. Same chunks, same vectors, different store."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from rag.chunking import Chunk
from rag.retrieve import Hit


@dataclass
class StoreInfo:
    backend: str
    persist_path: str | None
    note: str


class VectorStore(Protocol):
    backend: str

    def reset(self) -> None: ...

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None: ...

    def query(self, embedding: list[float], k: int = 5) -> list[Hit]: ...

    def info(self) -> StoreInfo: ...


ROOT = Path(__file__).resolve().parents[2]
STORE_DIR = ROOT / "store"


PRODUCTION_STORES = [
    {
        "name": "Chroma",
        "kind": "embedded vector DB",
        "lab": True,
        "key": False,
        "path": "store/chroma",
        "why": "Default in this course. Persist to a folder. Metadata filters. What many Python apps ship first.",
    },
    {
        "name": "FAISS",
        "kind": "in-process index files",
        "lab": True,
        "key": False,
        "path": "store/faiss",
        "why": "Meta's library. Fast cosine/IP search. Common in research and high-QPS services.",
    },
    {
        "name": "Qdrant",
        "kind": "vector DB",
        "lab": True,
        "key": False,
        "path": "store/qdrant",
        "why": "Production vector DB with filters and hybrid features. This lab uses the local client.",
    },
    {
        "name": "pgvector",
        "kind": "Postgres extension",
        "lab": True,
        "key": False,
        "path": "Postgres (docker compose)",
        "why": "The production default when the app already has Postgres. Optional: docker compose up.",
    },
    {
        "name": "Pinecone",
        "kind": "hosted",
        "lab": False,
        "key": True,
        "path": None,
        "why": "Hosted. Same add/query shape. Not run here (needs a paid key).",
    },
    {
        "name": "Weaviate",
        "kind": "hosted or self-host",
        "lab": False,
        "key": True,
        "path": None,
        "why": "Another production store. Same shape. Not run here.",
    },
    {
        "name": "Milvus / Zilliz",
        "kind": "hosted or self-host",
        "lab": False,
        "key": True,
        "path": None,
        "why": "Large-scale ANN. Named so you can recognize it. Not run here.",
    },
]
