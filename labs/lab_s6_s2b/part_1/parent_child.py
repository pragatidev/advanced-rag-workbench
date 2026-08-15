"""Parent-child, print both sizes."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import parent_child
from rag.corpus import load_documents

docs = load_documents()
chunks = []
for d in docs:
    chunks.extend(parent_child(d, child_size=40))
print("children", len(chunks))
hit = next(c for c in chunks if "revenue grew by 3%" in c.text.lower())
print("child_chars", hit.metadata["child_chars"], "parent_chars", hit.metadata["parent_chars"])
print("parent_id", hit.metadata["parent_id"])
print("parent names ACME:", "acme" in (hit.parent_text or "").lower())
print("child:", hit.text[:160])
