# Validation Playbook v1.1

## Governance
Workstream、脏工作树隔离、影响声明、FILE_SCOPE、WRITE_OWNER、Decision 模板全部关闭。

## Evidence Audit
所有 JSON 显式分类；UNKNOWN_STATUS 与 NOT_READY 分离；NOT_SUBMISSION 不报错；无静默跳过。

## Contracts
JSON 语法有效；Semantic Validator 覆盖跨字段；Evidence refs 为 ID；required=false 派生 NOT_REQUIRED。

## Reducer
验证 commutative、associative、idempotent、supersession-preserving、revision-isolated、conflict-dominating。

## Shadow
读取 QR-ANDROID-01-D01；未知 status 可见；不 PASS；不改 PHASES；Projection 保存 source refs 与 reducer version。

## Dashboard
只读 Projection；不解析 Markdown/终端；不复制 Reducer；不写回状态。
