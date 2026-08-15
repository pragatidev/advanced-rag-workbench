# %% [markdown]
# # Run the final comparison
#
# Lab `lab_s17_cap` / `part_1`.

# %%
"""Run the final comparison."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.runner import run_eval

summary = run_eval(a="naive", b="hybrid", out_dir=ROOT / "runs" / "naive_vs_hybrid")
print("n", summary["n"])
print("naive", summary["mean"]["naive"])
print("hybrid", summary["mean"]["hybrid"])
