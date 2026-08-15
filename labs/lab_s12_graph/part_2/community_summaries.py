"""Write community summaries."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.graph.tiny import community_summaries

sums = community_summaries()
for k, v in sums.items():
    print(f"{k:10} {v}")
