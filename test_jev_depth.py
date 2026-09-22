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
    propose_process_path,
    record_pm_process_decision,
    normalize_repo_path,
    check_hard_triggers,
    validate_jev_response,
    read_noul,
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
        """.agent-control/ 关键文件触发"""
        triggers = check_hard_triggers([".agent-control/TASK_BOARD.md"], {}, False, [])
        self.assertIn("AGENT_CONTROL_TRIGGER:TASK_BOARD.md", triggers)

    def test_agent_control_metadata_no_trigger(self):
        """.agent-control/ 元数据文件不触发"""
        triggers = check_hard_triggers([".agent-control/REVIEW_QUEUE.md"], {}, False, [])
        # REVIEW_QUEUE.md 是元数据文件，不应该触发
        self.assertEqual(triggers, [])

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
                "explicit_user_authorization": {"noul": 0.9},
                "scope_expansion": {"noul": 0.1},
            },
        }
        path, auth, scope, model = validate_jev_response(response)
        self.assertEqual(path, "NORMAL")
        self.assertEqual(auth, 0.9)
        self.assertEqual(scope, 0.1)
        self.assertEqual(model, "jev-1.13.0")

    def test_invalid_choice(self):
        """无效 choice 值"""
        response = {
            "answers": {
                "process_path": {"choice": "INVALID"},
            }
        }
        path, _, _, _ = validate_jev_response(response)
        self.assertIsNone(path)

    def test_missing_answers(self):
        """缺少 answers 字段"""
        response = {"model": "jev-1.13.0"}
        path, _, _, _ = validate_jev_response(response)
        self.assertIsNone(path)

    def test_empty_answers(self):
        """空 answers"""
        response = {"answers": {}}
        path, _, _, _ = validate_jev_response(response)
        self.assertIsNone(path)

    def test_missing_choice_field(self):
        """缺少 choice 字段"""
        response = {"answers": {"process_path": {"confidence": 0.8}}}
        path, _, _, _ = validate_jev_response(response)
        self.assertIsNone(path)

    def test_invalid_model_type(self):
        """model 类型无效"""
        response = {
            "model": 123,
            "answers": {
                "process_path": {"choice": "NORMAL"},
                "explicit_user_authorization": {"noul": 0.9},
                "scope_expansion": {"noul": 0.1},
            },
        }
        path, _, _, _ = validate_jev_response(response)
        self.assertIsNone(path)


