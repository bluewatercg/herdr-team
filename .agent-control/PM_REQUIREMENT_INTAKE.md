# PM Requirement Intake Queue

This queue is the intake layer before Requirement Mapping. It records unresolved or exploratory PM discussion without authorizing implementation. It is not a replacement for `MASTER_PLAN.md`, `TASK_BOARD.md`, `DECISIONS.md`, or OMP TODO. Full source chronology for captured entries lives under [`COMMUNICATION/`](COMMUNICATION/2026-09-21-pm-requirement-intake.md) and is referenced by `CHRONICLE_ID`; the queue remains the classification and routing authority.

## Processing Rules

- Exploration, PM interpretation, and agent suggestions are not implementation authorization.
- A confirmed intake MAY proceed to Requirement Mapping only after the user confirms the intended scope and destination.
- Only a valid Requirement Mapping may enter the existing `TASK_BOARD.md` flow.
- `SOURCE_EXCERPT_SHA256` protects the captured excerpt bytes; it is not a complete communication chronicle.
- Preserve unknowns as unknown. Do not infer user confirmation from silence, PM interpretation, or agent suggestion.
- `USER_VERBATIM`, `PM_INTERPRETATION`, `AGENT_SUGGESTION`, and `OPEN_QUESTION` remain distinct evidence types.

## Intake State

Allowed `INTAKE_STATE` values:

- `INTAKE_OPEN`: clarification or classification is still required.
- `USER_CONFIRMED_PENDING_MAPPING`: user confirmed intent; Requirement Mapping is not complete.
- `MAPPED_CURRENT_REQUIREMENT`: valid mapping exists and the item may be considered by the existing task gate.
- `MAPPED_RESEARCH_CANDIDATE`: mapped as research only; no implementation authorization follows.
- `MAPPED_FUTURE_SCOPE`: mapped to a future or parked scope.
- `CLOSED_NO_ACTION`: classified as requiring no action.

`USER_CONFIRMED` is a boolean and MUST remain `false` until the user explicitly confirms the intended scope. A PM proposal, agent recommendation, or historical requirement does not set it to `true`.

## Queue Entries

### PM-RI-001

