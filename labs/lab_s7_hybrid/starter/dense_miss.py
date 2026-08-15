"""STARTER Watch dense miss TS-999. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.embedders import HashEmbedder
from rag.retrieve import dense_search

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
hits = dense_search("What does error code TS-999 mean?", chunks, embedder=HashEmbedder(semantic_mode=True), k=5)
print("dense top:")
for h in hits:
    flag = "TS-999" in h.chunk.text
    print(f"  {h.score:.3f} ts999={flag} {h.chunk.chunk_id}")
    print("   ", h.chunk.text[:140].replace("\n", " "))
print("top_is_ts999", "TS-999" in hits[0].chunk.text)
