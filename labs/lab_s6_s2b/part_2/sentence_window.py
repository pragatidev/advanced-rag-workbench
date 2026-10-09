"""Retrieve a sentence with its window."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
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
print("sentences", len(chunks))
emb = HashEmbedder(semantic_mode=False)
query = "What was ACME revenue growth in Q2 2023?"
hits = dense_search(query, chunks, embedder=emb, k=3)
print("query", query)
for i, h in enumerate(hits):
    print("hit", i, h.chunk.chunk_id)
center = next((h.chunk for h in hits if "3%" in h.chunk.text), hits[0].chunk)
print("center_id", center.chunk_id)
print("sentence", center.text)
print(
    "sent_index",
    center.metadata["sent_index"],
    "sent_count",
    center.metadata["sent_count"],
)
print("prev_id", center.metadata["prev_id"])
print("next_id", center.metadata["next_id"])
print("chunker", center.metadata["chunker"])
print("parent_id", center.metadata.get("parent_id", ""))
win = window_text(chunks, center, radius=3)
print("radius", 3)
print("window_chars", len(win))
print("ACME in window:", "acme" in win.lower())
print("3pct in window:", "3%" in win)
print("window:")
print(win)
expanded = expand_window(hits[:1], chunks, radius=3)
print("expanded_id", expanded[0].chunk.chunk_id)
print("expanded_chars", len(expanded[0].chunk.text))
