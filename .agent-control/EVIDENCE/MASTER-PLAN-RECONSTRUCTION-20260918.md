# Master plan reconstruction evidence

## BTW-CHECK 1

TODO_ID: Extract complete deliverables from authoritative sources
Goal: Reconstruct one complete deliverable map from the controlled-MVP roadmap, frozen public research-v2 contract, v3 TODO and historical evidence.
Files Changed: herdr-team/.agent-control/MASTER_PLAN.md
Build Result: M0-M7 and M0-D01 through M7-D04 recorded.
Requirement Trace: MASTER_PLAN Sources and Deliverables sections.
Test Result: `python3 herdr-team/dashboard.py --check` parsed all eight milestones without errors.
Artifact Evidence: MASTER_PLAN.md; this report.
Known Limitations: Historical evidence does not establish current revision acceptance.
Open Post-Funding Gates: M7.
Current MVP Blocker Remaining: Current revision live-loop evidence remains incomplete.

## BTW-CHECK 2

TODO_ID: Resolve v2 and v3 execution conflict
Goal: Keep frozen Android Bundle 1.5/public research v2 current and preserve v3 without accidental adoption.
Files Changed: herdr-team/.agent-control/MASTER_PLAN.md; herdr-team/.agent-control/DECISIONS.md
Build Result: M0-M5 use frozen v2; M6 is PARKED v3 migration; M7 is PARKED post-funding work.
Requirement Trace: MASTER_PLAN machine header, Milestones and Dispatch protocol; DECISIONS master-plan reconstruction entry.
Test Result: Dashboard check returned current milestone M1, current deliverable M1-D02 and parked M6/M7.
Artifact Evidence: dashboard `--check` payload; this report.
Known Limitations: A future explicit user-authorized decision may change the baseline.
Open Post-Funding Gates: M7.
Current MVP Blocker Remaining: M1 API/Core/Web baseline audit is active.

## BTW-CHECK 3

TODO_ID: Create M0 through M7 master plan
Goal: Establish one short authority for direction, dependencies, exits, evidence gaps and next actions.
Files Changed: herdr-team/.agent-control/MASTER_PLAN.md; herdr-team/README.md
Build Result: Plan version 1.0 is ACTIVE at M1/M1-D02 with next Gate and 1/6 Investor-MVP progress.
Requirement Trace: MASTER_PLAN Ownership, Milestones, Deliverables and Dispatch/update protocol.
Test Result: Parser returned M0 ACCEPTED, M1 IN_PROGRESS, M2-M5 NOT_STARTED and M6-M7 PARKED.
Artifact Evidence: MASTER_PLAN.md; dashboard parser output; this report.
Known Limitations: M4-D03 remains BLOCKED until real laboratory source facts exist.
Open Post-Funding Gates: M7; production generalization and governance work remain nonblocking.
Current MVP Blocker Remaining: M1 exit and bounded M2 repairs are not accepted.

## BTW-CHECK 4

TODO_ID: Add PLAN_ID to current task board
Goal: Bind every current assignment to exactly one milestone, deliverable and task ID.
Files Changed: herdr-team/.agent-control/TASK_BOARD.md
Build Result: All six current rows contain PLAN_ID, DELIVERABLE_ID and TASK_ID.
Requirement Trace: TASK_BOARD seven-column schema; MASTER_PLAN dispatch protocol.
Test Result: Dashboard check returned task_count 6 and invalid_tasks [].
Artifact Evidence: TASK_BOARD.md; dashboard `--check` payload; this report.
Known Limitations: Task status still depends on role-owned evidence and review.
Open Post-Funding Gates: M6 and M7 cannot receive current dispatch.
Current MVP Blocker Remaining: RUN-20260918T043217Z-API-AUDIT remains assigned/active.

## BTW-CHECK 5

TODO_ID: Add master-plan status to dashboard
Goal: Display current milestone, progress, next Gate, parked work and task bindings from authoritative files.
Files Changed: herdr-team/dashboard.py; herdr-team/SHA256SUMS.txt
Build Result: Existing local read-only dashboard restarted ready at http://127.0.0.1:8765.
Requirement Trace: Dashboard reads MASTER_PLAN.md directly; no second state store or write/control API added.
Test Result: `py_compile`, `dashboard.py --check`, shell syntax and all static hashes passed. Chromium checks at 1440x1000 and 390x844 found no horizontal overflow; four plan metrics had no clipping/overlap; six agent cards and six task rows were present; refresh/pause controls were 44x44.
Artifact Evidence: /tmp/lfa-master-plan-1440.png; /tmp/lfa-master-plan-mobile.png; this report.
Known Limitations: Dashboard reports ledger state; it does not approve or execute work.
Open Post-Funding Gates: M6 and M7 display as parked.
Current MVP Blocker Remaining: Current revision end-to-end evidence is incomplete.

## BTW-CHECK 6

TODO_ID: Enforce plan binding in PM prompts
Goal: Prevent dispatch or acceptance without a valid PLAN_ID/DELIVERABLE_ID/TASK_ID tuple.
Files Changed: herdr-team/prompts/COMMON.md; herdr-team/prompts/pm.md; herdr-team/prompts/start.md; herdr-team/README.md; herdr-team/SHA256SUMS.txt
Build Result: Common recovery, PM governance and start dispatch gates all require the tuple and reject parked, blocked, accepted or out-of-scope work.
Requirement Trace: COMMON Plan binding; PM Master plan governance; Start Master Plan Gate.
Test Result: `bash -n` passed for launchers and `sha256sum -c herdr-team/SHA256SUMS.txt` passed every static file.
Artifact Evidence: Prompt files; checksum output; this report.
Known Limitations: Prompt enforcement is procedural; authoritative ledgers remain the source of state.
Open Post-Funding Gates: M6/M7 require an accepted prior Gate or explicit user-authorized plan change.
Current MVP Blocker Remaining: Open HIGH findings and incomplete M1 evidence remain visible and unaccepted.
