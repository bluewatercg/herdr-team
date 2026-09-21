# TASK_TEMPLATE.md 建议追加块

```yaml
DELIVERY_CONTEXT:
  profile_id:
  profile_revision:
  delivery_mode:
  change_class:
  risk_flags: []
  effective_policy_ref:

DEVELOPMENT_READINESS:
  behavior_clear:
  acceptance_observable:
  owner_assigned:
  file_scope_clear:
  required_contract_fields_frozen:
  unresolved_build_blockers: []
  result: READY | NOT_READY

TASK_ACCEPTANCE:
  schema_version: herdr-task-acceptance/1.0
  task_id:
  subject_revision:
    type: git | artifact-set
    value:
  acceptance_results: []
  repair:
    current_round: 0
    max_rounds: 2
    status: NOT_REQUIRED
    finding_refs: []
  regression:
    required: false
    scope: null
    result: UNVERIFIED
    evidence_refs: []
    reason_code: NOT_EXECUTED
    reason: null
```
