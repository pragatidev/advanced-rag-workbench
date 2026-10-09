"""The fixed cut on the ACME filing, both pieces, and which piece holds the name and which the number."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import fixed_size
from rag.corpus import load_documents

doc = next(item for item in load_documents() if item.doc_id == "filing_q2_2023")
chunks = fixed_size(doc, size=80, overlap=0)
print("document", doc.title, "| fixed cut, 80 words per chunk, chunk_count", len(chunks))
for i, c in enumerate(chunks):
    text = c.text
    if "Results of operations" in text:
        j = text.index("## Results of operations")
        window = "... " + text[j : j + 84] + " ..."
    else:
        window = text[:64] + " ..."
    print(f"--- chunk {i} ---  {window}")
    print(f"has_ACME {'ACME' in text}   has_3pct {'3%' in text}")
