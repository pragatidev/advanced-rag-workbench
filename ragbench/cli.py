"""Workbench CLI. python -m ragbench ask "..." --pipeline naive"""

from __future__ import annotations

import argparse
import json
import sys

import os

from ragbench.envload import generate_mode, load_dotenv
from ragbench.loops.retrieve_gate import needs_corpus
from ragbench.observe import log_ask
from ragbench.pipelines import PIPELINES

ROOT_LOG = __import__("pathlib").Path(__file__).resolve().parents[1] / "runs" / "ask.jsonl"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ragbench")
    sub = parser.add_subparsers(dest="cmd", required=True)

    ask = sub.add_parser("ask")
    ask.add_argument("question")
    ask.add_argument("--pipeline", default="naive", choices=sorted(PIPELINES))
    ask.add_argument(
        "--generate",
        default=None,
        choices=["extractive", "api"],
        help="extractive = no key. api = OpenAI-compatible (Qwen Token Plan).",
    )

    ev = sub.add_parser("eval")
    ev.add_argument("--a", default="naive")
    ev.add_argument("--b", default="hybrid")

    args = parser.parse_args(argv)

    if args.cmd == "ask":
        load_dotenv()
        os.environ["RAGBENCH_GENERATE"] = generate_mode(args.generate)
        if args.pipeline != "graph" and not needs_corpus(args.question):
            payload = {
                "pipeline": args.pipeline,
                "question": args.question,
                "answer": "REFUSE: question does not need the corpus.",
                "hits": [],
            }
        else:
            payload = PIPELINES[args.pipeline](args.question)
        log_ask(
            {
                "pipeline": payload.get("pipeline"),
                "question": args.question,
                "chunk_ids": [h.get("chunk_id") for h in payload.get("hits", [])],
            },
            ROOT_LOG,
        )
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 0

    from ragbench.eval.runner import run_eval

    summary = run_eval(a=args.a, b=args.b)
    sys.stdout.write(json.dumps(summary["mean"], ensure_ascii=False, indent=2) + "\n")
    return 0
