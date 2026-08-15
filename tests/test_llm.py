import pytest

from rag.envload import api_base, api_model, generate_mode
from rag.generate import generate_answer
from rag.chunkers import Chunk
from rag.llm import chat


def test_default_endpoint_is_model_studio_intl(monkeypatch):
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
    assert api_base() == "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    assert api_model() == "qwen3.8-max"


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
    chunk = Chunk(chunk_id="c", doc_id="d", title="t", text="hello")
    with pytest.raises(RuntimeError, match="key"):
        chat("q", [chunk])
