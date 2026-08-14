"""S4.2 screen walk. Same question. Dense store vs hybrid store. Print top hits."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ragbench.index import build_index, print_card

QUESTION = "What does error code TS-999 mean?"

# %% Build both indexes (writes store/naive and store/hybrid)
naive = build_index("naive")
hybrid = build_index("hybrid")
print("NAIVE")
print(print_card(naive))
print("HYBRID")
print(print_card(hybrid))

# %% Same question, two retrievers
print(f"question  {QUESTION}\n")
print("dense (naive store)")
for i, hit in enumerate(naive.dense_search(QUESTION, k=3), start=1):
    print(f"  #{i}  {hit.score:.3f}  {hit.chunk.chunk_id}  {hit.chunk.text[:90]!r}")

print("\nhybrid (BM25 + dense + RRF, stored chunks)")
for i, hit in enumerate(hybrid.hybrid_search(QUESTION, k=3), start=1):
    print(f"  #{i}  {hit.score:.3f}  {hit.chunk.chunk_id}  {hit.chunk.text[:90]!r}")
