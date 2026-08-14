"""Structured log line for one ask."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def log_ask(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
