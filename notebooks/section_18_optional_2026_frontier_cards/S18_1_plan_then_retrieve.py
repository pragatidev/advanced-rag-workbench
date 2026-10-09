# %% [markdown]
# # S18.1 Plan then retrieve, and Reason in Documents
#
# Named frontier card. Not the Monday loop.
# This file prints the card. It does not install Plan*RAG or Search-o1.

# %%
"""S18.1: print the plan-then-retrieve card. Does not install the papers."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

page = (ROOT / "docs" / "mechanisms" / "plan_then_retrieve.md").read_text(encoding="utf-8")

print("=== not the Monday loop ===")
print("file docs/mechanisms/plan_then_retrieve.md")
print("plan Plan*RAG DAG outside the window")
print("hops two parallel")
print("compressor Reason-in-Documents between verbose hit and next thought")
print("deeprag named +26.4 percent is their comparison")
print("rule A longer agent trace is not a plan.")
print()
print("=== plan_then_retrieve.md ===")
print(page.strip())
