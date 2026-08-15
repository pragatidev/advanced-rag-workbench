"""Redact PII before generate."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.gov import DETECTOR, redact

raw = "Do not send a national id to the model."
print("detector", DETECTOR)
print(redact(raw))
assert "[REDACTED_PII]" in redact(raw)
