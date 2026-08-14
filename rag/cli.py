"""Lab CLI. python -m rag ask is a test harness around run_ask, not the product."""

from __future__ import annotations

import argparse
import json
import sys

from rag.ask import run_ask
from rag.pipelines import PIPELINES


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rag")
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

    serve = sub.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8787)

    idx = sub.add_parser("index")
    idx.add_argument("name", choices=["naive", "hybrid"])

    inspect = sub.add_parser("inspect")
    inspect.add_argument("name", nargs="?", default="naive", choices=["naive", "hybrid"])

    args = parser.parse_args(argv)

    if args.cmd == "ask":
        payload = run_ask(args.question, pipeline=args.pipeline, generate=args.generate)
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
        return 0

    if args.cmd == "serve":
        from rag.serve import serve_forever

        serve_forever(host=args.host, port=args.port)
        return 0

    if args.cmd == "index":
        from rag.index import build_index, print_card

        built = build_index(args.name)
        sys.stdout.write(print_card(built))
        return 0

    if args.cmd == "inspect":
        from rag.store import load_index, print_card

        loaded = load_index(args.name)
        if loaded is None:
            sys.stderr.write(f"no index at store/{args.name}/. Run: python -m rag index {args.name}\n")
            return 1
        sys.stdout.write(print_card(loaded))
        return 0

    from rag.eval.runner import run_eval

    summary = run_eval(a=args.a, b=args.b)
    sys.stdout.write(json.dumps(summary["mean"], ensure_ascii=False, indent=2) + "\n")
    return 0
