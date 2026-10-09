"""Multi-query and measure rewrite diversity."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.query.rewrite import multi_query, ngram_overlap

q = "What was ACME revenue growth in Q2 2023?"
qs = multi_query(q)
print("n", len(qs))
for item in qs:
    print("-", item)
pairs = ngram_overlap(qs)
for i, j, score in pairs:
    print(f"pair {i}-{j}", round(score, 3))
uniq = {t.lower() for t in qs}
max_overlap = max(score for _, _, score in pairs)
print("diversity", len(uniq), "of", len(qs))
print("max_overlap", round(max_overlap, 3))
print("fuse", "yes" if max_overlap < 0.5 else "no")
