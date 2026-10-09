import urllib.error

import pytest

import rag.generate
import rag.llm
from rag.envload import api_base, api_model, generate_mode
from rag.generate import generate_answer
from rag.chunkers import Chunk
from rag.llm import chat
from rag.settings import _KEY_ENV_NAMES

# Every variable that can move generate off the local default door.
_DOOR_ENV_NAMES = (
    "RAGBENCH_API_BASE", "RAGBENCH_BASE_URL", "LLM_BASE_URL", "ANTHROPIC_BASE_URL",
    "RAGBENCH_PROVIDER", "LLM_PROVIDER", "RAGBENCH_API_BACKEND", "LLM_BACKEND",
)


def _local_door(monkeypatch, key: str = "") -> None:
    """The default local door (localhost:11434), no .env read, LLM_API_KEY = key ("" is none)."""
    monkeypatch.setattr(rag.generate, "load_dotenv", lambda path=None: None)
    for name in _KEY_ENV_NAMES:
        monkeypatch.setenv(name, "")
    for name in _DOOR_ENV_NAMES + ("RAGBENCH_MODEL", "LLM_MODEL", "ANTHROPIC_MODEL"):
        monkeypatch.delenv(name, raising=False)
    if key:
        monkeypatch.setenv("LLM_API_KEY", key)


def _refused(*args, **kwargs):
    # What urlopen raises when nothing listens at the address (Windows error 10061).
    raise urllib.error.URLError(ConnectionRefusedError(10061, "No connection could be made"))


def test_default_endpoint_is_local_and_keyless(monkeypatch):
    # No vendor default: with nothing set, the workbench points at a local Ollama server.
    for name in (
        "RAGBENCH_API_BASE",
        "RAGBENCH_BASE_URL",
        "LLM_BASE_URL",
        "ANTHROPIC_BASE_URL",
        "RAGBENCH_MODEL",
        "LLM_MODEL",
        "ANTHROPIC_MODEL",
    ):
        monkeypatch.delenv(name, raising=False)
    assert api_base() == "http://localhost:11434/v1"
    assert api_model() == "qwen3:8b"


def test_generate_mode_without_key_is_extractive(monkeypatch):
    monkeypatch.delenv("RAGBENCH_GENERATE", raising=False)
    for name in (
        "RAGBENCH_API_KEY",
        "LLM_API_KEY",
        "ANTHROPIC_API_KEY",
        "ANTHROPIC_AUTH_TOKEN",
        "BAILIAN_TOKEN_PLAN_API_KEY",
        "DASHSCOPE_API_KEY",
        "OPENAI_API_KEY",
        "GEMINI_API_KEY",
        "XAI_API_KEY",
        "DEEPSEEK_API_KEY",
    ):
        monkeypatch.setenv(name, "")
    assert generate_mode(None) == "extractive"


def test_generate_mode_with_key_is_api(monkeypatch):
    monkeypatch.delenv("RAGBENCH_GENERATE", raising=False)
    monkeypatch.setenv("RAGBENCH_API_KEY", "test-not-real")
    assert generate_mode(None) == "api"


def test_extractive_still_default():
    chunk = Chunk(chunk_id="c", doc_id="d", title="t", text="TS-999 means duplicate invoice.")
    answer, meta = generate_answer("What is TS-999?", [chunk], mode="extractive")
    assert "duplicate" in answer.lower()
    assert meta["generator"] == "extractive"


def test_api_without_key_raises(monkeypatch):
    # A hosted door with no key stops before any call. (The local door needs no key: next test.)
    _local_door(monkeypatch)
    monkeypatch.setenv("LLM_BASE_URL", "https://api.openai.com/v1")

    def no_network(*args, **kwargs):
        raise AssertionError("chat made a network call")

    monkeypatch.setattr(rag.llm, "_post", no_network)
    chunk = Chunk(chunk_id="c", doc_id="d", title="t", text="hello")
    with pytest.raises(RuntimeError, match="key"):
        chat("q", [chunk])


def _fake_post(calls):
    def fake(url, headers, body, timeout):
        calls.append({"url": url, "headers": headers, "body": body})
        return {"model": body["model"], "choices": [{"message": {"content": "TS-999 is a duplicate invoice [1]."}}]}

    return fake


def test_local_door_needs_no_key(monkeypatch):
    # No LLM_API_KEY at all: chat() sends the local placeholder, the same as ping().
    _local_door(monkeypatch)
    calls = []
    monkeypatch.setattr(rag.llm, "_post", _fake_post(calls))
    chunk = Chunk(chunk_id="c", doc_id="d", title="t", text="TS-999 means duplicate invoice.")
    result = chat("What is TS-999?", [chunk])
    assert result["text"] == "TS-999 is a duplicate invoice [1]."
    assert len(calls) == 1
    assert calls[0]["url"] == "http://localhost:11434/v1/chat/completions"
    assert calls[0]["headers"]["Authorization"] == "Bearer ollama"


def test_generate_api_on_the_local_door_without_a_key(monkeypatch):
    # python -m rag ask "..." --generate api with Ollama up and no key: the model writes it.
    _local_door(monkeypatch)
    calls = []
    monkeypatch.setattr(rag.llm, "_post", _fake_post(calls))
    chunk = Chunk(chunk_id="c", doc_id="d", title="t", text="TS-999 means duplicate invoice.")
    answer, meta = generate_answer("What is TS-999?", [chunk], mode="api")
    assert answer == "TS-999 is a duplicate invoice [1]."
    assert meta["generator"] == "api"
    assert meta["model"] == "qwen3:8b"
    assert len(calls) == 1


def test_unreachable_model_is_the_same_runtime_error(monkeypatch):
    # No server at the address: _post raises the RuntimeError an HTTP error becomes, not URLError.
    monkeypatch.setattr(rag.llm.urllib.request, "urlopen", _refused)
    with pytest.raises(RuntimeError, match=r"^model not reachable at http://127\.0\.0\.1:9/v1/chat/completions \("):
        rag.llm._post("http://127.0.0.1:9/v1/chat/completions", {}, {}, timeout=1)


def test_generate_with_no_local_server_is_skipped_not_a_traceback(monkeypatch):
    # The LOCAL block with Ollama not running: an answer copied from the text and a SKIPPED note.
    _local_door(monkeypatch, key="ollama")
    monkeypatch.setattr(rag.llm.urllib.request, "urlopen", _refused)
    chunk = Chunk(chunk_id="c", doc_id="d", title="t", text="TS-999 means duplicate invoice.")
    answer, meta = generate_answer("What is TS-999?", [chunk], mode="api")
    assert "duplicate" in answer.lower()
    assert meta["generator"] == "extractive"
    assert meta["note"].startswith(
        "SKIPPED: model not reachable at http://localhost:11434/v1/chat/completions ("
    )
