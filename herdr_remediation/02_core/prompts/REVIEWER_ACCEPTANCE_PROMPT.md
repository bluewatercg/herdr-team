# Reviewer Acceptance Prompt

Reviewer 必须针对当前 subject revision 输出机器结构：

- 每个 criterion 的 PASS | FAIL | UNVERIFIED
- evidence_refs
- reason_code
- declared / effective 分离由 validator/reducer 完成
- blocking finding 必须绑定 criterion、revision、owner scope
- 不得从 Agent 自报 done 推断 PASS
- MVP1 下只阻断 Demo 主链、错误/误导结果、Evidence 不可信、身份/revision 错误、必现演示缺陷
- NEXT/LATER/RESEARCH 记录但不阻断 MVP1
- 文本回复只输出 delta
