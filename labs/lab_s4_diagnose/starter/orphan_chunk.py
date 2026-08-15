"""STARTER Find the orphan 3 percent chunk. Fill the TODOs. part_1 is the first working slice."""
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
orphans = [c for c in chunks if "revenue grew by 3%" in c.text.lower()]
assert orphans
for c in orphans:
    low = c.text.lower()
    print("chunk_id", c.chunk_id)
    print("contains ACME:", "acme" in low)
    print("contains Q2:", "q2" in low)
    print(c.text)
    print("---")
