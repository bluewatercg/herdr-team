<!-- BEGIN HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE OVERVIEW -->

## Requirement Intake

`herdr-team/.agent-control/PM_REQUIREMENT_INTAKE.md` is the single non-executable
register before Requirement Mapping.

```text
User / PM discussion
→ PM Requirement Intake
→ explicit user confirmation
→ Requirement Mapping
→ current Deliverable Exit
→ TASK_BOARD
→ lfa-start Dispatch Gate
→ OMP TODO
```

An Intake is not a Requirement, Task, Gate, Blocker, OMP TODO, or implementation
authorization. `INTAKE_ID` cannot replace `REQUIREMENT_ID` or `TASK_ID`. Execution
sentinel fields may be present for non-regression checks, but must remain null.

Slice 1 Revision 2 does not add a runtime role, seventh pane, Chronicle implementation,
mandatory Intake Reviewer Gate, automatic dispatch, or decision-aid authority.

<!-- END HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE OVERVIEW -->
