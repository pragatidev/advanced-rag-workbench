"""Shared tokenization. Keep it boring so BM25 and the toy embedder see the same words."""

from __future__ import annotations

import re

_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_\-%]*")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in _TOKEN.finditer(text or "")]


def split_sentences(text: str) -> list[str]:
    """Split on end punctuation. Good enough for the ACME markdown corpus."""
    blob = re.sub(r"\s+", " ", (text or "").replace("\n", " ")).strip()
    if not blob:
        return []
    parts = _SENT_SPLIT.split(blob)
    return [p.strip() for p in parts if p.strip()]
