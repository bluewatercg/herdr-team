<!-- BEGIN HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE -->

## Requirement Intake

Exploratory discussion is not implementation authorization.

When scope is unresolved, `lfa-pm` records the discussion in the single authoritative
`herdr-team/.agent-control/PM_REQUIREMENT_INTAKE.md` before defining an executable task.

Mandatory behavior:

1. Keep `USER_VERBATIM`, `PM_INTERPRETATION`, `AGENT_SUGGESTION`, and `OPEN_QUESTION` separate.
2. Keep `USER_CONFIRMED: false` until explicit user wording confirms intent and scope. While false, Requirement Mapping is not allowed.
3. Do not create `TASK_ID`, `OMP_TODO`, `FILE_SCOPE`, `WRITE_OWNER`, `IMPLEMENTATION_OWNER`, or `DISPATCH_OWNER` from an Intake; the register retains these fields as null sentinels only.
4. Do not use `INTAKE_ID` as `REQUIREMENT_ID` or `TASK_ID`.
5. After explicit confirmation, route first to Requirement Mapping. Requirement Mapping must complete before formal Task creation.
6. Only a mapped current formal Requirement may proceed to task definition; an Intake never goes directly to `TASK_BOARD.md`.
7. Research candidates, future scope, no-action items, Agent suggestions, and open questions are non-dispatchable.
8. A DRAFT reference with `implementation_allowed: false` is non-authorizing.
9. External decision-aid tools have no authority to change Intake, Requirement, Task, Review, or Gate state.

Slice 1 does not define Communication Chronicle schema, immutable source storage,
normalization, or hash recomputation. If source capture is incomplete, keep
`SOURCE_CAPTURE_STATUS: INCOMPLETE`, `SOURCE_EXCERPT_SHA256: null`, and
`REQUIREMENT_MAPPING_ALLOWED: false`.

<!-- END HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE -->
