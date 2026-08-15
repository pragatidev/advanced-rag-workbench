# %% [markdown]
# # Auto-merge leaves into a parent
#
# Lab `lab_s6_s2b` / `part_3`.

# %%
"""Auto-merge leaves into a parent."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
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
hits = dense_search("What was ACME revenue growth in Q2 2023?", leaves, embedder=emb, k=8)
print("leaves", len(hits))
for h in hits[:5]:
    print(" ", h.chunk.chunk_id, h.chunk.metadata.get("parent_id"))
merged = merge_hits(hits, threshold=0.5)
print("merged", len(merged))
print("parent_replacement", any(h.source == "auto_merge" for h in merged))
