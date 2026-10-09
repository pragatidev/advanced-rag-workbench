# %% [markdown]
# # S18.2 Three retrieval tools, not one top k
#
# Named frontier card. Not the Monday loop.
# This file prints the card. It does not install A-RAG.

# %%
"""S18.2: print the three-retrieval-tools card. Does not install A-RAG."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

page = (ROOT / "docs" / "mechanisms" / "three_retrieval_tools.md").read_text(encoding="utf-8")

print("=== not one top k ===")
print("file docs/mechanisms/three_retrieval_tools.md")
print("tools keyword, dense, chunk-read")
print("agent picks granularity")
print("rule Retrieve is not always one top-k.")
print()
print("=== three_retrieval_tools.md ===")
print(page.strip())
