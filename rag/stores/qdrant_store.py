"""Qdrant local client. Persist under store/qdrant/. No Docker required."""

from __future__ import annotations

from pathlib import Path

from rag.chunking import Chunk
from rag.retrieve import Hit
from rag.stores.base import STORE_DIR, StoreInfo, as_embeddings


class QdrantStore:
    backend = "qdrant"

    def __init__(self, collection: str = "naive", path: Path | None = None) -> None:
        from qdrant_client import QdrantClient

        self.collection_name = collection
        self.path = path or (STORE_DIR / "qdrant")
        self.path.mkdir(parents=True, exist_ok=True)
        self.client = QdrantClient(path=str(self.path))

    def reset(self) -> None:
        from qdrant_client.http.exceptions import UnexpectedResponse

        try:
            self.client.delete_collection(self.collection_name)
        except UnexpectedResponse:
            pass
        except Exception:
            # local client may raise a generic error if missing
            try:
                self.client.delete_collection(self.collection_name)
            except Exception:
                pass

    def _ensure(self, dim: int) -> None:
        from qdrant_client.models import Distance, VectorParams

        names = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def add(self, chunks: list[Chunk], embeddings) -> None:
        from qdrant_client.models import PointStruct

        if not chunks:
            return
        embeddings = as_embeddings(chunks, embeddings)
        dim = len(embeddings[0])
        self._ensure(dim)
        points = []
        for i, (chunk, vec) in enumerate(zip(chunks, embeddings)):
            points.append(
                PointStruct(
                    id=i,
                    vector=list(map(float, vec)),
                    payload={
                        "chunk_id": chunk.chunk_id,
                        "doc_id": chunk.doc_id,
                        "title": chunk.title,
                        "text": chunk.text,
                        "metadata": chunk.metadata,
                    },
                )
            )
        # stable ids from hash of chunk_id so upsert is repeatable
        import hashlib

        for p, chunk in zip(points, chunks):
            digest = hashlib.sha256(chunk.chunk_id.encode("utf-8")).hexdigest()[:16]
            p.id = int(digest, 16) % (2**63)
        self.client.upsert(collection_name=self.collection_name, points=points)

    def query(self, embedding: list[float], k: int = 5) -> list[Hit]:
        names = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in names:
            return []
        vec = list(map(float, embedding))
        try:
            hits_raw = self.client.query_points(
                collection_name=self.collection_name,
                query=vec,
                limit=k,
            ).points
        except Exception:
            hits_raw = self.client.search(
                collection_name=self.collection_name,
                query_vector=vec,
                limit=k,
            )
        hits: list[Hit] = []
        for pt in hits_raw:
            payload = pt.payload or {}
            hits.append(
                Hit(
                    chunk=Chunk(
                        chunk_id=str(payload.get("chunk_id") or pt.id),
                        doc_id=str(payload.get("doc_id") or ""),
                        title=str(payload.get("title") or ""),
                        text=str(payload.get("text") or ""),
                        metadata=payload.get("metadata") or {},
                    ),
                    score=float(pt.score or 0.0),
                    source="qdrant",
                )
            )
        return hits

    def info(self) -> StoreInfo:
        n = 0
        names = [c.name for c in self.client.get_collections().collections]
        if self.collection_name in names:
            n = self.client.count(self.collection_name).count
        return StoreInfo(
            backend="qdrant",
            persist_path=str(self.path),
            note=f"collection={self.collection_name} count={n}",
            count=n,
            collection=self.collection_name,
        )
