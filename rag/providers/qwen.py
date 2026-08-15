"""Verified Qwen Model Studio International door.

Ids and URLs come from curriculum_gap_list.json provider_setup.qwen_max
(access 2026-08-15). Do not invent qwen-3.8-max or a token-plan host.
"""

from __future__ import annotations

MODEL_ID = "qwen3.8-max"
API_KEY_ENV = "DASHSCOPE_API_KEY"
LEGACY_INTL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
US_VIRGINIA = "https://dashscope-us.aliyuncs.com/compatible-mode/v1"
WORKSPACE = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
DOCS = "https://www.alibabacloud.com/help/en/model-studio/compatibility-of-openai-with-dashscope"
FREE_QUOTA = (
    "Singapore International only. qwen3.8-max: 1 million tokens. "
    "Real-time inference only. Turn Free Quota Only on in the console."
)


def describe() -> dict:
    return {
        "model_id": MODEL_ID,
        "api_key_env": API_KEY_ENV,
        "legacy_intl": LEGACY_INTL,
        "us": US_VIRGINIA,
        "workspace": WORKSPACE,
        "docs": DOCS,
        "free_quota": FREE_QUOTA,
    }
