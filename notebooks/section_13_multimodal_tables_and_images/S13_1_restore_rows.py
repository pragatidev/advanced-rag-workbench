# %% [markdown]
# # S13.1 Restore the rows
#
# Docling when installed. Labeled markdown fallback otherwise.
# The parser name is printed so you always know which engine gave you the row.

# %%
"""S13.1: restore table rows and print parser, note, row text, has_12420."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.multimodal import parse_tables

out = parse_tables()
print("parser", out["parser"])
print("note", out["note"])
for row in out["rows"]:
    print("-", row["text"])
print("has_12420", any("12420" in r["text"] for r in out["rows"]))
