# Herdr-team 整改实施包 v1.1

状态：**PROPOSAL / NOT_IMPLEMENTATION_BASELINE**

```yaml
implementation_allowed: false
```

v1.1 吸收两轮真实仓库对齐评审以及 A/B 评审结论。范围从“并行整体改造”收缩为：

```text
治理登记与基线隔离
→ Evidence 静态分类审计
→ 机器合同与 Reducer 语义冻结
→ 隔离的 Core 只读影子实现
→ 单任务 Shadow Projection 人工核对
→ 最后才考虑 stdlib Dashboard 只读显示
```

## 当前决策

```yaml
overall_decision: FEASIBLE_WITH_CHANGES

go_now:
  - Slice 0 治理登记与基线隔离
  - Slice 0.5 Evidence 静态分类审计
  - Core 机器合同详细设计

conditional_go:
  - 隔离的 Core Shadow 实现
  - 单任务 Versioned Projection 输出
  - stdlib Dashboard Shadow Verification 区域

no_go:
  - 修改现有 Gate 或 PHASES
  - Markdown 自动产生 PASS
  - 自动派发或自动 Repair
  - Delivery Wizard 实现
  - 全量 WebUI 重构或 Node 工具链
  - 正式 Gate 切换
```

## 核心架构

```text
Evidence JSON
→ Evidence Classifier
→ Dispatchable Envelope Validator
→ Evidence Registry
→ Immutable Event Envelope
→ Acceptance Semantic Validator
→ Artifact-set Revision Matcher
→ Record Selection
→ Per-dimension Concurrent Join
→ Versioned Projection
→ 单任务 Shadow JSON
```

Markdown 账本只能形成保守 observation，不得产生机器 PASS。

## 阅读顺序

1. `06_alignment/00_A_B_CONSOLIDATED_DECISION.md`
2. `06_alignment/01_REAL_REPO_ALIGNMENT.md`
3. `06_alignment/02_SCOPE_AND_GOVERNANCE.md`
4. `07_core_shadow_design/CORE_SHADOW_ARCHITECTURE.md`
5. `07_core_shadow_design/REDUCER_ALGEBRA.md`
6. `07_core_shadow_design/EVIDENCE_CLASSIFICATION.md`
7. `04_rollout/00_MASTER_REMEDIATION_PLAN.md`
8. `04_rollout/03_VALIDATION_PLAYBOOK.md`
