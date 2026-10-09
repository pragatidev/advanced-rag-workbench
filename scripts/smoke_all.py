"""Run every test file on its own, smoke canaries first. Print a PASS/FAIL table. No API key required."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_files() -> list[str]:
    """Every tests/test_*.py, so a new test file is covered the day it lands."""
    files = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "tests").glob("test_*.py"))
    files.remove("tests/test_smoke.py")
    return ["tests/test_smoke.py", *files]


def main() -> int:
    print("RAGBENCH smoke_all  (retrieval local; generate skips without a key)")
    print(f"{'suite':34} {'status':8} {'note'}")
    print("-" * 78)
    failed = 0
    files = test_files()
    for rel in files:
        # pytest.ini already adds -q, so the last line is pytest's count line.
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "--color=no", rel],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        status = "PASS" if proc.returncode == 0 else "FAIL"
        if proc.returncode != 0:
            failed += 1
        last = ""
        for line in out.splitlines():
            if line.strip():
                last = line.strip()
        print(f"{rel:34} {status:8} {last[:40]}")
    print("-" * 78)
    print(f"{'ALL':34} {'FAIL' if failed else 'PASS':8} {len(files)} files, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
