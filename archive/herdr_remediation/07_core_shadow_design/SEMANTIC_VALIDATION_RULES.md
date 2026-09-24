# Semantic Validation Rules

## Acceptance

- Criterion 必须存在于 Registry。
- required criterion 不得缺失。
- 同 revision + criterion + generation 不得重复，除非完全幂等。
- PASS/FAIL 至少一个 Evidence ID。
- UNVERIFIED 必须有 reason_code。

## Evidence

- Evidence ID 可解析。
- task/revision/criterion binding 匹配。
- hash、size、media type 通过。

## Repair

- `current_round <= max_rounds`。
- NOT_REQUIRED: round=0 且 finding_refs 为空。
- PENDING/IN_PROGRESS/READY_FOR_REVIEW/PASSED: round>=1。
- EXHAUSTED: round=max_rounds、max_rounds>0、finding_refs 非空。
- EXHAUSTED 不要求 regression.required=true。

## Regression

- required=false: scope/result/reason_code/reason 为 null，evidence_refs 为空。
- required=true: scope=FULL，result 必填。
- PASS: evidence 非空且 reason_code=null。
- FAIL: evidence 非空且 reason_code 必填。
- UNVERIFIED: reason_code 必填。
