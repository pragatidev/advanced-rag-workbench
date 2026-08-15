"""STARTER Prepend document context. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

from rag.chunkers import chunk_corpus, contextualize
from rag.corpus import load_documents

docs = load_documents()
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
orphan = next(c for c in chunks if "revenue grew by 3%" in c.text.lower())
ctx = contextualize(orphan)
print("before ACME", "acme" in orphan.text.lower())
print("after ACME", "acme" in ctx.text.lower())
print(ctx.text[:240])
