"""Four mixed asks through the adaptive router: none, single, multi, source.

The lab part in `labs/lab_s10_route/part_3/router.py` runs five asks and its two
source lines are a table cell and a policy. This file runs the four that show one
of each exit, including the named-source exit for an error code.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.query.router import route

questions = [
    "Good morning, how are you?",
    "What was ACME revenue growth in Q2 2023?",
    "What are the main themes in this ACME corpus?",
    "What does error code TS-999 mean?",
]

for q in questions:
    print(route(q), q)
