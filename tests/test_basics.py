import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "embed_two_sentences",
    "similarity_scores",
    "cut_one_document",
    "store_and_ask",
    "mini_rag",
]


def _load(name: str):
    path = ROOT / "basics" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"basics_{name}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_each_basics_script_importable():
    for name in SCRIPTS:
        module = _load(name)
        assert module.__doc__


def test_mini_rag_returns_nonempty_answer_keyless():
    module = _load("mini_rag")
    assert str(module.answer).strip()
