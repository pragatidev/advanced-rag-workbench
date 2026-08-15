# %% [markdown]
# # Support the answer or refuse it
#
# Lab `lab_s10_route` / `part_2`.

# %%
"""Support the answer or refuse it."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.loops.retrieve_gate import support_or_refuse

ctx = ["TS-999 means the billing ledger rejected a duplicate invoice id."]
print(support_or_refuse("TS-999 is a duplicate invoice rejection.", ctx))
print(support_or_refuse("The CEO is moving to Mars next week.", ctx))
