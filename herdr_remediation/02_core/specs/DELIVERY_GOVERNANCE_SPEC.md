# Delivery Governance Spec

## 1. 权威公式

```text
Effective Policy = Delivery Profile x Change Class x Risk Flags
```

## 2. Delivery Modes

- `MVP1_PROOF`: 最快证明真实、可运行、可验证的最小闭环。
- `MVP2_REPEATABLE`: 在有限边界内可重复。
- `PRODUCTIZATION`: 面向真实用户的产品能力。
- `REGULATED_RELEASE`: 正式质量、审计和监管控制。

## 3. Change Classes

- `PATCH`
- `FEATURE_LOCAL`
- `FEATURE_CROSS_COMPONENT`
- `CONTRACT_CHANGE`
- `ARCHITECTURE_CHANGE`

## 4. Risk Flags

- `SCIENTIFIC_RESULT`
- `DATA_INTEGRITY`
- `EVIDENCE_TRUST`
- `REVISION_IDENTITY`
- `SECURITY_PRIVACY`
- `IRREVERSIBLE_MIGRATION`
- `EXTERNAL_COMPATIBILITY`
- `REGULATORY_CLAIM`
- `NONE`

## 5. MVP1 默认策略

```yaml
requirement_review: MINIMUM_VISIBLE_SLICE
contract_review: CURRENT_SLICE_ONLY
implementation_priority: WORKING_PATH_FIRST
review_depth: MVP_BLOCKER_AND_HIGH
test_depth: DEMO_PATH_PLUS_CRITICAL_FAILURES
documentation_depth: TRACE_AND_LIMITATIONS
documentation_blocks_development: false
```

## 6. Development Readiness

只要以下全部满足，必须派发开发：

- behavior clear
- acceptance observable
- owner assigned
- file scope clear
- required current-slice contract fields frozen
- no real build blocker

Snapshot、措辞、状态复述、长期方案不得将 READY 改回 NOT_READY。

## 7. 配置向导

### `/delivery-setup`

1. 自动采集仓库事实。
2. 询问 delivery mode。
3. 询问 first visible goal。
4. 询问 approved constraints。
5. 询问 non-negotiable risks。
6. 生成 Agent calibration 推荐。
7. 展示摘要并等待确认。
8. 生成 profile revision。
9. 立即运行 Development Readiness。

### `/delivery-change`

只询问差异；必须展示 Before / After、受影响任务、增加/删除的 Gate。

### `/task-calibrate`

只改变当前任务的 Change Class、Risk Flags 和 Effective Policy，不改变全局 mode。

## 8. 问题预算

```yaml
quick_start_max_decisions: 6
custom_max_decisions_per_round: 5
ask_only_user_decisions: true
lookup_facts_automatically: true
allow_unknown: true
prototype_instead_of_speculation: true
```
