# %% [markdown]
# # BM25 hits the token
#
# Lab `lab_s7_hybrid` / `part_2`.

# %%
"""BM25 hits the token."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.retrieve import bm25_search

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
hits = bm25_search("What does error code TS-999 mean?", chunks, k=3)
print("bm25 top:")
for h in hits:
    print(f"  {h.score:.3f} ts999={'TS-999' in h.chunk.text} {h.chunk.chunk_id}")
print("BM25 top has TS-999", "TS-999" in hits[0].chunk.text)
assert "TS-999" in hits[0].chunk.text
