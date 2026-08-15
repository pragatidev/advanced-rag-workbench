"""STARTER Load the ACME corpus and cut fixed chunks. Fill the TODOs. part_1 is the first working slice."""
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
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
print("documents", len(docs))
print("files", [d.path for d in docs])
print("chunks", len(chunks))
span = next(c.text for c in chunks if "revenue grew by 3%" in c.text.lower())
print("three_percent_span:")
print(span)