class TestObserveTaskDepth(unittest.TestCase):
    """测试观察函数"""

    def test_no_api_key_returns_unavailable(self):
        """无 API Key 返回 UNAVAILABLE"""
        result = observe_task_depth(
            user_verbatim="简单任务",
            pm_interpretation="用户想要完成一个简单任务",
            candidate_action="执行简单修复",
            source_type="USER_VERBATIM",
            affected_files=["test.txt"],
            api_key=None,
        )
        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertIsNone(result["jev_recommendation"])
        self.assertEqual(result["authority_effect"], "NONE")

    def test_hard_triggers_force_deep(self):
        """硬规则强制 DEEP"""
        result = observe_task_depth(
            user_verbatim="修改 prompt",
            pm_interpretation="用户想要修改 PM 提示词",
            candidate_action="修改 prompts/pm.md",
            source_type="USER_VERBATIM",
            affected_files=["prompts/pm.md"],
            api_key=None,
        )
        self.assertIn("PATH_TRIGGER:prompts/", result["hard_triggers"])
        self.assertEqual(result["deterministic_override"], "DEEP")

    def test_authority_always_false(self):
        """Authority 始终为 False"""
        result = observe_task_depth(
            user_verbatim="测试",
            pm_interpretation="测试任务",
            candidate_action="执行测试",
            source_type="USER_VERBATIM",
            api_key=None,
        )
        for key, value in result["authority"].items():
            self.assertFalse(value, f"{key} 应为 False")

    def test_input_sha256_full_length(self):
        """SHA-256 完整长度"""
        result = observe_task_depth(
            user_verbatim="测试",
            pm_interpretation="测试任务",
            candidate_action="执行测试",
            source_type="USER_VERBATIM",
            api_key=None,
        )
        self.assertEqual(len(result["input_sha256"]), 64)
        self.assertEqual(len(result["input_digest"]), 16)

    def test_requested_model_present(self):
        """requested_model 存在"""
        result = observe_task_depth(
            user_verbatim="测试",
            pm_interpretation="测试任务",
            candidate_action="执行测试",
            source_type="USER_VERBATIM",
            api_key=None,
        )
        self.assertEqual(result["requested_model"], "jev-latest")

    def test_invalid_path_returns_invalid_input(self):
        """非法路径返回 INVALID_INPUT"""
        result = observe_task_depth(
            user_verbatim="修正 PM 规则",
            pm_interpretation="修改 PM Prompt",
            candidate_action="修改 prompts/pm.md",
            source_type="USER_VERBATIM",
            affected_files=["../prompts/pm.md"],
            api_key=None,
        )
        self.assertEqual(result["status"], "INVALID_INPUT")
        self.assertEqual(result["error_code"], "INVALID_REPOSITORY_PATH")
    def test_invalid_source_type_returns_invalid_input(self):
        """非法来源类型返回 INVALID_INPUT"""
        result = observe_task_depth(
            user_verbatim="测试",
            pm_interpretation="测试任务",
            candidate_action="执行测试",
            source_type="INVENTED_SOURCE",
            api_key=None,
        )
        self.assertEqual(result["status"], "INVALID_INPUT")
        self.assertEqual(result["error_code"], "INVALID_SOURCE_TYPE")

    @patch("jev_task_depth.call_jev_api")
    def test_mock_quick_response(self, mock_call):
        """Mock QUICK 响应"""
        mock_call.return_value = (
            {
                "model": "jev-1.13.0",
                "answers": {
                    "process_path": {"choice": "QUICK"},
                    "explicit_user_authorization": {"noul": 0.95},
                    "scope_expansion": {"noul": 0.05},
                },
            },
            None,
        )

        result = observe_task_depth(
            user_verbatim="简单修复",
            pm_interpretation="用户想要修复一个小问题",
            candidate_action="修复 src/fix.py 中的 bug",
            source_type="USER_VERBATIM",
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
            user_verbatim="测试",
            pm_interpretation="测试任务",
            candidate_action="执行测试",
            source_type="USER_VERBATIM",
            api_key="test-key",
        )

        self.assertEqual(result["status"], "INVALID_RESPONSE")
        self.assertIsNone(result["jev_recommendation"])

    @patch("jev_task_depth.call_jev_api")
    def test_mock_api_error(self, mock_call):
        """Mock API 错误"""
        mock_call.return_value = (None, "JEV_RATE_LIMITED")

        result = observe_task_depth(
            user_verbatim="测试",
            pm_interpretation="测试任务",
            candidate_action="执行测试",
            source_type="USER_VERBATIM",
            api_key="test-key",
        )

        self.assertEqual(result["status"], "UNAVAILABLE")
        self.assertEqual(result["error_code"], "JEV_RATE_LIMITED")



