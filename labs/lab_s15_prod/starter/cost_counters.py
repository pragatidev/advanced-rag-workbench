"""STARTER Count generate calls and tokens. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

from rag.eval.cost import count_tokens, estimate, usd_from_tokens

print("naive", estimate("naive", extra_generates=0))
print("hyde", estimate("hyde", extra_generates=1))
print("tokens", count_tokens("What does error code TS-999 mean?"))
print("usd_offline", usd_from_tokens(0, 0))
print("usd_example", round(usd_from_tokens(800, 120), 6))
