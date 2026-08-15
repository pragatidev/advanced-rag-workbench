# %% [markdown]
# # Run fixed and recursive chunkers
#
# Lab `lab_s5_chunk` / `part_1`.

# %%
"""Run fixed and recursive chunkers."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents

docs = load_documents()
fixed = chunk_corpus(docs, "fixed", size=80, overlap=0)
rec = chunk_corpus(docs, "recursive")
print("fixed", len(fixed))
print("recursive", len(rec))
hit = next(c for c in rec if "revenue grew by 3%" in c.text.lower())
print("recursive still holds 3 percent:", hit.chunk_id)
print(hit.text[:240])
