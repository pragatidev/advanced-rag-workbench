"""Parent-child, print both sizes."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import parent_child
from rag.chunking.parent_child import expand_to_parent
from rag.corpus import load_documents
from rag.retrieve import Hit

docs = load_documents()
chunks = []
for d in docs:
    chunks.extend(parent_child(d, child_size=40))
print("children", len(chunks))
print("parents", len({c.metadata["parent_id"] for c in chunks}))
hit = next(c for c in chunks if "revenue grew by 3%" in c.text.lower())
print("chunk_id", hit.chunk_id)
print("child_chars", hit.metadata["child_chars"], "parent_chars", hit.metadata["parent_chars"])
print("parent_id", hit.metadata["parent_id"])
print("parent names ACME:", "acme" in (hit.parent_text or "").lower())
print("child:", hit.text[:160])
print("parent:", (hit.parent_text or "")[:160].replace("\n", " / "))
big = next(c for c in chunks if c.metadata.get("parent_id") == "filing_q2_2023:parent:1")
print("big_parent_id", big.metadata["parent_id"])
print("big_child_chars", big.metadata["child_chars"], "big_parent_chars", big.metadata["parent_chars"])
expanded = expand_to_parent([Hit(chunk=hit, score=1.0, source="child")])
print("expanded_id", expanded[0].chunk.chunk_id)
print("expanded_chars", len(expanded[0].chunk.text))
