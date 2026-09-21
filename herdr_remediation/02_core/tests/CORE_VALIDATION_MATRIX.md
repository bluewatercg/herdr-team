# Core Validation Matrix

| ID | 输入 | 预期 |
|---|---|---|
| C01 | PASS + evidence | VALID / PASS |
| C02 | PASS 无 evidence | INVALID |
| C03 | FAIL + evidence + reason | VALID / FAIL |
| C04 | UNVERIFIED + reason | VALID / UNVERIFIED |
| C05 | UNVERIFIED 无 reason | INVALID |
| C06 | 必需 criterion 缺失 | INVALID |
| C07 | 未知 criterion | INVALID |
| C08 | 重复 criterion | INVALID |
| C09 | Evidence revision 不匹配 | effective INVALID |
| C10 | current revision 改变 | STALE |
| C11 | repair retry 基础设施失败 | round 不增加 |
| C12 | reviewer fail 且有剩余 | round + 1 / PENDING |
| C13 | reviewer fail 到 max | EXHAUSTED |
| C14 | Watch 重放相同 key | 无状态变化 |
| C15 | Legacy task | UNAVAILABLE / LEGACY |
| C16 | MVP1 PATCH | immediate implementation policy |
| C17 | MVP1 CONTRACT_CHANGE | current-slice contract freeze |
| C18 | Documentation-only event | 不更新 meaningful timestamp |
