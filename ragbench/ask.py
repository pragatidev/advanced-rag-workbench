"""The product. A chat widget, Slack bot, ticket desk, CLI, or harness skill all call this."""

from __future__ import annotations

import os
from pathlib import Path

from ragbench.envload import generate_mode, load_dotenv
from ragbench.loops.retrieve_gate import needs_corpus
from ragbench.observe import log_ask
from ragbench.pipelines import PIPELINES

ROOT_LOG = Path(__file__).resolve().parents[1] / "runs" / "ask.jsonl"


def run_ask(question: str, pipeline: str = "hybrid", generate: str | None = None) -> dict:
    """Retrieve, then generate. Call this from your app. Do not shell out to the CLI."""
    load_dotenv()
    os.environ["RAGBENCH_GENERATE"] = generate_mode(generate)
    if pipeline not in PIPELINES:
        raise ValueError(f"unknown pipeline: {pipeline}")
    if pipeline != "graph" and not needs_corpus(question):
        payload = {
            "pipeline": pipeline,
            "question": question,
            "answer": "REFUSE: question does not need the corpus.",
            "hits": [],
        }
    else:
        payload = PIPELINES[pipeline](question)
    log_ask(
        {
            "pipeline": payload.get("pipeline"),
            "question": question,
            "chunk_ids": [h.get("chunk_id") for h in payload.get("hits", [])],
        },
        ROOT_LOG,
    )
    return payload
