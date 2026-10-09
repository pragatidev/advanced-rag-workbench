"""Toy judges that print named failure modes. Not an LLM-as-judge install."""

from __future__ import annotations


def pick_first(left: str, right: str) -> str:
    """Position-biased judge. Always returns the first slot."""
    return left


def pick_longer(a: str, b: str) -> str:
    """Verbosity-biased judge. Always returns the longer answer."""
    a_n = len((a or "").split())
    b_n = len((b or "").split())
    return a if a_n >= b_n else b


def pick_same_family(
    a: tuple[str, str],
    b: tuple[str, str],
    judge_family: str,
) -> str:
    """Self-preference. Each pair is (text, family)."""
    a_text, a_fam = a
    b_text, b_fam = b
    if a_fam == judge_family and b_fam != judge_family:
        return a_text
    if b_fam == judge_family and a_fam != judge_family:
        return b_text
    return a_text


def agreement(pairs: list[tuple[str, str]]) -> tuple[int, int]:
    """pairs of (human_pick, judge_pick). Returns (agree, n)."""
    n = len(pairs)
    agree = sum(1 for human, judge in pairs if human == judge)
    return agree, n