```yaml
INTAKE_ID: PM-RI-001
SOURCE_TYPE: PM_CONVERSATION
SOURCE_REFERENCES:
  - herdr-team/.agent-control/MASTER_PLAN.md:738
  - herdr-team/.agent-control/MASTER_PLAN.md:789-793
SOURCE_ENTRY_RANGE: MASTER_PLAN.md:738; MASTER_PLAN.md:789-793
SOURCE_EXCERPT_SHA256: "aff48562763e4edc4af870a7c6c3fbd1e39a45e7f30c01698329dc08244cec45"
CAPTURED_BY: lfa-pm
CAPTURED_AT: "2026-09-21T01:59:42Z"
USER_CONFIRMED: false

INTAKE_TYPE: CLARIFY_USER_INTENT
INTAKE_STATE: INTAKE_OPEN

QUESTION_OR_ACTION: >
  确认两级图像质量检查当前只冻结合同，还是同时启动 observation mode。

EXIT_CONDITION: >
  用户明确选择唯一范围，并说明其最终去向：当前需求、研究候选、未来范围或无需动作。

PROPOSED_DESTINATION: REQUIREMENT_CANDIDATE

ROLE_MATRIX_REFERENCE:
  path: "herdr-team/ROLE_RESPONSIBILITY_MATRIX_V2.md"
  document_id: "ROLE-RESPONSIBILITY-MATRIX-V2"
  document_revision: "0.1"
  status: "DRAFT"
  implementation_allowed: false
  authority_effect: "NON_AUTHORIZING"
  permitted_use:
    - "RESPONSIBILITY_BOUNDARY_REFERENCE"
    - "GOVERNANCE_QA_REFERENCE"
    - "FUTURE_ROLE_DESIGN_REFERENCE"
  prohibited_use:
    - "REQUIREMENT_AUTHORIZATION"
    - "TASK_AUTHORIZATION"
    - "DISPATCH_AUTHORIZATION"
    - "ROLE_ACTIVATION_AUTHORIZATION"
    - "REVIEW_GATE_ACTIVATION"

RESPONSIBILITY_CHECK:
  intake_owner: "lfa-pm"
  independent_verifier_candidate: "lfa-review"
  reviewer_gate_required_for_current_intake: false
  implementation_owner: null
  dispatch_owner: null
  future_dispatch_gate_owner: "lfa-start"
  new_runtime_role_required_for_this_intake: false
  lfa_core_reference_status: "DESIGN_CANDIDATE_ONLY"
  requirement_mapping_complete: false
  task_creation_allowed: false
  dispatch_allowed: false

INTAKE_REVIEW_INTERPRETATION:
  matrix_assignment: "V"
  current_effect: "ADVISORY_QA_ONLY"
  mandatory_formal_reviewer_gate: false
  reviewer_task_required: false
  review_queue_entry_required: false
  independent_review_evidence_required_now: false

GOVERNANCE_QA:
  intake_state_check:
    expected: "INTAKE_OPEN"
  user_confirmation_check:
    expected: false
  execution_objects_absent:
    task_id: null
    omp_todo: null
    file_scope: null
    write_owner: null
    implementation_agent: null
    runtime_role_activation: null
    seventh_pane: null
  source_separation_required:
    - "USER_VERBATIM"
    - "PM_INTERPRETATION"
    - "AGENT_SUGGESTION"
    - "OPEN_QUESTION"
  source_integrity:
    algorithm: "sha256"
    source: "CHRONICLE_ORIGINAL_EXCERPT"
    expected_digest: "aff48562763e4edc4af870a7c6c3fbd1e39a45e7f30c01698329dc08244cec45"
    actual_digest: "aff48562763e4edc4af870a7c6c3fbd1e39a45e7f30c01698329dc08244cec45"
    status: "MATCHED"
  routing_rule:
    user_confirmation_destination: "REQUIREMENT_MAPPING"
    direct_task_board_promotion: false
  role_matrix_draft_rule:
    lfa_core_contract_approved: false
    lfa_core_activation_allowed: false
    role_boundaries_may_be_used_for_qa_only: true
  current_transition:
    classification_change_required: false
    requirement_mapping_allowed_now: false
    task_creation_allowed: false
    dispatch_allowed: false

ROLE_MATRIX_FREEZE:
  >-
  ROLE_RESPONSIBILITY_MATRIX_V2.md 在 DRAFT 且 implementation_allowed: false 时，只作为 PM-RI-001 的职责边界与治理 QA 参考。该引用不得改变 Intake 分类、不得满足用户确认、不得创建 Requirement、Task、Reviewer Gate、运行时角色或第七个 pane。用户确认后，事项必须先进入 Requirement Mapping；只有被确认和映射为当前正式需求的事项，才可能在 Development Readiness 与现有派发 Gate 满足后进入 TASK_BOARD。

DECISION_AID:
  decision_id: "DECISION-JEV-PM-INTAKE-PRECHECK"
  provider: "JEV_OR_AGENT_SIMULATION"
  status: "PROPOSED"
  implementation_allowed: false
  classification: "NON_AUTHORITATIVE_DECISION_AID"
  gate_authority: false
  requirement_authority: false
  task_authority: false
  dispatch_authority: false
  review_authority: false
  permitted_use:
    - "CLASSIFICATION_SUGGESTION"
    - "SOURCE_TYPE_OMISSION_CHECK"
    - "SCOPE_EXPANSION_WARNING"
    - "REQUIREMENT_MAPPING_PRECHECK"
    - "EVIDENCE_CONCLUSION_CONSISTENCY_HINT"
  prohibited_use:
    - "MUTATE_INTAKE_STATE"
    - "SET_USER_CONFIRMED"
    - "CREATE_REQUIREMENT"
    - "CREATE_TASK"
    - "CREATE_OMP_TODO"
    - "ASSIGN_OWNER"
    - "DISPATCH_AGENT"
    - "CHANGE_GATE"

  execution_mode:
    selected: "AGENT_SIMULATION"
    allowed:
      - "API_MODE"
      - "AGENT_SIMULATION"
    user_choice_required: true
  installation_scope:
    type: "EXPLICIT_SUBSET"
    intended_capabilities:
      - "INTAKE_TRIAGE"
      - "CONTEXT_PREPARATION"
      - "ROUTE_SUGGESTION"
      - "REVIEW_PRECHECK"
    full_nine_skills_now: false
    project_local_subset_candidate: true
  jev_output_rule:
    simulation_mode: "mode: agent_simulation; jev_called: false"
    simulation_probability: "FORBIDDEN"
    simulation_jev_confidence: "FORBIDDEN"
    host_confidence_label_allowed: true
    host_confidence_must_not_be_called_jev_probability: true

JEV_PRECHECK_INPUT:
  objective: >-
    判断 PM-RI-001 应保留为 Intake，还是已满足 Requirement Mapping 前置条件。
  current_state:
    intake_state: "INTAKE_OPEN"
    user_confirmed: false
    implementation_allowed: false
  authority_rules:
    - "INTAKE_ID_IS_NOT_REQUIREMENT_ID"
    - "DRAFT_ROLE_MATRIX_IS_NON_AUTHORIZING"
    - "REQUIREMENT_MAPPING_PRECEDES_TASK_BOARD"
    - "ONLY_CURRENT_FORMAL_REQUIREMENTS_MAY_REACH_DISPATCH"
    - "REVIEW_REMAINS_INDEPENDENT"
  source_evidence:
    user_verbatim_ref: "SOURCE_ITEMS[type=USER_VERBATIM]"
    pm_interpretation_ref: "SOURCE_ITEMS[type=PM_INTERPRETATION]"
    agent_suggestions_ref: null
    open_questions_ref: "SOURCE_ITEMS[type=OPEN_QUESTION]"
  candidate_labels:
    - "CLARIFY_USER_INTENT"
    - "CURRENT_REQUIREMENT_CANDIDATE"
    - "RESEARCH_CANDIDATE"
    - "FUTURE_SCOPE"
    - "NO_ACTION"
  prohibited_outcomes:
    - "TASK_CREATION"
    - "ROLE_ACTIVATION"
    - "DISPATCH"
    - "USER_CONFIRMATION_INFERENCE"

PM_RI_001_JEV_PILOT_ACCEPTANCE:
  status: "PASS"
  required:
    - "INTAKE_STATE_REMAINS_OPEN"
    - "USER_CONFIRMED_REMAINS_FALSE"
    - "NO_TASK_ID_CREATED"
    - "NO_OMP_TODO_CREATED"
    - "NO_FILE_SCOPE_CREATED"
    - "NO_WRITE_OWNER_CREATED"
    - "NO_AGENT_DISPATCHED"
    - "NO_SEVENTH_PANE_CREATED"
    - "USER_VERBATIM_IS_SEPARATE"
    - "PM_INTERPRETATION_IS_SEPARATE"
    - "AGENT_SUGGESTION_IS_SEPARATE"
    - "OPEN_QUESTION_IS_SEPARATE"
    - "SOURCE_DIGEST_IS_VERIFIED"
    - "DRAFT_ROLE_MATRIX_IS_NON_AUTHORIZING"
    - "DIRECT_TASK_BOARD_ROUTE_IS_REJECTED"
  failure:
    - "PROBABILITY_PRESENT_IN_AGENT_SIMULATION"
    - "INTAKE_STATE_MUTATED"
    - "USER_CONFIRMATION_INFERRED"
    - "REQUIREMENT_ID_FABRICATED"
    - "LFA_CORE_ACTIVATION_SUGGESTED_AS_AUTHORIZED"
    - "REVIEWER_USED_AS_EVIDENCE_GENERATOR"

JEV_PRECHECK_RESULT:
  mode: "agent_simulation"
  jev_called: false
  source_ref: "PM-RI-001"
  source_excerpt_sha256_status: "MATCHED"
  suggested_classification:
    value: "CLARIFY_USER_INTENT"
    authoritative: false
  confidence_label: "MEDIUM"
  confidence_basis:
    - "user confirmation absent"
    - "requirement mapping absent"
    - "source types separated in the intake record"
  missing_items:
    - "explicit user confirmation"
    - "authoritative requirement id"
    - "deliverable exit mapping"
  conflicts:
    - "role matrix remains DRAFT"
    - "lfa-core remains design candidate"
    - "implementation_allowed is false"
  prohibited_transition_detected:
    - "direct intake to task board"
  recommendation:
    keep_intake_state: "INTAKE_OPEN"
    keep_user_confirmed: false
    create_task: false
    dispatch: false
  pm_decision_required: true
  evidence_class: "AGENT_SUGGESTION"
  note: "This is a host-agent simulation; no Jev runtime or external API was called."

DECISION_AID_FREEZE: >-
  Jev 可以作为 lfa-pm 的只读分类和遗漏检查工具，但 Jev 或 Agent Simulation 的输出都不构成用户确认、Requirement、Task、Review Acceptance 或 Gate Evidence。任何分类建议必须由 PM 结合原始 Chronicle 审阅，用户确认后仍必须先进入 Requirement Mapping，不能直接进入 TASK_BOARD。
```



