# Dashboard Projection Spec

## 分层状态

- contract_status
- revision_status
- acceptance_status
- repair_status
- regression_status
- reviewer_gate_status
- pm_gate_status
- task_dashboard_status

## 顶层状态优先级

1. Contract invalid -> BLOCKED
2. Revision mismatch/stale -> BLOCKED
3. Repair exhausted -> BLOCKED，只有 PM 终止后 FAILED
4. Acceptance fail without repair -> BLOCKED
5. Repair pending/in progress -> REPAIRING
6. Repair ready -> READY_FOR_REVIEW
7. Regression fail/unverified -> BLOCKED
8. Reviewer ready/in review -> READY_FOR_REVIEW
9. Reviewer pass and PM waiting/ready -> READY_FOR_PM_GATE
10. PM pass -> PASSED
11. execution started -> ACTIVE
12. external wait -> WAITING
13. otherwise NOT_STARTED

## Declared / Effective

原记录不可变。Evidence 或 revision 校验失败时，显示 declared result 与 effective result，不覆盖历史。

## Attention 去重

`task_id + subject_revision + reason_code + criterion_id/finding_ref`
