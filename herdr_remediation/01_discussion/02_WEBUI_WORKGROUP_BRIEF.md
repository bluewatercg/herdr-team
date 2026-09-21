# WebUI / Projection 工作组任务书

## UI 主问题

Dashboard 必须回答：

1. 当前 Task 的 current revision 与 subject revision 是什么？
2. 每条 criterion 的 declared / effective 状态是什么？
3. 当前阻塞来自 Contract、Acceptance、Revision、Repair、Regression 还是 Gate？
4. Repair 是否收敛，剩余几轮？
5. 谁需要介入，下一动作是什么？
6. 当前 Delivery Mode、Change Class、Risk Flags 和 Effective Policy 是什么？
7. 是否出现 Documentation Drift 或 No Active Build？

## 页面层级

- Level 0: Delivery Profile Setup / Change
- Level 1: Run Overview
- Level 2: Task Detail
- Level 3: Evidence Detail
- Diagnostic: Activity / Evidence / Diff / Tests / Events / Terminal

## 必须遵守

- 不解析聊天或终端得到 PASS。
- 只消费 Dashboard Projection。
- 不允许直接 Mark as PASS、改 Evidence、改 Revision。
- 操作按钮只能触发受控工作流。
- 状态必须有文本，不只靠颜色。
- `last_meaningful_activity_at` 与 `last_any_activity_at` 分离。
