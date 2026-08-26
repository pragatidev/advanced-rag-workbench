# %% [markdown]
# # S13.1 Why text splitters smash tables
#
# Same KPI table, two views. A reading-order PDF extract shears the row.
# A layout parser (or the labeled fallback) restores the cell.

# %%
"""S13.1: smash a PDF table, then restore the row."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.multimodal import smash_report, parse_tables

print("=== smash ===")
rep = smash_report()
print("pdf data/acme/tables/q2_kpis.pdf")
print("chars", rep["chars"])
print("has_12420", rep["has_12420"])
print("row_intact", rep["row_intact"])
print("extract:")
print(rep["extract"])
print()
print("=== restore ===")
out = parse_tables()
print("parser", out["parser"])
print("note", out["note"])
for row in out["rows"]:
    print("-", row["text"])
print("has_12420", any("12420" in r["text"] for r in out["rows"]))
