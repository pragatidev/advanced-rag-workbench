# %% [markdown]
# # Prepend document context
#
# Lab `lab_s8_rerank` / `part_1`.

# %%
"""Prepend document context."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus, contextualize
from rag.corpus import load_documents

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
orphan = next(c for c in chunks if "revenue grew by 3%" in c.text.lower())
ctx = contextualize(orphan)
print("before ACME", "acme" in orphan.text.lower())
print("after ACME", "acme" in ctx.text.lower())
print(ctx.text[:240])
