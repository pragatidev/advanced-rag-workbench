# %% [markdown]
# # Rewrite one question, leave IDs alone
#
# Lab `lab_s9_query` / `part_1`.

# %%
"""Rewrite one question, leave IDs alone."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.query.rewrite import rewrite

q_id = "What does error code TS-999 mean?"
q_rev = "What was ACME revenue growth in Q2 2023?"
print("id_in", q_id)
print("id_out", rewrite(q_id))
assert "TS-999" in rewrite(q_id)
print("rev_in", q_rev)
print("rev_out", rewrite(q_rev))
