import runpy
from pathlib import Path

from rag.llm import ping
from rag.providers.qwen import MODEL_ID
from rag.settings import DEFAULT_LLM_MODEL, Settings, load_env

ROOT = Path(__file__).resolve().parents[1]


def test_section_02_settings_and_env_example():
    load_env()
    example = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "qwen3.8-max" in example
    assert "qwen3.8-max-preview" not in example
    assert "11434/v1" in example
    assert "1234/v1" in example
    assert DEFAULT_LLM_MODEL == "qwen3.8-max"
    assert MODEL_ID == "qwen3.8-max"
    print("base", Settings.llm_base_url, "model", Settings.llm_model)


def test_section_02_configure_scripts(capsys):
    runpy.run_path(str(ROOT / "labs" / "lab_s2_env" / "part_2" / "configure_env.py"), run_name="__main__")
    runpy.run_path(str(ROOT / "labs" / "lab_s2_env" / "part_3" / "configure_qwen.py"), run_name="__main__")
    out = capsys.readouterr().out
    assert "qwen3.8-max" in out


def test_section_02_ping_skips_without_key():
    result = ping("Reply with the single word pong.")
    assert "skipped" in result or result.get("ok") is True
    if result.get("skipped"):
        assert "SKIPPED" in (result.get("note") or "")
