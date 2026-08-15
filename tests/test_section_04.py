import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_section_04_orphan_and_golden(capsys):
    runpy.run_path(str(ROOT / "labs" / "lab_s4_diagnose" / "part_1" / "orphan_chunk.py"), run_name="__main__")
    runpy.run_path(str(ROOT / "labs" / "lab_s4_diagnose" / "part_2" / "inspect_golden.py"), run_name="__main__")
    out = capsys.readouterr().out
    assert "contains ACME: False" in out or "contains ACME:False" in out.replace(" ", "")
    assert "q_ts999" in out
