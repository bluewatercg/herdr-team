# Migration and Rollback v1.1

Core Shadow 不迁移、不覆盖旧任务。Legacy Phase 继续权威，Shadow Projection 可删除重算。

Slice 0-6 回滚：删除隔离生成的 `harness/` 与 `MACHINE/` 候选输出，不变更旧账本。

Slice 7 回滚：关闭 feature flag 并恢复新的 dashboard envelope revision；不修改历史 acceptance。
