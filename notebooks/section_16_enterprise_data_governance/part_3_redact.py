# %% [markdown]
# # Redact PII before generate
#
# Lab `lab_s16_gov` / `part_3`.

# %%
"""Redact PII before generate."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.gov import DETECTOR, redact

# Text that would have been stuffed into generate.
raw = "Do not send a national id to the model. ID 1234-5678-9012."
sent = redact(raw)

print("detector", DETECTOR)
print("stand_in", DETECTOR == "national_id_phrase")
print("raw", raw)
print("sent", sent)
assert "[REDACTED_PII]" in sent
assert "national id" not in sent.lower()
