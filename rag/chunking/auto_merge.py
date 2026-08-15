"""Auto-merging retrieval.

Index leaves. If enough leaves under one parent appear in the shortlist,
replace those leaves with the stored parent. Haystack/LlamaIndex idea,
thresholded on this corpus without a second library.
"""

from __future__ import annotations

from collections import defaultdict

from rag.chunkers import Chunk, parent_child
from rag.corpus import Document
from rag.retrieve import Hit


def build(doc: Document, child_size: int = 40) -> list[Chunk]:
    return parent_child(doc, child_size=child_size)


def merge_hits(hits: list[Hit], threshold: float = 0.5) -> list[Hit]:
    """If >= threshold of a parent's retrieved leaves are present, emit the parent."""
    by_parent: dict[str, list[Hit]] = defaultdict(list)
    parent_leaf_total: dict[str, int] = {}
    for hit in hits:
        pid = str((hit.chunk.metadata or {}).get("parent_id") or "")
        if not pid:
            by_parent[hit.chunk.chunk_id].append(hit)
            continue
        by_parent[pid].append(hit)
        parent_leaf_total[pid] = max(
            parent_leaf_total.get(pid, 0),
            int((hit.chunk.metadata or {}).get("leaf_index") or 0) + 1,
        )
    # We only know retrieved leaves, not the true sibling count. Use a simple
    # rule: two or more leaves of the same parent, or a single leaf that is
    # already most of a tiny parent, become the parent.
    merged: list[Hit] = []
    for pid, group in by_parent.items():
        parent_text = group[0].chunk.parent_text
        should_merge = parent_text is not None and (
            len(group) >= 2 or (threshold <= 1 and len(group) / max(parent_leaf_total.get(pid, 1), 1) >= threshold)
        )
        if should_merge and parent_text:
            score = max(h.score for h in group)
            chunk = Chunk(
                chunk_id=pid,
                doc_id=group[0].chunk.doc_id,
                title=group[0].chunk.title,
                text=parent_text,
                metadata={**group[0].chunk.metadata, "expanded": "auto_merge", "merged_leaves": len(group)},
                parent_text=parent_text,
            )
            merged.append(Hit(chunk=chunk, score=score, source="auto_merge"))
        else:
            merged.extend(group)
    merged.sort(key=lambda h: h.score, reverse=True)
    return merged
