"""scripts/smoke_all.py and the Makefile cover every test file, so a new one is never left out."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _smoke_all():
    spec = importlib.util.spec_from_file_location("smoke_all", ROOT / "scripts" / "smoke_all.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_smoke_all_runs_every_test_file():
    on_disk = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "tests").glob("test_*.py"))
    listed = _smoke_all().test_files()
    assert sorted(listed) == on_disk
    assert listed[0] == "tests/test_smoke.py"


def test_makefile_has_a_target_for_every_section_test_file():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    recipes = re.findall(r"^([\w-]+):\n\t(.+)$", makefile, re.M)
    run_by = {
        path: target
        for target, line in recipes
        if "pytest" in line
        for path in re.findall(r"tests/test_section_\w+\.py", line)
    }
    sections = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "tests").glob("test_section_*.py"))
    assert [s for s in sections if s not in run_by] == []
    assert any(target == "test" and line.endswith("-m pytest") for target, line in recipes)
    assert any(target == "smoke" and line.endswith("scripts/smoke_all.py") for target, line in recipes)
