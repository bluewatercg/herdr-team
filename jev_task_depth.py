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
from pathlib import PurePosixPath
from typing import Optional
import urllib.request
import urllib.error

# TypeSafe Jev API 配置
JEV_ENDPOINT = "https://api.typesafe.ai/v1/systemone"
JEV_MODEL = "jev-latest"
JEV_API_KEY_ENV = "TYPESAFE_API_KEY"

# Authority 合同 - 本地常量，不可被 API 响应覆盖
AUTHORITY = {
    "may_mutate_intake": False,
    "may_create_requirement": False,
    "may_create_task": False,
    "may_dispatch": False,
    "may_change_gate": False,
    "may_accept_review": False,
    "may_activate_role": False,
}

# 硬规则：这些文件路径强制 DEEP，Jev 不能降级
DEEP_HARD_PATH_PREFIXES = [
    "prompts/",
    ".agent-control/",
]

DEEP_HARD_FILE_NAMES = [
    "activate.sh",
    "review_dispatch.py",
]

# 结构化硬规则标志（优先于关键词）
DEEP_HARD_IMPACT_FLAGS = [
    "changes_schema",
    "changes_wire",
    "changes_secret_handling",
    "adds_hook",
    "changes_authority",
    "changes_gate",
    "changes_role_definition",
    "requires_migration",
]

# 关键词触发器（advisory only，优先级低于结构化标志）
DEEP_ADVISORY_KEYWORDS = [
    "schema",
    "wire",
    "secret",
    "hook",
    "migration",
    "authority",
    "gate",
    "role_definition",
]

# Sentinel for api_key parameter
_UNSET = object()


def normalize_repo_path(raw: str) -> str:
    """规范化仓库相对路径，拒绝绝对路径和路径逃逸"""
    value = raw.replace("\\", "/")
    path = PurePosixPath(value)

    if path.is_absolute():
        raise ValueError(f"invalid repository-relative path: {raw} (absolute)")
    if ".." in path.parts:
        raise ValueError(f"invalid repository-relative path: {raw} (path escape)")

    # 移除开头的 ./
    while path.parts and path.parts[0] == ".":
        if len(path.parts) == 1:
            return ""
        path = PurePosixPath(*path.parts[1:])

    return path.as_posix()


