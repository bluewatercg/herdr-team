# FILE_OWNERSHIP

同一路径同一时间只能有一个 `ACTIVE` 写 owner。`TASK_BOARD.md` 仍是任务状态权威；本账本只控制并发写入所有权。

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| herdr-team/.agent-control/FILE_OWNERSHIP.md | RUN-20260918T043217Z-PM-SCOPE | FILE-OWNERSHIP | lfa-pm(w12:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/TASK_BOARD.md | RUN-20260918T043217Z-START | CONTROL-LEDGERS | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/BLOCKERS.md | RUN-20260918T043217Z-START | CONTROL-LEDGERS | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/REVIEW_QUEUE.md | RUN-20260918T043217Z-START | CONTROL-LEDGERS | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/ROUNDS/20260918T043217Z-meeting.md | RUN-20260918T043217Z-START | TASK-DEFINITIONS | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/.agent-control/AGENT_STATUS/lfa-start.json | RUN-20260918T043217Z-START | ROLE-STATUS | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/RUN-20260918T043217Z-PM-SCOPE.md | RUN-20260918T043217Z-PM-SCOPE | REPORT | lfa-pm(w12:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/RUN-20260918T043217Z-PM-SCOPE.json | RUN-20260918T043217Z-PM-SCOPE | REPORT-CHECKS | lfa-pm(w12:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/MASTER_PLAN.md | RUN-20260918T043217Z-PM-SCOPE | PLAN-CONTROL | lfa-pm(w12:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/RUN-20260918T043217Z-REVIEW-BASELINE.md | RUN-20260918T043217Z-REVIEW-BASELINE | REPORT | lfa-review(w11:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/RUN-20260918T043217Z-REVIEW-BASELINE-checks.json | RUN-20260918T043217Z-REVIEW-BASELINE | REPORT-CHECKS | lfa-review(w11:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/RUN-20260918T043217Z-REPAIR-BOUNDARY.md | RUN-20260918T043217Z-REPAIR-BOUNDARY | REPORT | lfa-api(w13:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/RUN-20260918T043217Z-REPAIR-BOUNDARY-manifest.json | RUN-20260918T043217Z-REPAIR-BOUNDARY | PRESERVATION-MANIFEST | lfa-api(w13:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/RUN-20260918T043217Z-REPAIR-BOUNDARY-old-tracked.patch | RUN-20260918T043217Z-REPAIR-BOUNDARY | PRESERVATION-PATCH | lfa-api(w13:p1) | all roles | ACTIVE |
| herdr-team/dashboard.py | RUN-20260918T043217Z-DASHBOARD-REQUIREMENT-TRACE | DASHBOARD-TRACE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/SHA256SUMS.txt | RUN-20260918T043217Z-DASHBOARD-REQUIREMENT-TRACE | DASHBOARD-STATIC-HASH | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/.agent-control/TASKS/TASK_TEMPLATE.md | RUN-20260918T043217Z-DASHBOARD-REQUIREMENT-TRACE | PERSISTENT-TRACE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/prompts/COMMON.md | RUN-20260918T043217Z-DASHBOARD-REQUIREMENT-TRACE | PERSISTENT-TRACE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/prompts/pm.md | RUN-20260918T043217Z-DASHBOARD-REQUIREMENT-TRACE | PERSISTENT-TRACE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/prompts/start.md | RUN-20260918T043217Z-DASHBOARD-REQUIREMENT-TRACE | PERSISTENT-TRACE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/prompts/review-code.md | RUN-20260918T043217Z-DASHBOARD-REQUIREMENT-TRACE | PERSISTENT-TRACE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/README.md | RUN-20260918T043217Z-DASHBOARD-REQUIREMENT-TRACE | PERSISTENT-TRACE | lfa-start(w15:p1) | all roles | RELEASED |
| AGENTS.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/requirements/AGENTS.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/requirements/INDEX.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | RELEASED |
| docs/specs/AGENTS.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/specs/INDEX.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/technical/AGENTS.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/technical/INDEX.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/DOCUMENT_LIFECYCLE.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/review_dispatch.py | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/dashboard.py | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | RELEASED |
<!-- Old dashboard governance write is complete; this release grants no HARNESS-SHADOW-01 Slice 7 authority to lfa-start. -->
| herdr-team/SHA256SUMS.txt | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/README.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/prompts/COMMON.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/prompts/start.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/prompts/pm.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/prompts/review-code.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/TASKS/TASK_TEMPLATE.md | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/requirements/INDEX.md | RUN-20260918T043217Z-QR-PLAN-REVISION | REQUIREMENT-TRACE | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/README.md | RUN-20260918T043217Z-QR-PLAN-REVISION | QR-PLAN-PROPOSAL | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/01_QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.6.md | RUN-20260918T043217Z-QR-PLAN-REVISION | QR-PLAN-PROPOSAL | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/02_MASTER_PLAN_v1.1.md | RUN-20260918T043217Z-QR-PLAN-REVISION | QR-PLAN-PROPOSAL | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/03_DECISIONS_QR_MVP_VERTICAL_SLICE_v1.0.md | RUN-20260918T043217Z-QR-PLAN-REVISION | QR-PLAN-PROPOSAL | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/04_TASK_BOARD_QR_TEMPLATE_ROI_SIGNAL_v1.0.md | RUN-20260918T043217Z-QR-PLAN-REVISION | QR-PLAN-PROPOSAL | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/05_AUTHORITATIVE_CONTRACT_SYNC_CHECKLIST_v1.0.md | RUN-20260918T043217Z-QR-PLAN-REVISION | REQUIREMENTS-SYNC | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/06_TEMPLATE_ESTABLISHMENT_AND_VALIDATION_PLAN_v1.0.md | RUN-20260918T043217Z-QR-PLAN-REVISION | QR-PLAN-PROPOSAL | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/07_HERDR_RECENT_THREE_FAILURES_INVESTIGATION_v1.0.md | RUN-20260918T043217Z-QR-PLAN-REVISION | QR-PLAN-PROPOSAL | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/08_TEN_POINT_CAPTURE_RELEASE_AND_EXECUTION_PLAN_v1.0.md | RUN-20260918T043217Z-QR-PLAN-REVISION | QR-PLAN-PROPOSAL | lfa-start(w15:p1) | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/MANIFEST.sha256 | RUN-20260918T043217Z-QR-PLAN-REVISION | PACKAGE-INTEGRITY | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/ROUNDS/20260918T043217Z-meeting.md | RUN-20260918T043217Z-QR-PLAN-REVISION | AUTHORIZATION-TRACE-AND-EVIDENCE | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/RUN-20260918T075255Z-QRP-G0-AUTH.md | RUN-20260918T075255Z-QRP-G0-AUTH | G0-REPORT | lfa-review(w11:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/RUN-20260918T075255Z-QRP-G0-AUTH-checks.json | RUN-20260918T075255Z-QRP-G0-AUTH | G0-REPORT-CHECKS | lfa-review(w11:p1) | all roles | ACTIVE |
| herdr-team/review_dispatch.py | RUN-20260918-AUTO-DISPATCH-FIX | AUTO-DISPATCH | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/activate.sh | RUN-20260918-AUTO-DISPATCH-FIX | WATCH-LIFECYCLE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/lfa-team.sh | RUN-20260918-AUTO-DISPATCH-FIX | WATCH-LIFECYCLE | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/prompts/pm.md | RUN-20260918-AUTO-DISPATCH-FIX | CONTINUATION-POLICY | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/prompts/start.md | RUN-20260918-AUTO-DISPATCH-FIX | CONTINUATION-POLICY | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/README.md | RUN-20260918-AUTO-DISPATCH-FIX | CONTROL-DOC | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/SHA256SUMS.txt | RUN-20260918-AUTO-DISPATCH-FIX | STATIC-HASH | lfa-start(w15:p1) | all roles | RELEASED |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1-report.md | RUN-20260918-QR-G1-AUTH | G1-REPORT | lfa-api(w13:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1-dataset.json | RUN-20260918-QR-G1-AUTH | G1-DATASET | lfa-api(w13:p1) | authorized research custodians; reviewers without holdout disclosure to tool author | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1-geometry.json | RUN-20260918-QR-G1-AUTH | G1-GEOMETRY | lfa-api(w13:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1-checks.json | RUN-20260918-QR-G1-AUTH | G1-CHECKS | lfa-api(w13:p1) | all roles | ACTIVE |

状态仅使用 `PLANNED`、`ACTIVE`、`RELEASED`。默认登记具体文件；目录级 owner 仅用于明确独占模块。换 owner 时，PM 必须先把原记录改为 `RELEASED`，再登记新的 `ACTIVE` owner。禁止两个 pane 同时编辑后靠人工合并。

本表 path 均相对仓库根目录；同一 TASK_ID 的 ACTIVE path 集合即其明确 FILE_SCOPE。每行 WRITE_OWNER 为唯一写入角色及 pane。PM 按用户本次授权初始化本表；未登记路径无写入许可。API M1-D05 须回报完整具体 FILE_SCOPE 后另行登记，不以目录或通配符授权。所有登记仅覆盖当前 M1 控制、报告与保全任务，不授权业务修改、M2 实施或提前阶段验收。

API 已声明上述三个 M1-D05 路径为完整 FILE_SCOPE，新增文件 NONE；现有产物保留。登记只解除这三个路径在当前保全/精确规格准备任务中的写入暂停，不扩大任务。业务/source/docs/test 文件均不在授权范围；现有保全原件不得因登记而覆盖成新基线。

## Dashboard requirement trace control change

TASK_ID: RUN-20260918T043217Z-DASHBOARD-REQUIREMENT-TRACE. User-authorized control-plane change only; no M2/business authorization. Its direct FILE_SCOPE is exactly the eight ACTIVE paths registered above for this task; WRITE_OWNER lfa-start(w15:p1). SHA256SUMS.txt remains registered and may refresh entries only for dashboard.py and the six newly registered static files, adding their entries if absent; unrelated entries remain unchanged. Shared control records remain in their existing registered tasks, not duplicated as ACTIVE rows: MASTER_PLAN.md is written only by lfa-pm under PM-SCOPE; TASK_BOARD.md and ROUNDS/20260918T043217Z-meeting.md only by lfa-start under START. Task specification and Requirement Trace evidence use that existing meeting record; PM evidence stays in existing PM-SCOPE.md/.json. TASK_TEMPLATE.md is authorized for persistent template rules, not creation of additional task-spec or evidence files.

Required chain: authoritative requirement/acceptance ID -> MASTER_PLAN deliverable Exit -> TASK_BOARD REQUIREMENT_IDS -> task specification/evidence Requirement Trace -> Dashboard. Store references and IDs, not copied requirement prose. Do not invent authoritative IDs or claim unverified mappings. Acceptance requires every displayed task to resolve through that chain, with missing/invalid links explicitly shown rather than hidden. Start owns Dashboard implementation and executable verification; PM owns plan references. Any additional file requires explicit registration before writing. Existing D05 review ownership and preserved artifact history remain unchanged.

This scope extension does not authorize MASTER_PLAN or M1/M2 state changes. Mapping evidence uses PM-SCOPE:20–41 and existing reports; unknown mappings remain UNMAPPED. Every future formal task requires REQUIREMENT_IDS and an authoritative source reference. UNMAPPED blocks dispatch and acceptance until mapped. Finding IDs must not be promoted to requirement IDs. Apply minimal template/prompt/README edits; keep the authoritative requirement text at its source. Start must report the authorized static-file digest checks and verify unrelated checksum entries remained unchanged after completion.

## Independent documentation governance registration

TASK_ID RUN-20260918T043217Z-DOC-GOVERNANCE; PLAN_ID GOV-DOC-01; DELIVERABLE_ID GOV-DOC-01-D01. WRITE_OWNER lfa-start(w15:p1), the existing stable execution role. Status REGISTERED_FOR_EXECUTION. Start confirmed all eight prior trace-task paths stopped with no pending writes; PM marked their rows RELEASED before registering the seventeen exact ACTIVE paths for this task. The current main session must not directly write these execution-owned files; lfa-start executes. Earlier trace-task paragraphs are historical permissions only.

User supplied original numbered authorization and exact scope; MASTER_PLAN section Governance authorization and trace source binds GOV-REQ-01 through GOV-REQ-08 to the eight explicit current items. These IDs originate from user requirements, not findings. All seventeen ACTIVE paths above are the complete implementation FILE_SCOPE, including creation of named missing files; no directory/wildcard authorization. Index/lifecycle/routing/Review/Dashboard/validation must use those paths. SHA256SUMS may update/add entries only for authorized static files; unrelated entries stay unchanged. No deletion of source evidence or business-document rewrite is authorized by an index entry.

PM retains existing MASTER_PLAN/FILE_OWNERSHIP/PM evidence ownership. Dynamic TASK_BOARD/REVIEW_QUEUE and existing meeting remain under lfa-start's original START ownership, not transferred to current-main or duplicated as ACTIVE rows. Start records eight-item trace and validation there. Memmy synchronization is workspace-scoped verified project facts only, health/search/dedup/write/readback required, no repository memory files, credentials/transcripts or unsupported completion claims; service failure stays explicit, no alternate store. Governance completion requires explicit PM and independent Review acceptance; no self-approval.

Gate: explicit PM plus independent governance acceptance before QR plan review; separate QR plan review and explicit implementation authorization before vertical slice. No QR implementation dispatch now. CURRENT_MILESTONE M1 and CURRENT_DELIVERABLE M1-D05, business progress, R1/RBL04/HIGH/D04/M2/no Exit remain unchanged.

## Independent QR plan revision registration

PLAN_ID: QR-PLAN-01; DELIVERABLE_ID: QR-PLAN-01-D01; TASK_ID: RUN-20260918T043217Z-QR-PLAN-REVISION; TASK_TYPE: QR_PLAN_REVISION. Execution owner is lfa-start(w15:p1). The twelve exact ACTIVE rows for this task are its complete FILE_SCOPE; no wildcard, directory, new-file or source-code permission is granted. This registration follows the user's current plan-revision authorization and MASTER_PLAN.md sections `QR revision authorization source` and `Independent QR plan revision control phase`. QR-PLAN-REQ-01 through QR-PLAN-REQ-06 are the six user-derived plan requirements; QR-PM-B01 through B06 remain review findings, not Requirement IDs.

The INDEX and meeting rows previously assigned to GOV-DOC-01/START are RELEASED above before registration under the new task. WRITE_OWNER remains the same lfa-start pane; there is no concurrent ACTIVE claim. This specific transfer supersedes the historical shared-meeting/governance INDEX permissions in the paragraphs above. Preserve historical authorization, acceptance, findings and source evidence. Meeting edits are limited to this revision's user authorization, task specification, requirement/source trace, checks and review resubmission evidence; they do not rewrite earlier dispositions. Index edits map this plan-revision scope only and retain D05 UNMAPPED and implementation parking.

PM retains MASTER_PLAN.md and FILE_OWNERSHIP.md under its existing PM-SCOPE ownership. TASK_BOARD.md and REVIEW_QUEUE.md retain their existing lfa-start START ownership; this registration does not write them or grant a review decision. Start records the new task in TASK_BOARD before executing the registered documentation revision. The current PM session must not write any of the twelve execution-owned files. No other governance ownership is expanded or released by this registration.

Only proposal revision and its documentary evidence are authorized. Recompute package MANIFEST, perform the requirements sync check and submit the exact revision to independent Review before PM Gate, as required by QR-PLAN-01-D01 Exit. No result is reviewed or accepted here. M1/M1-D05, progress 1/6, D05 UNMAPPED, M2 NOT_STARTED and M6/M7 PARKED remain unchanged. QR implementation is NOT_AUTHORIZED; editing a proposed MASTER_PLAN or TASK_BOARD inside the package cannot change live milestones or dispatch business work.

## Independent QRP-G0 ownership reservation

PLAN_ID: QR-GEOMETRY-01; DELIVERABLE_ID: QR-GEOMETRY-01-G0; TASK_ID: RUN-20260918T075255Z-QRP-G0-AUTH; TASK_TYPE: READ_ONLY_PROTOCOL_BOUNDARY_REVIEW; REQUIREMENT_IDS: QR-G0-REQ-01, QR-G0-REQ-02, QR-G0-REQ-03, QR-G0-REQ-04, QR-G0-REQ-05, QR-G0-REQ-06. These independent G0 requirements and bounded Exit are defined in MASTER_PLAN.md section `G0 authorization source and trace`, bound to accepted QR-PLAN-01-D01 MANIFEST digest `90c5b32869f6a9f04d914ec3acb2c535b638da0fc84d88eedfc64c467ecbe2d2`. QR-PLAN-REQ-03/04 remain plan-only historical context, not G0 execution requirements. WORKSTREAM: QR_GEOMETRY_RESEARCH; DISPATCH_TRACK: PARALLEL_WORKSTREAM; MAINLINE_IMPACT: NONE; EXECUTION_STATUS: NOT_AUTHORIZED_PENDING_GATE; INTEGRATION_STATUS: NOT_AUTHORIZED. The formal dispatch and Integration Gate rules in MASTER_PLAN apply; this correction grants no execution or merge permission.

The two exact PLANNED rows above are the entire reserved future output FILE_SCOPE; both files were absent and neither path had an existing ownership claim at registration. Retain the user's proposed lfa-review(w11:p1) owner: no path-ownership conflict requires substitution. Existing REVIEW-BASELINE ownership is unchanged; this reservation makes no claim about live pane availability and sends no execution instruction. No ACTIVE output path exists for this task, and neither output may be created now.

Registration only: STATUS remains NOT_STARTED, EXECUTION_STATUS remains NOT_AUTHORIZED_PENDING_GATE, and INTEGRATION_STATUS remains NOT_AUTHORIZED. Separate explicit bounded read-only authorization, lfa-start requirement/task reference synchronization and PM ownership activation are required before writing the report/checks JSON. Both exact output rows remain PLANNED. Source/contracts/runtime are read-only even after that authorization. No App/API/OpenAPI/schema/fixtures/Gateway/Core/Web/package path, QR/homography tool, capture/experiment/investigation, Bundle1.6/v3 migration or authoritative ROI permission is included. Independent Review of G0 outputs must use a reviewer distinct from the report author, followed by PM Gate; neither registration nor later G0 acceptance dispatches G1 or authorizes integration. G0-G5 scheduling beside M1-M5 does not activate any ownership here; G3 tooling and R/C/A gates require separate authorization as defined in MASTER_PLAN.

PM writes only MASTER_PLAN.md and FILE_OWNERSHIP.md under existing PM-SCOPE ACTIVE ownership in this action. TASK_BOARD remains lfa-start START-owned. The existing meeting remains lfa-start-owned; its current ACTIVE QR-PLAN-REVISION row also permits recording this downstream G0 registration/source trace and task specification, without transferring ownership, duplicating an ACTIVE claim or altering historical dispositions. lfa-start performs those ledger writes separately; this registration does not perform or dispatch them. All other ownership rows are unchanged. QR_IMPLEMENTATION_NOT_AUTHORIZED; M1/M1-D05, D05 UNMAPPED, progress 1/6, M2 NOT_STARTED and M6/M7 PARKED remain unchanged.

## Automatic dispatch repair ownership

RUN-20260918-AUTO-DISPATCH-FIX / AUTO-DISPATCH-01-D01 is AUTHORIZED for lfa-start(w15:p1), requirement AUTO-DISPATCH-REQ-01 from the current user instruction persisted in MASTER_PLAN.md section `Automatic dispatch control repair`. The seven exact ACTIVE rows are the complete implementation scope. Five former DOC-GOVERNANCE claims are RELEASED as part of this transfer; the same writer remains, with no duplicate ACTIVE claim. Before editing, lfa-start must stop any writes under those superseded claims. No other historical ownership is changed.

Only control automation, both entrypoints' watch lifecycle, pm/start continuation prompts, brief README and scoped SHA256SUMS refresh are authorized. Existing START-owned TASK_BOARD/REVIEW_QUEUE/role-status paths remain shared control records; the existing lfa-start-owned meeting additionally permits this repair's task specification, requirement trace and executable evidence. No new evidence path or directory-wide ownership is granted. PM retains MASTER_PLAN/FILE_OWNERSHIP. QR G0 output reservations remain PLANNED and its execution remains unauthorized; M1/M1-D05 and every business Gate remain unchanged. Implement and verify now, then independent Review and separate PM Gate; no self-acceptance.

Latest user authorization: QR G0 bounded read-only documentary execution is now authorized for RUN-20260918T075255Z-QRP-G0-AUTH. The two exact G0 evidence rows above are ACTIVE, superseding their prior PLANNED reservations and prior execution prohibition only. No additional output path, source modification, QR/homography execution, G1 or Integration Gate is authorized. M1-D05 requirement mapping and Exit evaluation are separately authorized; acceptance remains evidence-bound and requires independent Review plus PM.

## G1 execution authorization and requirement registration

Authority: current explicit user authorization to register QR-GEOMETRY-01-G1 only, with four exact output paths, unique ACTIVE writer, QR-G1-REQ-01..04 and G1 Exit, then hand to lfa-start for validation and dispatch. MASTER_PLAN and frozen G0/M1 outputs must remain unchanged. This section records that authorization without amending the mother plan or any historical disposition.

PLAN_ID: QR-GEOMETRY-01; DELIVERABLE_ID: QR-GEOMETRY-01-G1; TASK_ID: RUN-20260918-QR-G1-AUTH; REQUIREMENT_IDS: QR-G1-REQ-01, QR-G1-REQ-02, QR-G1-REQ-03, QR-G1-REQ-04. DISPATCH_TRACK: PARALLEL_WORKSTREAM; WORKSTREAM: QR_GEOMETRY_RESEARCH; MAINLINE_IMPACT: NONE; EXECUTION_STATUS: AUTHORIZED_G1_ONLY; REGISTRATION_STATUS: OWNERSHIP_AND_REQUIREMENTS_REGISTERED_PENDING_START_VALIDATION; TASK_STATUS: NOT_STARTED; INTEGRATION_STATUS: NOT_AUTHORIZED. Unique WRITE_OWNER: lfa-api(w13:p1). ACTIVE ownership grants only the four exact output paths above; it is not evidence of dispatch, execution or acceptance.

Dependencies: accepted QR-PLAN-01-D01 package MANIFEST digest 90c5b32869f6a9f04d914ec3acb2c535b638da0fc84d88eedfc64c467ecbe2d2; accepted G0 exact key RUN-20260918T075255Z-QRP-G0-AUTH:d420e429a9cc1b24aa8e3697d52c58e266fa52dafbc42a11021c0d51aade5373. Existing MASTER_PLAN parallel-workstream boundary applies; M1 Exit and D01-D03 closure are not prerequisites for this isolated G1. D05/G0 continuation remains consumed.

Requirement sources: docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/06_TEMPLATE_ESTABLISHMENT_AND_VALIDATION_PLAN_v1.0.md (package06); herdr-team/.agent-control/EVIDENCE/RUN-20260918T075255Z-QRP-G0-AUTH.md sections Offline artifact contract and Dependency and next gates, including its manual-reference provenance. These new IDs derive from the current user authorization, not from review findings or reused plan/G0 execution IDs.

| REQUIREMENT_ID | Source | Authorized G1 requirement / Exit evidence |
|---|---|---|
| QR-G1-REQ-01 | package06 §3 | Before measurement/selection/results, record real sample/card/lot/assembly and upstream-source groups, seeded 12 establishment / 8 tuning / 20 holdout allocation and six slots per card. Shared source groups cannot cross partitions. Preserve custodian provenance and keep holdout JPEG, annotations and metrics inaccessible to the tool author until the required later freeze. No invented identities or independence claims. |
| QR-G1-REQ-02 | package06 §4 | Record each of 12 establishment cards' physical QR symbol corners excluding quiet zone, window boundaries, center vector, rotation, dimensions and assembly deviation in mm with card-oriented TL_TR_BR_BL, axes/origin, measurement resolution, repeat readings and actual human operator provenance. Coplanarity must be evidenced; unknown/invalid coplanarity stops the candidate. No G2 template/threshold computation or freeze. |
| QR-G1-REQ-03 | package06 §4; G0 Offline artifact contract | Register every original JPEG individually by exact path, SHA-256 and real source, bound to card/sample/partition/slot and registered capture conditions. Originals are read-only: no wildcard input grant, rotation, re-encoding, cropping or replacement. Preserve first attempts and all missing/failed/replacement-attempt records. Require 12 complete establishment cards and 72 valid geometric references for successful Exit; unsupported values remain null with reasons. |
| QR-G1-REQ-04 | package06 §5; G0 manual-reference/artifact contract | Preserve two independent human QR/window annotations blind to prediction, actual annotators, corrections and adjudication provenance. Window disagreement greater than 1% of short side requires third-person blind adjudication; unresolved identity/annotation issues remain missing and INCONCLUSIVE. Report/checks trace each requirement and exact input/output revisions. measurement_authority=false, quantification_allowed=false, formal_reporting_allowed=false. |

G1 Exit is evidence-bound: 12 independent establishment cards and 72 valid geometric references; preregistered grouping/holdout isolation; individually bound immutable originals and SHA/source; measured geometry/coplanarity; independent annotations and adjudication; missing/failed values null with explicit reasons, never zero-filled or omitted. Missing real inputs permit truthful incomplete reporting, not a fabricated successful Exit. Record actual physical measurement/annotation operators separately from the agent WRITE_OWNER; no invented person, signature or observation. No raw JPEG is an authorized output, no capture/device operation or external write is granted by these four paths. Any additional input access or output/capture scope requires exact registration first; do not expose holdout material merely to finish registration.

Control handoff: lfa-start(w15:p1) validates this registration and synchronizes TASK_BOARD under its existing ownership before G1 dispatch. Its existing unique ACTIVE docs/requirements/INDEX.md and ROUNDS/20260918T043217Z-meeting.md rows additionally permit only this G1 requirement/source mapping, verbatim current user authorization, task specification, immutable baseline and validation/dispatch record. No owner transfer or duplicate ACTIVE control-file claim is made. MASTER_PLAN.md is expressly excluded from writes; use its existing parallel-workstream reference plus this current authorization. No G1 output is created by PM registration.

Completion Gate: exact G1 output revision and checks require non-author independent Review (proposed lfa-review, not dispatched here), followed by separate lfa-pm PM acceptance. Neither task registration nor future G1 acceptance authorizes G2/G3, QR/homography development/execution, refinement, measurement, source/API/App/Core changes or Integration. M1 outputs, states and mother plan remain unchanged. START alone handles task validation and bounded dispatch; no review task is dispatched by this registration.

## Manual placement plan revision authorization

Current user explicitly requests a new plan revision for manual QR placement without a positioning jig. PM disposition: ENTER_NEW_PLAN_REVISION; documentary revision execution only, not plan acceptance or algorithm authorization. PLAN_ID=QR-PLAN-02; DELIVERABLE_ID=QR-PLAN-02-D01; TASK_ID=RUN-20260918-QR-MANUAL-PLACEMENT-REVISION; DISPATCH_TRACK=PARALLEL_WORKSTREAM; WORKSTREAM=QR_GEOMETRY_RESEARCH; MAINLINE_IMPACT=NONE; EXECUTION_STATUS=AUTHORIZED_DOCUMENTARY_REVISION_ONLY; INTEGRATION_STATUS=NOT_AUTHORIZED. Unique WRITE_OWNER=lfa-start(w15:p1).

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/09_MANUAL_QR_CONTROLLED_ROI_PLAN_REVISION_v1.0.md | RUN-20260918-QR-MANUAL-PLACEMENT-REVISION | PLAN-REVISION | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-PLAN-02-D01-checks.json | RUN-20260918-QR-MANUAL-PLACEMENT-REVISION | REVISION-CHECKS | lfa-start(w15:p1) | all roles | ACTIVE |

The two exact paths are the complete new output scope. The new 09 document is a separately reviewed amendment candidate, not a member of the previously accepted package manifest until a separately authorized cutover. Preserve accepted package files 01-08/README/MANIFEST and all old G1/G0/M1 evidence. Do not overwrite or relabel the old G1 Exit: it remains NOT_MET with documentary acceptance of truthful incompleteness only. MASTER_PLAN remains unchanged in this action. Existing START-owned TASK_BOARD, REVIEW_QUEUE, requirements INDEX and meeting permit this new revision's registration, original user instruction, trace, checks and Gate records only; retain unique current ownership and historical dispositions. START must record TASK_ID/requirements/exact FILE_SCOPE/writer before drafting. No directory-wide permission.

User-supplied facts: manual QR labels, no fixed positioning jig; upright card topology C above T, QR below observation window and above sample well; physical flow BOTTOM_TO_TOP. These facts are not measured placement distributions, original-JPEG evidence or validated direction detection. Required design statuses: QR_PRECISE_GEOMETRY_ANCHOR=NOT_SUPPORTED_BY_CURRENT_MANUAL_PLACEMENT; QR_IDENTITY_AND_DIRECTION=DESIGN_ROLE_ONLY_PENDING_VALIDATION; QR_COARSE_SEARCH_GUIDANCE=RESEARCH_CANDIDATE; AUTHORITATIVE_QR_TO_WINDOW_HOMOGRAPHY=NOT_AUTHORIZED; CONTROLLED_WINDOW_LOCALIZATION=PROPOSED_PRIMARY_ROI_PATH_NOT_YET_AUTHORIZED.

| REQUIREMENT_ID | Source | Required revision assessment |
|---|---|---|
| QR-REV2-REQ-01 | Current user item 1 | Redefine proposed G1 as PHYSICAL_LAYOUT_AND_MANUAL_QR_PLACEMENT_ASSESSMENT; define a new versioned Exit without rewriting or accepting old G1. |
| QR-REV2-REQ-02 | Current user item 2 | Define evidence for fixed card structure, target observation-window boundary, sample well, C/T/QR topology, manual-placement variation and final-JPEG boundary visibility. Separate supplied facts from observations still missing. |
| QR-REV2-REQ-03 | Current user item 3 | Define proposed G2 freeze of controlled-device priors, guide-to-final-JPEG mapping, local search region, manual reference and refusal rules. Assess image coordinates/EXIF, target-boundary-to-canonical mapping, group splits and old 12/72 criteria explicitly; no automatic reuse, deletion or fabricated replacement thresholds. |
| QR-REV2-REQ-04 | Current user item 4 | Redefine proposed G3 as CONTROLLED ROI LOCALIZATION AND QR COARSE-GUIDANCE COMPARISON; reconcile existing R1-R4 refinement responsibilities and G4/G5 dependencies without silently authorizing parked work. |
| QR-REV2-REQ-05 | Current user item 5 | Design comparison A CONTROLLED_DEVICE_PRIOR_ONLY, B CONTROLLED_DEVICE_PRIOR plus QR_COARSE_ABOVE_REGION, C QR_HOMOGRAPHY_DIAGNOSTIC_ONLY. Specify common independent references, eligibility, failures/denominators and candidate comparison criteria. C remains a planned comparison; unavailable justified geometry must be reported NOT_EVALUABLE rather than invented or silently omitted. No modes are implemented or run in this task. |
| QR-REV2-REQ-06 | Current user item 6 | C cannot supply a measurement ROI, T/C locations or authoritative rectification. QR reprojection residual is not window error. Manual placement is not proof of universal mathematical impossibility. |
| QR-REV2-REQ-07 | Current user item 7 | Keep current App/API/Core contracts and behavior unchanged; no new live failure codes, product hard gates, T/C, concentration or authoritative ROI integration. All experimental outputs retain measurement_authority=false, quantification_allowed=false and formal_reporting_allowed=false. |

Exit for this documentary revision: address all seven IDs; include old-to-proposed G1/G2/G3 and R/C/A dependency/Exit mapping, exact downstream-document/contract sync inventory, clear missing evidence and future implementation scope/owners as proposals; distinguish QR family payload from unique physical-card identity and sticker rotation from card direction. Bind the new plan/checks exact hashes for non-author independent Review followed by separate PM Gate. No self-acceptance. Accepted future plan alone still cannot dispatch G2/G3 code: separate precise implementation authorization remains required. START coordinates drafting and review submission; no G1 rerun, capture, QR/homography/ROI tool execution, source/schema/fixture edits or downstream dispatch in this registration.

## Single-annotator development reference documentary revision

Current explicit user authorization and MASTER_PLAN section Single-annotator development reference plan revision register QR-PLAN-03 / QR-PLAN-03-D01 / RUN-20260918-QR-SINGLE-ANNOTATOR-REVISION, QR-SINGLE-REQ-01..08. AUTHORIZED_DOCUMENTARY_REVISION_ONLY. PM retains MASTER_PLAN/FILE_OWNERSHIP unique ownership; the following are the two new START outputs. Existing START-owned requirements INDEX, TASK_BOARD, REVIEW_QUEUE and meeting scope extends to this task registration, source/requirement links, review submission and role-attributed Gate records. No duplicate ACTIVE ownership or directory permission.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/10_SINGLE_ANNOTATOR_DEVELOPMENT_REFERENCE_PLAN_v1.0.md | RUN-20260918-QR-SINGLE-ANNOTATOR-REVISION | PLAN-SUPPLEMENT | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-PLAN-03-D01-checks.json | RUN-20260918-QR-SINGLE-ANNOTATOR-REVISION | DOCUMENTARY-CHECKS | lfa-start(w15:p1) | all roles | ACTIVE |

START registers then drafts the exact supplement/checks and synchronizes requirements/Gates. Checks bind both PM-owned authority documents, new supplement, protected old package/MANIFEST/09/QR-PLAN-02 checks/G0/M1/original G1 evidence. Include the stable authority documents in the independent review scope; no PM self-acceptance of own changes. Non-author lfa-review reviews the complete exact submission before lfa-pm gives a separate disposition. Freeze reviewed files; external Gate records do not rewrite pending fields in evidence. No research images, measurements, randomization execution, annotation, tools, code, runtime or capture in this task. G1-D/G2-D/G3-D are proposed later execution nodes only; original G1 independent Exit FALSE, G4 closed to this branch, integration and G2-D/G3-D code NOT_AUTHORIZED.

## v1.7 baseline synchronization ownership

QR-PLAN-04 / QR-PLAN-04-D01 / RUN-20260918-V17-BASELINE-SYNC is AUTHORIZED_DOCUMENTARY_REVISION_ONLY by current user and MASTER_PLAN section v1.7 documentary synchronization authorization, QR-V17-REQ-01..05. Unique execution writer lfa-start(w15:p1). Register before editing; preserve the incoming v1.7 digest/length in checks. No previous ownership for either new path exists in this register.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| docs/QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.7_IMPLEMENTATION_BASELINE.md | RUN-20260918-V17-BASELINE-SYNC | BASELINE-SYNC | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-PLAN-04-D01-checks.json | RUN-20260918-V17-BASELINE-SYNC | DOCUMENTARY-CHECKS | lfa-start(w15:p1) | all roles | ACTIVE |

Existing START-owned requirements/INDEX.md, specs/INDEX.md, TASK_BOARD, REVIEW_QUEUE and meeting receive bounded scope for this revision's navigation, requirement trace, checks and actual role dispositions, without duplicate ACTIVE rows. PM alone updates MASTER_PLAN and FILE_OWNERSHIP. No other document/body/source permission; if a further path is essential, report exact need before editing. Preserve old package01-10/README/MANIFEST, QR-PLAN-02/03 checks, G0/G1/M1 evidence and frozen v2 contracts. Prior PM authority digests are historical and intentionally revised; preserve their old binding in external records, do not falsely claim old checks reproduce against new authority bytes. Submit both fresh full authority revisions plus revised v1.7, changed indexes and new checks to non-author lfa-review before separate lfa-pm Gate. Self-mutating ledgers remain references. No automatic execution, capture, images, annotations, tool experiments, code, schema migration or integration. After exact dual acceptance, record the documentary outcome only.

## G1-D eight-output ownership registration

TASK_ID=RUN-20260918-G1D-OWNERSHIP; DELIVERABLE_ID=G1D-OWNERSHIP-D01; requirements=G1D-OWN-REQ-01..03 in MASTER_PLAN. Explicit user authorization covers this new authority revision and independent review only. These eight exact paths come from TASK_BOARD RUN-20260918-G1D-INPUT-PREP. ACTIVE below means exclusive writer reservation, NOT permission to create/populate outputs now. OUTPUT_EXECUTION_AUTHORIZED=false; later bounded execution authorization and genuine evidence are required. No new files are produced by this registration.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1D-dataset.json | RUN-20260918-G1D-OWNERSHIP | DATASET | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1D-geometry.json | RUN-20260918-G1D-OWNERSHIP | GEOMETRY | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1D-annotations-first.json | RUN-20260918-G1D-OWNERSHIP | FIRST-ANNOTATION | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1D-repeat-protocol.json | RUN-20260918-G1D-OWNERSHIP | REPEAT-PROTOCOL | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1D-annotations-repeat.json | RUN-20260918-G1D-OWNERSHIP | REPEAT-ANNOTATION | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1D-self-correction.json | RUN-20260918-G1D-OWNERSHIP | SELF-CORRECTION | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1D-report.md | RUN-20260918-G1D-OWNERSHIP | REPORT | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-GEOMETRY-01-G1D-checks.json | RUN-20260918-G1D-OWNERSHIP | CHECKS | lfa-start(w15:p1) | all roles | ACTIVE |

Agent writer is not the physical operator or annotator; real PROJECT_LEAD supplies genuine measurement/annotation evidence. Historical 45 paths/43 SHA are not admitted G1-D records; missing identity, card/slot binding, geometry and round times stay null. Original G1 FALSE/NOT_MET, G1-D incomplete, five development/no-authority markers retained. No capture, annotation, randomization, tool development, code, Integration or downstream dispatch.

PM remains sole writer of MASTER_PLAN/FILE_OWNERSHIP. Existing START TASK_BOARD scope extends only to this task registration, exact prior/new authority SHA/bytes, verification and actual non-author Review then separate PM disposition; no duplicate ledger ownership. Both complete new authority revisions require fresh non-author lfa-review acceptance. Old QR-PLAN-04 six-file acceptance remains historical; v1.7/checks/two indexes stay frozen. Final acceptance is external and documentary ownership only; no rewriting frozen submitted files or old checks.

## QR product identification scope correction candidate

PLAN_ID=QR-SCOPE-05; DELIVERABLE_ID=QR-SCOPE-05-D01; TASK_ID=RUN-20260918-QR-PRODUCT-DECOUPLING. User formal scope correction authorizes dependency search, documentary revision candidates, three separate task candidates and non-author review only. PM owns this authority and MASTER_PLAN; START owns the following exact two new documentary outputs and existing TASK_BOARD/BLOCKERS external registration. No other path is authorized for edits. Existing historical Evidence, old Reviews, QR04 spec/index/checks, business files and all eight G1-D outputs remain protected. Unknown ownership is report-only. No new ACTIVE business ownership; candidate owner/WRITE_OWNER values are proposals, not grants.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| herdr-team/.agent-control/EVIDENCE/QR-SCOPE-05-D01-candidate.md | RUN-20260918-QR-PRODUCT-DECOUPLING | SCOPE-CANDIDATE | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-SCOPE-05-D01-checks.json | RUN-20260918-QR-PRODUCT-DECOUPLING | DOCUMENTARY-CHECKS | lfa-start(w15:p1) | all roles | ACTIVE |

Review submission binds complete new MASTER_PLAN, FILE_OWNERSHIP, candidate and checks SHA256/bytes. Freeze after submission; actual non-author lfa-review result belongs to external TASK_BOARD. Stop after Review awaiting a separate PM Gate; this task must not auto-accept itself or dispatch any of the three candidates. All QR decode/parse/match/shutter/final-JPEG recheck business execution permissions remain NO; QR ROI, Homography, measurement, quantification and ten-point capture remain NO.

## Management recording repair ownership

PLAN_ID=GOV-MGMT-01; DELIVERABLE_ID=GOV-MGMT-01-D01; TASK_ID=RUN-20260918-MANAGEMENT-RECORDING; REQUIREMENT_IDS=MGMT-REQ-01..05; source MASTER_PLAN §Management issue recording control repair. User explicitly authorizes this bounded control-plane execution. Existing ACTIVE single-writer scopes for TASK_TEMPLATE, BLOCKERS, ROUNDS and TASK_BOARD extend to this task without duplicate rows or owner changes. Historical ledger prefixes are append-only; historical Evidence and QR work are protected. PM owns authority files only and supplies assessment to START for recording. The following previously released or unregistered paths now have one ACTIVE writer:

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| herdr-team/prompts/pm.md | RUN-20260918-MANAGEMENT-RECORDING | MANAGEMENT-POLICY | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/prompts/start.md | RUN-20260918-MANAGEMENT-RECORDING | MANAGEMENT-POLICY | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/.agent-control/DECISIONS.md | RUN-20260918-MANAGEMENT-RECORDING | CONFIRMED-DECISIONS | lfa-start(w15:p1) | all roles | ACTIVE |
| herdr-team/SHA256SUMS.txt | RUN-20260918-MANAGEMENT-RECORDING | CHANGED-STATIC-DIGESTS | lfa-start(w15:p1) | all roles | ACTIVE |

Exact execution scope is the eight files enumerated in MASTER_PLAN. No new ledger, script, Evidence file, COMMON edit, business change or QR work is authorized. Before edits capture current hashes and historical prefixes; preserve prior review bindings. Evidence and verification belong in current ROUNDS, submission and actual Gate receipts in TASK_BOARD using frozen prefix/digest references. START executes/dispatches; actual lfa-review performs non-author review; PM then separately Gates the same revision. A transport ACK, issue record or improvement candidate is never acceptance or expanded permission.

## Authorized product identification implementation ownership

Current user whole-goal business authorization and MASTER_PLAN section QIUQIU DHEA product identification authorized execution govern these nodes. Stable agent names, no inferred pane IDs. Existing business ownership rows were absent; START must confirm no live conflicting writes before dispatch. All paths outside each exact node scope, all historical Evidence, geometry, v3/full-bundle migration, original captures and unrelated user changes remain protected. PM retains authority; START retains existing ledgers and appends authorization/receipts. No parallel shared-file writer.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| python_gateway/dhea_input.py | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| python_gateway/dhea_export.py | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| python_gateway/dhea.py | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| core/product_identity.py | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| docs/api/api-reference.md | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| docs/api/schemas/dhea-product.schema.json | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| docs/api/openapi-dhea-v2.json | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| fixtures/dhea-product/cases.json | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| python_gateway/tests/test_dhea_product_contract.py | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| python_gateway/tests/test_dhea.py | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-PC-01-D01.json | RUN-20260918-QR-PC | PRODUCT-CONTRACT | lfa-api | all roles | ACTIVE |
| Android_App/app/src/main/java/com/example/camera/NativeCameraManager.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/main/java/com/example/camera/PreviewGuidanceAnalyzer.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/main/java/com/example/ui/screens/CaptureScreen.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/main/java/com/example/ui/LfaViewModel.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/main/java/com/example/domain/model/Models.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/main/java/com/example/data/local/JournaledArtifactStore.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/main/java/com/example/network/DheaClient.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/main/java/com/example/network/DheaJson.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/build.gradle.kts | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/gradle/libs.versions.toml | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/main/java/com/example/camera/ProductGate.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/test/java/com/example/camera/ProductGateTest.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/test/java/com/example/network/DheaContractTest.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/app/src/test/java/com/example/camera/PreviewGuidanceAnalyzerTest.kt | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| Android_App/README.md | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-ANDROID-01-D01.json | RUN-20260918-QR-ANDROID | PRODUCT-IMPLEMENTATION | lfa-android | all roles | ACTIVE |
| core/dhea.py | RUN-20260918-QR-FINAL | PRODUCT-IMPLEMENTATION | lfa-api | all roles | ACTIVE |
| core/dhea_diagnostics.py | RUN-20260918-QR-FINAL | PRODUCT-IMPLEMENTATION | lfa-api | all roles | ACTIVE |
| python_gateway/tests/test_dhea_product_recheck.py | RUN-20260918-QR-FINAL | PRODUCT-IMPLEMENTATION | lfa-api | all roles | RELEASED_FOR_TASK-QIUQIU-04 |
| tests/test_dhea_product.py | RUN-20260918-QR-FINAL | PRODUCT-IMPLEMENTATION | lfa-api | all roles | RELEASED_FOR_TASK-QIUQIU-04 |
| python_gateway/tests/test_dhea_diagnostics.py | RUN-20260918-QR-FINAL | PRODUCT-IMPLEMENTATION | lfa-api | all roles | RELEASED_FOR_TASK-QIUQIU-04 |
| herdr-team/.agent-control/EVIDENCE/QR-FINAL-01-D01.json | RUN-20260918-QR-FINAL | PRODUCT-IMPLEMENTATION | lfa-api | all roles | ACTIVE |

Node2/Node3 activate after Node1 dual Gate. Shared Node1 paths retain lfa-api exclusively and extend to Node3 only after freeze; do not duplicate ownership rows. Node2 owns all Android changes including declaration persistence/serialization migration. Required additional paths are registered by PM before edit within existing user authorization. Each owner preserves baseline hashes and reports unrelated changes rather than overwriting them.

Activation receipt: Node1 Evidence 129730595d1bc42ef226df6a50a60e6e03793abb07a7a64e250e11dcc90491db / 22762 bytes obtained existing lfa-review CODE_REVIEW_ACCEPTED and lfa-pm PM_ACCEPTED. Above twenty-two Node2/Node3 rows are now ACTIVE. Existing shared rows for python_gateway/dhea_input.py, python_gateway/dhea.py, core/product_identity.py, docs/api/api-reference.md and python_gateway/tests/test_dhea_product_contract.py also cover RUN-20260918-QR-FINAL under the same sole lfa-api writer; no duplicate row or concurrent writer. QR-PC-01-D01.json stays frozen. START performs formal concurrent dispatch; exact declared scope only.

Node2 pre-edit baseline disposition: existing unstaged LfaViewModel.kt (25621 bytes, SHA256 28b65ed04d5c0846e0a755439533b58aed879e4f184274740e3f1fd76b6515f6) and CaptureScreen.kt (23773 bytes, SHA256 258f4da400d78484fa65a8b366e178681bec69810de48cb52327b6cea4168621), both at their registered Android paths above, are protected adoptable baseline, not Node2-authored changes. Preserve the existing processing/unknown-receipt lookup and retry-after behavior, and the timed top saved-capture notice. No reset, restore, overwrite from HEAD or attribution to Node2. Node2 may incrementally integrate its product gate on these bytes once START confirms no other live writer; all other nonconflicting Node2 paths remain actionable now. Dirty working-tree state alone is not an ownership conflict. If either baseline changes before first edit, re-read and coordinate the actual writer.

QR-FINAL-R3 repair ownership extension: existing sole lfa-api rows for python_gateway/dhea_export.py, docs/api/openapi-dhea-v2.json and python_gateway/tests/test_dhea.py also cover RUN-20260918-QR-FINAL as ACTIVE. Scope is only synchronization of enabled product-only final-JPEG acceptance and migration of the obsolete Node1 disabled-path expectation; preserve legacy v2, complete-v3 refusal, unrelated baseline work and frozen Node1 Evidence. No duplicate writer or new task. Bind the revised files in new Node3 Evidence and obtain existing non-author Review then same-revision PM Gate.

Node2 repair regression ownership correction: Android_App/app/src/test/java/com/example/network/ProductBundlePersistenceTest.kt is now explicitly assigned to RUN-20260918-QR-ANDROID, sole writer lfa-android, ACTIVE. Scope is real Bundle 1.6 product-only persistence/restart and legacy Bundle 1.5 preservation checks requested by the existing Review; no production or wire-schema expansion. The file already appears in submitted Evidence 26abe357bcd1ca527830e0da78d4f7f943718ead05769f3564d5578220d5ede0 / 16194 bytes before this explicit registration; this append corrects the missing path prospectively and does not claim prior registration. Preserve that submitted revision as historical. Author must bind this updated authority in the next exact Evidence revision; existing non-author Review and PM Gate must identify the resulting revision. Frozen Node1/3 Evidence remains unchanged.

## Android-origin integration ownership

All following paths are ACTIVE only for RUN-20260920-QR-E2E, QR-E2E-01-D01, after START dispatch. Existing accepted implementation files and frozen Node1/2/3 Evidence are read-only dependencies. Additional source changes require prior PM registration.

| Path | Task | Scope | Sole writer | Readers | Status |
|---|---|---|---|---|---|
| Android_App/app/src/test/java/com/example/network/ProductEndToEndTest.kt | RUN-20260920-QR-E2E | INTEGRATION | lfa-android | all roles | ACTIVE |
| experiments/qr-product-e2e/gateway.py | RUN-20260920-QR-E2E | INTEGRATION | lfa-api | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-E2E-01-D01.json | RUN-20260920-QR-E2E | INTEGRATION | lfa-android | all roles | ACTIVE |

Temporary certificates, isolated storage, fixtures, receipts and executable logs are generated artifacts outside tracked source; no real secrets or production storage. API owner supplies its exact source and execution digests to Android integration evidence owner. Do not create documentation or change business source merely to support the harness. Existing roles coordinate launch parameters directly; START alone formally dispatches.

## Live-device capture layout increment

ANDROID-UI-010-R01 is authorized by explicit user feedback recorded at MASTER_PLAN.md:411-417 and START dispatch. Existing sole writer lfa-android owns the bounded updates to `Android_App/app/src/main/java/com/example/ui/screens/CaptureScreen.kt`, `docs/design/app-android-ios-detail.md`, and `Android_App/README.md`; ACTIVE for this increment. Source baseline reported by owner: `410b17a00b63374f5d28a5531c478db8b30e8427`; preserve all pre-existing dirty content. Any affected existing Android UI test must be named before modification. Frozen Node and integration Evidence remains unchanged; generated revision digests/build/display evidence may live under Android_App/build. Original lfa-review provides non-author exact-revision Review, followed by PM Gate; only PM operates ADB and performs data-preserving installation and device display checks. API/Core/MLKit/ProductGate/payload/750ms/full-JPEG invariants remain unchanged. Shared guide geometry changes require explicit source-path extension before edit to prevent overlay/evidence divergence.

ANDROID-UI-010-R01 corrected pre-edit exact scope: sole writer lfa-android is ACTIVE for existing `Android_App/app/src/test/java/com/example/camera/CameraEvidenceTest.kt`, limited to observable unchanged-strip/lower-square-QR geometry, white-border spacing, in-bounds and non-overlap checks. The three existing source/document paths above remain assigned to the same owner. Proposed new `CaptureGuidanceLayoutTest.kt` and `herdr-team/.agent-control/EVIDENCE/ANDROID-UI-010-R01.json` are withdrawn before edit; no new process document or herdr Evidence file. Revision/digest/build evidence is generated under `Android_App/build/`. `guideRegion`, `NativeCameraManager`, `PreviewGuidanceAnalyzer`, `ProductGate`, API/Core/wire schema and historical Evidence remain unchanged. PM retains install-r and live display verification; host geometry checks do not establish device validation.

## HARNESS-VERIFICATION-SHADOW exact ownership

PLAN_ID=HARNESS-SHADOW-01; DELIVERABLE_ID=HARNESS-SHADOW-01-D01; TASK_ID=RUN-20260919-HARNESS-SHADOW-S2-S6; WORKSTREAM=HARNESS-VERIFICATION-SHADOW; MAINLINE_IMPACT=NONE. Authority: explicit user governance request and MASTER_PLAN HARNESS-SHADOW-01-GOV-R01, five gates SATISFIED, decision APPROVED, implementation_allowed=true for the three paths only. Unique future writer shadow-core; this registration neither starts an agent nor dispatches work. No lfa product implementer may be reused for this workstream.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| herdr-team/harness/shadow.py | RUN-20260919-HARNESS-SHADOW-S2-S6 | SHADOW-S2-S6 | shadow-core | all roles | ACTIVE |
| herdr-team/harness/verify_shadow.py | RUN-20260919-HARNESS-SHADOW-S2-S6 | SHADOW-S2-S6 | shadow-core | all roles | ACTIVE |
| herdr-team/.agent-control/MACHINE/HARNESS-VERIFICATION-SHADOW/qr-android-projection.json | RUN-20260919-HARNESS-SHADOW-S2-S6 | SHADOW-S2-S6 | shadow-core | all roles | RELEASED |

All three paths were absent at registration; no existing matching or overlapping harness ownership was found. No wildcard, directory-level ownership, package rewrite, additional Evidence or control-ledger write is granted. All other paths remain protected, including dashboard.py, review_dispatch.py, TASK_BOARD.md, BLOCKERS.md, REVIEW_QUEUE.md, ROUNDS, historical EVIDENCE and product code. Existing product owners and records remain effective. ACTIVE grants bounded future ownership only; PM performs governance registration only, with no runtime implementation or role startup in this request.

## HARNESS-SHADOW-01 Slice 7 exact ownership

Authority=explicit user governance-only request and MASTER_PLAN HARNESS-SHADOW-01-S7-GOV-R01. PLAN_ID=HARNESS-SHADOW-01, continuation Slice 7; DELIVERABLE_ID=HARNESS-SHADOW-01-S7-UI; TASK_ID=RUN-20260919-HARNESS-SHADOW-S7-UI; WORKSTREAM=HARNESS-VERIFICATION-SHADOW; MAINLINE_IMPACT=NONE. Slice 2–6 independently verified and CODE_REVIEW_ACCEPTED per user report; technical UI prerequisite=MET. Separate Slice 7 governance approval does not establish UI implementation acceptance.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| herdr-team/dashboard.py | RUN-20260919-HARNESS-SHADOW-S7-UI | SHADOW-S7-UI | shadow-ui | all roles | RELEASED |

Exact sole writable implementation path for this task is the row above; no wildcard. Permission is limited to read-only consumption/rendering of herdr-team/.agent-control/MACHINE/HARNESS-VERIFICATION-SHADOW/qr-android-projection.json. The projection itself is read-only for shadow-ui. Required display: ingestion/evidence/acceptance statuses, subject revision, criterion required/status/generation/selected/superseded/evidence references/reason codes, diagnostics and reducer digest/version. NOT_READY and UNVERIFIED must never become PASS through display logic.

Existing line 38 grants ACTIVE dashboard.py ownership to lfa-start for RUN-20260918T043217Z-DOC-GOVERNANCE. That record and all lfa-* ownership remain protected and unchanged. ACTIVE here grants the requested bounded Slice 7 authorization only; it does not permit simultaneous writers or silently revoke the prior claim. Before future dispatch/edit, explicitly reconcile/release the prior dashboard file lock through the existing ownership process. Future execution remains blocked by that exact conflict until resolved; shadow-ui is the sole authorized writer for Slice 7, with no role startup, reuse or dispatch in this request.

All other paths are protected from this task, including review_dispatch.py, product code, historical Evidence/Event/Projection/PHASES/Gates, the named projection input and control ledgers. Earlier Slice 2–6 restrictions remain effective for shadow-core. UI acceptance requires its own exact-revision rendering verification, non-author Review and PM Gate; current registration is approval only. No product acceptance or historical state changes are implied.

Slice 7 completion release: HARNESS-SHADOW-01-S7-PM-R01 records PM_ACCEPTED for dashboard.py SHA256=ba1ed40e8a78a8c43551282a3b47bde917bc95b8878929bc98351a642d80a54b, following user-reported independent shadow-ui-review CODE_REVIEW_ACCEPTED after repairs. PM matched the current subject digest and projection SHA256=3cdd0988dd8e1ecbe3ca64858b1336147647389a5f274213f8f6313af0d7b627. The prior lfa-start claim at line 38 is already RELEASED; the registration-time conflict is resolved in the current ledger. The Slice 7 row above is now RELEASED with no successor writer. This ends its write permission; all other ownership and protected paths remain unchanged. Acceptance is limited to the read-only UI and preserves VALID/NOT_READY/UNVERIFIED/DEVICE_EVIDENCE_PENDING; it does not accept product evidence, close the product Goal or claim full --check passes.

## Exact Android evidence revision ingestion

TASK_ID=RUN-20260920-SHADOW-QR-INGEST; PLAN_ID=HARNESS-SHADOW-01; WORKSTREAM=HARNESS-VERIFICATION-SHADOW; MAINLINE_IMPACT=NONE. User authorizes coordinator ingestion of Evidence SHA256=3bfca2be31ab0bd96601a9fc066a5d76009f97e77073e522b11e8a57a36d8b50 / 21574 bytes. Prior shadow-core projection claim released above before this temporary transfer; no live shadow-core in inspected roster. No harness source, dashboard, product source, Evidence or historical event write permitted. lfa-review and lfa-api are read-only for this task. PM-owned governance ledgers retain their existing owner.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| herdr-team/.agent-control/MACHINE/HARNESS-VERIFICATION-SHADOW/qr-android-projection.json | RUN-20260920-SHADOW-QR-INGEST | REDUCER-OUTPUT | lfa-pm | all roles | RELEASED |

Output must be serialized from existing reducer return value only, never hand-edited. Temporary ownership ends after focused verification and exact outcome receipt; no acceptance of the six unproven device scenarios is authorized.

RUN-20260920-SHADOW-QR-INGEST completion: temporary projection claim RELEASED after focused Shadow verification PASS and reducer-only output SHA256=3909f96aa7f7c1e012604f6ed106535eacc5fd88efe645c2af2c524900b98470 /1178 bytes. Result VALID/NOT_READY/UNVERIFIED with DEVICE_EVIDENCE_PENDING; six unproven scenarios remain. No source ownership transferred, no successor output writer, no product acceptance. Exact inputs and reviewer limitations retained in MASTER_PLAN.md:490 onward.

## Corrected Evidence ingestion R02 temporary ownership

User-authorized RUN-20260920-SHADOW-QR-INGEST-R02, Evidence c2d1185f1a56124dcf49089af239238852ad523f824ffb067e0f781d21ee1474 /21898 bytes. Prior output owners remain RELEASED. Only serialized shadow.project() output is writable; no source, fixture, Evidence or product authority. lfa-review read-only exact-digest review follows generation.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| herdr-team/.agent-control/MACHINE/HARNESS-VERIFICATION-SHADOW/qr-android-projection.json | RUN-20260920-SHADOW-QR-INGEST-R02 | REDUCER-OUTPUT | lfa-pm | all roles | RELEASED |

R02 output generation completed and temporary ownership RELEASED: Projection SHA256=d41e331c1389ec8df3f7ec797253be5c466e79375eb35a087087e578eb0ac8fa /1178 bytes; subject Evidence=c2d1185f1a56124dcf49089af239238852ad523f824ffb067e0f781d21ee1474 /21898. Focused schema/digest/order/readback PASS. Independent exact-pair review remains read-only. No successor write grant or product acceptance.

## QLI full-text cutover exact scope

RUN-20260920-QLI-CUTOVER; shared contract revision sha256:54da44fd6071410f765c5000efb6191653f9eafb6d68aeda8cb6cf433edfe94e. Explicit user authorization and PM cutover rule in MASTER_PLAN apply. Below extends existing same-owner claims to this new task, superseding old freeze only for editable source bodies. No ownership transfer/concurrent writer. Old Evidence remains frozen. Every path outside table is read-only; additions require PM registration. Generated freeze/check artifacts may be written under artifacts/qli-cutover; no existing Evidence replacement.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| core/product_identity.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| python_gateway/dhea_input.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| python_gateway/dhea_export.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| python_gateway/dhea.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| core/dhea.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| core/dhea_diagnostics.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| docs/api/api-reference.md | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| docs/api/schemas/dhea-product.schema.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| docs/api/openapi-dhea-v2.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-product/cases.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| python_gateway/tests/test_dhea_product_contract.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| python_gateway/tests/test_dhea.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| python_gateway/tests/test_dhea_product_recheck.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | RELEASED_FOR_TASK-QIUQIU-04 |
| tests/test_dhea_product.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | RELEASED_FOR_TASK-QIUQIU-04 |
| python_gateway/tests/test_dhea_diagnostics.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | RELEASED_FOR_TASK-QIUQIU-04 |
| experiments/qr-product-e2e/gateway.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| docs/api/generate_dhea_v3.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| python_gateway/dhea_v3_schema.py | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| docs/api/openapi-dhea-v3.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| docs/api/schemas/capture-bundle-1.6.schema.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| docs/api/schemas/dhea-capture-v3.schema.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| docs/api/schemas/dhea-result-v3.schema.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| docs/api/schemas/dhea-validation-v3.schema.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/http-cases.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/v2-baseline-sha256.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/qr-cases.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/jcs/metadata.jcs | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/jcs/product-gate-declaration.jcs | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/jcs/result-snapshot.jcs | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/jcs/sha256.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/negative/schema-cases.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/negative/transport-cases.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/bundle.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/capture.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/diagnostics.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/error-conflict.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/error.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/qr.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/result-failed.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/result-measured.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/result-processing.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/result-rejected.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| fixtures/dhea-v3/positive/validation.json | RUN-20260920-QLI-CUTOVER | API-CORE | lfa-api | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.2.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.3_IMPLEMENTATION_READY.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.4_IMPLEMENTATION_READY.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.5_IMPLEMENTATION_READY_AFTER_TEMPLATE_VALIDATION.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.6.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.6_MANUAL_QR_CONTROLLED_ROI_REVISED.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.7_IMPLEMENTATION_BASELINE.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/DHEA_NATIVE_APPS_API_RECOGNITION_TODO_2026-09-15.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/api/dhea-v3-product-gate.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/01_QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.6.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/02_MASTER_PLAN_v1.1.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/03_DECISIONS_QR_MVP_VERTICAL_SLICE_v1.0.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/04_TASK_BOARD_QR_TEMPLATE_ROI_SIGNAL_v1.0.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/05_AUTHORITATIVE_CONTRACT_SYNC_CHECKLIST_v1.0.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/06_TEMPLATE_ESTABLISHMENT_AND_VALIDATION_PLAN_v1.0.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/07_HERDR_RECENT_THREE_FAILURES_INVESTIGATION_v1.0.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/08_TEN_POINT_CAPTURE_RELEASE_AND_EXECUTION_PLAN_v1.0.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/09_MANUAL_QR_CONTROLLED_ROI_PLAN_REVISION_v1.0.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/10_SINGLE_ANNOTATOR_DEVELOPMENT_REFERENCE_PLAN_v1.0.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/README.md | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |
| docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/MANIFEST.sha256 | RUN-20260920-QLI-CUTOVER | DOCS | lfa-start | all roles | ACTIVE |

Android existing QLI code/declaration/tests are read-only dependencies for this cutover; lfa-android must freeze relevant current digests and report any actual mismatch before receiving write scope. Reviewer=lfa-review read-only. PM retains only governance ledgers. No historical event/Evidence/Projection edit authorized.

## Bounded Shadow dashboard presentation refinement

TASK_ID=RUN-20260920-SHADOW-DASHBOARD-REFINEMENT. User requested registration only, not implementation. Prior dashboard.py claims for lfa-start and shadow-ui are RELEASED. Herdr discovery returned agent_not_found for shadow-ui and shadow-ui-review; no replacement agent or alternate owner assigned.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| herdr-team/dashboard.py | RUN-20260920-SHADOW-DASHBOARD-REFINEMENT | PRESENTATION-ONLY | shadow-ui | shadow-ui-review read-only; all roles | RELEASED |

Exact write scope is dashboard.py only. Scope and prohibitions are registered in MASTER_PLAN under this TASK_ID: existing validated v1.3 projection display only, Legacy/Shadow visual separation, collapsed checklists/historical projects and responsive track wrapping. Projection, sources, schemas, dependencies, product behavior, Gates and other files are read-only. ACTIVE assigns sole ownership only; this registration does not dispatch execution or confer review acceptance. shadow-ui-review remains the required read-only reviewer.

Activation receipt: user reports existing shadow-ui live in pane wQ:p19. Conflict check found all three prior dashboard.py claims RELEASED and no competing ACTIVE claim. RESERVED_UNASSIGNED is now shadow-ui ACTIVE for this exact task/path only. All scope/prohibitions and the shadow-ui-review requirement remain unchanged. No implementation, prompt dispatch, role creation or restart performed.

Completion release: PM_GATE=PM_ACCEPTED for exact dashboard.py SHA256=a66743b965e366c6b00ebd7fbf1633fec19a85e5c2f57d64ed360e100b69b886 with read-only projection SHA256=d41e331c1389ec8df3f7ec797253be5c466e79375eb35a087087e578eb0ac8fa. User-reported independent shadow-ui-review CODE_REVIEW_ACCEPTED and focused desktop/mobile checks support presentation-only acceptance; PM matched both digests. Ownership is RELEASED. No product/device PASS, Legacy Phase change, dispatch or projection mutation is authorized.

## EXIF execution repair and device ingestion R03

RUN-20260920-EXIF-ORDER-REPAIR extends existing sole lfa-api ACTIVE ownership, without adding duplicate claims, for exactly core/product_identity.py, core/dhea.py, core/dhea_diagnostics.py, python_gateway/dhea.py, tests/test_dhea_product.py, python_gateway/tests/test_dhea_product_recheck.py, python_gateway/tests/test_dhea_diagnostics.py and docs/api/api-reference.md. Conflict inspection found only the same lfa-api owner for these paths. Prior accepted revisions remain historical, not acceptance of these future changes. No core/signal.py, geometry, Android, schema, original JPEG, stored result or runtime write is granted.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| artifacts/qli-cutover/exif-order-repair-evidence.json | RUN-20260920-EXIF-ORDER-REPAIR | EXACT-EVIDENCE | lfa-api | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-ANDROID-DEVICE-R03.json | RUN-20260920-SHADOW-QR-INGEST-R03 | IMMUTABLE-INTAKE | lfa-start | all roles | RELEASED |
| herdr-team/.agent-control/MACHINE/HARNESS-VERIFICATION-SHADOW/qr-android-r03-inputs.json | RUN-20260920-SHADOW-QR-INGEST-R03 | REGISTRY-EVENT-INPUTS | lfa-start | all roles | RELEASED |
| herdr-team/.agent-control/EVIDENCE/QR-ANDROID-DEVICE-R03-checks.json | RUN-20260920-SHADOW-QR-INGEST-R03 | INGESTION-CHECKS | lfa-start | all roles | RELEASED |
| herdr-team/.agent-control/MACHINE/HARNESS-VERIFICATION-SHADOW/qr-android-projection.json | RUN-20260920-SHADOW-QR-INGEST-R03 | TEMPORARY-REDUCER-OUTPUT | lfa-start | all roles | RELEASED |

R03 prior projection claims340/352 are RELEASED; no competing ACTIVE owner found. The new inputs file records existing-schema registry/events for reproducibility, not a new event-store implementation. Preserve historical Evidence/events. Projection permission is conditional: receive original independent evidence review and Android source-binding disposition first, freeze new exact intake subject, validate through existing ingestion/reducer, then serialize only shadow.project() output. Until then preserve current c2d1185f subject/projection bytes. UNVERIFIED source binding remains explicit if unresolved; it cannot inherit old subject acceptance. No manual PASS, source/schema changes, ADB, uploads, retries or restart. Required independent reviewer=lfa-review; subsequent separate PM Gate and ownership release required.

R03 release receipt: RUN-20260920-SHADOW-QR-INGEST-R03-PM=PM_ACCEPTED for ingestion/projection correctness following original lfa-review CODE_REVIEW_ACCEPTED and independent PM4/4 SHA256/byte checks; exact bindings and limitations recorded in MASTER_PLAN R03 PM Gate. All four claims450–453 RELEASED, no successor writer. Projection50e629198cc08eb36744430e43f212803963de9ec8ba526300c4cdcc70d6b462 remains VALID/NOT_READY/UNVERIFIED under fresh subject216f8f35; no product or overall device acceptance. Immutable submission artifacts including pending-review fields are not rewritten. EXIF ownership is unchanged.

## Auxiliary preview clarity UI

RUN-20260920-ANDROID-CLARITY-UI-R01 extends existing sole lfa-android ownership for Android_App/app/src/main/java/com/example/camera/PreviewGuidanceAnalyzer.kt, Android_App/app/src/main/java/com/example/ui/screens/CaptureScreen.kt, Android_App/app/src/main/java/com/example/ui/LfaViewModel.kt, Android_App/app/src/test/java/com/example/camera/PreviewGuidanceAnalyzerTest.kt and Android_App/README.md. Scope is only non-blocking preview clarity guidance as registered in MASTER_PLAN. Same-owner overlapping product-confirmation work must be serialized by lfa-android; no second writer or authorization of the held product contract.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| Android_App/app/src/test/java/com/example/ui/PreviewClarityGuidanceTest.kt | RUN-20260920-ANDROID-CLARITY-UI-R01 | AUXILIARY-UI | lfa-android | lfa-review; all roles | ACTIVE |

## Requirements consolidation dedicated pane

RUN-20260920-REQUIREMENTS-CONSOLIDATION-R01 sole writer lfa-docs(w12:p2), configured aliyun/qwen3.7-plus; PM integration owner lfa-pm. Existing live documents remain read-only until exact shared ownership/archive transfer; old no-bulk-migration prohibition is superseded only for the user-authorized reversible documentary task after mapping/review.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| docs/requirements/DHEA_MVP_完整需求.md | RUN-20260920-REQUIREMENTS-CONSOLIDATION-R01 | COMPLETE-REQUIREMENTS | lfa-docs | all roles | ACTIVE |
| docs/requirements/DHEA_需求来源与归档映射.md | RUN-20260920-REQUIREMENTS-CONSOLIDATION-R01 | SOURCE-ARCHIVE-MAP | lfa-docs | all roles | ACTIVE |

## PM patrol minimal repair

Explicit user authorization: TASK_ID=RUN-20260920-PM-PATROL-R01; PLAN_ID=PM-PATROL-01; DELIVERABLE_ID=PM-PATROL-01-D01; sole writer=lfa-start(w15:p1). START reports the previous claims for these three paths RELEASED and no overlapping ACTIVE claims. Accept that supplied ownership check without repeating it. Exact FILE_SCOPE is limited to the three rows below.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| herdr-team/review_dispatch.py | RUN-20260920-PM-PATROL-R01 | PM-PATROL-01-D01 | lfa-start | all roles | RELEASED |
| herdr-team/prompts/pm.md | RUN-20260920-PM-PATROL-R01 | PM-PATROL-01-D01 | lfa-start | all roles | RELEASED |
| herdr-team/SHA256SUMS.txt | RUN-20260920-PM-PATROL-R01 | PM-PATROL-01-D01 | lfa-start | all roles | RELEASED |

Implementation scope: minimal repair of the existing watchdog's idle/done handling; one-time PM_PENDING recovery; one-time ACTIVE-owner and PM recovery with independent keys; protection of working agents; and the corresponding self-test. No expansion beyond these behaviors or exact paths. START records TASK_BOARD/DECISIONS under its existing governance permissions; those permissions are not new implementation FILE_SCOPE. This registration does not change MASTER_PLAN conclusions or Gates and grants no product runtime, device, deployment or archive-move authority.

Administrative release receipt — ROLE=lfa-pm; TASK_ID=RUN-20260920-PM-PATROL-R01; PLAN_ID=PM-PATROL-01; DELIVERABLE_ID=PM-PATROL-01-D01. Under the user's explicit final release authorization and reported CLOSED queue with sequential lfa-review CODE_REVIEW_ACCEPTED and lfa-pm PM_ACCEPTED, the three exact claims above transition ACTIVE → RELEASED. Accepted submission key remains RUN-20260920-PM-PATROL-R01:663322c28c65f93b4907e028737b3d7315e829275f8d38736045ad744337f0ce:46794:REVIEW. This is a subsequent authorized ownership-ledger change, not an artifact revision or a new acceptance. Preserve historical accepted source_hashes and artifact digests without rewriting the queue. No business Gate, MASTER_PLAN conclusion or unrelated claim changes; no new execution authority. Original task administrative ownership release is complete; START retains responsibility for the final TASK_BOARD BTW receipt.
## DHEA QR Window independent preparation R04

RUN-20260920-DHEA-MAINLINE-REPLAN-R01 / NODE-01-QR-WINDOW-PREP binds only the first executable preparation node after R04 bounded acceptance. Sole writer is lfa-api. The node may prepare and bind the independent geometry-policy artifact, asymmetric synthetic fixture identity, and independent geometry entry/oracle required by R04; it MUST NOT alter the frozen R04/predecessor receipts, select the legacy candidate as authorization, change runtime/default/gateway behavior, or execute device/schema/Room/archive work. The policy artifact path and digest remain unknown until the node produces them truthfully; no nonexistent artifact is registered here.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| core/geometry.py | RUN-20260920-DHEA-MAINLINE-REPLAN-R01 | NODE-01-QR-WINDOW-PREP | lfa-api | all roles | ACTIVE |
| tests/test_geometry.py | RUN-20260920-DHEA-MAINLINE-REPLAN-R01 | NODE-01-QR-WINDOW-PREP | lfa-api | all roles | ACTIVE |

Conflict result: these two paths had no existing ACTIVE writer. core/dhea.py, core/dhea_diagnostics.py, and tests/test_dhea_product.py already have ACTIVE lfa-api ownership under existing tasks and are not duplicated. tests/test_dhea.py has no competing ACTIVE writer and remains outside NODE-01 until the independent entry/oracle is bound. This is preparation-node ownership only; implementation authorization remains NO until the policy artifact, fixture, executable entry/oracle and future implementation gate are all satisfied.
Three-node preparation sequence under the same existing task (no new TASK_ID or agent):

| node | deliverable | status | WRITE_OWNER | exact path status |
|---|---|---|---|---|
| NODE-01-QR-WINDOW-PREP | geometry-policy artifact preparation and binding | ACTIVE | lfa-api | concrete paths already registered at rows 495-496 |
| NODE-02-ASYMMETRIC-FIXTURE-BINDING | asymmetric non-quarter-turn synthetic fixture identity | PLANNED | lfa-api | path/digest not yet produced; no write permission |
| NODE-03-INDEPENDENT-ENTRY-ORACLE | independent geometry entry and executable oracle binding | PLANNED | lfa-api | path/digest not yet produced; no write permission |

Activation boundary: lfa-api is the sole active writer only for NODE-01's two registered paths. NODE-02 and NODE-03 are registered as pending preparation nodes without invented paths, hashes, or ownership claims; they activate only after their exact output paths and conflict-free ownership are truthfully identified by PM. Runtime, schema, gateway, device, Room, archive and implementation release remain unauthorized.

## R04 minimum single-QR direction implementation release

RUN-20260920-DHEA-MAINLINE-REPLAN-R01, original sole writer=lfa-api. Separate PM gate in MASTER_PLAN follows original Review R02, SHA256=8831cdce826260d16a07ae3000601275786fa55cfd97aeca57f3679d2e1e6efb, against exact TASK_BOARD SHA256=71a2e7ef6fe53b5164dc25e8ce2f561809241625d420addae2262af499c60140. This amendment supersedes the preparation-only restriction solely for the bounded minimum contract. Existing same-owner claims are consolidated, not assigned a second writer.

| path | TASK_ID | SUBTASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|
| core/dhea.py | RUN-20260920-DHEA-MAINLINE-REPLAN-R01 | R04-MINIMUM-DIRECTION | lfa-api | all roles | ACTIVE |
| core/geometry.py | RUN-20260920-DHEA-MAINLINE-REPLAN-R01 | R04-MINIMUM-DIRECTION | lfa-api | all roles | ACTIVE |
| core/dhea_diagnostics.py | RUN-20260920-DHEA-MAINLINE-REPLAN-R01 | R04-MINIMUM-DIRECTION | lfa-api | all roles | ACTIVE |
| tests/test_dhea.py | RUN-20260920-DHEA-MAINLINE-REPLAN-R01 | R04-MINIMUM-DIRECTION | lfa-api | all roles | RELEASED_FOR_TASK-QIUQIU-04 |
| tests/test_geometry.py | RUN-20260920-DHEA-MAINLINE-REPLAN-R01 | R04-MINIMUM-DIRECTION | lfa-api | all roles | ACTIVE |

Conflict determination: four paths already belong to lfa-api; tests/test_dhea.py had no competing ACTIVE writer in the recovered ledger. IMPLEMENTATION_AUTHORIZED=YES within these five paths only. No new agent or task, no other path promotion, and no deployment/device/gateway/schema/Room/archive permission. Preserve prior edits as an unaccepted incoming baseline; original owner supplies focused executable evidence and fresh independent implementation review. Existing broader historical acceptance is not inherited.

## Local detection clear corrective ownership receipt

RUN-20260920-DHEA-MAINLINE-REPLAN-R01 / LOCAL-DETECTION-DATA-CLEAR. Original sole writer=lfa-android. This records the PM implementation instruction already delivered after the original owner's read-only assessment; it is a late ledger entry, not a backdated authorization or implementation acceptance. Existing same-owner claims remain consolidated.

| path | WRITE_OWNER | status |
|---|---|---|
| Android_App/app/src/main/java/com/example/data/local/JournaledArtifactStore.kt | lfa-android | IMPLEMENTED_PENDING_REVIEW |
| Android_App/app/src/main/java/com/example/data/local/db/Daos.kt | lfa-android | IMPLEMENTED_PENDING_REVIEW |
| Android_App/app/src/main/java/com/example/ui/LfaViewModel.kt | lfa-android | IMPLEMENTED_PENDING_REVIEW |
| Android_App/app/src/main/java/com/example/ui/screens/SettingsScreen.kt | lfa-android | IMPLEMENTED_PENDING_REVIEW |
| Android_App/app/src/test/java/com/example/ExampleRobolectricTest.kt | lfa-android | IMPLEMENTED_PENDING_REVIEW |

Scope: local detection clearing only, preserving configuration, credentials and server data; no Room schema migration, uninstall, full-app clear or device action. Subsequent edits invalidate the submitted review digest. Original lfa-review is read-only; no second writer is assigned.
## QIUQIU DHEA QR product-identification end-to-end registration

| path | PLAN_ID | DELIVERABLE_ID | TASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|---|
| core/product_identity.py | PLAN-QIUQIU-01 | DELIVERABLE-QIUQIU-01 | TASK-QIUQIU-01 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| python_gateway/dhea_input.py | PLAN-QIUQIU-01 | DELIVERABLE-QIUQIU-01 | TASK-QIUQIU-01 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| docs/api/api-reference.md | PLAN-QIUQIU-01 | DELIVERABLE-QIUQIU-01 | TASK-QIUQIU-01 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| docs/api/schemas/dhea-product.schema.json | PLAN-QIUQIU-01 | DELIVERABLE-QIUQIU-01 | TASK-QIUQIU-01 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| fixtures/dhea-product/cases.json | PLAN-QIUQIU-01 | DELIVERABLE-QIUQIU-01 | TASK-QIUQIU-01 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| python_gateway/tests/test_dhea_product_contract.py | PLAN-QIUQIU-01 | DELIVERABLE-QIUQIU-01 | TASK-QIUQIU-01 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/main/java/com/example/camera/ProductGate.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/main/java/com/example/camera/PreviewGuidanceAnalyzer.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/main/java/com/example/camera/NativeCameraManager.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/main/java/com/example/ui/LfaViewModel.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/main/java/com/example/ui/screens/CaptureScreen.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/main/java/com/example/domain/model/Models.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/main/java/com/example/data/local/JournaledArtifactStore.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/main/java/com/example/network/DheaJson.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/test/java/com/example/camera/ProductGateTest.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/test/java/com/example/camera/PreviewGuidanceAnalyzerTest.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/test/java/com/example/network/DheaContractTest.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/test/java/com/example/network/ProductBundlePersistenceTest.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/app/src/test/java/com/example/network/ProductEndToEndTest.kt | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| Android_App/README.md | PLAN-QIUQIU-02 | DELIVERABLE-QIUQIU-02 | TASK-QIUQIU-02 | lfa-android | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| core/dhea.py | PLAN-QIUQIU-03 | DELIVERABLE-QIUQIU-03 | TASK-QIUQIU-03 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| core/dhea_diagnostics.py | PLAN-QIUQIU-03 | DELIVERABLE-QIUQIU-03 | TASK-QIUQIU-03 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| python_gateway/dhea.py | PLAN-QIUQIU-03 | DELIVERABLE-QIUQIU-03 | TASK-QIUQIU-03 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| python_gateway/app.py | PLAN-QIUQIU-03 | DELIVERABLE-QIUQIU-03 | TASK-QIUQIU-03 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| python_gateway/service.py | PLAN-QIUQIU-03 | DELIVERABLE-QIUQIU-03 | TASK-QIUQIU-03 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| python_gateway/tests/test_dhea_product_recheck.py | PLAN-QIUQIU-03 | DELIVERABLE-QIUQIU-03 | TASK-QIUQIU-03 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| python_gateway/tests/test_dhea_diagnostics.py | PLAN-QIUQIU-03 | DELIVERABLE-QIUQIU-03 | TASK-QIUQIU-03 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| tests/test_dhea_product.py | PLAN-QIUQIU-03 | DELIVERABLE-QIUQIU-03 | TASK-QIUQIU-03 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
| core/product_identity.py (NODE3 recheck portion; serialized after NODE1) | PLAN-QIUQIU-03 | DELIVERABLE-QIUQIU-03 | TASK-QIUQIU-03 | lfa-api | lfa-review; lfa-pm | FROZEN_CONTRACT_RELEASED |
NODE1 conflicts: `core/product_identity.py`, `python_gateway/dhea_input.py`, and `docs/api/api-reference.md` have prior same-owner ACTIVE QR-PC/QLI-CUTOVER/EXIF claims. Those claims remain historical/serialized; NODE1 is the sole successor writer after exact conflict disposition. NODE3 has exclusive sequential access to `core/product_identity.py` only after NODE1 PM gate. `python_gateway/dhea.py` is explicitly bound to NODE3. NODE2 depends on NODE1 contract freeze. No source dispatch is authorized by this ledger edit.

Disposition for the three named NODE1 overlaps: TASK-QIUQIU-01 is the sole current successor scope for lfa-api; prior QR-PC/QLI-CUTOVER/EXIF rows remain historical evidence, not concurrent write permission on these paths. NODE1 review bytes remain frozen until review disposition. NODE2 excludes API/Core and waits for NODE1 contract freeze; its exact paths above replace the former category rows. NODE3 excludes Android and waits for NODE1 exact-revision Review plus PM Gate and explicit file release. All other historical claims remain protected. Registration is not implementation dispatch or acceptance.

## QIUQIU-04 bounded implementation ownership (HEAD b307830089b51aca793ca693e375c217ec8e45ea)

Each `AUTHORIZED_ACTIVE` row below is a single-writer PM grant for the named task only; lfa-start must record a bounded START before implementation. Historical same-owner ACTIVE rows are serialized, not concurrent permission; lfa-test receives the four paths explicitly released from older lfa-api claims at lines 273-275, 374-376 and 518. Other frozen QIUQIU-01/02/03 records remain historical. `RESERVED_NOT_ACTIVE` is not write permission. No wildcard directory grant, old evidence overwrite or device action follows from this table.

| path | PLAN_ID | DELIVERABLE_ID | TASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|---|
| core/dhea.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| core/product_identity.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| core/dhea_diagnostics.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/dhea.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/app.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/service.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/dhea_input.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/dhea_export.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/workbench.html | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| docs/api/api-reference.md | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| docs/specs/API.md | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| docs/requirements/MVP.md | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| docs/LFA_最新完整文档集合/11_DHEA原生Android研究v2公开契约.md | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| docs/api/schemas/lfa-dual.schema.json | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| docs/api/openapi-lfa-dual.json | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/network/DheaClient.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/network/DheaJson.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/camera/ProductGate.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/domain/model/Models.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/data/local/JournaledArtifactStore.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/ui/LfaViewModel.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/ui/screens/CaptureScreen.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/ui/screens/QueueScreen.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/test/java/com/example/network/DheaContractTest.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/test/java/com/example/network/ProductBundlePersistenceTest.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/test/java/com/example/ui/ProductGateDisplayTest.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| tests/test_dhea.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| tests/test_dhea_product.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/tests/test_dhea_diagnostics.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/tests/test_dhea_product_recheck.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/tests/test_dhea_product_contract.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/tests/test_dhea.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |

| docs/LFA_最新完整文档集合/config/cor_template.v1.json | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | RESERVED_NOT_ACTIVE |
| artifacts/cor-dual-analyte-validation-20260923/ | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | RESERVED_NOT_ACTIVE |

Cor physical layout/matrix/direction/line-window measurements and two new physical-sample identities are absent from verified current evidence. The Cor numerical template cannot be promoted or written until those inputs exist. Fresh device artifacts have the single reserved destination above; this is not yet a device write grant. Historical `artifacts/cor-*` and original JPEGs are read-only.

Only the currently listed exact paths are granted; any newly discovered callsite must be registered by PM before editing. Historical `dhea-capture/2.0`, `2.1-product`, frozen `2.2-confirmed`, rejected `3.0`, original images and old evidence are outside this write scope.

## QIUQIU-04 current candidate-only ownership overlay / HEAD b307830089b51aca793ca693e375c217ec8e45ea

The following exact existing paths are registered for TASK-QIUQIU-04 as inactive candidates only. This current overlay is authoritative for current dispatch status; historical `AUTHORIZED_ACTIVE` rows above remain append-only history and do not grant current write permission. No implementation, integration, device execution, Review or PM acceptance follows from this registration.

| path | PLAN_ID | DELIVERABLE_ID | TASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|---|
| core/dhea.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| core/product_identity.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| python_gateway/dhea.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| python_gateway/dhea_input.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| docs/api/schemas/lfa-dual.schema.json | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| docs/api/openapi-lfa-dual.json | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| Android_App/app/src/main/java/com/example/network/DheaClient.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| Android_App/app/src/main/java/com/example/network/DheaJson.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| Android_App/app/src/main/java/com/example/camera/ProductGate.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| tests/test_dhea.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| tests/test_dhea_product.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| python_gateway/tests/test_dhea_diagnostics.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |
| python_gateway/tests/test_dhea_product_recheck.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | CANDIDATE_NOT_ACTIVE |

Candidate count is exactly 13 (lfa-api 6, lfa-android 3, lfa-test 4). Cor template/config and device evidence remain `RESERVED_NOT_ACTIVE`; iOS remains deferred with empty file scope.

## QIUQIU-04 current dispatch disposition / 2026-09-24

`TASK-QIUQIU-04` is `BLOCKED / NOT_DISPATCHED`. The 13 rows in the current candidate-only overlay remain inactive and confer no write authority. Historical `AUTHORIZED_ACTIVE` rows are not current permission. Cor configuration/source additions and the new-sample evidence destination require a later exact PM registration before any owner may write.

## QIUQIU-04 current authorized activation / 2026-09-24

This append supersedes only the dispatch status of the candidate overlay at lines 619-643. The user's `CODE_DOCUMENTATION_PLUS_EVIDENCE_EXPORT` selection and START delta activate exactly these paths. Historical rows remain unchanged; no wildcard permission follows.

| path | PLAN_ID | DELIVERABLE_ID | TASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|---|
| core/dhea.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| core/product_identity.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/dhea.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/dhea_input.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| docs/api/schemas/lfa-dual.schema.json | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| docs/api/openapi-lfa-dual.json | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-api | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/network/DheaClient.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/network/DheaJson.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| Android_App/app/src/main/java/com/example/camera/ProductGate.kt | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-android | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| tests/test_dhea.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| tests/test_dhea_product.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/tests/test_dhea_diagnostics.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| python_gateway/tests/test_dhea_product_recheck.py | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | AUTHORIZED_ACTIVE |
| artifacts/cor-bundle-1df42409-a789-47e4-9dc2-66bd270b603e/ | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-review; lfa-pm | AUTHORIZED_ACTIVE_EXPORT_ONLY |

`docs/LFA_最新完整文档集合/config/cor_template.v1.json` and `artifacts/cor-dual-analyte-validation-20260923/` remain `RESERVED_NOT_ACTIVE`. The device source is read-only: no new capture, install, clear or App-data mutation.

## QIUQIU-04 single Cor capture evidence activation / 2026-09-24

The existing `lfa-test` ownership of `artifacts/cor-bundle-1df42409-a789-47e4-9dc2-66bd270b603e/` is extended from export-only to `AUTHORIZED_ACTIVE_SINGLE_CAPTURE_TRACE` for the user's one App Cor capture/upload and API-layer trace. This changes no source owner. Device mutation is limited to the normal capture/upload; no install, clear-data, settings change or template/config write.

## 2026-09-24 TASK-QIUQIU-04 实施写入释放（append-only）

- Receipt: `TASK-QIUQIU-04-DELIVERY-20260924-01`
- `TASK_QIUQIU_04_ACTIVE_WRITE_CLAIMS = 0`
- `TASK_QIUQIU_04_WRITE_SCOPE = []`
- 原 `TASK-QIUQIU-04-START-DELTA-20260924-01` 的 13 条精确实现路径已完成实施并释放写入占用；后续仅允许独立 Reviewer 读取，任何整改或部署须新建明确授权与文件清单。
- `docs/LFA_最新完整文档集合/config/cor_template.v1.json` 始终未激活、未修改。

## 2026-09-24 TASK-QIUQIU-04 文档事实同步整改（append-only）

用户要求在修复 `DheaJson.kt` 编译错误后继续聚焦验证；验证中确认以下五份现行文档仍描述修复前的 Cor→DHEA 误路由状态。本次只同步已交付源码事实，不修改历史 wire、archive、设备、部署或 Cor 物理配置。

| path | PLAN_ID | DELIVERABLE_ID | TASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|---|
| docs/requirements/DHEA_MVP_完整需求.md | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-pm | lfa-review | RELEASED |
| docs/QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.7_IMPLEMENTATION_BASELINE.md | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-pm | lfa-review | RELEASED |
| docs/LFA_最新完整文档集合/02_LFA端到端处理流程_v1.4_DHEA_MVP.md | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-pm | lfa-review | RELEASED |
| docs/api/dhea-v2-app-integration.md | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-pm | lfa-review | RELEASED |
| docs/design/app-android-ios-detail.md | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-pm | lfa-review | RELEASED |

`docs/LFA_最新完整文档集合/config/cor_template.v1.json` 继续为 `RESERVED_NOT_ACTIVE`；本整改不声称 Cor 科学验收、新 APK 真机验收、部署、独立 Review 或 PM acceptance。

## 2026-09-24 TASK-QIUQIU-04 文档事实同步整改释放（append-only）

- 上述五份现行文档已完成 Cor 独立 successor identity、安全拒绝与历史 v2 wire 边界同步。
- `TASK_QIUQIU_04_DOCUMENT_REMEDIATION_ACTIVE_WRITE_CLAIMS = 0`
- `TASK_QIUQIU_04_DOCUMENT_REMEDIATION_WRITE_SCOPE = []`
- Cor 模板、archive、设备、部署、独立 Review 和 PM acceptance 未激活。
- 2026-09-24 状态同步（append-only）：上述五行已按本释放回执从 `AUTHORIZED_ACTIVE_REMEDIATION` 改为 `RELEASED`；此为账本一致性行政修正，不改变任何授权语义或历史回执。

## TASK-QIUQIU-04 post-install Cor device evidence activation / 2026-09-24

| path | PLAN_ID | DELIVERABLE_ID | TASK_ID | WRITE_OWNER | READERS | status |
|---|---|---|---|---|---|---|
| artifacts/cor-dual-analyte-validation-20260923/ | PLAN-QIUQIU-04 | DELIVERABLE-QIUQIU-04 | TASK-QIUQIU-04 | lfa-test | lfa-start; lfa-review; lfa-pm | AUTHORIZED_APPEND_ONLY_SINGLE_POSTINSTALL_COR_RUN_AFTER_START |

This activates only the previously reserved evidence destination at line 613 for the installed-APK Redmi K30 Pro run in PM_GATE `PM_QIUQIU_04_POST_INSTALL_COR_DEVICE_TRACE_AUTH_20260924`. Existing files and original JPEGs are immutable; add only new run artifacts with provenance and checksums after START delta. No business-code/config write is reopened; Cor template stays `RESERVED_NOT_ACTIVE`. Earlier evidence directory `artifacts/cor-bundle-1df42409-a789-47e4-9dc2-66bd270b603e/` is prior-run history, not this run's write target.


## TASK-QIUQIU-04 post-install Cor evidence scope consumed / 2026-09-24

RECEIPT_ID: `PM-QIUQIU-04-POSTINSTALL-COR-EVIDENCE-20260924-01`. The one-run `lfa-test` write authorization at line 706 is `CONSUMED / RELEASED` after the user-supplied lfa-test receipt. Evidence remains at `artifacts/cor-dual-analyte-validation-20260923/`; no further device action or evidence write is authorized by that row. Historical JPEGs and evidence remain unchanged; `cor_template.v1.json` remains `RESERVED_NOT_ACTIVE`.
