# Migration and Rollback

## Legacy

旧任务：

```yaml
contract_status: UNAVAILABLE
acceptance_status: PENDING
migration_status: LEGACY
```

不补造 PASS，不批量迁移 Acceptance。

## 双读期

- Ledger 继续保持现有权威记录。
- 新 reducer 只读。
- WebUI 增加 feature flag。
- Gate 在影子期仍使用旧路径。

## 切换条件

- Core Matrix 全过。
- UI Scenarios 全过。
- 重放一致性通过。
- 两套状态差异已解释。
- PM 明确批准切换 revision。

## 回滚

- 关闭新 Dashboard flag。
- Gate 切回旧路径。
- 保留新事件，不删除。
- 不反向覆盖旧账本。
- 记录 rollback reason 和 affected revisions。
