#!/usr/bin/env python3
"""Jev Task Depth Evaluator - 评估任务需要的处理深度

使用 TypeSafe Jev API 对任务进行分类：
- quick: 简单任务，直接执行
- normal: 标准任务，适度协调
- deep: 复杂任务，完整流程
"""
import json
import os
import sys
from pathlib import Path
from typing import Any, Optional
import urllib.request
import urllib.error

# TypeSafe Jev API 配置
JEV_ENDPOINT = "https://api.typesafe.ai/v1/systemone"
JEV_MODEL = "jev-latest"
JEV_API_KEY_ENV = "TYPESAFE_API_KEY"


def get_api_key() -> Optional[str]:
    """从环境变量获取 API Key"""
    return os.environ.get(JEV_API_KEY_ENV)


def call_jev_api(state: dict, questions: list, api_key: str) -> dict:
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
    except urllib.error.HTTPError as e:
        print(f"Jev API error: {e.code} {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Jev API request failed: {e}", file=sys.stderr)
        return None


def evaluate_task_depth(
    task_description: str,
    files_involved: int = 1,
    has_dependencies: bool = False,
    risk_level: str = "low",
    uncertainty: str = "none",
    requires_coordination: bool = False,
    api_key: Optional[str] = None
) -> dict:
    """
    评估任务需要的处理深度
    
    Args:
        task_description: 任务描述
        files_involved: 涉及文件数量
        has_dependencies: 是否有依赖
        risk_level: 风险等级 (low/medium/high)
        uncertainty: 不确定性 (none/partial/unknown)
        requires_coordination: 是否需要多 Agent 协调
        api_key: TypeSafe API Key（可选，默认从环境变量读取）
    
    Returns:
        {
            "depth": "quick" | "normal" | "deep",
            "confidence": 0.0-1.0,
            "reasoning": str,
            "recommendations": list
        }
    """
    if api_key is None:
        api_key = get_api_key()
    
    if not api_key:
        # 降级：基于规则的评估
        return _rule_based_evaluation(
            files_involved, has_dependencies, risk_level, 
            uncertainty, requires_coordination
        )
    
    # 构建 Jev 状态
    state = {
        "task_description": task_description,
        "files_involved": files_involved,
        "has_dependencies": has_dependencies,
        "risk_level": risk_level,
        "uncertainty": uncertainty,
        "requires_coordination": requires_coordination
    }
    
    # 构建 Jev 问题
    questions = [
        {
            "id": "research_depth",
            "type": "choice",
            "instructions": "这个任务需要多深的研究和协调？",
            "criteria": {
                "labels": ["quick", "normal", "deep"]
            }
        },
        {
            "id": "confidence",
            "type": "score",
            "instructions": "你对这个判断的置信度是多少？",
            "criteria": [0.0, 1.0]
        },
        {
            "id": "reasoning",
            "type": "choice",
            "instructions": "主要考虑因素是什么？",
            "criteria": {
                "labels": [
                    "single_file_simple_fix",
                    "multi_file_coordination",
                    "unknown_implementation",
                    "high_risk_change",
                    "historical_precedent",
                    "complex_dependencies"
                ]
            }
        }
    ]
    
    # 调用 Jev API
    response = call_jev_api(state, questions, api_key)
    
    if not response or "answers" not in response:
        # API 调用失败，降级到规则评估
        return _rule_based_evaluation(
            files_involved, has_dependencies, risk_level,
            uncertainty, requires_coordination
        )
    
    # 解析响应
    answers = response["answers"]
    
    depth = "normal"
    confidence = 0.5
    reasoning = "unknown"
    
    if "research_depth" in answers:
        depth = answers["research_depth"].get("choice", "normal")
    
    if "confidence" in answers:
        confidence = answers["confidence"].get("score", 0.5)
    
    if "reasoning" in answers:
        reasoning = answers["reasoning"].get("choice", "unknown")
    
    # 生成建议
    recommendations = _generate_recommendations(depth, confidence, reasoning)
    
    return {
        "depth": depth,
        "confidence": confidence,
        "reasoning": reasoning,
        "recommendations": recommendations
    }


def _rule_based_evaluation(
    files_involved: int,
    has_dependencies: bool,
    risk_level: str,
    uncertainty: str,
    requires_coordination: bool
) -> dict:
    """基于规则的降级评估（当 Jev API 不可用时）"""
    
    # 简单任务：单文件、无依赖、低风险、无不确定性
    if (files_involved == 1 and not has_dependencies and 
        risk_level == "low" and uncertainty == "none" and 
        not requires_coordination):
        return {
            "depth": "quick",
            "confidence": 0.85,
            "reasoning": "single_file_simple_fix",
            "recommendations": ["直接执行", "简单测试验证"]
        }
    
    # 复杂任务：多文件、有依赖、高风险或高不确定性
    if (files_involved > 3 or has_dependencies or 
        risk_level == "high" or uncertainty == "unknown" or
        requires_coordination):
        return {
            "depth": "deep",
            "confidence": 0.80,
            "reasoning": "multi_file_coordination" if requires_coordination else "complex_dependencies",
            "recommendations": ["详细分析", "多角色协调", "完整验证"]
        }
    
    # 标准任务
    return {
        "depth": "normal",
        "confidence": 0.70,
        "reasoning": "standard_task",
        "recommendations": ["适度协调", "标准验证"]
    }


def _generate_recommendations(depth: str, confidence: float, reasoning: str) -> list:
    """根据评估结果生成建议"""
    
    if depth == "quick":
        if confidence > 0.9:
            return ["直接执行", "简单测试"]
        else:
            return ["快速验证后执行", "检查边界情况"]
    
    elif depth == "deep":
        recs = ["详细需求分析"]
        if reasoning == "multi_file_coordination":
            recs.extend(["多 Agent 协调", "文件所有权检查"])
        elif reasoning == "complex_dependencies":
            recs.extend(["依赖分析", "集成测试"])
        elif reasoning == "high_risk_change":
            recs.extend(["风险评估", "回滚方案"])
        recs.append("完整验证")
        return recs
    
    else:  # normal
        return ["标准协调流程", "适度验证"]


def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="评估任务处理深度")
    parser.add_argument("task", help="任务描述")
    parser.add_argument("--files", type=int, default=1, help="涉及文件数")
    parser.add_argument("--dependencies", action="store_true", help="有依赖")
    parser.add_argument("--risk", choices=["low", "medium", "high"], default="low", help="风险等级")
    parser.add_argument("--uncertainty", choices=["none", "partial", "unknown"], default="none", help="不确定性")
    parser.add_argument("--coordination", action="store_true", help="需要协调")
    
    args = parser.parse_args()
    
    result = evaluate_task_depth(
        task_description=args.task,
        files_involved=args.files,
        has_dependencies=args.dependencies,
        risk_level=args.risk,
        uncertainty=args.uncertainty,
        requires_coordination=args.coordination
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
