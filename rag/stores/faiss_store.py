"""FAISS IndexFlatIP on L2-normalized vectors. Files live in store/faiss/."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from rag.chunking import Chunk
from rag.retrieve import Hit
from rag.stores.base import STORE_DIR, StoreInfo, as_embeddings


def _norm(mat: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    return mat / norms


class FaissStore:
    backend = "faiss"

    def __init__(self, collection: str = "naive", path: Path | None = None) -> None:
        self.collection_name = collection
        self.path = path or (STORE_DIR / "faiss" / collection)
        self.path.mkdir(parents=True, exist_ok=True)
        self._index = None
        self._chunks: list[Chunk] = []
        self._load()

    def _index_path(self) -> Path:
        return self.path / "index.faiss"

    def _meta_path(self) -> Path:
        return self.path / "chunks.jsonl"

    def _load(self) -> None:
        import faiss

        if not self._index_path().is_file():
            self._index = None
            self._chunks = []
            return
        self._index = faiss.read_index(str(self._index_path()))
        self._chunks = []
        with self._meta_path().open(encoding="utf-8") as fh:
            for line in fh:
                row = json.loads(line)
                self._chunks.append(
                    Chunk(
                        chunk_id=row["chunk_id"],
                        doc_id=row["doc_id"],
                        title=row["title"],
                        text=row["text"],
                        metadata=row.get("metadata") or {},
                    )
                )

    def _save(self) -> None:
        import faiss

        if self._index is None:
            return
        faiss.write_index(self._index, str(self._index_path()))
        with self._meta_path().open("w", encoding="utf-8") as fh:
            for c in self._chunks:
                fh.write(
                    json.dumps(
                        {
                            "chunk_id": c.chunk_id,
                            "doc_id": c.doc_id,
                            "title": c.title,
                            "text": c.text,
                            "metadata": c.metadata,
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )

    def reset(self) -> None:
        self._index = None
        self._chunks = []
        for p in (self._index_path(), self._meta_path()):
            if p.is_file():
                p.unlink()

    def add(self, chunks: list[Chunk], embeddings) -> None:
        import faiss

        if not chunks:
            return
        embeddings = as_embeddings(chunks, embeddings)
        mat = _norm(np.asarray(embeddings, dtype=np.float32))
        if self._index is None:
            self._index = faiss.IndexFlatIP(mat.shape[1])
        self._index.add(mat)
        self._chunks.extend(chunks)
        self._save()

    def query(self, embedding: list[float], k: int = 5) -> list[Hit]:
        if self._index is None or self._index.ntotal == 0:
            return []
        q = _norm(np.asarray([embedding], dtype=np.float32))
        take = min(k, self._index.ntotal)
        scores, idxs = self._index.search(q, take)
        hits: list[Hit] = []
        for score, i in zip(scores[0], idxs[0]):
            if int(i) < 0:
                continue
            hits.append(
                Hit(chunk=self._chunks[int(i)], score=float(score), source="faiss")
            )
        return hits

    def info(self) -> StoreInfo:
        n = 0 if self._index is None else int(self._index.ntotal)
        return StoreInfo(
            backend="faiss",
            persist_path=str(self.path),
            note=f"IndexFlatIP ntotal={n}",
            count=n,
            collection=self.collection_name,
        )
