# Supersession and Reducer

A supersedes B 当且仅当：

```text
A.supersedes_event_id == B.event_id
A.task_id == B.task_id
A.subject_revision == B.subject_revision
A.criterion_id == B.criterion_id
A.generation == B.generation + 1
```

规则：generation 1 必须 supersedes=null；generation>1 必须引用存在且有效目标；禁止自引用、环、跨 task/revision/criterion；一个事件最多一个有效后继；两个后继为 CONCURRENT_RESULT_CONFLICT。无效后继为 INVALID。被有效 supersede 的事件保留历史但不参与当前 join。

`IDEMPOTENCY_CONFLICT` 只属于 ingestion 层，不是 Acceptance 状态。

Reducer 流程：revision 分区 → criterion 分区 → 验证单链 → 选择唯一末端 → Evidence 校验 → 当前 revision 聚合。

任务级聚合仅使用 required criteria，按 `CONFLICTED > INVALID > STALE > FAIL > UNVERIFIED > PENDING > PASS` 选择最高优先级。optional criterion 仅显示，不改变任务级状态。历史 revision 永不重写；每个 revision 独立 reduce 和投影。
