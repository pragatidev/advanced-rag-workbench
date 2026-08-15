# %% [markdown]
# # Load the ACME corpus and cut fixed chunks
#
# Lab `lab_s3_naive` / `part_1`.

# %%
"""Load the ACME corpus and cut fixed chunks."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
print("documents", len(docs))
print("files", [d.path for d in docs])
print("chunks", len(chunks))
span = next(c.text for c in chunks if "revenue grew by 3%" in c.text.lower())
print("three_percent_span:")
print(span)
