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
    # The install gate: the full suite, every section, no API key, about 20 seconds.
    # pytest.ini adds -q, so it prints dots and one count line (the s is pgvector,
    # which skips unless Docker is up).
    proc = subprocess.run([sys.executable, "-m", "pytest"], cwd=ROOT)
    print("pytest_exit", proc.returncode, flush=True)
