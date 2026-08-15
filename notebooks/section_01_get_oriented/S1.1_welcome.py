# %% [markdown]
# # Welcome: what Advanced RAG is for
#
# Read `docs/mechanisms/retrieve_then_generate.md`.
# Point at `eval/questions.jsonl` and `data/acme/`.

# %%
"""Welcome pointers."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print((ROOT / 'docs' / 'mechanisms' / 'retrieve_then_generate.md').read_text(encoding='utf-8')[:400])
print('questions', (ROOT / 'eval' / 'questions.jsonl').is_file())
print('corpus', (ROOT / 'data' / 'acme').is_dir())
