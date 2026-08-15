"""Sentence-window retrieval.

Index one sentence. At query time, reconstruct a neighbor window from
metadata (prev/next sentence ids). This is not parent-child: the window
is assembled, not stored as a second object.
"""

from __future__ import annotations

from rag.chunkers import Chunk
from rag.corpus import Document
from rag.retrieve import Hit
from rag.text import split_sentences


def build(doc: Document) -> list[Chunk]:
    sentences = split_sentences(doc.text)
    chunks: list[Chunk] = []
    for i, sent in enumerate(sentences):
        chunks.append(
            Chunk(
                chunk_id=f"{doc.doc_id}:sent:{i}",
                doc_id=doc.doc_id,
                title=doc.title,
                text=sent,
                metadata={
                    **doc.metadata,
                    "chunker": "sentence_window",
                    "sent_index": i,
                    "sent_count": len(sentences),
                    "prev_id": f"{doc.doc_id}:sent:{i - 1}" if i > 0 else "",
                    "next_id": f"{doc.doc_id}:sent:{i + 1}" if i + 1 < len(sentences) else "",
                },
            )
        )
    return chunks


def window_text(chunks: list[Chunk], center: Chunk, radius: int = 3) -> str:
    same = [c for c in chunks if c.doc_id == center.doc_id]
    same.sort(key=lambda c: int((c.metadata or {}).get("sent_index") or 0))
    idx = int((center.metadata or {}).get("sent_index") or 0)
    lo = max(0, idx - radius)
    hi = min(len(same), idx + radius + 1)
    return " ".join(c.text for c in same[lo:hi])


def expand_window(hits: list[Hit], corpus_chunks: list[Chunk], radius: int = 3) -> list[Hit]:
    out: list[Hit] = []
    seen: set[str] = set()
    for hit in hits:
        key = f"{hit.chunk.doc_id}:{int((hit.chunk.metadata or {}).get('sent_index') or 0)}"
        if key in seen:
            continue
        seen.add(key)
        text = window_text(corpus_chunks, hit.chunk, radius=radius)
        chunk = Chunk(
            chunk_id=f"{hit.chunk.chunk_id}:win",
            doc_id=hit.chunk.doc_id,
            title=hit.chunk.title,
            text=text,
            metadata={**hit.chunk.metadata, "expanded": "sentence_window", "radius": radius},
            parent_text=text,
        )
        out.append(Hit(chunk=chunk, score=hit.score, source="sentence_window"))
    return out
