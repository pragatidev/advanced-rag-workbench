"""Cost column. Local toy pipelines are 0.00. Live model lectures fill tokens in."""

from __future__ import annotations


# Rough public list prices used only for the offline board. Swap from usage.
USD_PER_1K_IN = 0.0012
USD_PER_1K_OUT = 0.0048


def estimate(pipeline: str, extra_generates: int = 0) -> dict:
    # One generate for naive/hybrid. HyDE adds one. Multi-query adds N.
    generates = 1 + extra_generates
    return {
        "generate_calls": generates,
        "usd": 0.0,
        "note": "local toy stack. replace with provider usage in live lectures.",
        "pipeline": pipeline,
    }


def usd_from_tokens(prompt_tokens: int, completion_tokens: int) -> float:
    return (prompt_tokens / 1000.0) * USD_PER_1K_IN + (completion_tokens / 1000.0) * USD_PER_1K_OUT


def count_tokens(text: str) -> int:
    return max(1, len((text or "").split()))
