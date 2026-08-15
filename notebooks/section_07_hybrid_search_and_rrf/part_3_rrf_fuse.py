# %% [markdown]
# # Fuse with Reciprocal Rank Fusion
#
# Lab `lab_s7_hybrid` / `part_3`.

# %%
"""Fuse with Reciprocal Rank Fusion."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.retrieve import bm25_search, dense_search, rrf_fuse

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
q = "What does error code TS-999 mean?"
dense = dense_search(q, chunks, embedder=HashEmbedder(semantic_mode=True), k=8)
sparse = bm25_search(q, chunks, k=8)
fused = rrf_fuse([dense, sparse], top_n=16)
print("dense", [h.chunk.chunk_id for h in dense[:3]])
print("bm25 ", [h.chunk.chunk_id for h in sparse[:3]])
print("rrf  ", [h.chunk.chunk_id for h in fused[:5]])
print("fused set holds TS-999", any("TS-999" in h.chunk.text for h in fused))
