"""pgvector in Postgres. Optional. Start with docker compose -f docker-compose.yml up -d."""

from __future__ import annotations

import json
import os
from pathlib import Path

from rag.chunking import Chunk
from rag.retrieve import Hit
from rag.stores.base import StoreInfo

DEFAULT_URL = "postgresql://acme:acme@127.0.0.1:5432/acme_rag"


def database_url() -> str:
    return os.environ.get("DATABASE_URL") or os.environ.get("PGVECTOR_URL") or DEFAULT_URL


def available() -> bool:
    try:
        import psycopg

        with psycopg.connect(database_url(), connect_timeout=2) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
        return True
    except Exception:
        return False


class PgVectorStore:
    backend = "pgvector"

    def __init__(self, collection: str = "naive") -> None:
        import psycopg

        self.collection_name = collection
        self.url = database_url()
        self.conn = psycopg.connect(self.url)
        self.conn.autocommit = True
        with self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS rag_chunks (
                    chunk_id TEXT PRIMARY KEY,
                    collection TEXT NOT NULL,
                    doc_id TEXT,
                    title TEXT,
                    body TEXT,
                    metadata JSONB,
                    embedding vector
                )
                """
            )

    def reset(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM rag_chunks WHERE collection = %s",
                (self.collection_name,),
            )

    def add(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        dim = len(embeddings[0])
        with self.conn.cursor() as cur:
            # Widen the column if needed (first insert wins the dim).
            cur.execute(
                f"ALTER TABLE rag_chunks ALTER COLUMN embedding TYPE vector({dim})"
            )
            for chunk, vec in zip(chunks, embeddings):
                lit = "[" + ",".join(str(float(x)) for x in vec) + "]"
                cur.execute(
                    """
                    INSERT INTO rag_chunks
                        (chunk_id, collection, doc_id, title, body, metadata, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s::jsonb, %s::vector)
                    ON CONFLICT (chunk_id) DO UPDATE SET
                        collection = EXCLUDED.collection,
                        doc_id = EXCLUDED.doc_id,
                        title = EXCLUDED.title,
                        body = EXCLUDED.body,
                        metadata = EXCLUDED.metadata,
                        embedding = EXCLUDED.embedding
                    """,
                    (
                        chunk.chunk_id,
                        self.collection_name,
                        chunk.doc_id,
                        chunk.title,
                        chunk.text,
                        json.dumps(chunk.metadata or {}, ensure_ascii=False),
                        lit,
                    ),
                )

    def query(self, embedding: list[float], k: int = 5) -> list[Hit]:
        lit = "[" + ",".join(str(float(x)) for x in embedding) + "]"
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT chunk_id, doc_id, title, body, metadata,
                       1 - (embedding <=> %s::vector) AS score
                FROM rag_chunks
                WHERE collection = %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (lit, self.collection_name, lit, k),
            )
            rows = cur.fetchall()
        hits: list[Hit] = []
        for chunk_id, doc_id, title, body, metadata, score in rows:
            meta = metadata if isinstance(metadata, dict) else (metadata or {})
            hits.append(
                Hit(
                    chunk=Chunk(
                        chunk_id=chunk_id,
                        doc_id=doc_id or "",
                        title=title or "",
                        text=body or "",
                        metadata=meta,
                    ),
                    score=float(score or 0.0),
                    source="pgvector",
                )
            )
        return hits

    def info(self) -> StoreInfo:
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM rag_chunks WHERE collection = %s",
                (self.collection_name,),
            )
            n = cur.fetchone()[0]
        return StoreInfo(
            backend="pgvector",
            persist_path=self.url.split("@")[-1] if "@" in self.url else self.url,
            note=f"collection={self.collection_name} count={n}",
        )
