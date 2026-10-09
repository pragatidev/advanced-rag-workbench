import runpy
from pathlib import Path

from rag.llm import ping
from rag.providers.hosted import ANTHROPIC, OPENAI, door_for
from rag.settings import DEFAULT_LLM_BASE_URL, DEFAULT_LLM_MODEL, Settings, load_env

ROOT = Path(__file__).resolve().parents[1]


def test_section_02_settings_and_env_example():
    load_env()
    example = (ROOT / ".env.example").read_text(encoding="utf-8")
    # the three doors are all documented, and the four variables are named
    for needle in ("LLM_BACKEND=anthropic", "LLM_BACKEND=openai", ANTHROPIC["base_url"], OPENAI["base_url"],
                   "11434/v1", "1234/v1", ANTHROPIC["default_model"], OPENAI["default_model"]):
        assert needle in example, needle
    # no vendor default: the repo starts local and keyless
    assert DEFAULT_LLM_MODEL == "qwen3:8b"
    assert DEFAULT_LLM_BASE_URL == "http://localhost:11434/v1"
    print("base", Settings.llm_base_url, "model", Settings.llm_model)


def test_section_02_door_label_never_lies():
    assert door_for("https://api.anthropic.com", "anthropic") == "anthropic"
    assert door_for("https://api.openai.com/v1", "openai") == "openai"
    assert door_for("http://localhost:11434/v1", "openai") == "local"
    assert door_for("https://api.groq.com/openai/v1", "openai") == "openai-compatible"


def test_section_02_configure_scripts(capsys):
    runpy.run_path(str(ROOT / "labs" / "lab_s2_env" / "part_2" / "configure_env.py"), run_name="__main__")
    runpy.run_path(str(ROOT / "labs" / "lab_s2_env" / "part_3" / "configure_hosted.py"), run_name="__main__")
    out = capsys.readouterr().out
    assert "THE TWO HOSTED DOORS" in out
    assert "backend" in out and "key_present" in out
    assert "sk-ant-" not in out.replace("sk-ant-...", "")  # the key itself is never printed


def test_section_02_ping_skips_without_key():
    result = ping("Reply with the single word pong.")
    assert "skipped" in result or result.get("ok") is True
    if result.get("skipped"):
        assert "SKIPPED" in (result.get("note") or "")
