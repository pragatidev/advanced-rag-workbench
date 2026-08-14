"""S3.2 screen walk. Same corpus, three chunkers, print counts and the 3% sentence."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ragbench.chunkers import CHUNKERS, chunk_corpus
from ragbench.corpus import load_documents

docs = load_documents()

# %% Compare chunkers on the same files
print("chunker          chunks  3% chunks  3% also names ACME or Q2")
for name in CHUNKERS:
    kwargs = {"size": 80, "overlap": 0} if name == "fixed" else {}
    chunks = chunk_corpus(docs, name, **kwargs) if kwargs else chunk_corpus(docs, name)
    hit = [c for c in chunks if "3%" in c.text]
    named = [c for c in hit if "acme" in c.text.lower() or "q2" in c.text.lower()]
    print(f"{name:16}  {len(chunks):6}  {len(hit):9}  {len(named)}")

# %% Show one recursive chunk that keeps the heading near the number
rec = chunk_corpus(docs, "recursive")
keep = next((c for c in rec if "3%" in c.text), None)
print("\nrecursive chunk that holds the 3% sentence:")
if keep:
    print(f"  {keep.chunk_id}")
    print(f"  {keep.text[:400]}")
