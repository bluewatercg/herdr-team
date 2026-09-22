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
]

# .agent-control/ 目录下的关键状态文件（非元数据）
DEEP_HARD_AGENT_CONTROL_FILES = [
    "MASTER_PLAN.md",
    "TASK_BOARD.md",
    "BLOCKERS.md",
    "DECISIONS.md",
    "PM_GATE",
    "FILE_OWNERSHIP.md",
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
                    "JEV_NETWORK_UNAVAILABLE" | "JEV_RESPONSE_INVALID_JSON" |
                    "JEV_CLIENT_INTERNAL_ERROR"
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
        return None, "JEV_CLIENT_INTERNAL_ERROR"


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

        # 检查前缀匹配（如 prompts/）
        for prefix in DEEP_HARD_PATH_PREFIXES:
            if path.startswith(prefix):
                triggers.add(f"PATH_TRIGGER:{prefix}")

        # 检查 .agent-control/ 目录下的关键文件（排除元数据文件）
        if path.startswith(".agent-control/"):
            filename = PurePosixPath(path).name
            if filename in DEEP_HARD_AGENT_CONTROL_FILES:
                triggers.add(f"AGENT_CONTROL_TRIGGER:{filename}")

        # 检查特定文件名（如 activate.sh、review_dispatch.py）
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

def read_noul(answer: object) -> Optional[float]:
    """
    严格验证 noul 值

    Returns:
        float | None
        必须满足：
        - 是 dict 且包含 "noul" 字段
        - 值是 float 或 int（不是 bool）
        - 0.0 <= value <= 1.0
        - 不是 NaN 或 Infinity
    """
    if not isinstance(answer, dict):
        return None

    value = answer.get("noul")

    # bool 是 int 的子类，必须排除
    if isinstance(value, bool):
        return None

    if not isinstance(value, (int, float)):
        return None

    value = float(value)

    # 检查 NaN 和 Infinity
    import math
    if math.isnan(value) or math.isinf(value):
        return None

    if not 0.0 <= value <= 1.0:
        return None

    return value


def validate_jev_response(response: dict) -> tuple[Optional[str], Optional[float], Optional[float], Optional[str]]:
    """
    验证 Jev 响应是否符合合同

    Returns:
        (process_path, explicit_user_authorization, scope_expansion, resolved_model)
        任何验证失败返回 (None, None, None, None)
    """
    answers = response.get("answers")
    if not isinstance(answers, dict):
        return None, None, None, None

    # 验证 process_path
    process_path_answer = answers.get("process_path")
    if not isinstance(process_path_answer, dict):
        return None, None, None, None

    process_path = process_path_answer.get("choice")
    if process_path not in {"QUICK", "NORMAL", "DEEP"}:
        return None, None, None, None

    # 验证 explicit_user_authorization (noul)
    explicit_user_authorization = read_noul(answers.get("explicit_user_authorization"))

    # 验证 scope_expansion (noul)
    scope_expansion = read_noul(answers.get("scope_expansion"))

    # 验证 resolved_model (M-02)
    resolved_model = response.get("model")
    if resolved_model is not None and not isinstance(resolved_model, str):
        return None, None, None, None

    return process_path, explicit_user_authorization, scope_expansion, resolved_model


def observe_task_depth(
    *,
    user_verbatim: str,
    pm_interpretation: str,
    candidate_action: str,
    source_type: str,
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

    # H-02: 规范化路径，非法路径返回 INVALID_INPUT
    normalized_files = []
    for raw_path in affected_files:
        try:
            normalized_files.append(normalize_repo_path(raw_path))
        except ValueError:
            return {
                "status": "INVALID_INPUT",
                "error_code": "INVALID_REPOSITORY_PATH",
                "invalid_path": raw_path,
                "jev_recommendation": None,
                "hard_triggers": [],
                "advisory_triggers": [],
                "deterministic_override": None,
                "authority": AUTHORITY,
                "authority_effect": "NONE",
            }

    inputs = {
        "user_verbatim": user_verbatim,
        "pm_interpretation": pm_interpretation,
        "candidate_action": candidate_action,
        "source_type": source_type,
        "affected_files": normalized_files,
        "affected_domains": affected_domains,
        "impact_flags": impact_flags,
        "requires_real_device_evidence": requires_real_device_evidence,
    }
    input_sha256, input_digest = compute_input_digest(inputs)

    # 1. 检查硬规则触发
    hard_triggers = check_hard_triggers(
        normalized_files, impact_flags, requires_real_device_evidence, affected_domains
    )
    advisory_triggers = check_advisory_triggers(user_verbatim, normalized_files)

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

    # 构建 Jev 状态（B-02: 包含完整输入）
    state = {
        "user_verbatim": user_verbatim,
        "pm_interpretation": pm_interpretation,
        "candidate_action": candidate_action,
        "source_type": source_type,
        "affected_files": normalized_files,
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

    # 验证响应（M-02: validate_jev_response 现在返回 4 元组）
    process_path, explicit_user_authorization, scope_expansion, resolved_model = validate_jev_response(response)

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


def propose_process_path(observation: dict) -> dict:
    """
    提出处理路径建议（H-03: 分离 Jev Observation 与 PM Decision）

    返回建议，但不自动成为最终决策。
    只有硬规则可以不经 PM 降级。

    Returns:
        {
            "proposed_path": str,
            "decision_required": bool,
            "reasons": list[str],
        }
    """
    hard_triggers = observation.get("hard_triggers", [])
    jev_recommendation = observation.get("jev_recommendation")
    status = observation.get("status")

    # 硬规则强制 DEEP，不需要 PM 决策
    if hard_triggers:
        return {
            "proposed_path": "DEEP",
            "decision_required": False,
            "reasons": hard_triggers,
        }

    # Jev 建议可用，需要 PM 决策
    if status == "AVAILABLE" and jev_recommendation:
        return {
            "proposed_path": jev_recommendation,
            "decision_required": True,
            "reasons": [],
        }

    # Jev 不可用或响应无效，需要 PM 决策
    return {
        "proposed_path": "NORMAL",
        "decision_required": True,
        "reasons": ["JEV_UNAVAILABLE" if status == "UNAVAILABLE" else "JEV_INVALID_RESPONSE"],
    }


def record_pm_process_decision(
    *,
    observation: dict,
    proposal: dict,
    selected_path: str,
    rationale: str,
) -> dict:
    """
    记录 PM 最终决策（H-03）

    Args:
        observation: observe_task_depth 的输出
        proposal: propose_process_path 的输出
        selected_path: PM 最终选择的路径
        rationale: PM 决策理由

    Returns:
        {
            "selected_path": str,
            "jev_recommendation": str | null,
            "deterministic_overrides": list[str],
            "rationale": str,
        }
    """
    # 验证：如果硬规则触发，selected_path 必须是 DEEP
    hard_triggers = observation.get("hard_triggers", [])
    if hard_triggers and selected_path != "DEEP":
        raise ValueError(
            f"硬规则触发时必须选择 DEEP，但选择了 {selected_path}。"
            f"触发器: {hard_triggers}"
        )

    return {
        "selected_path": selected_path,
        "jev_recommendation": observation.get("jev_recommendation"),
        "deterministic_overrides": hard_triggers,
        "rationale": rationale,
    }


def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Jev 任务深度观察器（PM 语义传感器，authority_effect=NONE）"
    )
    parser.add_argument("user_verbatim", help="用户原始表达")
    parser.add_argument("--pm-interpretation", default="", help="PM 对用户意图的理解")
    parser.add_argument("--candidate-action", default="", help="PM 候选动作")
    parser.add_argument("--source-type", default="USER_VERBATIM", help="来源类型")
    parser.add_argument("--files", nargs="*", default=[], help="涉及文件路径（仓库相对路径）")
    parser.add_argument("--domains", nargs="*", default=[], help="涉及领域")
    parser.add_argument("--real-device", action="store_true", help="是否需要真机证据")
    parser.add_argument("--no-jev", action="store_true", help="强制禁用 Jev API")

    args = parser.parse_args()

    api_key = None if args.no_jev else _UNSET

    result = observe_task_depth(
        user_verbatim=args.user_verbatim,
        pm_interpretation=args.pm_interpretation,
        candidate_action=args.candidate_action,
        source_type=args.source_type,
        affected_files=args.files,
        affected_domains=args.domains,
        requires_real_device_evidence=args.real_device,
        api_key=api_key,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
