# %% [markdown]
# # Multi-query and measure rewrite diversity
#
# Lab `lab_s9_query` / `part_2`.

# %%
"""Multi-query and measure rewrite diversity."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.query.rewrite import multi_query

q = "What was ACME revenue growth in Q2 2023?"
qs = multi_query(q)
print("n", len(qs))
for item in qs:
    print("-", item)
uniq = {t.lower() for t in qs}
print("diversity", len(uniq), "of", len(qs))
