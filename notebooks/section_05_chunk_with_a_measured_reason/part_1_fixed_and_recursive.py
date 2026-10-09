# %% [markdown]
# # Run fixed and recursive chunkers
#
# Lab `lab_s5_chunk` / `part_1`.

# %%
"""Run fixed and recursive chunkers."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.chunkers import chunk_corpus
from rag.corpus import load_documents

docs = load_documents()
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
    hit = next(c for c in chunks if "revenue grew by 3%" in c.text.lower())
    print(name, "3pct chunk_id", hit.chunk_id)
    print(name, "3pct names ACME:", "acme" in hit.text.lower())
    print(hit.text)
    print("---")


report("fixed", fixed)
report("recursive", rec)
