# Task Acceptance Spec

## 权威对象

```yaml
TASK_ACCEPTANCE:
  schema_version: herdr-task-acceptance/1.0
  task_id: TASK-001
  subject_revision:
    type: git
    value: abc123
  acceptance_results: []
  repair:
    current_round: 0
    max_rounds: 2
    status: NOT_REQUIRED
    finding_refs: []
  regression:
    required: false
    scope: null
    result: UNVERIFIED
    evidence_refs: []
    reason_code: NOT_EXECUTED
    reason: null
```

## Result 语义

- `PASS`: 已执行且证据足以证明满足；至少一个 evidence ref；reason_code 为 null。
- `FAIL`: 已执行且证据证明不满足；至少一个 evidence ref；reason_code 必填。
- `UNVERIFIED`: 无法形成 PASS/FAIL；reason_code 必填；不能聚合为 PASS。

缺字段、非法类型、未知字段属于 `CONTRACT_INVALID`。

## Repair

状态：`NOT_REQUIRED | PENDING | IN_PROGRESS | READY_FOR_REVIEW | PASSED | EXHAUSTED`

轮次只在 Reviewer 对正式 repair revision 复审失败且仍有剩余轮次时增加。基础设施失败、重放、命令重试不增加。

## Regression

v1 只允许 `FULL`。定向修复不等于定向回归。

## Revision

Acceptance、Regression、Reviewer Gate、PM Gate 必须引用同一 subject revision。新 revision 使旧结果变成 STALE。

## 聚合

`INVALID > STALE > FAIL > UNVERIFIED > PENDING > PASS`

## Gate

Gate PASS 要求 schema valid、所有必需 criterion PASS、证据可解析、需要时 regression PASS、repair 已闭环、revision 全部一致。
