"""Keep the suite offline. Live generate is a CLI demo, not CI."""

import os

os.environ["RAGBENCH_GENERATE"] = "extractive"
for name in (
    "RAGBENCH_API_KEY",
    "LLM_API_KEY",
    "DASHSCOPE_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "BAILIAN_TOKEN_PLAN_API_KEY",
    "GEMINI_API_KEY",
    "XAI_API_KEY",
    "DEEPSEEK_API_KEY",
):
    os.environ[name] = ""
