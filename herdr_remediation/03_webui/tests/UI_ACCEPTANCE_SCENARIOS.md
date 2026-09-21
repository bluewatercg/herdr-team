# UI Acceptance Scenarios

1. 全 PASS -> PASSED。
2. Criterion UNVERIFIED -> BLOCKED / ACCEPTANCE_UNVERIFIED。
3. FAIL 且 repair 已创建 -> REPAIRING。
4. Repair 第 2 轮失败 -> BLOCKED / REPAIR_EXHAUSTED；PM 终止后 FAILED。
5. 旧 revision PASS -> STALE / CURRENT_REVISION_CHANGED。
6. PASS 无证据 -> declared PASS / effective INVALID。
7. Repair PASS 但 Regression 未执行 -> BLOCKED。
8. Evidence hash mismatch -> effective INVALID。
9. Documentation-only activity -> 不刷新 meaningful activity。
10. 有 Build TODO 无 owner -> NO_ACTIVE_BUILD。
11. 重复 recap -> REPEATED_RECAP。
12. Delivery Profile 变更 -> Before/After 与受影响任务可见。
13. R5 类 PATCH -> UI 显示轻策略，不继承父 Contract Gate。
14. Legacy task -> UNAVAILABLE / LEGACY，不伪造失败。
