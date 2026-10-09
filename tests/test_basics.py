import importlib.util
from pathlib import Path

import rag.llm
from rag.llm import _source_blob
from rag.settings import _KEY_ENV_NAMES

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "embed_two_sentences",
    "similarity_scores",
    "cut_one_document",
    "store_and_ask",
    "mini_rag",
    "grounded_ask",
    "cold_ask",
]
# Every variable that can move generate off the local default door, or pick the embedder.
_DOOR_ENV_NAMES = (
    "RAGBENCH_API_BASE", "RAGBENCH_BASE_URL", "LLM_BASE_URL", "ANTHROPIC_BASE_URL",
    "RAGBENCH_PROVIDER", "LLM_PROVIDER", "RAGBENCH_API_BACKEND", "LLM_BACKEND",
    "RAGBENCH_MODEL", "LLM_MODEL", "ANTHROPIC_MODEL", "RAGBENCH_EMBED_MODEL",
)


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


def _grounded_ask_offline(monkeypatch, server_up: bool):
    """grounded_ask with no .env, no key, the default local door and the offline hash embedder."""
    module = _load("grounded_ask")
    monkeypatch.setattr(module, "load_dotenv", lambda path=None: None)
    for name in _KEY_ENV_NAMES + _DOOR_ENV_NAMES:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("EMBED_MODEL", "hash")
    monkeypatch.setattr(module, "_port_open", lambda host, port, timeout=0.3: server_up)
    return module


def test_grounded_ask_offline_prints_step_one_and_skips_step_two(monkeypatch, capsys):
    module = _grounded_ask_offline(monkeypatch, server_up=False)
    calls = []

    def no_network(*args, **kwargs):
        calls.append(args)
        raise AssertionError("grounded_ask made a network call")

    monkeypatch.setattr(rag.llm, "_post", no_network)
    monkeypatch.setattr(rag.llm.urllib.request, "urlopen", no_network)
    assert module.main() == 0
    out = capsys.readouterr().out
    _, hits = module.retrieved(module.QUESTION)
    assert len(hits) == 3
    for i, h in enumerate(hits, 1):
        assert f"\n    {i}. {h.chunk.chunk_id}  score {h.score:.3f}\n" in out
    assert "\n    SKIPPED: no model server at http://localhost:11434/v1 " in out
    assert "user message" not in out and "ANSWER (" not in out
    assert calls == []


def test_grounded_ask_prints_the_user_message_exactly_as_sent(monkeypatch, capsys):
    module = _grounded_ask_offline(monkeypatch, server_up=True)
    sent = []

    def fake_post(url, headers, body, timeout):
        sent.append(body)
        return {"model": body["model"], "choices": [{"message": {"content": "It is a duplicate [1]."}}]}

    monkeypatch.setattr(rag.llm, "_post", fake_post)
    assert module.main() == 0
    out = capsys.readouterr().out
    assert len(sent) == 1
    user = sent[0]["messages"][1]["content"]
    _, hits = module.retrieved(module.QUESTION)
    assert user == _source_blob(module.QUESTION, [h.chunk for h in hits])
    for i, h in enumerate(hits, 1):
        assert f"       | [{i}] {h.chunk.chunk_id}\n" in out
    printed = "\n".join(f"       | {line}" for line in user.splitlines())
    assert printed in out
    assert "\n    ANSWER (qwen3:8b):\n    It is a duplicate [1].\n" in out


def _cold_ask(monkeypatch, **env):
    """cold_ask with no .env, the offline hash embedder, and only the given variables set."""
    module = _load("cold_ask")
    monkeypatch.setattr(module, "load_dotenv", lambda path=None: None)
    for name in _KEY_ENV_NAMES + _DOOR_ENV_NAMES:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("EMBED_MODEL", "hash")
    for name, value in env.items():
        monkeypatch.setenv(name, value)
    return module


