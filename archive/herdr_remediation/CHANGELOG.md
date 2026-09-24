# Changelog

## v1.1

- 收缩为 Core 只读 Shadow Slice。
- 新 Verification 与旧 PHASES 并存。
- Reducer 改为 revision 隔离、显式 supersession、并发 join。
- 只统一 Dispatchable Evidence Envelope，不统一所有 JSON。
- 增加 Evidence 六分类和 Slice 0.5 静态审计。
- `evidence_refs` 改为 Evidence ID。
- `regression.required=false` 派生 NOT_REQUIRED。
- 修正 Repair EXHAUSTED 语义。
- 复用 JCS 和 MANIFEST.sha256 约定。
- 路径改为 `harness/` 与 `.agent-control/MACHINE/`。
- WebUI 保持 stdlib 单文件；正式切换暂缓。
