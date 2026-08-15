"""Restore rows with Docling."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.multimodal import parse_tables

out = parse_tables()
print("parser", out["parser"])
print("note", out["note"])
for row in out["rows"]:
    print("-", row["text"])
print("has_12420", any("12420" in r["text"] for r in out["rows"]))
