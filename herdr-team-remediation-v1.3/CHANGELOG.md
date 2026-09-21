# Changelog

## v1.3

- 删除持久化 Evidence Registry 方向。
- Evidence Envelope 自包含 subject revision、artifacts、完整性和 criterion binding。
- 扫描时仅构建进程内 `dict[evidence_id, envelope]`。
- Event Type 收缩为 `EVIDENCE_OBSERVED` 与 `ACCEPTANCE_RECORDED`。
- Supersession 冻结为严格 generation +1 单链。
- `IDEMPOTENCY_CONFLICT` 只属于 ingestion 层。
- QR-ANDROID 固定分类为 NOT_READY，并新增 UNKNOWN_STATUS fixture。
- Projection 增加 criterion 级事件、Evidence 和诊断追踪。
- 正式设计路径与 ZIP review package 明确分离。
- 修复所有 Schema 的绝对 `$id`，Event `$ref` 可由 Draft 2020-12 validator 解析。
- 增加 artifact-set revision、nullable diagnostic evidence ID、Projection conflict 状态与 required-criterion 聚合规则。
- 替换 Event/Projection 占位摘要，加入真实可解析 artifact。
- C01-C18 已实体化并由 `05_validation/verify_fixtures.py` 执行。
- 真实 QR 历史 Evidence 保持只读；新增独立 Shadow Event 和 revision-scoped Projection fixture。
