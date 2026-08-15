"""A chunk is one cut piece of a real document — look at a full ACME chunk."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import fixed_size
from rag.corpus import load_documents

doc = next(item for item in load_documents() if item.doc_id == "filing_q2_2023")
chunks = fixed_size(doc, size=80, overlap=0)
print("document", doc.title)
print("path", doc.path)
print("chunk_count", len(chunks))
print("one_full_chunk:")
print(chunks[0].text)
