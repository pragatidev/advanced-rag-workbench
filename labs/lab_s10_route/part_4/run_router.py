"""Mixed traffic and the route log."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from collections import Counter

from rag.query.router import route

traffic = [
    "Good morning, how are you?",
    "What does error code TS-999 mean?",
    "How many paid seats did ACME have in Q2?",
    "What are the main themes in this ACME corpus?",
    "What was ACME revenue growth in Q2 2023?",
    "Thanks",
    "Can helix-east reset a password?",
]
hist = Counter()
for q in traffic:
    r = route(q)
    hist[r["route"]] += 1
    print(f"{r['route']:8} {r.get('source') or '-':16} {q}")
print("histogram", dict(hist))
