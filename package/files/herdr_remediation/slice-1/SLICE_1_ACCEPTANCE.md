# Slice 1 Revision 2 Acceptance Checklist

> Runtime modification allowed: `false`

## Authoritative Intake

- [ ] `PM-RI-001` exists only in `herdr-team/.agent-control/PM_REQUIREMENT_INTAKE.md`.
- [ ] No independent `PM_RI_001.yaml` copy exists in the package or repository.
- [ ] `INTAKE_STATE` is `INTAKE_OPEN`.
- [ ] `USER_CONFIRMED` is `false`.
- [ ] Requirement, Task, Dispatch, and Gate authority flags are `false`.

## Execution sentinels

The following fields may appear for non-regression checks, but each must remain null:

```yaml
TASK_ID: null
OMP_TODO: null
FILE_SCOPE: null
WRITE_OWNER: null
IMPLEMENTATION_OWNER: null
DISPATCH_OWNER: null
```

- [ ] No formal Requirement, Task, OMP TODO, implementation owner, or dispatch owner is created.
- [ ] `INTAKE_ID` is not used as `REQUIREMENT_ID` or `TASK_ID`.

## Source closure boundary

- [ ] Source types remain distinct: `USER_VERBATIM`, `PM_INTERPRETATION`, `AGENT_SUGGESTION`, `OPEN_QUESTION`.
- [ ] `PM_INTERPRETATION` references an existing `SOURCE_REFERENCE`.
- [ ] `SOURCE_CAPTURE_STATUS` is `INCOMPLETE` while valid source capture is unavailable.
- [ ] `SOURCE_EXCERPT_SHA256` is `null` while source capture is incomplete.
- [ ] `REQUIREMENT_MAPPING_ALLOWED` is `false`.
- [ ] Slice 1 does not implement Chronicle schema, immutable source storage, normalization, or hash recomputation.

## Promotion and dispatch

- [ ] Explicit confirmation routes first to Requirement Mapping.
- [ ] Requirement Mapping completes before formal Task definition.
- [ ] Research candidates, future scope, no-action items, Agent suggestions, and open questions are non-dispatchable.
- [ ] The Intake Dispatch Guard applies only to Intake-shaped objects or explicit Intake promotion requests.
- [ ] Existing formal Tasks are not rejected merely because they lack `USER_CONFIRMED`.
- [ ] Rejection returns to `lfa-pm` without rewriting Intake, Requirement, Acceptance, or scope.

## Reviewer and Role Matrix boundaries

- [ ] `lfa-review` is a future independent QA candidate, not a mandatory Gate for each Intake.
- [ ] `PM-RI-001` creates no Reviewer Task and does not enter `REVIEW_QUEUE` before clarification.
- [ ] Slice 1 defines no Communication Chronicle QA.
- [ ] Unavailable Role Matrix path is `null`, validation is `PENDING`, and authority effect is `NON_AUTHORIZING`.
- [ ] External decision-aid tools have no authority effect and are not coupled to state changes.

## Runtime non-regression

- [ ] `activate.sh` and `config.env` are unchanged.
- [ ] Six-role runtime chain is unchanged.
- [ ] No `lfa-core`, `lfa-qa`, `lfa-scribe`, `lfa-requirements`, or seventh pane is created.

## Package integrity

- [ ] `bash -n apply_slice1.sh` passes.
- [ ] Package manifest excludes itself and `sha256sum -c MANIFEST.sha256` passes.
- [ ] Dry-run performs no writes.
- [ ] `--apply` is required and repeated application is idempotent.
- [ ] No `.slice1.bak` or other undeclared package-external file remains.
- [ ] `git diff --check` passes and no secret/API key is introduced.
