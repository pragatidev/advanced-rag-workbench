"""Screen walk twin of labs/lab_s2_env/part_3/configure_hosted.py: point generate at Anthropic or an
OpenAI-compatible provider. Same four variables, same code; the key is never printed."""

from __future__ import annotations

import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
runpy.run_path(str(ROOT / "labs" / "lab_s2_env" / "part_3" / "configure_hosted.py"), run_name="__main__")
