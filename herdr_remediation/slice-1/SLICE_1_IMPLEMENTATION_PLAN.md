# Slice 1 Revision 2 Implementation Plan

> Scope: Requirement Intake contract and prompt governance only
>
> This package permits documentation and prompt-contract changes only. It does not authorize product implementation, runtime role changes, or a new pane.

## Delivery outcome

Keep one authoritative PM Requirement Intake register, block unconfirmed discussion from becoming a formal task, and preserve the existing six-role runtime chain.

## Required changes

1. Keep `PM-RI-001` only in `herdr-team/.agent-control/PM_REQUIREMENT_INTAKE.md`.
2. Keep `INTAKE_OPEN`, `USER_CONFIRMED: false`, all authority flags false, and all execution sentinel fields null.
3. Keep source types separate. Link `PM_INTERPRETATION` to an existing `SOURCE_REFERENCE`; when source capture is incomplete, use `SOURCE_CAPTURE_STATUS: INCOMPLETE`, `SOURCE_EXCERPT_SHA256: null`, and `REQUIREMENT_MAPPING_ALLOWED: false`.
4. Route explicit confirmation to Requirement Mapping before any formal Task definition. Never promote an Intake directly to `TASK_BOARD.md`.
5. Limit the Orchestrator guard to Intake-shaped objects; do not require `USER_CONFIRMED` on existing formal Tasks.
6. Define only a Requirement Intake QA boundary. Do not define Communication Chronicle QA, Chronicle schema, immutable storage, normalization, or hash tooling.
7. Treat an unavailable Role Matrix path as `path: null`, `reference_validation: PENDING`, and `NON_AUTHORIZING`.
8. Describe external decision-aid tools as having no authority effect; do not name a vendor in the permanent Slice 1 contract.

## Explicitly unchanged

```text
herdr-team/activate.sh
herdr-team/config.env
herdr-team/lfa-team.sh
herdr-team/preflight.sh
herdr-team/review_dispatch.py
herdr-team/dashboard.py
herdr-team/.agent-control/MASTER_PLAN.md
herdr-team/.agent-control/TASK_BOARD.md
herdr-team/.agent-control/PM_GATE
herdr-team/.agent-control/FILE_OWNERSHIP.md
```

## Package integrity

- `MANIFEST.sha256` excludes itself and passes `sha256sum -c`.
- The apply script defaults to dry-run and requires `--apply`.
- Application is idempotent and replaces marked prior Slice 1 sections.
- Temporary backups, if needed, live under `mktemp`, never in the repository.
- The package contains no independent Intake YAML copy.

## Stop conditions

Stop and return to review if the change creates a task, OMP TODO, owner, runtime role, seventh pane, Reviewer Gate, Chronicle implementation, decision-aid authority, secret, or any modification to the protected runtime files.
