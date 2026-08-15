# %% [markdown]
# # Concept, lab parts, then the full run
#
# Read `docs/mechanisms/modular_rag_workbench.md`.

# %%
"""Course modes."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

print((ROOT / 'docs' / 'mechanisms' / 'modular_rag_workbench.md').read_text(encoding='utf-8')[:400])
print('labs', sorted(p.name for p in (ROOT / 'labs').iterdir() if p.is_dir()))
