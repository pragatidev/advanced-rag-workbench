"""Run the final comparison. Same runner as S14, on the stack you kept."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.runner import run_eval

OUT = ROOT / "runs" / "naive_vs_hybrid"
summary = run_eval(a="naive", b="hybrid", out_dir=OUT)
print("=== same runner, stack you kept ===")
print("a", summary["a"])
print("b", summary["b"])
print("n", summary["n"])
print("naive", summary["mean"]["naive"])
print("hybrid", summary["mean"]["hybrid"])
print("metrics", OUT / "metrics.json")
