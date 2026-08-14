import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_naive_lab_is_a_visible_program():
    text = (ROOT / "labs" / "02_naive_pipeline.py").read_text(encoding="utf-8")
    assert "STAGE 3  embedder" in text
    assert "ToyEmbedder" in text or "LAB_EMBEDDER" in text
    assert "store/naive" in text
    assert "# %%" in text


def test_naive_lab_runs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # Lab writes to the workbench store/ via ragbench.settings.STORE_ROOT.
    # Running it is the screen walk. Keep it extractive.
    monkeypatch.setenv("RAGBENCH_GENERATE", "extractive")
    runpy.run_path(str(ROOT / "labs" / "02_naive_pipeline.py"), run_name="__lab__")
    manifest = ROOT / "store" / "naive" / "manifest.json"
    assert manifest.is_file()
    blob = manifest.read_text(encoding="utf-8")
    assert "ToyEmbedder" in blob
