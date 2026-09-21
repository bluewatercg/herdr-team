# PM Requirement Intake

> Slice 1 Revision 2: non-executable intake register
>
> Requirement authority: `false`
> Task authority: `false`
> Dispatch authority: `false`
> Gate authority: `false`

## Purpose

This file is the single authoritative register for unresolved or exploratory intent before Requirement Mapping. An Intake is not a Requirement, Task, Gate, Blocker, OMP TODO, or implementation authorization.

## Contract

- `USER_VERBATIM`, `PM_INTERPRETATION`, `AGENT_SUGGESTION`, and `OPEN_QUESTION` remain separate source types.
- `USER_CONFIRMED: false` blocks Requirement Mapping and task creation.
- A confirmed Intake routes only to Requirement Mapping first; it never goes directly to `TASK_BOARD.md`.
- `INTAKE_ID` must not be used as `REQUIREMENT_ID` or `TASK_ID`.
- Research candidates, future scope, no-action items, Agent suggestions, and open questions are non-dispatchable.
- A DRAFT reference with `implementation_allowed: false` is non-authorizing.
- The execution fields below are retained as null-valued non-regression sentinels. Their presence does not authorize execution.
- Slice 1 does not implement Chronicle schema, immutable source storage, normalization, or hash recomputation.

## Allowed values

```text
INTAKE_STATE: INTAKE_OPEN | INTAKE_READY_FOR_CLASSIFICATION | INTAKE_RESOLVED
SOURCE_TYPE: USER_VERBATIM | PM_INTERPRETATION | AGENT_SUGGESTION | OPEN_QUESTION
PROPOSED_DESTINATION: NO_ACTION | RESEARCH_CANDIDATE | FUTURE_SCOPE | DECISION_CANDIDATE | REQUIREMENT_CANDIDATE | EXISTING_REQUIREMENT
```

## PM-RI-001

```yaml
INTAKE_ID: PM-RI-001
TITLE: Confirm the current scope of the two-level image-quality approach
INTAKE_STATE: INTAKE_OPEN
USER_CONFIRMED: false
SOURCE_REFERENCES:
  - herdr-team/.agent-control/COMMUNICATION/2026-09-21-pm-requirement-intake.md:20-32
  - herdr-team/.agent-control/COMMUNICATION/2026-09-21-pm-requirement-intake.md:34-45
  - herdr-team/.agent-control/COMMUNICATION/2026-09-21-pm-requirement-intake.md:47-58
SOURCE_CAPTURE_STATUS: INCOMPLETE
SOURCE_EXCERPT_SHA256: null
SOURCE_TYPES:
  USER_VERBATIM:
    - text: 确认两级图像质量检查当前只冻结合同，还是同时启动 observation mode。
      source_reference: herdr-team/.agent-control/COMMUNICATION/2026-09-21-pm-requirement-intake.md:20-32
  PM_INTERPRETATION:
    - text: The proposed approach separates App preview guidance from Core measurement eligibility.
      source_reference: herdr-team/.agent-control/COMMUNICATION/2026-09-21-pm-requirement-intake.md:34-45
  AGENT_SUGGESTION:
    - text: Introduce a dedicated lfa-core role only after separate role-contract review.
      source_reference: null
  OPEN_QUESTION:
    - text: Does the user want only the contract boundary frozen now, or also a Core observation-mode experiment?
      source_reference: herdr-team/.agent-control/COMMUNICATION/2026-09-21-pm-requirement-intake.md:47-58

QUESTION_OR_ACTION: Obtain explicit user confirmation of the intended scope and destination.
EXPECTED_INPUT: Explicit user wording selecting current requirement, research candidate, future scope, or no action.
EXIT_CONDITION: USER_CONFIRMED is true and one destination is confirmed; current requirements then enter Requirement Mapping.
PROPOSED_DESTINATION: REQUIREMENT_CANDIDATE
REQUIREMENT_MAPPING_ALLOWED: false

ROLE_MATRIX_REFERENCE:
  path: null
  document_id: ROLE-RESPONSIBILITY-MATRIX-V2
  status: DRAFT
  reference_validation: PENDING
  implementation_allowed: false
  authority_effect: NON_AUTHORIZING

RESPONSIBILITY_CHECK:
  intake_owner: lfa-pm
  independent_verifier_candidate: lfa-review
  reviewer_gate_required_for_current_intake: false
  implementation_owner: null
  dispatch_owner: null
  requirement_mapping_complete: false
  task_creation_allowed: false
  dispatch_allowed: false

EXECUTION_OBJECTS:
  TASK_ID: null
  OMP_TODO: null
  FILE_SCOPE: null
  WRITE_OWNER: null
  IMPLEMENTATION_OWNER: null
  DISPATCH_OWNER: null

RESOLUTION:
  type: null
  requirement_id: null
  requirement_source_reference: null
  master_plan_reference: null
  task_id: null
  reason: null
```

`SOURCE_CAPTURE_STATUS: INCOMPLETE` and the null digest remain until a valid original source excerpt is registered. Slice 1 does not create that capture mechanism.
