#!/usr/bin/env python3
"""测试 Jev 任务深度评估模块"""

import sys
import json
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from jev_task_depth import evaluate_task_depth


def test_simple_task():
    """测试简单任务：删除备份文件"""
    result = evaluate_task_depth(
        task_description="删除备份文件",
        files_involved=1,
        has_dependencies=False,
        risk_level="low",
        uncertainty="none",
        requires_coordination=False
    )
    
    print("=== 简单任务测试 ===")
    print(f"任务: 删除备份文件")
    print(f"深度: {result['depth']}")
    print(f"置信度: {result['confidence']}")
    print(f"理由: {result['reasoning']}")
    print(f"建议: {result['recommendations']}")
    print()
    
    assert result['depth'] == 'quick', f"期望 quick，实际 {result['depth']}"
    assert result['confidence'] >= 0.8, f"置信度过低: {result['confidence']}"
    print("✓ 简单任务测试通过\n")


def test_complex_task():
    """测试复杂任务：修复并发 bug"""
    result = evaluate_task_depth(
        task_description="修复并发 bug 涉及多个文件",
        files_involved=5,
        has_dependencies=True,
        risk_level="high",
        uncertainty="unknown",
        requires_coordination=True
    )
    
    print("=== 复杂任务测试 ===")
    print(f"任务: 修复并发 bug 涉及多个文件")
    print(f"深度: {result['depth']}")
    print(f"置信度: {result['confidence']}")
    print(f"理由: {result['reasoning']}")
    print(f"建议: {result['recommendations']}")
    print()
    
    assert result['depth'] == 'deep', f"期望 deep，实际 {result['depth']}"
    assert result['confidence'] >= 0.7, f"置信度过低: {result['confidence']}"
    assert "多角色协调" in result['recommendations'] or "完整验证" in result['recommendations']
    print("✓ 复杂任务测试通过\n")


def test_medium_task():
    """测试中等任务：修改 API 接口"""
    result = evaluate_task_depth(
        task_description="修改 API 接口",
        files_involved=3,
        has_dependencies=True,
        risk_level="medium",
        uncertainty="partial",
        requires_coordination=False
    )
    
    print("=== 中等任务测试 ===")
    print(f"任务: 修改 API 接口")
    print(f"深度: {result['depth']}")
    print(f"置信度: {result['confidence']}")
    print(f"理由: {result['reasoning']}")
    print(f"建议: {result['recommendations']}")
    print()
    
    assert result['depth'] in ['normal', 'deep'], f"期望 normal 或 deep，实际 {result['depth']}"
    print("✓ 中等任务测试通过\n")


def test_config_task():
    """测试配置任务：修改配置文件"""
    result = evaluate_task_depth(
        task_description="修改配置文件",
        files_involved=1,
        has_dependencies=False,
        risk_level="low",
        uncertainty="none",
        requires_coordination=False
    )
    
    print("=== 配置任务测试 ===")
    print(f"任务: 修改配置文件")
    print(f"深度: {result['depth']}")
    print(f"置信度: {result['confidence']}")
    print(f"理由: {result['reasoning']}")
    print(f"建议: {result['recommendations']}")
    print()
    
    assert result['depth'] == 'quick', f"期望 quick，实际 {result['depth']}"
    print("✓ 配置任务测试通过\n")


def test_security_task():
    """测试安全任务：修复安全漏洞"""
    result = evaluate_task_depth(
        task_description="修复安全漏洞",
        files_involved=2,
        has_dependencies=False,
        risk_level="high",
        uncertainty="partial",
        requires_coordination=False
    )
    
    print("=== 安全任务测试 ===")
    print(f"任务: 修复安全漏洞")
    print(f"深度: {result['depth']}")
    print(f"置信度: {result['confidence']}")
    print(f"理由: {result['reasoning']}")
    print(f"建议: {result['recommendations']}")
    print()
    
    assert result['depth'] == 'deep', f"期望 deep，实际 {result['depth']}"
    assert "风险评估" in result['recommendations'] or "完整验证" in result['recommendations']
    print("✓ 安全任务测试通过\n")


def main():
    """运行所有测试"""
    print("=" * 60)
    print("Jev 任务深度评估模块测试")
    print("=" * 60)
    print()
    
    try:
        test_simple_task()
        test_complex_task()
        test_medium_task()
        test_config_task()
        test_security_task()
        
        print("=" * 60)
        print("✓ 所有测试通过！")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
