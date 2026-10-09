"""Auto-merge leaves into a parent."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunking.auto_merge import merge_hits
from rag.chunkers import parent_child
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.retrieve import dense_search

docs = load_documents()
leaves = []
for d in docs:
    leaves.extend(parent_child(d, child_size=40))
emb = HashEmbedder(semantic_mode=False)
query = "What was ACME revenue growth in Q2 2023?"
hits = dense_search(query, leaves, embedder=emb, k=8)
print("query", query)
print("threshold", 0.5)
print("leaves", len(hits))
for h in hits:
    meta = h.chunk.metadata or {}
    print(" ", h.chunk.chunk_id, meta.get("parent_id"), "leaf", meta.get("leaf_index"))
merged = merge_hits(hits, threshold=0.5)
print("merged", len(merged))
print("parent_replacement", any(h.source == "auto_merge" for h in merged))
for h in merged:
    meta = h.chunk.metadata or {}
    print(" ", h.source, h.chunk.chunk_id, "merged_leaves", meta.get("merged_leaves"))
