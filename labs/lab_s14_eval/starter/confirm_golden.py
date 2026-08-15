"""STARTER Confirm golden tags before you score. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

from rag.eval.golden import confirm_tags, load_golden

rows = load_golden()
rep = confirm_tags(rows)
print("n", rep["n"])
print("categories", rep["categories"])
print("canary_ids", rep["canary_ids"])
assert rep["ok"], rep
