# %% [markdown]
# # Tenant metadata filter
#
# Lab `lab_s16_gov` / `part_1`.

# %%
"""Tenant metadata filter."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.gov import allowed, prefilter

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
east = prefilter(chunks, "helix-east")
west = prefilter(chunks, "helix-west")
print("all", len(chunks), "east", len(east), "west", len(west))
print("east > west (FAQ is helix-east)", len(east) > len(west))
print("denied west faq", [c.chunk_id for c in chunks if c.doc_id == "faq" and not allowed(c, "helix-west")])
