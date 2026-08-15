"""SOLUTION Two pipelines and metrics.json."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.eval.runner import run_eval

summary = run_eval(a="naive", b="hybrid", out_dir=ROOT / "runs" / "naive_vs_hybrid")
print("n", summary["n"])
print("mean", summary["mean"])
print("metrics", ROOT / "runs" / "naive_vs_hybrid" / "metrics.json")
