# BTW Execution Policy

## 定义

- Build: 执行最高优先级、当前可执行的实现工作。
- Trace: 自动记录最小结构化事实，不生成叙事文档。
- Verify: 对当前 revision 运行针对性验证；Repair 后运行完整回归。

## WIP

- 每个 Worker 最多一个 active build TODO。
- 可有一个 verify TODO。
- Trace 是副作用，不是独立主任务。

## 文档触发器

只允许：

- CONTRACT_CHANGED
- GATE_REACHED
- BLOCKER_CREATED
- TASK_COMPLETED

禁止在 active build 时执行：

- STATUS_RECAP
- SNAPSHOT_REWRITE
- HISTORY_REWRITE
- DUPLICATE_EVIDENCE_SUMMARY

## Delta 输出

每次只返回：action、result、evidence_ref、blocker、next executable action。

## Kill Switch

如 Development Ready 且存在 executable build TODO，但连续产生文档事件且没有新的 contract、acceptance、finding 或 evidence 变化，发出 `DOC_LOOP_DETECTED`，停止文档主流程并恢复 Build。
