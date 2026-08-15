# %% [markdown]
# # Embed the chunks and persist Chroma
#
# Lab `lab_s3_naive` / `part_2`.

# %%
"""Embed the chunks and persist Chroma."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import get_embedder
from rag.settings import Settings
from rag.stores.chroma_store import ChromaStore

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
embedder = get_embedder(Settings.embed_model)
print("embedder", embedder.name, "dim", embedder.dim)
store = ChromaStore("naive", persist=True)
store.reset()
store.add(chunks, embedder)
print(store.info())
