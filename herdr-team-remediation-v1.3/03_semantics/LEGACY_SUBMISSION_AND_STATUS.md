# Legacy Submission and Status

## 识别

```text
record_kind == DISPATCHABLE_SUBMISSION → 新 Envelope
无 record_kind，但具有 task_id + deliverable_id + status + (implementation_files 或 artifacts) → Legacy Candidate
其他合法 JSON → NOT_SUBMISSION
```

## 版本化词表

```yaml
AUTHOR_COMPLETE: DISPATCHABLE
IMPLEMENTED_PENDING_REVIEW: DISPATCHABLE
REVIEW_PENDING: DISPATCHABLE
IMPLEMENTED_DEVICE_EVIDENCE_PENDING: NOT_READY
```

不得通过字符串包含 `PENDING` 推断。词表外为 UNKNOWN_STATUS。

QR-ANDROID-01-D01 固定为 NOT_READY。另设 FUTURE_UNKNOWN_STATUS fixture 验证 UNKNOWN_STATUS。两者均不派发、不 PASS、不改变旧 PHASES。
