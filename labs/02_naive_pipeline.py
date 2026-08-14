"""S2.2 screen walk. A program you step through, not a CLI dump.

In VS Code: click Run Cell on each # %% block (Python Interactive).
Or run the whole file: python labs/02_naive_pipeline.py

What this file is for:
  1. See which documents were loaded
  2. See how they were chunked
  3. See which embedding model ran (and what you would swap)
  4. See where the index was stored (open store/naive/)
  5. Retrieve, then generate
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ragbench.chunkers import chunk_corpus
from ragbench.corpus import load_documents
from ragbench.embed import ToyEmbedder
from ragbench.generate import generate_answer
from ragbench.settings import LAB_EMBEDDER
from ragbench.store import print_card, save_index

QUESTION = "What was ACME revenue growth in Q2 2023?"

# %% Stage 1: load the corpus (these are the files)
docs = load_documents()
print("STAGE 1  load")
print(f"  {len(docs)} documents from data/acme/")
for doc in docs:
    print(f"  {doc.doc_id:18}  {doc.path}")

# %% Stage 2: chunk (fixed size, no overlap: the naive default)
chunks = chunk_corpus(docs, "fixed", size=80, overlap=0)
print("\nSTAGE 2  chunk")
print(f"  chunker=fixed  size=80  overlap=0  ->  {len(chunks)} chunks")
lost = [
    c
    for c in chunks
    if "3%" in c.text or "3 percent" in c.text.lower()
]
print("  chunks that still contain the 3% sentence:")
for c in lost:
    has_acme = "acme" in c.text.lower()
    has_q2 = "q2" in c.text.lower()
    print(f"    {c.chunk_id}  acme={has_acme}  q2={has_q2}")
    print(f"    {c.text[:220]}")

# %% Stage 3: name the embedding model
print("\nSTAGE 3  embedder")
print(f"  name           {LAB_EMBEDDER['name']}")
print(f"  dim            {LAB_EMBEDDER['dim']}")
print(f"  semantic_mode  {LAB_EMBEDDER['semantic_mode']}")
print(f"  role           {LAB_EMBEDDER['role']}")
print(f"  why            {LAB_EMBEDDER['why']}")
print("  production swap:")
for name in LAB_EMBEDDER["production_swap"]:
    print(f"    - {name}")
embedder = ToyEmbedder(semantic_mode=True)
vectors = embedder.encode([c.text for c in chunks])
print(f"  vectors.shape  {tuple(vectors.shape)}")

# %% Stage 4: store on disk (open this folder on screen)
index = save_index(
    "naive",
    chunks,
    vectors,
    extra={
        "chunker": "fixed",
        "chunk_kwargs": {"size": 80, "overlap": 0},
        "contextual": False,
        "search": "dense",
        "doc_ids": [d.doc_id for d in docs],
        "doc_count": len(docs),
    },
)
print("\nSTAGE 4  store")
print(print_card(index))
print("  open store/naive/manifest.json  to see the model name again")
print("  open store/naive/chunks.jsonl   to see the text that was indexed")
print("  open store/naive/vectors.npy    the dense matrix (not human text)")

# %% Stage 5: retrieve from the store (not from a rebuilt RAM index)
hits = index.dense_search(QUESTION, k=3)
print("\nSTAGE 5  retrieve")
print(f"  question  {QUESTION}")
for i, hit in enumerate(hits, start=1):
    preview = hit.chunk.text.replace("\n", " ")[:160]
    print(f"  #{i}  {hit.score:.3f}  {hit.chunk.chunk_id}")
    print(f"      {preview}")

# %% Stage 6: generate only from those hits
answer, meta = generate_answer(QUESTION, [h.chunk for h in hits], mode="extractive")
print("\nSTAGE 6  generate")
print(f"  generator  {meta.get('generator')}")
print(f"  answer     {answer}")
