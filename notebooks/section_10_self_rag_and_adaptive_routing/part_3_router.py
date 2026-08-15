# %% [markdown]
# # Route none, single, multi, and source
#
# Lab `lab_s10_route` / `part_3`.

# %%
"""Route none, single, multi, and source."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
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
