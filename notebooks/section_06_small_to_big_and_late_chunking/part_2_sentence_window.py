# %% [markdown]
# # Retrieve a sentence with its window
#
# Lab `lab_s6_s2b` / `part_2`.

# %%
"""Retrieve a sentence with its window."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunking.sentence_window import build, expand_window, window_text
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.retrieve import dense_search

docs = load_documents()
chunks = []
for d in docs:
    chunks.extend(build(d))
emb = HashEmbedder(semantic_mode=False)
hits = dense_search("What was ACME revenue growth in Q2 2023?", chunks, embedder=emb, k=3)
center = next((h.chunk for h in hits if "3%" in h.chunk.text), hits[0].chunk)
print("sentence", center.text)
win = window_text(chunks, center, radius=3)
print("window_sentences ~", len(win.split(". ")))
print("ACME in window:", "acme" in win.lower())
print(win[:400])
expanded = expand_window(hits[:1], chunks, radius=3)
print("expanded_id", expanded[0].chunk.chunk_id)
