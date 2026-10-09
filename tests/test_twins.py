import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import make_twins  # noqa: E402


def test_every_twin_matches_its_lab_part():
    # A lab part is the source of truth. Fix a drift with: python scripts/make_twins.py
    assert make_twins.drifted() == []


def test_twins_cover_every_part_of_a_twinned_lab():
    parts = make_twins.part_files()
    assert len(parts) == 65
    assert all(make_twins.twin_path(p).is_file() for p in parts)


def test_only_the_lab_with_no_notebook_folder_has_no_twins():
    labs = {p.name for p in (ROOT / "labs").iterdir() if p.is_dir() and p.name.startswith("lab_")}
    assert labs - set(make_twins.TWIN_FOLDERS) == {"lab_s11b_hop"}


def test_two_parts_never_share_a_twin(tmp_path, monkeypatch):
    # Known answer: two labs in one folder with the same part name must stop the build.
    folder = make_twins.TWIN_FOLDERS["lab_s17_walk"]
    for lab in ("lab_a", "lab_b"):
        shutil.copytree(ROOT / "labs" / "lab_s17_walk" / "part_1", tmp_path / "labs" / lab / "part_1",
                        ignore=shutil.ignore_patterns("__pycache__"))
    monkeypatch.setattr(make_twins, "ROOT", tmp_path)
    monkeypatch.setattr(make_twins, "TWIN_FOLDERS", {"lab_a": folder, "lab_b": folder})
    try:
        make_twins.part_files()
    except SystemExit as exc:
        assert "both map to part_1_whiteboard_stack.py" in str(exc)
    else:
        raise AssertionError("two parts mapped to one twin and nothing stopped it")


def test_drift_is_caught(tmp_path, monkeypatch):
    # Known answer: one line added to a part must show up as that twin drifting.
    lab, folder = "lab_s7_hybrid", make_twins.TWIN_FOLDERS["lab_s7_hybrid"]
    shutil.copytree(ROOT / "labs" / lab, tmp_path / "labs" / lab, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "notebooks" / folder, tmp_path / "notebooks" / folder)
    monkeypatch.setattr(make_twins, "ROOT", tmp_path)
    monkeypatch.setattr(make_twins, "TWIN_FOLDERS", {lab: folder})
    assert make_twins.drifted() == []
    part = tmp_path / "labs" / lab / "part_3" / "rrf_fuse.py"
    part.write_text(part.read_text(encoding="utf-8") + "print('one more line')\n", encoding="utf-8")
    assert make_twins.drifted() == [f"notebooks/{folder}/part_3_rrf_fuse.py"]
