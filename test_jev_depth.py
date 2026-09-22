#!/usr/bin/env python3
"""Jev 任务深度观察器测试 - PM 语义传感器"""

import json
import os
import sys
import unittest
from unittest.mock import patch

# 导入被测模块
from jev_task_depth import (
    observe_task_depth,
    select_pm_process_path,
    normalize_repo_path,
    check_hard_triggers,
    validate_jev_response,
    AUTHORITY,
)


class TestNormalizeRepoPath(unittest.TestCase):
    """测试路径规范化"""

    def test_simple_path(self):
        """简单路径"""
        self.assertEqual(normalize_repo_path("prompts/pm.md"), "prompts/pm.md")

    def test_dot_slash_prefix(self):
        """移除 ./ 前缀"""
        self.assertEqual(normalize_repo_path("./prompts/pm.md"), "prompts/pm.md")

    def test_backslash_to_slash(self):
        """Windows 路径转换"""
        self.assertEqual(normalize_repo_path("prompts\\pm.md"), "prompts/pm.md")

    def test_absolute_path_rejected(self):
        """拒绝绝对路径"""
        with self.assertRaises(ValueError):
            normalize_repo_path("/etc/passwd")

    def test_path_escape_rejected(self):
        """拒绝路径逃逸"""
        with self.assertRaises(ValueError):
            normalize_repo_path("../etc/passwd")


class TestHardTriggers(unittest.TestCase):
    """测试硬规则触发器"""

    def test_prompts_path_trigger(self):
        """prompts/ 路径触发"""
        triggers = check_hard_triggers(["prompts/pm.md"], {}, False, [])
        self.assertIn("PATH_TRIGGER:prompts/", triggers)

    def test_agent_control_trigger(self):
        """.agent-control/ 路径触发"""
        triggers = check_hard_triggers([".agent-control/TASK_BOARD.md"], {}, False, [])
        self.assertIn("PATH_TRIGGER:.agent-control/", triggers)

    def test_impact_flag_trigger(self):
        """结构化标志触发"""
        triggers = check_hard_triggers([], {"changes_schema": True}, False, [])
        self.assertIn("IMPACT_FLAG:changes_schema", triggers)

    def test_real_device_trigger(self):
        """真机证据触发"""
        triggers = check_hard_triggers([], {}, True, [])
        self.assertIn("REAL_DEVICE_EVIDENCE", triggers)

    def test_cross_domain_trigger(self):
        """跨领域触发"""
        triggers = check_hard_triggers([], {}, False, ["android", "api"])
        self.assertIn("CROSS_DOMAIN", triggers)

    def test_single_domain_no_trigger(self):
        """单领域不触发"""
        triggers = check_hard_triggers([], {}, False, ["android"])
        self.assertNotIn("CROSS_DOMAIN", triggers)

    def test_triggers_sorted_unique(self):
        """触发器排序且去重"""
        triggers = check_hard_triggers(
            ["prompts/pm.md", "prompts/start.md"], {}, False, []
        )
        self.assertEqual(triggers, ["PATH_TRIGGER:prompts/"])


class TestValidateJevResponse(unittest.TestCase):
    """测试 Jev 响应验证"""

    def test_valid_response(self):
        """有效响应"""
        response = {
            "model": "jev-1.13.0",
            "answers": {
                "process_path": {"choice": "NORMAL"},
                "explicit_user_authorization": {"bool": 0.9},
                "scope_expansion": {"bool": 0.1},
            },
        }
        path, auth, scope = validate_jev_response(response)
        self.assertEqual(path, "NORMAL")
        self.assertEqual(auth, 0.9)
        self.assertEqual(scope, 0.1)

    def test_invalid_choice(self):
        """无效 choice 值"""
        response = {
            "answers": {
                "process_path": {"choice": "INVALID"},
            }
        }
        path, _, _ = validate_jev_response(response)
        self.assertIsNone(path)

    def test_missing_answers(self):
        """缺少 answers 字段"""
        response = {"model": "jev-1.13.0"}
        path, _, _ = validate_jev_response(response)
        self.assertIsNone(path)

    def test_empty_answers(self):
        """空 answers"""
        response = {"answers": {}}
        path, _, _ = validate_jev_response(response)
        self.assertIsNone(path)

    def test_missing_choice_field(self):
        """缺少 choice 字段"""
        response = {"answers": {"process_path": {"confidence": 0.8}}}
        path, _, _ = validate_jev_response(response)
        self.assertIsNone(path)


