# %% [markdown]
# # Smash a real PDF table
#
# Lab `lab_s13_mm` / `part_1`.

# %%
"""Smash a real PDF table."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.multimodal import PDF_PATH, smash_report

rep = smash_report()
print("pdf", PDF_PATH)
print("chars", rep["chars"])
print("has_12420", rep["has_12420"])
print("row_intact", rep["row_intact"])
print("extract:", rep["extract"])
