# %% [markdown]
# # Tag the golden file and the canaries
#
# Lab `lab_s4_diagnose` / `part_2`.

# %%
"""Tag the golden file and the canaries."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.golden import REQUIRED_CATEGORIES, confirm_tags, load_golden

rows = load_golden()
report = confirm_tags(rows)
print("n", report["n"])
print("categories", report["categories"])
print("canary_ids", report["canary_ids"])
print("required", list(REQUIRED_CATEGORIES))
print("missing_categories", report["missing_categories"])
print("missing_canary_categories", report["missing_canary_categories"])
assert report["ok"], report
