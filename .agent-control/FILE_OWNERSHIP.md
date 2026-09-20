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
| herdr-team/dashboard.py | RUN-20260918T043217Z-DOC-GOVERNANCE | GOVERNANCE | lfa-start(w15:p1) | all roles | ACTIVE |
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
| python_gateway/tests/test_dhea_product_recheck.py | RUN-20260918-QR-FINAL | PRODUCT-IMPLEMENTATION | lfa-api | all roles | ACTIVE |
| tests/test_dhea_product.py | RUN-20260918-QR-FINAL | PRODUCT-IMPLEMENTATION | lfa-api | all roles | ACTIVE |
| python_gateway/tests/test_dhea_diagnostics.py | RUN-20260918-QR-FINAL | PRODUCT-IMPLEMENTATION | lfa-api | all roles | ACTIVE |
| herdr-team/.agent-control/EVIDENCE/QR-FINAL-01-D01.json | RUN-20260918-QR-FINAL | PRODUCT-IMPLEMENTATION | lfa-api | all roles | ACTIVE |

Node2/Node3 activate after Node1 dual Gate. Shared Node1 paths retain lfa-api exclusively and extend to Node3 only after freeze; do not duplicate ownership rows. Node2 owns all Android changes including declaration persistence/serialization migration. Required additional paths are registered by PM before edit within existing user authorization. Each owner preserves baseline hashes and reports unrelated changes rather than overwriting them.

Activation receipt: Node1 Evidence 129730595d1bc42ef226df6a50a60e6e03793abb07a7a64e250e11dcc90491db / 22762 bytes obtained existing lfa-review CODE_REVIEW_ACCEPTED and lfa-pm PM_ACCEPTED. Above twenty-two Node2/Node3 rows are now ACTIVE. Existing shared rows for python_gateway/dhea_input.py, python_gateway/dhea.py, core/product_identity.py, docs/api/api-reference.md and python_gateway/tests/test_dhea_product_contract.py also cover RUN-20260918-QR-FINAL under the same sole lfa-api writer; no duplicate row or concurrent writer. QR-PC-01-D01.json stays frozen. START performs formal concurrent dispatch; exact declared scope only.

Node2 pre-edit baseline disposition: existing unstaged LfaViewModel.kt (25621 bytes, SHA256 28b65ed04d5c0846e0a755439533b58aed879e4f184274740e3f1fd76b6515f6) and CaptureScreen.kt (23773 bytes, SHA256 258f4da400d78484fa65a8b366e178681bec69810de48cb52327b6cea4168621), both at their registered Android paths above, are protected adoptable baseline, not Node2-authored changes. Preserve the existing processing/unknown-receipt lookup and retry-after behavior, and the timed top saved-capture notice. No reset, restore, overwrite from HEAD or attribution to Node2. Node2 may incrementally integrate its product gate on these bytes once START confirms no other live writer; all other nonconflicting Node2 paths remain actionable now. Dirty working-tree state alone is not an ownership conflict. If either baseline changes before first edit, re-read and coordinate the actual writer.

QR-FINAL-R3 repair ownership extension: existing sole lfa-api rows for python_gateway/dhea_export.py, docs/api/openapi-dhea-v2.json and python_gateway/tests/test_dhea.py also cover RUN-20260918-QR-FINAL as ACTIVE. Scope is only synchronization of enabled product-only final-JPEG acceptance and migration of the obsolete Node1 disabled-path expectation; preserve legacy v2, complete-v3 refusal, unrelated baseline work and frozen Node1 Evidence. No duplicate writer or new task. Bind the revised files in new Node3 Evidence and obtain existing non-author Review then same-revision PM Gate.
