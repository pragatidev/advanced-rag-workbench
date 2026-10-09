"""STARTER Tenant metadata filter. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import allowed and prefilter from rag.gov
from rag.chunkers import chunk_corpus
from rag.corpus import load_documents
from rag.gov import allowed, prefilter

docs = load_documents()
chunks = chunk_corpus(docs, "recursive")
# TODO: stencil east and west with prefilter
east = prefilter(chunks, "helix-east")
west = prefilter(chunks, "helix-west")
faq = [c for c in chunks if c.doc_id == "faq"]

print("=== same index, two ACLs ===")
print("all", len(chunks))
print("east", len(east), "west", len(west))
print("east > west (FAQ is helix-east)", len(east) > len(west))
print("faq_ids", [c.chunk_id for c in faq])
print("faq_tenant", [c.metadata.get("tenant") for c in faq])
print("denied west faq", [c.chunk_id for c in faq if not allowed(c, "helix-west")])
shared_west = [c.chunk_id for c in west if c.metadata.get("tenant") == "shared"]
print("shared in west", len(shared_west))
print("shared stay visible", bool(shared_west))
