<!-- BEGIN HERDR SLICE 1 REVISION 2: INTAKE DISPATCH GUARD -->

## Intake Dispatch Guard

This guard applies only when the object is an Intake, contains `INTAKE_ID` without
a formal `TASK_ID`, or explicitly requests promotion from Intake to dispatch.
It must not add a `USER_CONFIRMED` requirement to an existing formal Task.

Reject and return the object to `lfa-pm` when the Intake path is missing explicit
confirmation, valid Requirement Mapping, or the current-scope Deliverable Exit.
Reject research candidates, future scope, no-action items, Agent suggestions, and
open questions. Reject an `INTAKE_ID` used as a Requirement or Task ID.

Formal Tasks continue to use the existing Requirement Mapping, three-part binding,
Deliverable, `FILE_SCOPE`, and unique `WRITE_OWNER` Gates. `lfa-start` only rejects
and returns the object; it does not rewrite Intake, Requirement, Acceptance, or scope.

<!-- END HERDR SLICE 1 REVISION 2: INTAKE DISPATCH GUARD -->
