# TASK
TASK_ID:
PLAN_ID:
DELIVERABLE_ID:
REQUIREMENT_IDS: UNMAPPED
REQUIREMENT_SOURCE_REFERENCES:
OWNER:
FILE_SCOPE:
WRITE_OWNER:
DEPENDENCIES:
ALLOWED_FILES:
FORBIDDEN_FILES:
ACCEPTANCE_CRITERIA:
REQUIRED_TESTS:
REQUIRED_EVIDENCE:
STATUS: DRAFT

正式派发/验收前按 [需求追踪 Gate](../../prompts/COMMON.md#需求追踪-gate) 补齐权威映射；`UNMAPPED` 阻止派发和验收。仅填权威 ID 与来源引用，不填 finding IDs 或复制需求正文。

## 管理评估摘要

遵循 [管理问题记录规则](../../prompts/start.md#管理问题记录规则)。每个blocked/rejected/cancelled/completed终态必填，由PM评估、START记录并回执；无发现填NONE_OBSERVED及范围/证据，未收到评估填PENDING_PM_ASSESSMENT。这里只引用现有账本，不复制issue或维护第二份状态。

management_summary:
assessment_scope:
assessment_evidence:
pm_assessment_ref:
issue_refs:
start_receipt_ref:
