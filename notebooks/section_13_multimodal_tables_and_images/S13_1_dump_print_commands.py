# %% [markdown]
# # S13.1 Dump the print commands
#
# A PDF table is stored as drawing commands, not as rows.
# This file lists every Tj print command so you can see whether a
# number still sits in the same command as its label.

# %%
"""S13.1: dump every Tj print command in a PDF."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd() if (Path.cwd() / "rag").is_dir() else Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rag.multimodal import PDF_PATH, emit_print_commands

src = Path(sys.argv[1]) if len(sys.argv) > 1 else PDF_PATH
emit_print_commands(src)