class TestObserveTaskDepth(unittest.TestCase):
    """测试观察函数"""

    def test_no_api_key_returns_unavailable(self):
        """无 API Key 返回 UNAVAILABLE"""
        result = observe_task_depth(
            task_description="简单任务",
            affected_files=["test.txt"],
            api_key=None,
        )
        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertIsNone(result["jev_recommendation"])
        self.assertEqual(result["authority_effect"], "NONE")

    def test_hard_triggers_force_deep(self):
        """硬规则强制 DEEP"""
        result = observe_task_depth(
            task_description="修改 prompt",
            affected_files=["prompts/pm.md"],
            api_key=None,
        )
        self.assertIn("PATH_TRIGGER:prompts/", result["hard_triggers"])
        self.assertEqual(result["deterministic_override"], "DEEP")

    def test_authority_always_false(self):
        """Authority 始终为 False"""
        result = observe_task_depth(
            task_description="测试",
            api_key=None,
        )
        for key, value in result["authority"].items():
            self.assertFalse(value, f"{key} 应为 False")

    def test_input_sha256_full_length(self):
        """SHA-256 完整长度"""
        result = observe_task_depth(
            task_description="测试",
            api_key=None,
        )
        self.assertEqual(len(result["input_sha256"]), 64)
        self.assertEqual(len(result["input_digest"]), 16)

    def test_requested_model_present(self):
        """requested_model 存在"""
        result = observe_task_depth(
            task_description="测试",
            api_key=None,
        )
        self.assertEqual(result["requested_model"], "jev-latest")

    @patch("jev_task_depth.call_jev_api")
    def test_mock_quick_response(self, mock_call):
        """Mock QUICK 响应"""
        mock_call.return_value = (
            {
                "model": "jev-1.13.0",
                "answers": {
                    "process_path": {"choice": "QUICK"},
                    "explicit_user_authorization": {"bool": 0.95},
                    "scope_expansion": {"bool": 0.05},
                },
            },
            None,
        )

        result = observe_task_depth(
            task_description="简单修复",
            affected_files=["src/fix.py"],
            api_key="test-key",
        )

        self.assertEqual(result["status"], "AVAILABLE")
        self.assertEqual(result["jev_recommendation"], "QUICK")
        self.assertEqual(result["resolved_model"], "jev-1.13.0")

    @patch("jev_task_depth.call_jev_api")
    def test_mock_invalid_response(self, mock_call):
        """Mock 无效响应"""
        mock_call.return_value = (
            {
                "answers": {"process_path": {"choice": "INVALID"}},
            },
            None,
        )

        result = observe_task_depth(
            task_description="测试",
            api_key="test-key",
        )

        self.assertEqual(result["status"], "INVALID_RESPONSE")
        self.assertIsNone(result["jev_recommendation"])

    @patch("jev_task_depth.call_jev_api")
    def test_mock_api_error(self, mock_call):
        """Mock API 错误"""
        mock_call.return_value = (None, "JEV_RATE_LIMITED")

        result = observe_task_depth(
            task_description="测试",
            api_key="test-key",
        )

        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertEqual(result["error_code"], "JEV_RATE_LIMITED")


class TestSelectPmProcessPath(unittest.TestCase):
    """测试 PM 决策函数"""

    def test_hard_triggers_force_deep(self):
        """硬规则强制 DEEP"""
        observation = {
            "status": "AVAILABLE",
            "jev_recommendation": "QUICK",
            "hard_triggers": ["PATH_TRIGGER:prompts/"],
        }
        decision = select_pm_process_path(observation)
        self.assertEqual(decision["selected_path"], "DEEP")
        self.assertEqual(decision["jev_recommendation"], "QUICK")

    def test_jev_available_uses_recommendation(self):
        """Jev 可用时使用建议"""
        observation = {
            "status": "AVAILABLE",
            "jev_recommendation": "NORMAL",
            "hard_triggers": [],
        }
        decision = select_pm_process_path(observation)
        self.assertEqual(decision["selected_path"], "NORMAL")

    def test_jev_unavailable_defaults_normal(self):
        """Jev 不可用默认 NORMAL"""
        observation = {
            "status": "UNAVAILABLE",
            "jev_recommendation": None,
            "hard_triggers": [],
        }
        decision = select_pm_process_path(observation)
        self.assertEqual(decision["selected_path"], "NORMAL")
        self.assertIn("JEV_UNAVAILABLE", decision["deterministic_overrides"])

    def test_invalid_response_defaults_normal(self):
        """无效响应默认 NORMAL"""
        observation = {
            "status": "INVALID_RESPONSE",
            "jev_recommendation": None,
            "hard_triggers": [],
        }
        decision = select_pm_process_path(observation)
        self.assertEqual(decision["selected_path"], "NORMAL")
        self.assertIn("JEV_INVALID_RESPONSE", decision["deterministic_overrides"])


class TestEnvironmentIsolation(unittest.TestCase):
    """测试环境隔离"""

    def test_no_env_var_no_api_call(self):
        """无环境变量不调用 API"""
        with patch.dict(os.environ, {}, clear=True):
            result = observe_task_depth(
                task_description="测试",
                affected_files=["test.txt"],
            )
            self.assertEqual(result["status"], "UNAVAILABLE")

    def test_api_key_none_forces_offline(self):
        """api_key=None 强制离线"""
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "real-key"}):
            result = observe_task_depth(
                task_description="测试",
                api_key=None,
            )
            self.assertEqual(result["status"], "UNAVAILABLE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
