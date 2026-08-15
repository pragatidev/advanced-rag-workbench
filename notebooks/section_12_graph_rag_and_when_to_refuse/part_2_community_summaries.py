# %% [markdown]
# # Write community summaries
#
# Lab `lab_s12_graph` / `part_2`.

# %%
"""Write community summaries."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.graph.tiny import community_summaries

sums = community_summaries()
for k, v in sums.items():
    print(f"{k:10} {v}")
