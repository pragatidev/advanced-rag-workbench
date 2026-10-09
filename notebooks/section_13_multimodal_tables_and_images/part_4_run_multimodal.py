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

from rag.multimodal import multimodal_chunks
from rag.retrieve import bm25_search

chunks = multimodal_chunks()
print("chunks", len(chunks))
for c in chunks:
    print(c.chunk_id)

print()
print("=== table question ===")
q_table = "paid_seats in Q2"
table_hits = bm25_search(q_table, chunks, k=3)
print("query", q_table)
for i, h in enumerate(table_hits, 1):
    print(f"{i} {h.chunk.chunk_id}")
print(table_hits[0].chunk.text)
print("12420", "12420" in table_hits[0].chunk.text)

print()
print("=== figure question ===")
q_figure = "how many seats in the south region"
figure_hits = bm25_search(q_figure, chunks, k=3)
print("query", q_figure)
for i, h in enumerate(figure_hits, 1):
    print(f"{i} {h.chunk.chunk_id}")
print(figure_hits[0].chunk.text)
print("South 2000", "South 2000" in figure_hits[0].chunk.text)
