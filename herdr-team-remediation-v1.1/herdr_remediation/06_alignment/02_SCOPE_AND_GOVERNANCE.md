# Workstream 与影响声明

```yaml
WORKSTREAM: HARNESS-VERIFICATION-SHADOW
PURPOSE: 建立只读机器验证链，不替换现有 Gate，不自动派发。
MAINLINE_IMPACT:
  slice_0_to_6: NONE
  slice_7: BOUNDED
EXECUTION_STATUS: PLANNED
INTEGRATION_STATUS: NOT_REQUESTED

READ_SCOPE:
  - herdr-team/.agent-control/EVIDENCE/**
  - herdr-team/.agent-control/TASK_BOARD.md
  - herdr-team/.agent-control/REVIEW_QUEUE.md
  - herdr-team/review_dispatch.py
  - herdr-team/dashboard.py
  - herdr-team/SHA256SUMS.txt

DESIGN_WRITE_SCOPE:
  - herdr-team/herdr_remediation/07_core_shadow_design/**

FUTURE_IMPLEMENTATION_SCOPE:
  - herdr-team/harness/**
  - herdr-team/.agent-control/MACHINE/**

FORBIDDEN_WRITE_SCOPE:
  - existing accepted Evidence
  - TASK_BOARD.md
  - REVIEW_QUEUE.md
  - review_dispatch.py before integration approval
  - dashboard.py before Slice 7 approval
  - product application code
```

```yaml
ACCEPTED_DELIVERABLE_IMPACT:
  affected_deliverable: GOV-DOC-01-D01
  historical_acceptance_mutated: false
  slice_0_to_6:
    source_hash_impact: false
  slice_7:
    source_hash_impact: true
    affected_files: [dashboard.py]
  future_gate_integration:
    source_hash_impact: true
    affected_files: [review_dispatch.py]
  required_action:
    - create new envelope revision
    - record new source hashes
    - run bounded independent review
    - never rewrite historical acceptance
```
