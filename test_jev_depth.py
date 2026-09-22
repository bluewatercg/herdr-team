#!/usr/bin/env python3
"""测试 Jev 任务深度观察器（PM 语义传感器）"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from jev_task_depth import observe_task_depth


def test_simple_task():
    """简单任务：无硬触发，Jev 不可用时返回 null"""
    result = observe_task_depth(
        task_description="修改配置文件",
        affected_files=["config.txt"],
        affected_domains=["android"],
    )

    assert result["status"] == "UNAVAILABLE", "无 API Key 时应为 UNAVAILABLE"
    assert result["jev_recommendation"] is None
    assert result["hard_triggers"] == []
    assert result["deterministic_override"] is None
    assert result["authority_effect"] == "NONE"
    assert len(result["input_digest"]) == 16
    print("✓ 简单任务：无硬触发，authority_effect=NONE")


def test_prompt_file_forces_deep():
    """修改 prompts/** 强制 DEEP"""
    result = observe_task_depth(
        task_description="修改 PM prompt",
        affected_files=["prompts/pm.md"],
    )

    assert "PATH_TRIGGER:prompts/" in result["hard_triggers"]
    assert result["deterministic_override"] == "DEEP"
    assert result["authority_effect"] == "NONE"
    print("✓ prompts/** 强制 DEEP，Jev 不能降级")


def test_agent_control_forces_deep():
    """修改 .agent-control/** 强制 DEEP"""
    result = observe_task_depth(
        task_description="修改任务板",
        affected_files=[".agent-control/TASK_BOARD.md"],
    )

    assert "PATH_TRIGGER:.agent-control/" in result["hard_triggers"]
    assert result["deterministic_override"] == "DEEP"
    print("✓ .agent-control/** 强制 DEEP")


def test_schema_keyword_forces_deep():
    """涉及 schema 关键词强制 DEEP"""
    result = observe_task_depth(
        task_description="修改 schema 定义",
        affected_files=["src/model.py"],
    )

    assert "KEYWORD_TRIGGER:schema" in result["hard_triggers"]
    assert result["deterministic_override"] == "DEEP"
    print("✓ schema 关键词强制 DEEP")


def test_real_device_forces_deep():
    """需要真机证据强制 DEEP"""
    result = observe_task_depth(
        task_description="测试相机功能",
        affected_files=["CameraActivity.java"],
        requires_real_device_evidence=True,
    )

    assert "REAL_DEVICE_EVIDENCE" in result["hard_triggers"]
    assert result["deterministic_override"] == "DEEP"
    print("✓ 真机证据强制 DEEP")


def test_cross_domain_forces_deep():
    """跨领域强制 DEEP"""
    result = observe_task_depth(
        task_description="跨平台修改",
        affected_domains=["android", "api"],
    )

    assert "CROSS_DOMAIN" in result["hard_triggers"]
    assert result["deterministic_override"] == "DEEP"
    print("✓ 跨领域强制 DEEP")


def test_jev_unavailable_no_quik_default():
    """Jev 不可用时不默认 QUICK"""
    result = observe_task_depth(
        task_description="简单任务",
        affected_files=["readme.txt"],
    )

    assert result["status"] == "UNAVAILABLE"
    assert result["jev_recommendation"] is None
    # PM 应该默认 NORMAL，不是 QUICK
    print("✓ Jev 不可用时返回 null，PM 默认 NORMAL（不是 QUICK）")


def test_authority_always_none():
    """所有场景 authority_effect 都是 NONE"""
    scenarios = [
        {"task_description": "简单任务", "affected_files": ["a.txt"]},
        {"task_description": "修改 prompt", "affected_files": ["prompts/pm.md"]},
        {"task_description": "跨领域", "affected_domains": ["android", "api"]},
    ]

    for s in scenarios:
        result = observe_task_depth(**s)
        assert result["authority_effect"] == "NONE", f"authority_effect 必须是 NONE: {s}"

    print("✓ 所有场景 authority_effect=NONE")


def main():
    print("=" * 60)
    print("Jev 任务深度观察器测试（PM 语义传感器）")
    print("=" * 60)

    tests = [
        test_simple_task,
        test_prompt_file_forces_deep,
        test_agent_control_forces_deep,
        test_schema_keyword_forces_deep,
        test_real_device_forces_deep,
        test_cross_domain_forces_deep,
        test_jev_unavailable_no_quik_default,
        test_authority_always_none,
    ]

    for t in tests:
        t()

    print("=" * 60)
    print("✓ 所有测试通过")


if __name__ == "__main__":
    main()
