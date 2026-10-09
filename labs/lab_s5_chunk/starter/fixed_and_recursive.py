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
# TODO: run fixed size 80 overlap 0, then recursive with its default
fixed = chunk_corpus(docs, "fixed", size=80, overlap=0)
rec = chunk_corpus(docs, "recursive")
print("fixed", len(fixed))
print("recursive", len(rec))

filing = next(d for d in docs if d.doc_id == "filing_q2_2023")
parts = [p.strip() for p in filing.text.split("\n## ")]
print("heading parts", len(parts))
for i, part in enumerate(parts):
    low = part.lower()
    print(
        "part",
        i,
        "words",
        len(part.split()),
        "names ACME:",
        "acme" in low,
        "holds 3pct:",
        "revenue grew by 3%" in low,
    )


def report(name, chunks):
    # TODO: hunt the 3 percent sentence and print whether that strip still names ACME
    hit = next(c for c in chunks if "revenue grew by 3%" in c.text.lower())
    print(name, "3pct chunk_id", hit.chunk_id)
    print(name, "3pct names ACME:", "acme" in hit.text.lower())
    print(hit.text)
    print("---")


report("fixed", fixed)
report("recursive", rec)
