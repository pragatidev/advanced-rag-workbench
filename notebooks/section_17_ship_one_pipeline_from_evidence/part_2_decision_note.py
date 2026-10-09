# %% [markdown]
# # Metrics file and the decision note
#
# Lab `lab_s17_cap` / `part_2`.

# %%
"""Metrics file and the decision note."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

metrics_path = ROOT / "runs" / "naive_vs_hybrid" / "metrics.json"
if not metrics_path.is_file():
    from rag.eval.runner import run_eval

    run_eval(a="naive", b="hybrid", out_dir=metrics_path.parent)

data = json.loads(metrics_path.read_text(encoding="utf-8"))
mean = data["mean"]
present = {data["a"], data["b"]}


def row_for(qid: str, pipeline: str) -> dict:
    for pair in data["rows"]:
        hit = pair.get(pipeline) or {}
        if hit.get("id") == qid:
            return hit
    raise KeyError(qid)


def cite(hit: dict) -> str:
    return (
        f"row id={hit['id']} pipeline={hit['pipeline']} "
        f"context_recall={hit['context_recall']}"
    )


naive_ts = row_for("q_ts999", "naive")
hybrid_ts = row_for("q_ts999", "hybrid")

lines = [
    "# Decision note",
    "",
    "Corpus: data/acme/. Questions: eval/questions.jsonl.",
    f"File: {metrics_path.relative_to(ROOT).as_posix()}",
    f"n {data['n']}",
    f"pipelines in this file: {sorted(present)}",
    "",
    f"naive mean: {mean['naive']}",
    f"hybrid mean: {mean['hybrid']}",
    "",
    "## Keep or kill",
    "",
    f"- naive fixed chunks: KILL. {cite(naive_ts)}. answer={naive_ts['answer']}",
    f"- hybrid + RRF: KEEP. {cite(hybrid_ts)}. answer={hybrid_ts['answer']}",
    "- semantic cosine chunker: NO ROW in this file. Not a keep.",
    "- late chunking: NO ROW in this file. Not a keep.",
    "- HyDE: NO ROW in this file. Not a keep.",
    "- GraphRAG: NO ROW in this file. Not a keep.",
    "- web CRAG: NO ROW in this file. Not a keep.",
    "",
    "Rule: a technique list is not a decision. A cited row is a decision.",
    "Fluency is not a citation.",
]
dest = ROOT / "runs" / "naive_vs_hybrid" / "decision.md"
dest.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("=== cited row, not a list ===")
print(dest.read_text(encoding="utf-8"))
print("wrote", dest)
