# Master Remediation Plan v1.1

## Slice 0 治理与基线
注册 Workstream；隔离脏工作树；复用 SHA256SUMS；冻结 scope；追加 Accepted Deliverable 影响；决策符合模板。

## Slice 0.5 Evidence 静态审计
只读分类全部 Evidence JSON。不得派发、写回或静默跳过。

## Slice 1 机器合同
冻结 Criterion Registry、Dispatchable Evidence Envelope、Event Envelope、Task Acceptance、Artifact-set Revision、Dashboard Projection。

## Slice 2 Semantic Validator
封堵 criterion、repair、regression、Evidence binding/hash/status 问题。

## Slice 3 Local Evidence Resolver
只支持本地文件、SHA-256、size、media type、task/revision/criterion binding。

## Slice 4a Evidence Normalizer
只规范真正 submission；其他 JSON 分为 NOT_SUBMISSION 等诊断类。

## Slice 4b Markdown Conservative Classifier
默认 UNAVAILABLE；只能 EXACT/PARTIAL/UNAVAILABLE/CONFLICTED；不得 PASS。

## Slice 5 Pure Reducer
Revision Isolation、Criterion Partition、Explicit Supersession、Concurrent Join、Conflict Dominance。

## Slice 6 单任务 Shadow
固定 `QR-ANDROID-01-D01`，人工核对，不推进旧 PHASES。

## Slice 7 stdlib Dashboard Shadow 区域
仅在 0-6 通过后允许；Dashboard 只读 Projection，不含 reducer/Gate 逻辑。

## 暂缓
Delivery Wizard、自动派发、自动 Repair、正式 Gate、全量 WebUI、Node 工具链。
