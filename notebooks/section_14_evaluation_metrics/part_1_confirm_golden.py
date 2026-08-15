# %% [markdown]
# # Confirm golden tags before you score
#
# Lab `lab_s14_eval` / `part_1`.

# %%
"""Confirm golden tags before you score."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.golden import confirm_tags, load_golden

rows = load_golden()
rep = confirm_tags(rows)
print("n", rep["n"])
print("categories", rep["categories"])
print("canary_ids", rep["canary_ids"])
assert rep["ok"], rep