class TestProposeProcessPath(unittest.TestCase):
    """测试 PM 提议函数"""

    def test_hard_triggers_propose_deep(self):
        """硬规则提议 DEEP"""
        observation = {
            "status": "AVAILABLE",
            "jev_recommendation": "QUICK",
            "hard_triggers": ["PATH_TRIGGER:prompts/"],
        }
        proposal = propose_process_path(observation)
        self.assertEqual(proposal["proposed_path"], "DEEP")
        self.assertFalse(proposal["decision_required"])

    def test_jev_available_proposes_recommendation(self):
        """Jev 可用时提议建议"""
        observation = {
            "status": "AVAILABLE",
            "jev_recommendation": "NORMAL",
            "hard_triggers": [],
        }
        proposal = propose_process_path(observation)
        self.assertEqual(proposal["proposed_path"], "NORMAL")
        self.assertTrue(proposal["decision_required"])

    def test_jev_unavailable_proposes_normal(self):
        """Jev 不可用提议 NORMAL"""
        observation = {
            "status": "UNAVAILABLE",
            "jev_recommendation": None,
            "hard_triggers": [],
        }
        proposal = propose_process_path(observation)
        self.assertEqual(proposal["proposed_path"], "NORMAL")
        self.assertTrue(proposal["decision_required"])
        self.assertIn("JEV_UNAVAILABLE", proposal["reasons"])

    def test_invalid_response_proposes_normal(self):
        """无效响应提议 NORMAL"""
        observation = {
            "status": "INVALID_RESPONSE",
            "jev_recommendation": None,
            "hard_triggers": [],
        }
        proposal = propose_process_path(observation)
        self.assertEqual(proposal["proposed_path"], "NORMAL")
        self.assertTrue(proposal["decision_required"])
        self.assertIn("JEV_INVALID_RESPONSE", proposal["reasons"])


class TestRecordPmProcessDecision(unittest.TestCase):
    """测试 PM 决策记录函数"""

    def test_record_decision_without_hard_triggers(self):
        """无硬规则时记录决策"""
        observation = {
            "status": "AVAILABLE",
            "jev_recommendation": "NORMAL",
            "hard_triggers": [],
        }
        proposal = propose_process_path(observation)
        decision = record_pm_process_decision(
            observation=observation,
            proposal=proposal,
            selected_path="NORMAL",
            rationale="PM 审核后同意 Jev 建议",
        )
        self.assertEqual(decision["selected_path"], "NORMAL")
        self.assertEqual(decision["jev_recommendation"], "NORMAL")
        self.assertEqual(decision["rationale"], "PM 审核后同意 Jev 建议")

    def test_record_decision_with_hard_triggers(self):
        """有硬规则时记录 DEEP 决策"""
        observation = {
            "status": "AVAILABLE",
            "jev_recommendation": "QUICK",
            "hard_triggers": ["PATH_TRIGGER:prompts/"],
        }
        proposal = propose_process_path(observation)
        decision = record_pm_process_decision(
            observation=observation,
            proposal=proposal,
            selected_path="DEEP",
            rationale="硬规则强制 DEEP",
        )
        self.assertEqual(decision["selected_path"], "DEEP")
        self.assertEqual(decision["jev_recommendation"], "QUICK")

    def test_record_decision_rejects_non_deep_with_hard_triggers(self):
        """有硬规则时拒绝非 DEEP 决策"""
        observation = {
            "status": "AVAILABLE",
            "jev_recommendation": "QUICK",
            "hard_triggers": ["PATH_TRIGGER:prompts/"],
        }
        proposal = propose_process_path(observation)
        with self.assertRaises(ValueError) as ctx:
            record_pm_process_decision(
                observation=observation,
                proposal=proposal,
                selected_path="NORMAL",
                rationale="PM 想要降级",
            )
        self.assertIn("硬规则触发时必须选择 DEEP", str(ctx.exception))


class TestEnvironmentIsolation(unittest.TestCase):
    """测试环境隔离"""

    def test_no_env_var_no_api_call(self):
        """无环境变量不调用 API"""
        with patch.dict(os.environ, {}, clear=True):
            result = observe_task_depth(
                user_verbatim="测试",
                pm_interpretation="测试任务",
                candidate_action="执行测试",
                source_type="USER_VERBATIM",
                affected_files=["test.txt"],
            )
            self.assertEqual(result["status"], "UNAVAILABLE")

    def test_api_key_none_forces_offline(self):
        """api_key=None 强制离线"""
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "real-key"}):
            result = observe_task_depth(
                user_verbatim="测试",
                pm_interpretation="测试任务",
                candidate_action="执行测试",
                source_type="USER_VERBATIM",
                api_key=None,
            )
            self.assertEqual(result["status"], "UNAVAILABLE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
