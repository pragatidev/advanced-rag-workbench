import runpy
from pathlib import Path

import rag.llm
import rag.settings
from rag.llm import ping
from rag.providers.hosted import ANTHROPIC, OPENAI, door_for
from rag.settings import _KEY_ENV_NAMES, DEFAULT_LLM_BASE_URL, DEFAULT_LLM_MODEL, Settings, load_env

ROOT = Path(__file__).resolve().parents[1]
# Every variable that can move generate off the local default door.
_DOOR_ENV_NAMES = (
    "RAGBENCH_API_BASE", "RAGBENCH_BASE_URL", "LLM_BASE_URL", "ANTHROPIC_BASE_URL",
    "RAGBENCH_PROVIDER", "LLM_PROVIDER", "RAGBENCH_API_BACKEND", "LLM_BACKEND",
)


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


def test_section_02_ping_skips_without_key(monkeypatch):
    # Offline on every machine, even one with Ollama on 11434 or a key in .env:
    # no .env, no key, no local server, and any network call fails the test.
    monkeypatch.setattr(rag.settings, "load_env", lambda path=None: None)
    for name in _KEY_ENV_NAMES + _DOOR_ENV_NAMES:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(rag.llm, "_port_open", lambda host, port, timeout=0.3: False)
    calls = []

    def no_network(*args, **kwargs):
        calls.append(args)
        raise AssertionError("ping made a network call")

    monkeypatch.setattr(rag.llm, "_post", no_network)
    monkeypatch.setattr(rag.llm.urllib.request, "urlopen", no_network)
    result = ping("Reply with the single word pong.")
    assert calls == []
    assert result["skipped"] is True
    assert "SKIPPED" in result["note"]
    assert result["endpoint"] == DEFAULT_LLM_BASE_URL
