# %% [markdown]
# # S18.3 Conversation memory is not the document index
#
# Named frontier card. Not the Monday loop.
# This file prints the card. It does not install Mem0 or Neo4j.

# %%
"""S18.3: print the conversation-memory card. Does not install Mem0 or Neo4j."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

page = (ROOT / "docs" / "mechanisms" / "conversation_memory.md").read_text(encoding="utf-8")

print("=== not the document index ===")
print("file docs/mechanisms/conversation_memory.md")
print("left ACME policies")
print("right Priya's team is Helix-East, updated 12 Mar")
print("hit right drawer first, then left")
print("rule Memory has a validity date. The corpus does not.")
print()
print("=== conversation_memory.md ===")
print(page.strip())
