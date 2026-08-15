# %% [markdown]
# # Index the figure as a caption
#
# Lab `lab_s13_mm` / `part_3`.

# %%
"""Index the figure as a caption."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.multimodal import caption_chunks

caps = caption_chunks()
print(caps[0].text)
print("South 2000", "South 2000" in caps[0].text)
