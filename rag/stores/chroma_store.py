"""Chroma PersistentClient. Open store/chroma/ after you build."""

from __future__ import annotations

from pathlib import Path

from rag.chunking import Chunk
from rag.retrieve import Hit
from rag.stores.base import STORE_DIR, StoreInfo


class ChromaStore:
    backend = "chroma"

    def __init__(
        self,
        collection: str = "naive",
        path: Path | None = None,
        persist: bool = True,
    ) -> None:
        import chromadb

        self.collection_name = collection
        self.persist = persist
        if persist:
            self.path = path or (STORE_DIR / "chroma")
            self.path.mkdir(parents=True, exist_ok=True)
            self.client = chromadb.PersistentClient(path=str(self.path))
        else:
            self.path = None
            self.client = chromadb.EphemeralClient()
        self.col = self.client.get_or_create_collection(
            name=collection,
            metadata={"hnsw:space": "cosine"},
        )

    def reset(self) -> None:
        self.client.delete_collection(self.collection_name)
        self.col = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        self.col.upsert(
            ids=[c.chunk_id for c in chunks],
            documents=[c.text for c in chunks],
            metadatas=[
                {
                    "doc_id": c.doc_id,
                    "title": c.title,
                    "chunker": str((c.metadata or {}).get("chunker") or ""),
                    "tenant": str((c.metadata or {}).get("tenant") or "shared"),
                }
                for c in chunks
            ],
            embeddings=embeddings,
        )

    def query(self, embedding: list[float], k: int = 5) -> list[Hit]:
        if self.col.count() == 0:
            return []
        out = self.col.query(
            query_embeddings=[embedding],
            n_results=min(k, self.col.count()),
            include=["documents", "metadatas", "distances"],
        )
        hits: list[Hit] = []
        ids = (out.get("ids") or [[]])[0]
        docs = (out.get("documents") or [[]])[0]
        metas = (out.get("metadatas") or [[]])[0]
        dists = (out.get("distances") or [[]])[0]
        for i, cid in enumerate(ids):
            meta = metas[i] if i < len(metas) else {}
            dist = float(dists[i]) if i < len(dists) else 0.0
            hits.append(
                Hit(
                    chunk=Chunk(
                        chunk_id=cid,
                        doc_id=str(meta.get("doc_id") or ""),
                        title=str(meta.get("title") or ""),
                        text=docs[i] if i < len(docs) else "",
                        metadata=dict(meta or {}),
                    ),
                    score=1.0 - dist,
                    source="chroma",
                )
            )
        return hits

    def info(self) -> StoreInfo:
        return StoreInfo(
            backend="chroma",
            persist_path=None if self.path is None else str(self.path),
            note=f"collection={self.collection_name} count={self.col.count()}",
        )
