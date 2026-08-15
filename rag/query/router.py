"""Adaptive router: none, single, multi, or a named source.

This is a prompt-loop classifier, not Jeong et al. trained Adaptive-RAG.
"""

from __future__ import annotations

import re

from rag.loops.retrieve_gate import needs_corpus

_ID = re.compile(r"\b(TS-\d+|[A-Z]{2,}-\d+)\b")
_TABLE = re.compile(r"\b(kpi|seats?|table|cell|paid_seats|12420)\b", re.I)
_GLOBAL = re.compile(r"\b(themes?|across (the )?corpus|overall|main topics?)\b", re.I)
_SOURCE_ERROR = re.compile(r"\b(error code|TS-\d+|runbook|catalog)\b", re.I)
_SOURCE_POLICY = re.compile(r"\b(access control|tenant|pii|privacy|acl)\b", re.I)


def route(question: str) -> dict:
    q = (question or "").strip()
    if not needs_corpus(q):
        return {"route": "none", "reason": "chitchat or greeting", "source": None}
    if _GLOBAL.search(q):
        return {"route": "multi", "reason": "global / theme question", "source": None}
    if _SOURCE_ERROR.search(q) or _ID.search(q):
        return {"route": "source", "reason": "error id wants the catalog", "source": "error_catalog"}
    if _SOURCE_POLICY.search(q):
        return {"route": "source", "reason": "policy question", "source": "access_control"}
    if _TABLE.search(q):
        return {"route": "source", "reason": "table or figure cell", "source": "q2_kpis"}
    return {"route": "single", "reason": "local factual question", "source": None}


def route_name(question: str) -> str:
    return route(question)["route"]
