# %% [markdown]
# # S17.6 What this course did not teach
#
# Named refusals. Course 2 is Agentic Architecture.
# This file prints the refuse page. It does not install any refused stack.

# %%
"""S17.6: print the refuse page. Does not install any refused stack."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

page = (ROOT / "docs" / "mechanisms" / "refuse_shelf.md").read_text(encoding="utf-8")
lines = [ln for ln in page.splitlines() if ln.startswith("- ")]

print("=== named, not shipped ===")
print("file docs/mechanisms/refuse_shelf.md")
print("n", len(lines))
print("course 2 Agentic Architecture")
print("rule You can name the paper and still not ship it.")
print()
print("=== refuse_shelf.md ===")
print(page.strip())
