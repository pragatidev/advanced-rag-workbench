"""Cost column. Local toy pipelines are 0.00. Live model lectures fill tokens in."""

from __future__ import annotations


def estimate(pipeline: str, extra_generates: int = 0) -> dict:
    # One generate for naive/hybrid. HyDE adds one. Multi-query adds N.
    generates = 1 + extra_generates
    return {
        "generate_calls": generates,
        "usd": 0.0,
        "note": "local toy stack. replace with provider usage in live lectures.",
        "pipeline": pipeline,
    }