### PM-RI-001 Source Items

The following items preserve the minimum provenance needed before a full Chronicle exists:

```yaml
SOURCE_ITEMS:
  - type: PM_INTERPRETATION
    ref: herdr-team/.agent-control/MASTER_PLAN.md:738
    digest: null
    note: "Existing PM ledger records the two-level image-quality attachment as REQUIREMENT_CANDIDATE and outside implementation scope."

  - type: USER_VERBATIM
    ref: current-request:two-level-image-quality-question
    digest: "aff48562763e4edc4af870a7c6c3fbd1e39a45e7f30c01698329dc08244cec45"
    excerpt: "确认两级图像质量检查当前只冻结合同，还是同时启动 observation mode。"

  - type: OPEN_QUESTION
    ref: PM-RI-001
    digest: "aff48562763e4edc4af870a7c6c3fbd1e39a45e7f30c01698329dc08244cec45"
    note: "The user has not selected the scope or destination in the captured intake."
```

No `TASK_ID`, OMP TODO, `FILE_SCOPE`, `WRITE_OWNER`, or implementation-agent assignment is created by this entry.

## Chronicle Link

```yaml
CHRONICLE_ID: COMM-20260921-PM-RI-001
CHRONICLE_PATH: herdr-team/.agent-control/COMMUNICATION/2026-09-21-pm-requirement-intake.md
CHRONICLE_STATUS: CAPTURED_MINIMUM_EVIDENCE
```

The Chronicle preserves the captured sequence and source types. It does not change `INTAKE_STATE` or grant implementation authorization.
