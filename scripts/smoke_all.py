"""Run every section smoke test in order. Print a PASS/FAIL table. No API key required."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [f"tests/test_section_{i:02d}.py" for i in range(1, 18)]
SECTIONS.insert(0, "tests/test_smoke.py")


def main() -> int:
    print("RAGBENCH smoke_all  (retrieval local; generate skips without a key)")
    print(f"{'suite':28} {'status':8} {'note'}")
    print("-" * 72)
    failed = 0
    for rel in SECTIONS:
        path = ROOT / rel
        if not path.is_file():
            print(f"{rel:28} {'FAIL':8} missing file")
            failed += 1
            continue
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "--color=no", str(path)],
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
        print(f"{rel:28} {status:8} {last[:40]}")
    print("-" * 72)
    print(f"{'ALL':28} {'FAIL' if failed else 'PASS':8} {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
