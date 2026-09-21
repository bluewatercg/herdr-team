# Dashboard Architecture

## 数据边界

```text
Ledger Events -> Validator -> Reducer -> Dashboard Projection -> UI
```

UI 禁止读取终端文本来计算状态，禁止写回 Projection。

## 页面

### Delivery Profile

- Current Mode
- First Visible Goal
- Approved Constraints
- Blocking Risks
- Agent Calibration
- Deferred Scope
- Change History
- Reconfigure

### Run Overview

- Run Header
- Summary counts
- Needs Attention
- Pipeline
- Task Table

### Task Detail

- Task Header
- 六格状态条：Revision / Acceptance / Repair / Regression / Reviewer / PM
- Acceptance Panel
- Repair Panel
- Regression Panel
- Gate Chain
- Attention Panel
- Tabs: Activity / Evidence / Diff / Tests / Events / Terminal

### Evidence Detail

- identity
- type
- producer
- task / revision / criterion refs
- URI / hash
- validation status
- content

## 主排序

BLOCKING -> READY_FOR_REVIEW -> READY_FOR_PM_GATE -> REPAIRING -> ACTIVE -> WAITING -> PASSED

同级使用 attention 创建时间；活动时间使用 `last_meaningful_activity_at`。
