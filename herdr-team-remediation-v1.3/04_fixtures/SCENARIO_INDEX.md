# C01-C18 Fixtures

所有场景均已实体化在 `scenarios.json`，由 `../05_validation/verify_fixtures.py` 执行。C01、C04 读取独立合同 fixture；C02 使用真实 QR legacy 状态；C14 同时由完整 Event fixtures 覆盖。

| ID | 场景 | 预期 |
|---|---|---|
| C01 | Valid Criterion Registry | VALID |
| C02 | QR-ANDROID known NOT_READY | NOT_READY |
| C03 | FUTURE_UNKNOWN_STATUS | UNKNOWN_STATUS |
| C04 | Valid UNVERIFIED Acceptance | VALID |
| C05 | PASS without Evidence | PASS_EVIDENCE_REQUIRED |
| C06 | Required criterion missing | REQUIRED_CRITERION_MISSING |
| C07 | Unknown criterion | UNKNOWN_CRITERION |
| C08 | Duplicate criterion result | DUPLICATE_CRITERION_RESULT |
| C09 | Artifact path escape | ARTIFACT_PATH_ESCAPE |
| C10 | Hash/size mismatch | ARTIFACT_INTEGRITY_MISMATCH |
| C11 | Criterion binding mismatch | CRITERION_BINDING_MISMATCH |
| C12 | Duplicate Evidence same canonical bytes | DUPLICATE |
| C13 | Duplicate Evidence conflict | EVIDENCE_ID_CONFLICT |
| C14 | Valid supersession | E2 |
| C15 | Missing/cross-revision supersession | INVALID_SUPERSESSION |
| C16 | Supersession fork | CONCURRENT_RESULT_CONFLICT |
| C17 | Revision isolation | 2 partitions |
| C18 | Idempotency conflict and permutation properties | IDEMPOTENCY_CONFLICT; C14-C16 permutation invariant |

此 fixture verifier 是合同审查工具，不是 Slice 2-6 runtime 实现，也不授权实现。
