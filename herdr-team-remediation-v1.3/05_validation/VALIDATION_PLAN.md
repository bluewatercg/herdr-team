# Validation Plan

1. 5 个 Schema 通过 Draft 2020-12 metaschema。
2. 所有实体 fixtures 通过预期的 schema/semantic 结果。
3. C01-C18 全部实体化。
4. Reducer 性质：commutative、associative、idempotent、revision-isolated、supersession-preserving、conflict-dominating。
5. QR-ANDROID = NOT_READY；FUTURE_UNKNOWN_STATUS = UNKNOWN_STATUS。
6. 两者均不得进入评审队列、产生 PASS 或修改旧 PHASES。
7. Projection 可通过 selected_event_id、Evidence ID、source_ref 重建人工核对链。

执行：`python 05_validation/verify_fixtures.py`。真实 QR fixture 只读取 `herdr-team/.agent-control/EVIDENCE/QR-ANDROID-01-D01.json` 的现有字节与状态；不得修改该文件、旧 Event、旧 Projection、旧 PHASES 或 Gate。`EVIDENCE_OBSERVED` 和 Projection 是新 Shadow revision 的派生 fixture。
