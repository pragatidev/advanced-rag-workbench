"""Keep or kill each rewrite from cost."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.cost import estimate
from rag.eval.metrics import context_recall
from rag.pipelines.hybrid import run_hybrid
from rag.query.hyde import run_hyde
from rag.query.rewrite import multi_query

q = "What was ACME revenue growth in Q2 2023?"
gold = ["revenue grew by 3%"]
base = run_hybrid(q)
hyde = run_hyde(q)
print(f"{'method':12} {'recall':>7} {'gens':>5} {'usd':>6} keep?")
for name, result, extra in (
    ("hybrid", base, 0),
    ("hyde", hyde, 1),
    ("multi", base, len(multi_query(q)) - 1),
):
    rec = context_recall(gold, [h["text"] for h in result["hits"]])
    cost = estimate(name, extra_generates=extra)
    keep = rec > 0 and cost["generate_calls"] <= 2
    print(f"{name:12} {rec:7.2f} {cost['generate_calls']:5d} {cost['usd']:6.2f} {keep}")