def compute_input_digest(inputs: dict) -> tuple[str, str]:
    """计算输入摘要，返回 (full_sha256, short_digest)"""
    canonical = json.dumps(
        inputs,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    full_sha = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return full_sha, full_sha[:16]


def get_api_key() -> Optional[str]:
    """从环境变量获取 API Key"""
    return os.environ.get(JEV_API_KEY_ENV)


def call_jev_api(state: dict, questions: dict, api_key: str) -> tuple[Optional[dict], Optional[str]]:
    """
    调用 TypeSafe Jev API

    Returns:
        (response, error_code)
        error_code: None | "JEV_AUTH_FAILED" | "JEV_INVALID_REQUEST" |
                    "JEV_RATE_LIMITED" | "JEV_SERVER_ERROR" |
                    "JEV_NETWORK_UNAVAILABLE" | "JEV_RESPONSE_INVALID_JSON"
    """
    request_body = {
        "model": JEV_MODEL,
        "state": state,
        "questions": questions,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    req = urllib.request.Request(
        JEV_ENDPOINT,
        data=json.dumps(request_body).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            return None, "JEV_AUTH_FAILED"
        if exc.code in (400, 422):
            return None, "JEV_INVALID_REQUEST"
        if exc.code == 429:
            return None, "JEV_RATE_LIMITED"
        if 500 <= exc.code < 600:
            return None, "JEV_SERVER_ERROR"
        return None, f"JEV_HTTP_{exc.code}"
    except urllib.error.URLError:
        return None, "JEV_NETWORK_UNAVAILABLE"
    except TimeoutError:
        return None, "JEV_NETWORK_UNAVAILABLE"
    except json.JSONDecodeError:
        return None, "JEV_RESPONSE_INVALID_JSON"
    except Exception:
        return None, "JEV_NETWORK_UNAVAILABLE"


def check_hard_triggers(
    affected_files: list[str],
    impact_flags: dict[str, bool],
    requires_real_device_evidence: bool,
    affected_domains: list[str],
) -> list[str]:
    """检查是否触发 DEEP 硬规则"""
    triggers = set()

    # 检查文件路径
    for raw_path in affected_files:
        try:
            path = normalize_repo_path(raw_path)
        except ValueError:
            continue

        for prefix in DEEP_HARD_PATH_PREFIXES:
            if path.startswith(prefix):
                triggers.add(f"PATH_TRIGGER:{prefix}")

        filename = PurePosixPath(path).name
        if filename in DEEP_HARD_FILE_NAMES:
            triggers.add(f"FILE_TRIGGER:{filename}")

    # 检查结构化硬规则标志
    for flag in DEEP_HARD_IMPACT_FLAGS:
        if impact_flags.get(flag, False):
            triggers.add(f"IMPACT_FLAG:{flag}")

    # 检查真机证据
    if requires_real_device_evidence:
        triggers.add("REAL_DEVICE_EVIDENCE")

    # 检查跨领域
    if len(affected_domains) > 1:
        triggers.add("CROSS_DOMAIN")

    return sorted(triggers)


def check_advisory_triggers(
    task_description: str,
    affected_files: list[str],
) -> list[str]:
    """检查 advisory 关键词触发器（仅建议，不强制）"""
    triggers = set()
    combined_text = task_description.lower()

    for raw_path in affected_files:
        try:
            path = normalize_repo_path(raw_path)
        except ValueError:
            continue
        combined_text += " " + path.lower()

    for keyword in DEEP_ADVISORY_KEYWORDS:
        if keyword in combined_text:
            triggers.add(f"ADVISORY_KEYWORD:{keyword}")

    return sorted(triggers)


def validate_jev_response(response: dict) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    验证 Jev 响应是否符合合同

    Returns:
        (process_path, explicit_user_authorization, scope_expansion)
        任何验证失败返回 (None, None, None)
    """
    answers = response.get("answers")
    if not isinstance(answers, dict):
        return None, None, None

    # 验证 process_path
    process_path_answer = answers.get("process_path")
    if not isinstance(process_path_answer, dict):
        return None, None, None

    process_path = process_path_answer.get("choice")
    if process_path not in {"QUICK", "NORMAL", "DEEP"}:
        return None, None, None

    # 验证 explicit_user_authorization (noul)
    auth_answer = answers.get("explicit_user_authorization")
    explicit_user_authorization = None
    if isinstance(auth_answer, dict):
        explicit_user_authorization = auth_answer.get("bool")

    # 验证 scope_expansion (noul)
    scope_answer = answers.get("scope_expansion")
    scope_expansion = None
    if isinstance(scope_answer, dict):
        scope_expansion = scope_answer.get("bool")

    return process_path, explicit_user_authorization, scope_expansion


def observe_task_depth(
    task_description: str,
    affected_files: list[str] | None = None,
    affected_domains: list[str] | None = None,
    impact_flags: dict[str, bool] | None = None,
    requires_real_device_evidence: bool = False,
    api_key=_UNSET,
) -> dict:
    """
    观察任务复杂度，返回语义建议。

    Args:
        task_description: 任务描述
        affected_files: 涉及文件路径（仓库相对路径）
        affected_domains: 涉及领域
        impact_flags: 结构化硬规则标志
        requires_real_device_evidence: 是否需要真机证据
        api_key: TypeSafe API Key
            - _UNSET (默认): 从环境变量读取
            - None: 强制禁用网络，返回 UNAVAILABLE
            - str: 使用指定 Key

    Returns:
        {
            "status": "AVAILABLE" | "UNAVAILABLE" | "INVALID_RESPONSE",
            "input_sha256": str,
            "input_digest": str,
            "requested_model": str,
            "resolved_model": str | null,
            "jev_recommendation": "QUICK" | "NORMAL" | "DEEP" | null,
            "explicit_user_authorization": float | null,
            "scope_expansion": float | null,
            "hard_triggers": list[str],
            "advisory_triggers": list[str],
            "deterministic_override": "DEEP" | null,
            "authority": dict,
            "authority_effect": "NONE"
        }
    """
    if affected_files is None:
        affected_files = []
    if affected_domains is None:
        affected_domains = []
    if impact_flags is None:
        impact_flags = {}

    inputs = {
        "task_description": task_description,
        "affected_files": affected_files,
        "affected_domains": affected_domains,
        "impact_flags": impact_flags,
        "requires_real_device_evidence": requires_real_device_evidence,
    }
    input_sha256, input_digest = compute_input_digest(inputs)

    # 1. 检查硬规则触发
    hard_triggers = check_hard_triggers(
        affected_files, impact_flags, requires_real_device_evidence, affected_domains
    )
    advisory_triggers = check_advisory_triggers(task_description, affected_files)

    deterministic_override = "DEEP" if hard_triggers else None

    # 2. 尝试 Jev 观察
    if api_key is _UNSET:
        api_key = get_api_key()

    if not api_key:
        return {
            "status": "UNAVAILABLE",
            "input_sha256": input_sha256,
            "input_digest": input_digest,
            "requested_model": JEV_MODEL,
            "resolved_model": None,
            "jev_recommendation": None,
            "explicit_user_authorization": None,
            "scope_expansion": None,
            "hard_triggers": hard_triggers,
            "advisory_triggers": advisory_triggers,
            "deterministic_override": deterministic_override,
            "authority": AUTHORITY,
            "authority_effect": "NONE",
        }

    # 构建 Jev 状态
    state = {
        "task_description": task_description,
        "affected_files_count": len(affected_files),
        "affected_domains": affected_domains,
        "impact_flags": impact_flags,
        "requires_real_device_evidence": requires_real_device_evidence,
    }

    # 构建 Jev 问题（符合公开 API 合同）
    questions = {
        "process_path": {
            "type": "choice",
            "instructions": "这个任务适合哪种处理路径？",
            "criteria": {
                "QUICK": (
                    "单领域、窄文件范围、无治理文件、无合同变化、"
                    "无安全敏感变化、无真机证据要求"
                ),
                "NORMAL": (
                    "标准领域功能，需要常规测试和独立 Review，"
                    "但不涉及高风险合同或治理变化"
                ),
                "DEEP": (
                    "跨领域、治理、Prompt、Schema、Wire、Secret、"
                    "迁移、自动 Hook、Authority 或真实设备证据"
                ),
            },
        },
        "explicit_user_authorization": {
            "type": "noul",
            "instructions": "用户是否明确授权当前实施？",
            "criteria": {
                "true": "用户明确要求现在实施",
                "false": "仅讨论、建议、未来范围或未明确授权",
            },
        },
        "scope_expansion": {
            "type": "noul",
            "instructions": "候选动作是否扩大了用户原始范围？",
            "criteria": {
                "true": "候选动作增加了用户没有要求的范围",
                "false": "候选动作严格保持用户原始范围",
            },
        },
    }

    response, error_code = call_jev_api(state, questions, api_key)

    if not response:
        return {
            "status": "UNAVAILABLE",
            "error_code": error_code,
            "input_sha256": input_sha256,
            "input_digest": input_digest,
            "requested_model": JEV_MODEL,
            "resolved_model": None,
            "jev_recommendation": None,
            "explicit_user_authorization": None,
            "scope_expansion": None,
            "hard_triggers": hard_triggers,
            "advisory_triggers": advisory_triggers,
            "deterministic_override": deterministic_override,
            "authority": AUTHORITY,
            "authority_effect": "NONE",
        }

    # 验证响应
    resolved_model = response.get("model")
    process_path, explicit_user_authorization, scope_expansion = validate_jev_response(response)

    if process_path is None:
        return {
            "status": "INVALID_RESPONSE",
            "input_sha256": input_sha256,
            "input_digest": input_digest,
            "requested_model": JEV_MODEL,
            "resolved_model": resolved_model,
            "jev_recommendation": None,
            "explicit_user_authorization": None,
            "scope_expansion": None,
            "hard_triggers": hard_triggers,
            "advisory_triggers": advisory_triggers,
            "deterministic_override": deterministic_override,
            "authority": AUTHORITY,
            "authority_effect": "NONE",
        }

    return {
        "status": "AVAILABLE",
        "input_sha256": input_sha256,
        "input_digest": input_digest,
        "requested_model": JEV_MODEL,
        "resolved_model": resolved_model,
        "jev_recommendation": process_path,
        "explicit_user_authorization": explicit_user_authorization,
        "scope_expansion": scope_expansion,
        "hard_triggers": hard_triggers,
        "advisory_triggers": advisory_triggers,
        "deterministic_override": deterministic_override,
        "authority": AUTHORITY,
        "authority_effect": "NONE",
    }


def select_pm_process_path(observation: dict) -> dict:
    """
    PM 根据观察结果选择处理路径

    决策逻辑：
    1. 硬规则触发 → DEEP
    2. Jev 建议可用 → PM 审核并记录决定
    3. Jev 不可用 → 默认 NORMAL（不是 QUICK）
    """
    hard_triggers = observation.get("hard_triggers", [])
    jev_recommendation = observation.get("jev_recommendation")
    status = observation.get("status")

    if hard_triggers:
        return {
            "selected_path": "DEEP",
            "jev_recommendation": jev_recommendation,
            "deterministic_overrides": hard_triggers,
            "rationale": "硬规则强制 DEEP",
        }

    if status == "AVAILABLE" and jev_recommendation:
        return {
            "selected_path": jev_recommendation,
            "jev_recommendation": jev_recommendation,
            "deterministic_overrides": [],
            "rationale": "PM 审核 Jev 建议后决定",
        }

    # Jev 不可用或响应无效
    return {
        "selected_path": "NORMAL",
        "jev_recommendation": None,
        "deterministic_overrides": ["JEV_UNAVAILABLE" if status == "UNAVAILABLE" else "JEV_INVALID_RESPONSE"],
        "rationale": "Jev 不可用，PM 人工决定默认 NORMAL",
    }


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Jev 任务深度观察器（PM 语义传感器，authority_effect=NONE）"
    )
    parser.add_argument("description", help="任务描述")
    parser.add_argument("--files", nargs="*", default=[], help="涉及文件路径（仓库相对路径）")
    parser.add_argument("--domains", nargs="*", default=[], help="涉及领域")
    parser.add_argument("--dependencies", action="store_true", help="是否有依赖")
    parser.add_argument("--real-device", action="store_true", help="是否需要真机证据")
    parser.add_argument("--no-jev", action="store_true", help="强制禁用 Jev API")

    args = parser.parse_args()

    api_key = None if args.no_jev else _UNSET

    result = observe_task_depth(
        task_description=args.description,
        affected_files=args.files,
        affected_domains=args.domains,
        requires_real_device_evidence=args.real_device,
        api_key=api_key,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
