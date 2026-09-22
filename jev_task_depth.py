#!/usr/bin/env python3
"""Jev Task Depth Observer - PM 语义传感器

角色：PM_SEMANTIC_SENSOR
权威效应：NONE

只提供结构化语义观察，不创建任务、不派发、不改变 Gate。
PM 结合本地硬规则作出最终决定。
"""
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error

# TypeSafe Jev API 配置
JEV_ENDPOINT = "https://api.typesafe.ai/v1/systemone"
JEV_MODEL = "jev-latest"
JEV_API_KEY_ENV = "TYPESAFE_API_KEY"

# 硬规则：这些文件/场景强制 DEEP，Jev 不能降级
DEEP_HARD_TRIGGERS = [
    "prompts/",
    ".agent-control/",
    "activate.sh",
    "review_dispatch.py",
]

DEEP_HARD_KEYWORDS = [
    "schema",
    "wire",
    "secret",
    "hook",
    "migration",
    "real_device",
    "authority",
    "gate",
    "role_definition",
]


def compute_input_digest(inputs: dict) -> str:
    """计算输入摘要，用于证据追踪"""
    canonical = json.dumps(inputs, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]


def get_api_key() -> Optional[str]:
    """从环境变量获取 API Key"""
    return os.environ.get(JEV_API_KEY_ENV)


def call_jev_api(state: dict, questions: list, api_key: str) -> Optional[dict]:
    """调用 TypeSafe Jev API"""
    request_body = {
        "model": JEV_MODEL,
        "state": state,
        "questions": questions
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    req = urllib.request.Request(
        JEV_ENDPOINT,
        data=json.dumps(request_body).encode("utf-8"),
        headers=headers,
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, Exception) as e:
        print(f"Jev API error: {e}", file=sys.stderr)
        return None


def check_hard_triggers(
    affected_files: list[str],
    task_description: str
) -> list[str]:
    """检查是否触发 DEEP 硬规则"""
    triggers = []

    for f in affected_files:
        for trigger_path in DEEP_HARD_TRIGGERS:
            if f.startswith(trigger_path):
                triggers.append(f"PATH_TRIGGER:{trigger_path}")

    desc_lower = task_description.lower()
    for keyword in DEEP_HARD_KEYWORDS:
        if keyword in desc_lower:
            triggers.append(f"KEYWORD_TRIGGER:{keyword}")

    return triggers


def observe_task_depth(
    task_description: str,
    affected_files: list[str] | None = None,
    affected_domains: list[str] | None = None,
    has_dependencies: bool = False,
    requires_real_device_evidence: bool = False,
    api_key: Optional[str] = None,
) -> dict:
    """
    观察任务复杂度，返回语义建议。

    输出格式符合 SOP：
    {
        "status": "AVAILABLE" | "UNAVAILABLE" | "NOT_RUN",
        "input_digest": str,
        "jev_recommendation": "QUICK" | "NORMAL" | "DEEP" | null,
        "hard_triggers": list[str],
        "deterministic_override": "DEEP" | null,
        "authority_effect": "NONE"
    }

    注意：
    - Jev 建议只是观察，不授权任何动作
    - 硬规则触发时强制 DEEP，Jev 不能降级
    - Jev 不可用时返回 null，PM 人工决定（默认 NORMAL）
    """
    if affected_files is None:
        affected_files = []
    if affected_domains is None:
        affected_domains = []

    inputs = {
        "task_description": task_description,
        "affected_files": affected_files,
        "affected_domains": affected_domains,
        "has_dependencies": has_dependencies,
        "requires_real_device_evidence": requires_real_device_evidence,
    }
    input_digest = compute_input_digest(inputs)

    # 1. 检查硬规则触发
    hard_triggers = check_hard_triggers(affected_files, task_description)
    if requires_real_device_evidence:
        hard_triggers.append("REAL_DEVICE_EVIDENCE")
    if len(affected_domains) > 1:
        hard_triggers.append("CROSS_DOMAIN")

    deterministic_override = "DEEP" if hard_triggers else None

    # 2. 尝试 Jev 观察
    api_key = api_key or get_api_key()

    if not api_key:
        return {
            "status": "UNAVAILABLE",
            "input_digest": input_digest,
            "jev_recommendation": None,
            "hard_triggers": hard_triggers,
            "deterministic_override": deterministic_override,
            "authority_effect": "NONE",
        }

    state = {
        "task_description": task_description,
        "affected_files_count": len(affected_files),
        "affected_domains": affected_domains,
        "has_dependencies": has_dependencies,
        "requires_real_device_evidence": requires_real_device_evidence,
    }

    questions = [
        {
            "id": "process_path",
            "type": "choice",
            "instructions": "这个任务适合哪种处理路径？",
            "criteria": {"labels": ["QUICK", "NORMAL", "DEEP"]},
        },
        {
            "id": "explicit_user_authorization",
            "type": "bool",
            "instructions": "用户是否明确授权当前实施？",
        },
        {
            "id": "scope_expansion",
            "type": "bool",
            "instructions": "候选动作是否扩大了用户原始范围？",
        },
    ]

    response = call_jev_api(state, questions, api_key)

    if not response or "answers" not in response:
        return {
            "status": "UNAVAILABLE",
            "input_digest": input_digest,
            "jev_recommendation": None,
            "hard_triggers": hard_triggers,
            "deterministic_override": deterministic_override,
            "authority_effect": "NONE",
        }

    answers = response["answers"]
    jev_recommendation = answers.get("process_path", {}).get("choice", "NORMAL")

    return {
        "status": "AVAILABLE",
        "input_digest": input_digest,
        "jev_recommendation": jev_recommendation,
        "hard_triggers": hard_triggers,
        "deterministic_override": deterministic_override,
        "authority_effect": "NONE",
    }


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Jev 任务深度观察器（PM 语义传感器，authority_effect=NONE）"
    )
    parser.add_argument("description", help="任务描述")
    parser.add_argument("--files", nargs="*", default=[], help="涉及文件路径")
    parser.add_argument("--domains", nargs="*", default=[], help="涉及领域")
    parser.add_argument("--dependencies", action="store_true", help="是否有依赖")
    parser.add_argument("--real-device", action="store_true", help="是否需要真机证据")

    args = parser.parse_args()

    result = observe_task_depth(
        task_description=args.description,
        affected_files=args.files,
        affected_domains=args.domains,
        has_dependencies=args.dependencies,
        requires_real_device_evidence=args.real_device,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
