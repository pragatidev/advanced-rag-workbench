"""Shared tokenization. Keep it boring so BM25 and the toy embedder see the same words."""

from __future__ import annotations

import re

_TOKEN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_\-%]*")


def tokenize(text: str) -> list[str]:
    return [m.group(0).lower() for m in _TOKEN.finditer(text or "")]
