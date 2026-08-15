# %% [markdown]
# # Run the loop and read the path
#
# Lab `lab_s11_crag` / `part_4`.

# %%
"""Run the loop and read the path."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.loops.tool_loop import run_loop

for q in (
    "Good morning, how are you?",
    "What does error code TS-999 mean?",
    "What are the main themes in this ACME corpus?",
):
    out = run_loop(q, web_enabled=False)
    print(q)
    print("  path", out["path"], "grade", out["grade"], "web_called", out["web_called"])
    print("  hygiene", out.get("hygiene"))
    print("  answer", out["answer"][:160])
