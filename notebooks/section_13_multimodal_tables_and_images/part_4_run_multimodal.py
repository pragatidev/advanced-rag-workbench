# %% [markdown]
# # Retrieve the table cell and caption
#
# Lab `lab_s13_mm` / `part_4`.

# %%
"""Retrieve the table cell and caption."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.embedders import HashEmbedder
from rag.multimodal import multimodal_chunks
from rag.retrieve import bm25_search, dense_search

chunks = multimodal_chunks()
emb = HashEmbedder(semantic_mode=False)
seats = bm25_search("How many paid seats did ACME have in Q2?", chunks, k=3)
south = dense_search("How many seats did the south region have?", chunks, embedder=emb, k=3)
print("12420 in top?", any("12420" in h.chunk.text for h in seats))
print("caption has South 2000?", any("South 2000" in h.chunk.text for h in south))
for h in seats[:2] + south[:2]:
    print(h.source, h.chunk.chunk_id, h.chunk.text[:120])
