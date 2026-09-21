# Semantic Validation

- Criterion Registry 内 criterion_id 全局唯一。
- Acceptance acceptance_results[].criterion_id 全局唯一。
- required criterion 恰好一个当前有效结果；optional 可缺失。
- Acceptance task/revision 必须与 Registry 和 Evidence Envelope 匹配。
- criterion_registry_ref = SHA-256(JCS(registry))。
- PASS/FAIL 至少一个可解析 Evidence ID。
- PASS reason_code/reason 必须 null。
- FAIL reason_code 非空。
- UNVERIFIED 可无 Evidence，但 reason_code 非空。
- Evidence artifacts 至少一个；路径解析后必须仍在 workspace 内；hash/size/media type 必须实测匹配；criterion 必须存在。
- duplicate evidence_id + 相同 JCS envelope 为重复；不同内容为 CONFLICTED。
- regression.required=false 时 scope/result/reason/reason_code=null 且 evidence_refs=[]。

- EVIDENCE_OBSERVED classification 为 MALFORMED 或 NOT_SUBMISSION 时 evidence_id 必须为 null；其他 classification 必须为非空 ID。
- artifact_set_revision 必须等于按 `DETERMINISTIC_DIGESTS.md` 从 artifacts 重算的值。
- repair.status=NOT_REQUIRED 时 current_round=0 且 finding_refs=[]；EXHAUSTED 时 current_round=max_rounds 且 finding_refs 非空；其他 repair 状态必须满足 current_round<=max_rounds。
- regression.required=true 时 scope=FULL、result 非 null；result=PASS/FAIL 时 evidence_refs 非空；result=FAIL/UNVERIFIED 时 reason_code 非空；result=PASS 时 reason_code/reason 为 null。
- Projection 仅以 required criteria 聚合 task acceptance，优先级为 CONFLICTED > INVALID > STALE > FAIL > UNVERIFIED > PENDING > PASS；optional criterion 保留显示但不改变 task acceptance。
- 历史 task、Evidence、Event 和 Projection 不修改。新结果仅能在相同 task_id、subject_revision、criterion_id 内通过 generation+1 supersede；不同 revision 独立投影。
