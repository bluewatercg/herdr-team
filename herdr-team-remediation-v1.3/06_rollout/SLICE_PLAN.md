# Slice Plan v1.3

```text
Slice 0
正式登记 Workstream、Owner、FILE_SCOPE、Decision

Slice 0.5
冻结 Legacy Submission 与 Status Vocabulary
验证 NOT_READY 与 UNKNOWN_STATUS

Slice 1
冻结五个 Schema、JCS、Artifact-set 与 Projection event digest

Gate
Decision APPROVED
implementation_allowed = true

Slice 2
Semantic Validator

Slice 3
Local path/hash/size/media resolver

Slice 4
Evidence 六分类 + Markdown 保守 Observation

Slice 5
Revision-scoped Pure Reducer

Slice 6
Criterion-level Projection + QR-ANDROID 人工核对

Slice 7
另行审批 dashboard.py
```

正式批准前 `implementation_allowed` 必须保持 false。`review_dispatch.py` 与旧 PHASES 始终不在当前范围。
