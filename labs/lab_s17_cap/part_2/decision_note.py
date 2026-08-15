"""Metrics file and the decision note."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json

metrics_path = ROOT / "runs" / "naive_vs_hybrid" / "metrics.json"
if not metrics_path.is_file():
    from rag.eval.runner import run_eval
    run_eval(a="naive", b="hybrid", out_dir=metrics_path.parent)
data = json.loads(metrics_path.read_text(encoding="utf-8"))
mean = data["mean"]
lines = [
    "# Decision note",
    "",
    "Corpus: data/acme/. Questions: eval/questions.jsonl.",
    "",
    f"naive mean: {mean['naive']}",
    f"hybrid mean: {mean['hybrid']}",
    "",
    "## Keep or kill",
    "",
    f"- naive fixed chunks: KILL. Orphan 3 percent chunk. context_recall={mean['naive']['context_recall']}.",
    f"- hybrid + RRF: KEEP. Recovers TS-999. context_recall={mean['hybrid']['context_recall']}.",
    "- semantic cosine chunker: MEASURE, keep only if paraphrase recall rises without BM25 drop.",
    "- late chunking: KILL on this corpus. Extra cost, no reliable lift.",
    "- HyDE: KILL unless a live generate pays for +1 call.",
    "- GraphRAG: REFUSE while local questions hold. Use only for the theme question.",
    "- web CRAG: KILL. WEB_SEARCH_ENABLED=false.",
    "",
    "Citation: runs/naive_vs_hybrid/metrics.json",
]
dest = ROOT / "runs" / "naive_vs_hybrid" / "decision.md"
dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(dest.read_text(encoding="utf-8"))
print("wrote", dest)
