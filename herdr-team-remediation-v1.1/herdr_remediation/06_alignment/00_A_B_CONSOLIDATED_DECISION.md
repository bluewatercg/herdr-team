# A/B 评审合并决策

```yaml
overall_status: FEASIBLE_WITH_CHANGES
implementation_allowed: false
```

## 共识

- 新 Verification 与旧 PHASES 并存。
- Criterion Registry 独立版本化。
- WebUI 保持 stdlib。
- 不建立第二套 PARKED 权威。
- 使用 `harness/` 与 `.agent-control/MACHINE/`。
- 复用 `SHA256SUMS.txt`，先处理脏工作树。
- 不修改项目根 `AGENTS.md`。
- Markdown 不得独立产生 PASS。

## Reducer 裁决

不使用全历史 global max，也不使用 arrival-order fold。

```text
Revision Isolation
→ Criterion Partition
→ Explicit Supersession
→ Concurrent Join
→ Evidence Validation
→ Current Revision Aggregation
```

同 revision、criterion、generation 内：

```text
IDEMPOTENCY_CONFLICT
> INVALID
> STALE
> FAIL
> UNVERIFIED
> PENDING
> PASS
```

旧 revision 仅保留历史，不参与新 revision 聚合。

## Evidence 裁决

只统一 `herdr-dispatchable-evidence-envelope/1.0`，不强迫全部 JSON 共用 submission schema。

扫描结果固定为：

```text
DISPATCHABLE
NOT_READY
NOT_SUBMISSION
MALFORMED
UNKNOWN_STATUS
CONFLICTED
```

非 DISPATCHABLE 进入诊断，不静默、不产生 PASS。

## Shadow 验收

不比较新旧 Projection 等价性，只人工核对新 Projection 与原始 Evidence/Ledger。首个目标为 `QR-ANDROID-01-D01`。
