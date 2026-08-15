"""STARTER Tenant metadata filter. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

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
