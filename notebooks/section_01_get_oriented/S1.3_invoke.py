# %% [markdown]
# # How a program invokes RAG
#
# Open `rag/ask.py`. Production calls `run_ask` or `POST /ask`.

# %%
"""Product door."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.ask import run_ask
print(run_ask.__doc__)
print('HTTP door: python app.py  ->  POST /ask')
