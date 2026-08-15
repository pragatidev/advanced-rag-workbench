"""STARTER Run fixed and recursive chunkers. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

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
