# TEAM OWNERSHIP AND DASHBOARD EVIDENCE — 2026-09-18

## BTW-CHECK
TODO_ID: Define file ownership ledger
Goal: Add one lightweight concurrent-write authority without creating task-state duplication.
Files Changed: herdr-team/.agent-control/FILE_OWNERSHIP.md
Build Result: Ledger created with path, TASK_ID, SUBTASK_ID, WRITE_OWNER, READERS and status.
Requirement Trace: One ACTIVE writer per path; concrete files by default; release-before-transfer.
Test Result: Reviewed by parser-independent Markdown read.
Artifact Evidence: FILE_OWNERSHIP.md
Known Limitations: Existing tasks without auditable FILE_SCOPE were not backfilled.
Open Post-Funding Gates: none
Current MVP Blocker Remaining: none introduced

## BTW-CHECK
TODO_ID: Enforce PM ownership assignments
Goal: Make PM define FILE_SCOPE and unique WRITE_OWNER.
Files Changed: herdr-team/prompts/pm.md; herdr-team/.agent-control/TASKS/TASK_TEMPLATE.md
Build Result: PM and task-template contracts updated.
Requirement Trace: PM owns ledger updates and release-before-transfer.
Test Result: Static checksum verification passed.
Artifact Evidence: PM prompt and task template
Known Limitations: Prose gate, not an OS file lock.
Open Post-Funding Gates: none
Current MVP Blocker Remaining: none introduced

## BTW-CHECK
TODO_ID: Enforce dispatcher conflict checks
Goal: Stop overlapping writes before dispatch.
Files Changed: herdr-team/prompts/start.md
Build Result: Dispatch gate requires serial execution or resplitting on overlap.
Requirement Trace: lfa-start owns conflict scheduling.
Test Result: Static checksum verification passed; live lfa-start notified.
Artifact Evidence: start prompt; successful herdr prompt delivery
Known Limitations: Conflict comparison remains an agent decision.
Open Post-Funding Gates: none
Current MVP Blocker Remaining: none introduced

## BTW-CHECK
TODO_ID: Enforce pane write boundaries
Goal: Restrict writes to the designated pane.
Files Changed: herdr-team/prompts/COMMON.md; prompts/app-apk.md; prompts/api.md; prompts/app-ios.md
Build Result: Primary agents manage pane scope; secondary panes are read-only.
Requirement Trace: Scope expansion routes to PM/start.
Test Result: Static checksum verification passed.
Artifact Evidence: shared and role prompts
Known Limitations: Existing running implementation agents load the rule on their next assignment unless directly notified.
Open Post-Funding Gates: none
Current MVP Blocker Remaining: none introduced

## BTW-CHECK
TODO_ID: Enforce review scope checks
Goal: Make scope violations independently reviewable.
Files Changed: herdr-team/prompts/review-code.md
Build Result: Out-of-scope, non-owner and overlapping ACTIVE writes require CHANGES_REQUESTED.
Requirement Trace: Review checks actual diff against ownership records.
Test Result: Static checksum verification passed; live lfa-review notified.
Artifact Evidence: review prompt; successful herdr prompt delivery
Known Limitations: Review cannot attribute historical edits lacking ownership records.
Open Post-Funding Gates: none
Current MVP Blocker Remaining: none introduced

## BTW-CHECK
TODO_ID: Complete master task tree
Goal: Show milestone and deliverable progress from the authoritative master plan.
Files Changed: herdr-team/dashboard.py
Build Result: Dashboard renders 8 milestones and 36 deliverables with current-node highlighting.
Requirement Trace: MASTER_PLAN remains the only stage-status source.
Test Result: dashboard --check and live browser DOM checks passed.
Artifact Evidence: http://127.0.0.1:8765/; /api/status
Known Limitations: Counts use ACCEPTED only; evidence-ready work is intentionally not counted complete.
Open Post-Funding Gates: M6 and M7 remain visibly PARKED.
Current MVP Blocker Remaining: none introduced

## BTW-CHECK
TODO_ID: Show agent task node bindings
Goal: Show which Agent executes each deliverable task and its status.
Files Changed: herdr-team/dashboard.py
Build Result: Seven TASK_BOARD rows render beneath their exact DELIVERABLE_ID nodes.
Requirement Trace: TASK_BOARD remains task-status authority.
Test Result: Browser found 7 task chips under the expected M1 nodes.
Artifact Evidence: live dashboard tree
Known Limitations: Unassigned deliverables show no dispatched Agent task.
Open Post-Funding Gates: none
Current MVP Blocker Remaining: none introduced

## BTW-CHECK
TODO_ID: Run control and dashboard checks
Goal: Prove the changed control package remains executable.
Files Changed: herdr-team/SHA256SUMS.txt
Build Result: Python and shell syntax valid; dashboard payload generated.
Requirement Trace: Static distribution files remain hash-bound.
Test Result: py_compile passed; dashboard --check passed; bash -n passed; sha256sum -c passed for every entry.
Artifact Evidence: command results from 2026-09-18 session
Known Limitations: No automated file lock was added.
Open Post-Funding Gates: none
Current MVP Blocker Remaining: none introduced

## BTW-CHECK
TODO_ID: Verify desktop and mobile dashboard
Goal: Verify the actual read-only web surface.
Files Changed: none
Build Result: Dashboard service restarted and ready on 127.0.0.1:8765.
Requirement Trace: Read-only local binding retained.
Test Result: Desktop and 390x844 checks found no horizontal overflow; 8 milestones, 36 deliverables and 7 task chips visible; longest mobile task chip not clipped.
Artifact Evidence: live browser DOM and screenshot capture
Known Limitations: Full tree is vertically long by design.
Open Post-Funding Gates: none
Current MVP Blocker Remaining: none introduced

## BTW-CHECK
TODO_ID: Record BTW-CHECK evidence
Goal: Preserve build, trace and verification results.
Files Changed: this evidence file
Build Result: Ten task results recorded.
Requirement Trace: AGENTS.md Build → Trace → Verify reporting contract.
Test Result: Evidence uses observed command and browser results only.
Artifact Evidence: this file
Known Limitations: No product-science acceptance claimed.
Open Post-Funding Gates: unchanged
Current MVP Blocker Remaining: none introduced