def _record_posts(monkeypatch, module, answer: bool = True):
    """Every request cold_ask makes, through its own _post or the workbench's; nothing leaves."""
    import urllib.error

    sent = []

    def fake_post(url, headers, body, timeout=90):
        sent.append((url, headers, body))
        if not answer:
            # What urlopen raises when nothing listens at the address (Windows error 10061).
            raise urllib.error.URLError(ConnectionRefusedError(10061, "No connection could be made"))
        if url.endswith("/chat/completions"):
            return {"model": body["model"], "choices": [{"message": {"content": "No idea."}}]}
        return {"model": body["model"], "content": [{"type": "text", "text": "No idea."}]}

    def no_network(*args, **kwargs):
        raise AssertionError("cold_ask made a real network call")

    monkeypatch.setattr(module, "_post", fake_post)
    monkeypatch.setattr(rag.llm, "_post", fake_post)
    monkeypatch.setattr(rag.llm.urllib.request, "urlopen", no_network)
    return sent


_ASKED = [{"role": "user", "content": "What does error code TS-999 mean? Answer in one or two sentences."}]


def test_cold_ask_no_key_and_nothing_running_prints_the_lines_the_lectures_show(monkeypatch, capsys):
    module = _cold_ask(monkeypatch)
    sent = _record_posts(monkeypatch, module, answer=False)
    assert module.main() == 0
    out = capsys.readouterr().out
    assert ("\n[1] COLD, hosted frontier model, no documents\n"
            "    skipped: LLM_API_KEY is not set. The other two legs still run.\n") in out
    assert ("\n[2] COLD, local model on this machine, no documents\n"
            "    skipped: no local model answered on http://localhost:11434/v1 (URLError)\n") in out
    assert [url for url, _, _ in sent] == ["http://localhost:11434/v1/chat/completions"]


def test_cold_ask_no_key_local_leg_sends_what_it_always_sent(monkeypatch, capsys):
    module = _cold_ask(monkeypatch)
    sent = _record_posts(monkeypatch, module)
    assert module.main() == 0
    assert sent == [(
        "http://localhost:11434/v1/chat/completions",
        {"Content-Type": "application/json", "Authorization": "Bearer ollama"},
        {"model": "qwen3:8b", "messages": _ASKED, "temperature": 0},
    )]
    assert "\n    model: qwen3:8b\n    No idea.\n" in capsys.readouterr().out


def test_cold_ask_openai_door_speaks_chat_completions(monkeypatch, capsys):
    # The old leg [1] sent Anthropic's format to any base URL: .../v1/v1/messages on this door.
    module = _cold_ask(monkeypatch, LLM_BACKEND="openai", LLM_BASE_URL="https://api.openai.com/v1",
                       LLM_API_KEY="test-key", LLM_MODEL="gpt-6-luna")
    sent = _record_posts(monkeypatch, module)
    assert module.main() == 0
    url, headers, body = sent[0]
    assert url == "https://api.openai.com/v1/chat/completions"
    assert headers["Authorization"] == "Bearer test-key"
    assert body == {"model": "gpt-6-luna", "messages": _ASKED}
    assert sent[1][0] == "http://localhost:11434/v1/chat/completions"  # leg [2] keeps Ollama's default
    assert "\n    model: gpt-6-luna\n    No idea.\n" in capsys.readouterr().out


def test_cold_ask_anthropic_door_asks_with_no_system_prompt(monkeypatch):
    module = _cold_ask(monkeypatch, LLM_BACKEND="anthropic", LLM_BASE_URL="https://api.anthropic.com",
                       LLM_API_KEY="test-key", LLM_MODEL="claude-haiku-5-5")
    sent = _record_posts(monkeypatch, module)
    assert module.main() == 0
    url, headers, body = sent[0]
    assert url == "https://api.anthropic.com/v1/messages"
    assert headers["x-api-key"] == "test-key" and headers["anthropic-version"] == "2023-06-01"
    assert body == {"model": "claude-haiku-5-5", "max_tokens": 300, "messages": _ASKED}


def test_cold_ask_local_leg_reads_the_door_from_settings(monkeypatch):
    # LM Studio, no key: the old leg [2] always asked localhost:11434 for qwen3:8b.
    module = _cold_ask(monkeypatch, LLM_BACKEND="openai", LLM_BASE_URL="http://localhost:1234/v1",
                       LLM_MODEL="my-loaded-model")
    sent = _record_posts(monkeypatch, module)
    assert module.main() == 0
    assert sent == [(
        "http://localhost:1234/v1/chat/completions",
        {"Content-Type": "application/json", "Authorization": "Bearer lm-studio"},
        {"model": "my-loaded-model", "messages": _ASKED, "temperature": 0},
    )]
