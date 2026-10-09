"""Clone the workbench and get pytest green."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import os
import subprocess

print("python", sys.version.split()[0], flush=True)
print("root", ROOT, flush=True)
print("pyproject", (ROOT / "pyproject.toml").is_file(), flush=True)
print("python-version", (ROOT / ".python-version").read_text(encoding="utf-8").strip(), flush=True)
if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("RAGBENCH_SMOKE"):
    print("SKIP pytest inside an existing test run")
else:
    # S2.2 install gate (PROPS 2026-09-03): three-door repo, no API key.
    # Full `pytest -q` is a later-section suite and can fail on files this lab
    # does not own.
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "tests/test_section_02.py",
            "tests/test_labs.py",
            "tests/test_llm.py",
        ],
        cwd=ROOT,
    )
    print("pytest_exit", proc.returncode, flush=True)
