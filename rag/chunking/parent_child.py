"""Parent-child retrieval: index the child, generate from the stored parent."""

from __future__ import annotations

from rag.chunkers import Chunk, parent_child as build_parent_child
from rag.corpus import Document
from rag.retrieve import Hit


def build(doc: Document, child_size: int = 40) -> list[Chunk]:
    return build_parent_child(doc, child_size=child_size)


def expand_to_parent(hits: list[Hit]) -> list[Hit]:
    """Replace each child hit text with its parent for generation."""
    out: list[Hit] = []
    seen: set[str] = set()
    for hit in hits:
        parent = hit.chunk.parent_text or hit.chunk.text
        parent_id = str((hit.chunk.metadata or {}).get("parent_id") or hit.chunk.chunk_id)
        if parent_id in seen:
            continue
        seen.add(parent_id)
        chunk = Chunk(
            chunk_id=parent_id,
            doc_id=hit.chunk.doc_id,
            title=hit.chunk.title,
            text=parent,
            metadata={**hit.chunk.metadata, "expanded": "parent"},
            parent_text=parent,
        )
        out.append(Hit(chunk=chunk, score=hit.score, source="parent_child"))
    return out
