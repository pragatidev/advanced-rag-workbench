from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_section_01_orientation_files():
    assert (ROOT / "docs" / "mechanisms" / "retrieve_then_generate.md").is_file()
    assert (ROOT / "docs" / "mechanisms" / "modular_rag_workbench.md").is_file()
    assert (ROOT / "rag" / "ask.py").is_file()
    from rag.ask import run_ask

    assert callable(run_ask)
