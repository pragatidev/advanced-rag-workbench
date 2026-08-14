"""Real vector stores. Local four: Chroma, FAISS, Qdrant, pgvector."""

from rag.stores.base import PRODUCTION_STORES, STORE_DIR, StoreInfo
from rag.stores.chroma_store import ChromaStore
from rag.stores.faiss_store import FaissStore
from rag.stores.qdrant_store import QdrantStore

__all__ = [
    "ChromaStore",
    "FaissStore",
    "QdrantStore",
    "PRODUCTION_STORES",
    "STORE_DIR",
    "StoreInfo",
    "open_store",
]


def open_store(backend: str, collection: str = "naive"):
    backend = backend.lower()
    if backend == "chroma":
        return ChromaStore(collection)
    if backend == "faiss":
        return FaissStore(collection)
    if backend == "qdrant":
        return QdrantStore(collection)
    if backend == "pgvector":
        from rag.stores.pgvector_store import PgVectorStore

        return PgVectorStore(collection)
    raise ValueError(f"unknown store backend: {backend}")
