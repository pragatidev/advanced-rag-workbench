"""Run two pipelines on the same question file. Write runs/<id>/metrics.json."""

from __future__ import annotations

import json
import time
from pathlib import Path

from ragbench.eval.cost import estimate
from ragbench.eval.metrics import context_recall, faithfulness, needles_hit
from ragbench.pipelines import PIPELINES

ROOT = Path(__file__).resolve().parents[2]
QUESTIONS = ROOT / "eval" / "questions.jsonl"
RUNS = ROOT / "runs"


def load_questions(path: Path | None = None) -> list[dict]:
    rows = []
    with (path or QUESTIONS).open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _score(row: dict, result: dict, elapsed: float, extra_generates: int = 0) -> dict:
    texts = [h["text"] for h in result["hits"]]
    return {
        "id": row["id"],
        "query_class": row.get("query_class"),
        "pipeline": result["pipeline"],
        "answer": result["answer"],
        "n_hits": len(result["hits"]),
        "context_recall": context_recall(row.get("gold_spans") or [], texts),
        "needles": needles_hit(row.get("needles") or [], texts),
        "faithfulness": faithfulness(result["answer"], texts),
        "latency_s": round(elapsed, 4),
        "cost": estimate(result["pipeline"], extra_generates=extra_generates),
        "chunk_ids": [h["chunk_id"] for h in result["hits"]],
    }


def run_eval(a: str = "naive", b: str = "hybrid", out_dir: Path | None = None) -> dict:
    if a not in PIPELINES or b not in PIPELINES:
        raise ValueError(f"unknown pipeline. have {sorted(PIPELINES)}")
    questions = load_questions()
    dest = out_dir or (RUNS / f"{a}_vs_{b}")
    dest.mkdir(parents=True, exist_ok=True)
    rows = []
    for q in questions:
        pack = {}
        for name in (a, b):
            t0 = time.perf_counter()
            result = PIPELINES[name](q["question"])
            elapsed = time.perf_counter() - t0
            extra = 1 if name == "hyde" else 0
            pack[name] = _score(q, result, elapsed, extra_generates=extra)
        rows.append(pack)
    summary = {
        "a": a,
        "b": b,
        "n": len(rows),
        "mean": {
            name: {
                metric: round(
                    sum(r[name][metric] for r in rows) / max(len(rows), 1),
                    4,
                )
                for metric in ("context_recall", "needles", "faithfulness")
            }
            for name in (a, b)
        },
        "rows": rows,
    }
    (dest / "metrics.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary
