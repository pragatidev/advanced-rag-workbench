"""A support ticket arrived. The product calls run_ask. It does not open a terminal.

This is the practical shape: Slack, Zendesk, a chat widget, or an internal
bot all look like handle_ticket. Retrieve stays in-process. Generate is
extractive here so the example runs without a key.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.ask import run_ask


def handle_ticket(ticket_id: str, body: str, pipeline: str = "hybrid") -> dict:
    result = run_ask(body, pipeline=pipeline, generate="extractive")
    return {
        "ticket_id": ticket_id,
        "reply": result["answer"],
        "sources": [h["chunk_id"] for h in result.get("hits", [])],
        "pipeline": result.get("pipeline"),
    }


def main() -> int:
    ticket = handle_ticket("T-1042", "What does error code TS-999 mean?")
    sys.stdout.write(json.dumps(ticket, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
