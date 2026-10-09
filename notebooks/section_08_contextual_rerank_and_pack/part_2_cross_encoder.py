# %% [markdown]
# # Rerank a wide shortlist with a cross-encoder
#
# Lab `lab_s8_rerank` / `part_2`.

# %%
"""Rerank a wide shortlist with a cross-encoder."""
from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.rerank import rerank_cross_encoder
from rag.retrieve import bm25_search, dense_search, rrf_fuse

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
q = "What does error code TS-999 mean?"
wide = rrf_fuse(
    [
        dense_search(q, chunks, embedder=HashEmbedder(semantic_mode=True), k=20),
        bm25_search(q, chunks, k=20),
    ],
    top_n=20,
)
t0 = time.perf_counter()
ranked, backend = rerank_cross_encoder(q, wide, keep=5)
ms = (time.perf_counter() - t0) * 1000.0
print("backend", backend)
print("chunks", len(chunks), "wide", len(wide), "kept", len(ranked))
print(f"rerank_ms {ms:.1f}")
for h in ranked:
    print(f"  {h.score:.3f} {h.chunk.chunk_id} ts999={'TS-999' in h.chunk.text}")
