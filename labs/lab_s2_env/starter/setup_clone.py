"""STARTER Clone the workbench and get pytest green. Fill the TODOs. part_1 is the first working slice."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# TODO: import the package symbols this lab needs

import os
import subprocess

print("python", sys.version.split()[0])
print("root", ROOT)
print("pyproject", (ROOT / "pyproject.toml").is_file())
print("python-version", (ROOT / ".python-version").read_text(encoding="utf-8").strip())
if os.environ.get("PYTEST_CURRENT_TEST") or os.environ.get("RAGBENCH_SMOKE"):
    print("SKIP pytest inside an existing test run")
else:
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=ROOT)
    print("pytest_exit", proc.returncode)
