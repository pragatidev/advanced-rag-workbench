"""STARTER Run the final comparison. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

from rag.eval.runner import run_eval

summary = run_eval(a="naive", b="hybrid", out_dir=ROOT / "runs" / "naive_vs_hybrid")
print("n", summary["n"])
print("naive", summary["mean"]["naive"])
print("hybrid", summary["mean"]["hybrid"])
