"""Golden file helpers. Categories and canaries are the production object."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
QUESTIONS = ROOT / "eval" / "questions.jsonl"

REQUIRED_CATEGORIES = ("id", "paraphrase", "table", "global", "abstention", "acl_deny")
REQUIRED_FIELDS = ("id", "question", "gold_spans", "source_id", "category", "canary")


def load_golden(path: Path | None = None) -> list[dict]:
    rows = []
    with (path or QUESTIONS).open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def canaries(rows: list[dict] | None = None) -> list[dict]:
    return [r for r in (rows or load_golden()) if r.get("canary") is True]


def confirm_tags(rows: list[dict] | None = None) -> dict:
    rows = rows or load_golden()
    missing_fields = []
    for row in rows:
        for field in REQUIRED_FIELDS:
            if field not in row:
                missing_fields.append((row.get("id"), field))
    cats = {r.get("category") for r in rows}
    missing_cats = [c for c in REQUIRED_CATEGORIES if c not in cats]
    canary_rows = canaries(rows)
    canary_cats = {r.get("category") for r in canary_rows}
    missing_canary_cats = [c for c in REQUIRED_CATEGORIES if c not in canary_cats]
    return {
        "n": len(rows),
        "n_canaries": len(canary_rows),
        "categories": sorted(c for c in cats if c),
        "canary_ids": [r["id"] for r in canary_rows],
        "missing_fields": missing_fields,
        "missing_categories": missing_cats,
        "missing_canary_categories": missing_canary_cats,
        "ok": not missing_fields and not missing_cats and not missing_canary_cats,
    }
