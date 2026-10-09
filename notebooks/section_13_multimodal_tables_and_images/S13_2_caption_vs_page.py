# %% [markdown]
# # S13.2 When a caption is not enough
#
# Monday image path: caption as text. Page as image is the next tax.

# %%
"""S13.2: caption-as-text retrieve, then name the page-as-image tax."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.corpus import load_documents
from rag.multimodal import caption_chunks, multimodal_chunks, table_row_chunks
from rag.retrieve import bm25_search

print("=== caption ===")
caps = caption_chunks()
print("file data/acme/figures/caption.txt")
print("chunk_id", caps[0].chunk_id)
print("text:")
print(caps[0].text)
print("has_South_2000", "South 2000" in caps[0].text)
print()
print("=== retrieve caption ===")
chunks = multimodal_chunks()
print("chunks", len(chunks))
q = "how many seats in the south region"
hits = bm25_search(q, chunks, k=3)
print("query", q)
for i, h in enumerate(hits, 1):
    print(f"{i} {h.chunk.chunk_id}")
print("top_has_South_2000", "South 2000" in hits[0].chunk.text)
print()
print("=== table only miss ===")
docs = {d.doc_id: d for d in load_documents()}
rows = table_row_chunks(docs["q2_kpis"])
print("table_chunks", len(rows))
print("table_has_South_2000", any("South 2000" in r.text for r in rows))
print()
print("=== page as image ===")
print("name ColPali ColQwen")
print("kind late-interaction over page images")
print("lab installed False")
print("tax next")
