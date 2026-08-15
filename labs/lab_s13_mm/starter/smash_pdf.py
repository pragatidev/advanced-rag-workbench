"""STARTER Smash a real PDF table. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

from rag.multimodal import PDF_PATH, smash_report

rep = smash_report()
print("pdf", PDF_PATH)
print("chars", rep["chars"])
print("has_12420", rep["has_12420"])
print("row_intact", rep["row_intact"])
print("extract:", rep["extract"])
