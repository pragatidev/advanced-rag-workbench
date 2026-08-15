"""Index the figure as a caption."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.multimodal import caption_chunks

caps = caption_chunks()
print(caps[0].text)
print("South 2000", "South 2000" in caps[0].text)
