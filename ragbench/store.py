"""On-disk index. This is the folder the lecture opens: model name, chunks, vectors."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from ragbench.chunkers import Chunk
from ragbench.embed import ToyEmbedder
from ragbench.retrieve import Hit, bm25_search, rerank_lexical, rrf_fuse
from ragbench.settings import LAB_EMBEDDER, STORE_ROOT


@dataclass
class Index:
    name: str
    path: Path
    chunks: list[Chunk]
    vectors: np.ndarray
    manifest: dict
    embedder: ToyEmbedder

    def dense_search(self, query: str, k: int = 5) -> list[Hit]:
        q = self.embedder.embed(query)
        qn = float(np.linalg.norm(q)) or 1.0
        norms = np.linalg.norm(self.vectors, axis=1)
        denom = np.where(norms * qn == 0, 1.0, norms * qn)
        scores = (self.vectors @ q) / denom
        order = np.argsort(scores)[::-1][:k]
        return [
            Hit(chunk=self.chunks[int(i)], score=float(scores[int(i)]), source="dense")
            for i in order
        ]

    def hybrid_search(self, query: str, k: int = 8, rerank: bool = True) -> list[Hit]:
        dense = self.dense_search(query, k=max(k, 8))
        sparse = bm25_search(query, self.chunks, k=max(k, 8))
        fused = rrf_fuse([dense, sparse], top_n=max(k * 2, 10))
        if rerank:
            return rerank_lexical(query, fused, keep=k)
        return fused[:k]


def _row(chunk: Chunk) -> dict:
    return {
        "chunk_id": chunk.chunk_id,
        "doc_id": chunk.doc_id,
        "title": chunk.title,
        "text": chunk.text,
        "metadata": chunk.metadata,
        "parent_text": chunk.parent_text,
    }


def _chunk(row: dict) -> Chunk:
    return Chunk(
        chunk_id=row["chunk_id"],
        doc_id=row["doc_id"],
        title=row["title"],
        text=row["text"],
        metadata=row.get("metadata") or {},
        parent_text=row.get("parent_text"),
    )


def save_index(
    name: str,
    chunks: list[Chunk],
    vectors: np.ndarray,
    extra: dict | None = None,
    root: Path | None = None,
) -> Index:
    dest = (root or STORE_ROOT) / name
    dest.mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": name,
        "chunk_count": len(chunks),
        "embedder": dict(LAB_EMBEDDER),
        "built_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": ["manifest.json", "chunks.jsonl", "vectors.npy"],
    }
    if extra:
        manifest.update(extra)
    (dest / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with (dest / "chunks.jsonl").open("w", encoding="utf-8") as fh:
        for ch in chunks:
            fh.write(json.dumps(_row(ch), ensure_ascii=False) + "\n")
    np.save(dest / "vectors.npy", vectors)
    embedder = ToyEmbedder(semantic_mode=bool(LAB_EMBEDDER["semantic_mode"]))
    return Index(
        name=name,
        path=dest,
        chunks=chunks,
        vectors=vectors,
        manifest=manifest,
        embedder=embedder,
    )


def load_index(name: str, root: Path | None = None) -> Index | None:
    dest = (root or STORE_ROOT) / name
    man_path = dest / "manifest.json"
    if not man_path.is_file():
        return None
    manifest = json.loads(man_path.read_text(encoding="utf-8"))
    chunks: list[Chunk] = []
    with (dest / "chunks.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                chunks.append(_chunk(json.loads(line)))
    vectors = np.load(dest / "vectors.npy")
    mode = bool((manifest.get("embedder") or {}).get("semantic_mode", True))
    return Index(
        name=name,
        path=dest,
        chunks=chunks,
        vectors=vectors,
        manifest=manifest,
        embedder=ToyEmbedder(semantic_mode=mode),
    )


def print_card(index: Index) -> str:
    emb = index.manifest.get("embedder") or {}
    swap = ", ".join(emb.get("production_swap") or [])
    lines = [
        f"INDEX     {index.path.as_posix()}",
        f"chunks    {index.manifest.get('chunk_count')}",
        f"chunker   {index.manifest.get('chunker')} {index.manifest.get('chunk_kwargs') or ''}",
        f"embedder  {emb.get('name')}  dim={emb.get('dim')}  semantic_mode={emb.get('semantic_mode')}",
        f"why       {emb.get('why')}",
        f"swap      {swap}",
        f"search    {index.manifest.get('search')}",
        f"files     {', '.join(index.manifest.get('files') or [])}",
    ]
    return "\n".join(lines) + "\n"
