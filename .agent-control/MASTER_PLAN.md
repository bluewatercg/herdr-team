# MASTER_PLAN

PLAN_VERSION: 1.0
PLAN_STATUS: ACTIVE
CURRENT_MILESTONE: M1
CURRENT_DELIVERABLE: M1-D05
CURRENT_EXECUTION_BASELINE: FROZEN_ANDROID_BUNDLE_1_5_PUBLIC_RESEARCH_V2
NEXT_GATE: M1_EXIT_BASELINE_AND_REPAIR_BOUNDARIES_ACCEPTED
PROGRAM_PROGRESS: 1/6
PARKED_MILESTONES: M6,M7
LAST_RECONSTRUCTED: 2026-09-18

## Mission

在固定设备和受控拍摄条件下，用真实 Android 首代完整 JPEG、标准 API 和统一 Python Core，生成可追溯的 DHEA 研究结果，并在 App 与 Web 中展示同一次执行的完整证据。当前结果仅为 `MVP_RESEARCH_RESULT_ONLY`；`formal_reporting_allowed=false`。

## Authority and control

- 本文件唯一拥有项目的阶段、当前位置、阶段依赖、下一 Gate 和停放工作。
- `TASK_BOARD.md` 只拥有当前可执行任务；每个任务必须绑定一个 `PLAN_ID`（里程碑）和一个 `DELIVERABLE_ID`（交付物）。
- 具体字段、Wire、算法和 UI 行为仍由 AGENTS.md 指定的权威契约与规格拥有，本文件不重复定义。
- `EVIDENCE/` 和 `artifacts/` 证明做过什么；历史关闭报告不自动证明当前 revision 已验收。
- 状态只允许 `PARKED`、`NOT_STARTED`、`IN_PROGRESS`、`BLOCKED`、`EVIDENCE_READY`、`ACCEPTED`。
- M0-M5 是当前 Investor MVP 计划分母；M6-M7 停放，不计入当前进度，也不得阻断 M0-M5。

## Milestones

| ID | Milestone | Depends on | Status | Exit | Evidence now | Gap | Next action |
|---|---|---|---|---|---|---|---|
| M0 | 权威边界与执行纪律 | none | ACCEPTED | v2 当前基线、v3 停放边界、任务绑定规则全部明确 | AGENTS.md; DECISIONS.md; frozen v2 contract; this plan | none | Enforce PLAN_ID on every dispatch |
| M1 | 当前基线与缺口核验 | M0 | IN_PROGRESS | Android/API/Core/Web 审计、修复边界和当前证据清单经 PM 与 Review 接受 | Complete Android/API/PM/review reports | M1-D04 inventory and M1-D05 precise protected repair boundaries plus dual acceptance pending; HIGH repairs remain later work | Complete M1-D04/D05 and dual review before any M2 dispatch |
| M2 | Investor MVP 最小修复 | M1 | NOT_STARTED | 所有阻断真实闭环的 HIGH 缺陷修复并通过聚焦验证 | Known findings RBL-01/03, A-SEC-01, A-DIAG-01 | No authorized repair tasks yet | Start only after M1 exit |
| M3 | 当前 revision 真实端到端闭环 | M2 | NOT_STARTED | 指定设备的一次真实 capture 到 App/Web 结果全链 revision-bound | Historical v2 device/API/Core evidence | No current APK/runtime-bound run | Coordinate one controlled run after M2 |
| M4 | 科学证据与实验室桥接 | M3 | NOT_STARTED | ROI、重复拍摄、真实参考绑定或明确缺失、失败分析形成结论 | Historical captures; five unbound QA rows | Provenance and repeatability absent | Collect only real bound facts |
| M5 | Investor Demo Gate | M4 | NOT_STARTED | Demo A-D、限制说明、PM acceptance 和独立 review 完整 | Historical artifacts only | Current integrated demo package absent | Package accepted M3-M4 evidence |
| M6 | v3 Product Gate 迁移 | M5 | PARKED | Bundle 1.6/v3 API/App/Core/Diagnostics/Validation 和 legacy recovery 全部验收 | Contract 00-09 and preacceptance work exist | Ownership and legal cutover not authorized; implementation partial | Resume only by explicit milestone decision after M5 |
| M7 | 融资后产品化 | M5 | PARKED | 泛化、人因、法规、许可、生产监控由未来角色关闭 | Track B roadmap and open-gate register | POST_FUNDING_GATE | Keep non-blocking |

## Deliverables

| DELIVERABLE_ID | Deliverable | Depends on | Status | Exit / observable result | Evidence / source |
|---|---|---|---|---|---|
| M0-D01 | 冻结项目使命与当前执行基线 | none | ACCEPTED | DHEA controlled Investor MVP + frozen Bundle 1.5/public v2 明确 | AGENTS.md; v2 contract; DECISIONS.md |
| M0-D02 | 冻结权威来源与 v2/v3 冲突裁定 | M0-D01 | ACCEPTED | v3 被保护并停放，不能替换当前 v2 | DECISIONS.md PM scope ruling |
| M0-D03 | 建立唯一母计划与 PLAN_ID 规则 | M0-D02 | ACCEPTED | Master plan、task board、dashboard、PM/start 共同执行绑定 | this plan and control integration |
| M1-D01 | Android 当前基线审计 | M0 | EVIDENCE_READY | 原图/SHA、Bundle、上传恢复、结果 UI、构建和缺口可评审 | EVIDENCE/RUN-20260918T043217Z-AND-AUDIT.md |
| M1-D02 | API/Core/Web 当前基线审计 | M0 | EVIDENCE_READY | 持久化、统一请求、Core、ICC、诊断、实验室能力和缺口可评审 | EVIDENCE/RUN-20260918T043217Z-API-AUDIT.md; role-reported 30/11/5 isolated checks; no live acceptance |
| M1-D03 | 验收矩阵与独立基线评审 | M1-D01,M1-D02 | EVIDENCE_READY | A01-A16、HIGH findings、保护边界明确；不冒充实现验收 | PM-SCOPE and REVIEW-BASELINE reports |
| M1-D04 | 当前 revision 证据清单 | M1-D01,M1-D02 | IN_PROGRESS | source/dirty hashes、APK、runtime/profile、历史与当前证据分离 | PROJECT_SNAPSHOT; audit reports |
| M1-D05 | 最小修复任务图 | M1-D02,M1-D03,M1-D04 | IN_PROGRESS | 每项 HIGH finding 有 owner、hunk、依赖、Exit 和 review 输入 | RUN-20260918T043217Z-REPAIR-BOUNDARY assigned for preservation/spec only; M1-D04 and dual acceptance required for exit |
| M2-D01 | 移除 Android 源码内嵌凭据 | M1 | NOT_STARTED | 本地显式配置可用，源码/APK 不含凭据，现有设置保留 | A-SEC-01 |
| M2-D02 | 生成并持久化真实 ICC evidence | M1 | NOT_STARTED | ICC presence/disposition 在移除 tag 前记录；原字节/SHA 不变 | RBL-03; B-PM-04 |
| M2-D03 | 修复 Android ICC 未报告显示 | M2-D02 | NOT_STARTED | 缺失显示 UNKNOWN/NOT_REPORTED，显式值才显示 PASS/NO | A-DIAG-01 |
| M2-D04 | 实现真实 UnifiedAnalysisRequest 边界 | M1 | NOT_STARTED | Gateway identity/capture/JPEG/hash/frozen config 进入同一 DheaRuntime；错误绑定拒绝 | RBL-01; A05 |
| M2-D05 | 补齐实际 multipart 与 Web lookup 证明路径 | M2-D04 | NOT_STARTED | 真实 multipart 可观测；request_id=analysis_id 可定位同 execution artifacts | A04; A12 |
| M2-D06 | 修复集成评审与 Gate | M2-D01..M2-D05 | NOT_STARTED | 聚焦检查通过，PM_ACCEPTED 与 CODE_REVIEW_ACCEPTED，无 HIGH open | REVIEW_QUEUE |
| M3-D01 | 冻结本轮设备、APK、服务和配置身份 | M2 | NOT_STARTED | source/dirty hash、APK SHA、device、runtime/profile/dependency manifest 完整 | A16 |
| M3-D02 | 真机首代 JPEG 与 SHA 链 | M3-D01 | NOT_STARTED | camera/persisted/multipart/API/Core original bytes 与 SHA 相同 | A01-A04 |
| M3-D03 | API 到 Core 科学链 | M3-D02 | NOT_STARTED | ROI→256x24→Green→profile→T/C→4PL 或明确 null/refusal | A05-A10 |
| M3-D04 | App 结果与恢复 | M3-D03 | NOT_STARTED | 同 bundle/analysis 在 App 展示；GET-first 恢复不产生重复结果 | A03; A11 |
| M3-D05 | Web 同 execution 诊断 | M3-D03 | NOT_STARTED | 操作者从 request_id 找到正确 bundle、stages、artifacts 和 original | A12 |
| M3-D06 | revision-bound E2E manifest | M3-D02..M3-D05 | NOT_STARTED | 一份 manifest 绑定全部身份、hash、结果、失败和证据路径 | RBL-02 |
| M4-D01 | 自动/受控/人工 ROI 双轨证据 | M3 | NOT_STARTED | ROI source、corners、manual audit、同测量链可追溯 | IMVP-3; A06 |
| M4-D02 | 同卡同样本重复拍摄比较 | M3 | NOT_STARTED | 每次条件、T/C 或拒绝保留；不要求伪造实验室浓度 | A15 |
| M4-D03 | 真实实验室参考 provenance | M3 | BLOCKED | 真实 value/unit/method/time/card/sample/bundle 绑定；未知保持 null | A14; B-PM-05; needs real source facts |
| M4-D04 | 实验室桥接与失败分析 | M4-D01..M4-D03 | NOT_STARTED | 结论为 DEMONSTRATED、REJECTED 或 INCONCLUSIVE，含失败分层 | IMVP-5 |
| M5-D01 | Demo A：App→API→Core→App | M3 | NOT_STARTED | 可重复现场演示并保留 manifest | IMVP-6 |
| M5-D02 | Demo B：逐阶段科学证据 | M3 | NOT_STARTED | original→ROI→canonical→Green→T/C→4PL 可查看 | IMVP-6 |
| M5-D03 | Demo C/D：参考、重复、失败与边界 | M4 | NOT_STARTED | 真实可用信息与 null、失败、限制同时展示 | IMVP-6 |
| M5-D04 | 最终 Investor MVP 双验收 | M5-D01..M5-D03 | NOT_STARTED | PM_ACCEPTED + CODE_REVIEW_ACCEPTED；允许表述仅限受控技术可行性 | AGENTS.md allowed conclusion |
| M6-D01 | v3 所有权、基线和迁移决策 | M5 | PARKED | 明确 owner、protected diff、cutover/rollback 与授权 | v3 TODO; protected paths |
| M6-D02 | v3 Gateway/Core/Diagnostics/Validation | M6-D01 | PARKED | API-01..06, CORE-01..03, DIAG-01..02, WEB-01 accepted | v3 TODO |
| M6-D03 | Android Bundle 1.6/Product Gate/v3 client | M6-D01 | PARKED | APP-01..11 and APP-TEST-01..06 accepted | v3 TODO |
| M6-D04 | v3 integration and v2 recovery-only | M6-D02,M6-D03 | PARKED | INT-01..07 pass; historical v2 immutable and no Core rerun | v3 TODO |
| M7-D01 | 多设备、背景、角度和 Lot 泛化 | M5 | PARKED | independent validation evidence | POST_FUNDING_GATE |
| M7-D02 | Production YOLO 与数据治理 | M5 | PARKED | model/data/license validation | POST_FUNDING_GATE |
| M7-D03 | 人因、法规、临床与正式报告 | M5 | PARKED | future specialist approvals and evidence | POST_FUNDING_GATE |
| M7-D04 | 生产安全、监控和生命周期治理 | M5 | PARKED | operational controls and monitoring evidence | POST_FUNDING_GATE |

## Dispatch and update protocol

1. 每个正式任务必须包含 `PLAN_ID`、`DELIVERABLE_ID` 和 `TASK_ID`；前两者必须匹配，且交付物状态不能是 `PARKED`、`BLOCKED` 或 `ACCEPTED`。
2. `MAINLINE` 是正常开发主流程，`lfa-start` 按 `CURRENT_MILESTONE` 派单；主线跨阶段仍须 PM 更新本计划并在 `DECISIONS.md` 记录理由。`PARALLEL_WORKSTREAM` 是经影响分析注册的独立变更工作流；PM 可明确授权并派发不改变当前主线运行行为的隔离任务，无须改变 `CURRENT_MILESTONE`，也不绕过主线 Exit。
3. 变更先做影响分析，再选择 MAINLINE 或 PARALLEL_WORKSTREAM。每个 workstream 必须登记 `WORKSTREAM`、`MAINLINE_IMPACT`、`EXECUTION_STATUS`、`INTEGRATION_STATUS`、需求与来源、owner、依赖、精确读写文件隔离、Exit 和 Integration Gate。执行状态与集成状态独立记录；注册、依赖完成或任务完成均不等于执行授权或合并授权。未分类或隔离不成立时不得派发，先交 PM 裁定。
4. 任务完成只更新 `TASK_BOARD` 和证据；PM 与独立 Review 接受后，才可更新本计划为 `ACCEPTED`。
5. 每次里程碑状态变化必须同步 `CURRENT_MILESTONE`、`CURRENT_DELIVERABLE`、`NEXT_GATE`、`PROGRAM_PROGRESS` 和 Dashboard。
6. 不得删除历史失败、未知值或人工干预；不得用历史 Gate 自动替代当前 revision 证据。

| MAINLINE_IMPACT | 调度裁决 | 合并边界 |
|---|---|---|
| NONE | 依赖满足、精确 ownership 激活且 PM 明确授权后，可与主线并行执行 | 不改变主线运行行为；完成后仍须 Integration Gate |
| BOUNDED | 可在明确授权的隔离范围内开发，记录影响范围与隔离证据 | 不得合并；先重新评估影响并通过独立 Integration Gate |
| BLOCKING | 进入当前 MAINLINE，由 PM 登记当前交付物依赖与优先级 | 不得以并行分支绕开当前主线 Gate |
| FUTURE | 保持 PARKED | 不派发、不合并，重新分类并授权后才可启动 |

Integration Gate：提交精确 revision、依赖完成与 Exit 可执行证据、需求/协议/下游影响分析、目标主线基线及精确合并文件范围、适用回归检查和恢复方案；先由非作者独立 Review，再由 PM 明确授权合并。共享路径须先解决 ownership 冲突，不能靠并行写后合并。Gate 仅覆盖指定 revision/范围；变更后重新绑定和评审。通过前 `INTEGRATION_STATUS=NOT_AUTHORIZED`，即使 `EXECUTION_STATUS` 已完成或 workstream 已 ACCEPTED，也不自动改变主线里程碑、进度、Exit 或授权合并。本次仅建立规则，不授予任何执行或集成许可。

## Independent documentation governance control phase

User authorization: current PM instruction establishing an independent documentation-governance phase, with the first eight authorized governance items current and QR plan review/vertical slice only later gates. This control phase does not move CURRENT_MILESTONE M1 or CURRENT_DELIVERABLE M1-D05, change business progress, clear D05 UNMAPPED, or authorize source/business implementation.

PLAN_ID: GOV-DOC-01
DELIVERABLE_ID: GOV-DOC-01-D01
TASK_ID: RUN-20260918T043217Z-DOC-GOVERNANCE
STATUS: ACCEPTED
ACCEPTED_KEY: RUN-20260918T043217Z-DOC-GOVERNANCE:f348c1da5ea03d3076b867222a3e951b34bd6ee02c42dc270537b3d3eb6b8a2d
ACCEPTANCE_SCOPE: Reviewed GOV-DOC-01-D01 revision only; subsequent control-record edits change bound source hashes and do not assert current envelope freshness or grant business/QR implementation authorization.
SCOPE_CLASS: DOCUMENTATION_AND_CONTROL_ONLY

This is the explicit user-authorized control-plane exception to dispatch rule 2, not a business cross-milestone dispatch. Only exact ACTIVE paths in FILE_OWNERSHIP may be written. The user supplied the original ten numbered items in the follow-up authorization beginning “补充用户原始授权，逐项如下”. The eight current requirements below are newly assigned governance IDs for those explicit user instructions, not promoted finding/milestone IDs. REQUIREMENT_SOURCE_REFERENCES must cite this table and the numbered user authorization; business requirement sources remain unchanged. Execution owner is lfa-start(w15:p1); the current main session may coordinate but must not directly write execution-owned files.

Exit: all eight authorized governance items have authoritative source references and complete trace; document navigation/lifecycle and Review transitions are consistent; Dashboard and applicable executable/visual checks have evidence; workspace-scoped Memmy synchronization has verified IDs or an explicit unresolved failure, never a fabricated success; PM and independent Review explicitly accept this governance deliverable. Mapping alone is not acceptance.

GATE: governance acceptance precedes QR plan review; a separately reviewed and explicitly authorized QR plan precedes any vertical-slice implementation dispatch. Governance registration/acceptance alone grants no QR implementation permission. No QR development in this task. R1/RBL-04/HIGH/D04/M2 and M1 Exit remain unchanged.

### Governance authorization and trace source

| REQUIREMENT_ID | User item | Authorized result | Scope / evidence |
|---|---|---|---|
| GOV-REQ-01 | 1 | 建立文档分类与权威入口 | Registered root and domain entrypoints; linked authoritative sources |
| GOV-REQ-02 | 2 | 建立需求 ID 和文档章节索引 | Three domain INDEX.md files; source/section references, no fabricated IDs |
| GOV-REQ-03 | 3 | 定义文档生命周期与失效规则 | docs/DOCUMENT_LIFECYCLE.md |
| GOV-REQ-04 | 4 | 更新 AGENTS.md 开发方式和路由 | Root and three domain AGENTS.md paths |
| GOV-REQ-05 | 5 | 实现 Review 自动触发状态机 | review_dispatch.py, registered prompts/template; live shared queue remains start-owned |
| GOV-REQ-06 | 6 | 更新 Dashboard 文档健康和 Review 状态 | dashboard.py and existing registered control records |
| GOV-REQ-07 | 7 | 验证结构、兼容性、页面和哈希 | Executable focused checks, actual browser evidence and authorized digest verification; evidence in existing start meeting |
| GOV-REQ-08 | 8 | 同步 Memmy 项目记忆 | Project workspace only; verified facts, returned memory IDs/readback or explicit failure; no repository memory file |

All eight map to GOV-DOC-01-D01 Exit above and TASK_ID RUN-20260918T043217Z-DOC-GOVERNANCE. These control requirements do not resolve unrelated UNMAPPED business tasks. User item 9 (PM审核二维码计划更新) and item 10 (Gate通过后派发二维码最小垂直切片) are downstream gates only, not current implementation requirements or dispatch authorization. No QR plan/implementation write path is registered here. Governance automatic review must honor existing unique ownership, idempotent dispatch and explicit acceptance boundaries; it cannot self-approve or bypass these gates.

## Independent QR plan revision control phase

PLAN_ID: QR-PLAN-01
DELIVERABLE_ID: QR-PLAN-01-D01
TASK_ID: RUN-20260918T043217Z-QR-PLAN-REVISION
TASK_TYPE: QR_PLAN_REVISION
STATUS: NOT_STARTED
SCOPE_CLASS: DOCUMENTATION_AND_CONTROL_ONLY
EXECUTION_OWNER: lfa-start(w15:p1)
QR_IMPLEMENTATION: NOT_AUTHORIZED

This separately authorized plan-revision task is an exception to dispatch rule 2 only for the exact documentation paths registered in FILE_OWNERSHIP.md. It does not start M2 or M6, grant M1 Exit, change M1/M1-D05 or progress 1/6, clear D05 UNMAPPED, accept a QR plan, or authorize implementation, experimental-tool execution, failure investigation or new capture. GOV-DOC-01-D01 acceptance is unchanged. NOT_STARTED records registration, not an execution or acceptance claim. Start records the task in its existing TASK_BOARD ownership before execution; PM does not write that ledger here.

### QR revision authorization source

USER_AUTHORIZATION_QR_PLAN_REVISION_20260918 is the current user instruction: “修订 QR 计划并关闭 QR-PM-B01 至 B06 后重新提交 PM Gate”, with this PM action restricted to “仅执行控制面注册，不审核结果、不授权实现”. The same instruction explicitly requires B01 trace, B02 proposal status/ID collision, B03 protocol boundary and recovery, B04 acyclic dependencies, B05 stage-preserving nullability, and B06 executable dataset/threshold/denominator/INCONCLUSIVE/curve-condition acceptance. This paragraph is the persisted source of that authorization, not a claim that any blocker is closed.

All six requirements below derive from that user instruction, with the item 9 PM disposition at `ROUNDS/20260918T043217Z-meeting.md`, section `User item 9: QR PM plan review`, lines 339-350, as review context. Source package revision is bound by MANIFEST.sha256 digest `0416b38055f3482fdebd82c22937aeed4dfca1041d8210238c325102183eee64`. Package filenames below are relative to `docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/`; source sections refer to that reviewed revision. These stable requirement IDs identify user-requested plan outcomes, not findings, task IDs or milestone IDs. Revisions retain these IDs and record new source-section references without erasing the original mapping.

| REQUIREMENT_ID | Required plan outcome / Exit | Disposition context | Package source sections |
|---|---|---|---|
| QR-PLAN-REQ-01 | Establish requirement-to-source-section-to-deliverable-Exit-to-task-to-evidence trace; index the six plan requirements without clearing unrelated D05 UNMAPPED or authorizing QR business tasks | meeting item 9, line 344, B01 | README.md §权威边界; 04_TASK_BOARD_QR_TEMPLATE_ROI_SIGNAL_v1.0.md §派单纪律 |
| QR-PLAN-REQ-02 | Use proposal-only statuses consistently; remove self-authorization; resolve proposed ID collisions while retaining current M2-D06 identity and historical references; distinguish package proposals from live control authority | meeting item 9, line 345, B02 | README.md §文档状态/§权威边界; 01_QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.6.md §§0-1; 02_MASTER_PLAN_v1.1.md §Milestones/M2 and §Dispatch规则; 03_DECISIONS_QR_MVP_VERTICAL_SLICE_v1.0.md §Decision/§影响 |
| QR-PLAN-REQ-03 | Choose an explicit protocol boundary: unchanged-v2 offline study or bounded migration proposal; specify new submissions, historical lookup, queue identity, idempotency, recovery and rollback; enumerate exact downstream synchronization before any later coding authorization | meeting item 9, line 346, B03 | 01_QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.6.md §§0,12-13; 03_DECISIONS_QR_MVP_VERTICAL_SLICE_v1.0.md §裁决; 05_AUTHORITATIVE_CONTRACT_SYNC_CHECKLIST_v1.0.md §目标/§同步对象/§Exit |
| QR-PLAN-REQ-04 | Supply an acyclic dependency graph separating geometry establishment, candidate tooling, refinement design, independent validation, freeze and authoritative enablement; include contract/registry gates consistently in every task and sequence | meeting item 9, line 347, B04 | 01_QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.6.md §§6,8,15; 04_TASK_BOARD_QR_TEMPLATE_ROI_SIGNAL_v1.0.md §派单纪律/§禁止并行冲突; 06_TEMPLATE_ESTABLISHMENT_AND_VALIDATION_PLAN_v1.0.md §§5,7-8 |
| QR-PLAN-REQ-05 | Define stage-preserving nullability and refusal matrix for not-executed, failed and valid-but-not-quantifiable outputs; invalid C blocks T/C; downstream model failure preserves valid upstream measurements; no failure zero-fill | meeting item 9, line 348, B05 | 01_QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.6.md §§10-11,13; 05_AUTHORITATIVE_CONTRACT_SYNC_CHECKLIST_v1.0.md §三个必补失败码 |
| QR-PLAN-REQ-06 | Define executable dataset allocation and independent units, establishment/tuning/holdout separation, threshold provenance and freeze timing, pass/fail denominators and minimum useful outcomes, stopping and INCONCLUSIVE rules, nonblocking color diagnostics, and explicit DRY_5H/15_MIN curve-condition eligibility; missing real evidence remains missing | meeting item 9, line 349, B06 | 06_TEMPLATE_ESTABLISHMENT_AND_VALIDATION_PLAN_v1.0.md §§2,4,6-8; 08_TEN_POINT_CAPTURE_RELEASE_AND_EXECUTION_PLAN_v1.0.md §当前状态/§Release Gate/§四水平启动批/§完整10点/§颜色候选/§本轮主要终点; 07_HERDR_RECENT_THREE_FAILURES_INVESTIGATION_v1.0.md §状态/§结论标签 |

All six map exclusively to QR-PLAN-01-D01 and RUN-20260918T043217Z-QR-PLAN-REVISION. Start must reference this authorization section, the item 9 disposition and the named package sections in docs/requirements/INDEX.md and the meeting task specification. No QR-PM-Bxx finding is promoted to a Requirement ID.

Exit: submit a revised proposal satisfying all six rows with explicit closure evidence per requirement; recompute the package MANIFEST.sha256 for README and 01-08, verify every entry and bind the resubmission to its exact revision digest. Perform requirements sync check covering API/OpenAPI/schema/fixture/App/Gateway/Core/Web/acceptance, with exact paths, sections, differences and later synchronization gates. This task may document required downstream changes but may not edit unregistered downstream implementation/contracts or claim those changes already implemented. Independent Review must assess that exact revision before a separate PM Gate; changes after Review require renewed revision binding/review. Neither registration, manifest success, requirements sync check nor Review alone grants PM acceptance or implementation authorization. Item 10 remains NOT_AUTHORIZED pending a separate explicit implementation authorization after the plan gates.

## Independent QRP-G0 registration

PLAN_ID: QR-GEOMETRY-01
DELIVERABLE_ID: QR-GEOMETRY-01-G0
TASK_ID: RUN-20260918T075255Z-QRP-G0-AUTH
TASK_TYPE: READ_ONLY_PROTOCOL_BOUNDARY_REVIEW
REQUIREMENT_IDS: QR-G0-REQ-01, QR-G0-REQ-02, QR-G0-REQ-03, QR-G0-REQ-04, QR-G0-REQ-05, QR-G0-REQ-06
PROPOSAL_NODE: QRP-G0
DISPATCH_TRACK: PARALLEL_WORKSTREAM
WORKSTREAM: QR_GEOMETRY_RESEARCH
MAINLINE_IMPACT: NONE
EXECUTION_STATUS: NOT_AUTHORIZED_PENDING_GATE
INTEGRATION_STATUS: NOT_AUTHORIZED
DEPENDENCIES: accepted QR-PLAN-01-D01 digest below; separate G0 read-only execution Gate; synchronized requirement/task references; exact output ownership activation. No M1-M5 completion dependency for isolated G0 review.
FILE_ISOLATION: exact read targets in accepted package 05; only the two PLANNED evidence outputs below may become writable after authorization; no mainline source/runtime writes.
EXIT: all QR-G0-REQ-01..06 with executable documentary evidence, independent Review and separate PM Gate.
INTEGRATION_GATE: Dispatch and update protocol; no current merge or authoritative integration authorization.

Scheduling boundary for QR_GEOMETRY_RESEARCH: QRP-G0 -> G1 -> G2 -> G3 -> G4 -> G5 may progress beside MAINLINE M1-M5, without waiting for mainline milestone completion, but only after each node's own impact analysis, dependencies, explicit execution Gate and exact isolated ownership. This is parallelism between tracks, not permission to run dependent G nodes concurrently. Failure or INCONCLUSIVE does not satisfy dependencies. Only G0 is registered here; no later node is dispatched or authorized.

G0 is documentary boundary review; G1 establishes physical geometry; G2 freezes candidate geometry/thresholds before holdout. Only G3, after separate authorization and G2 acceptance, may develop/run the offline QR/homography candidate tool, with no refinement or measurement authority. G4 is independent geometry holdout; G5 reports/freezes candidate geometry evidence, not authoritative measurement. This classification does not authorize capture, experiments or tools now or expand G0 scope.

The accepted package 04 dependency graph remains: G5 -> R1 -> R2 -> R3 -> R4; G5 -> C1; R4 + C1 -> A1 -> A2. R refinement, C contract/migration and A authoritative enablement each require their own Gate and remain PARKED/unauthorized here. G0 cannot substitute for C1; G5 cannot substitute for R validation. Any App/API/Core authoritative integration must also pass the formal Integration Gate above with explicit target-mainline authorization; no G-stage completion, candidate freeze or R/C/A Gate alone grants merge permission. Current integration is NOT_AUTHORIZED.
STATUS: NOT_STARTED
REGISTRATION_DISPOSITION: REGISTERED_AND_BOUNDED_EXECUTION_AUTHORIZED
EXECUTION_OWNER: lfa-review(w11:p1)
EXECUTION_AUTHORIZATION: AUTHORIZED_READ_ONLY_DOCUMENTARY_G0
QR_IMPLEMENTATION_NOT_AUTHORIZED: true

### G0 authorization source and trace

Historical registration authorization was registration-only, with no execution or result review; bounded execution is now authorized by the later M1-D05 mapping and G0 execution authorization section. Source: QR-PLAN-01-D01 exact MANIFEST.sha256 digest `90c5b32869f6a9f04d914ec3acb2c535b638da0fc84d88eedfc64c467ecbe2d2`, `CODE_REVIEW_ACCEPTED_FOR_PM_GATE` plus `PM_ACCEPTED_FOR_IMPLEMENTATION_AUTHORIZATION`, recorded in meeting sections `QR-PLAN-01-D01 independent Review Gate` and `QR-PLAN-01-D01 PM Gate`. Those prior plan dispositions are not G0 acceptance. Package sources remain package 04 QRP-G0 and package 05 协议边界 / 下游盘点与差异.

The six G0 execution requirements below are sourced to the accepted package digest and sections above. QR-PLAN-REQ-03/04 remain historical QR-PLAN-01-D01 context only. All six IDs map exclusively to QR-GEOMETRY-01-G0 and RUN-20260918T075255Z-QRP-G0-AUTH. Trace: requirement table and source sections -> G0 Exit -> task -> two exact evidence outputs. START synchronizes INDEX, TASK_BOARD and meeting under its ownership before dispatch. Current permission comes from the later explicit execution authorization, not requirement mapping alone.

| REQUIREMENT_ID | G0 required result / Exit evidence | Accepted source |
|---|---|---|
| QR-G0-REQ-01 | v2/runtime unchanged: path/symbol evidence for Android Bundle 1.5/research-v2, POST/GET, queue identity, idempotency, GET-first, Gateway/Core/Web boundaries; checked revision/digests and limitations | package 05 协议边界 / 下游盘点与差异 |
| QR-G0-REQ-02 | Offline artifact contract: source JPEG path/SHA, identity, candidate QR quad, H, predicted window, manual comparison, status/reason, config SHA; measurement_authority=false and quantification_allowed=false; missing values explicit | package 04 QRP-G0; package 05 协议边界 |
| QR-G0-REQ-03 | Exact read/write isolation: enumerate package 05 read paths/symbols and checked digests; write only the two reserved outputs after ownership activation; demonstrate reviewed inputs unchanged | package 05 下游盘点与差异; this registration FILE_SCOPE |
| QR-G0-REQ-04 | Prohibited operations: preserve every prohibition in G0 bounded scope, record actual actions and any gap without repair, source mutation or runtime execution | package 04 QRP-G0; package 05 协议边界; this registration prohibitions |
| QR-G0-REQ-05 | Executable Exit evidence: after separate authorization, include reproducible read-only document/hash/field/isolation check commands or inline script in the report; checks JSON records commands, checked revision/input digests, per-requirement expected/observed results and pass/fail/not-evaluated reasons. Do not substitute narrative PASS or execute QR tools/runtime/API/device checks | package 04 QRP-G0; package 05 下游盘点与差异 / Exit; current user executable-evidence requirement |
| QR-G0-REQ-06 | G1 and integration boundary: record dependencies, unresolved conflicts and separate G1 authorization; independent Review then PM Gate; no automatic G1 dispatch or App/API/Core authoritative integration | package 04 QRP-G0 and dependency gates; this plan Integration Gate |

### G0 bounded scope and execution gate

The separate bounded read-only execution authorization is now granted; START must record and dispatch the task before execution. Read targets and symbols remain the exact downstream inventory in accepted package 05: frozen Android research-v2 contract; `DheaClient.submit/lookup/freeze/existing/metadata/persistResult`, `DheaJson.result/replay`, `JournaledArtifactStore`, `ReconciliationEngine`, `QueueRecordEntity`; `python_gateway/dhea.py` DheaStore/DheaService/create_dhea_app; `core/dhea.py` DheaRuntime.analyze/_analyze and `core/dhea_diagnostics.py`; `python_gateway/workbench.html` and `python_gateway/dhea_diagnostics.py`. Authorization does not claim the checks have run or runtime behavior is verified.

The complete future output FILE_SCOPE is exactly:

- `herdr-team/.agent-control/EVIDENCE/RUN-20260918T075255Z-QRP-G0-AUTH.md`
- `herdr-team/.agent-control/EVIDENCE/RUN-20260918T075255Z-QRP-G0-AUTH-checks.json`

Both exact output ownership rows are now ACTIVE for the registered G0 author. Read-only refers to reviewed contracts/source; only these two documentary outputs may be written. No directory or wildcard permission is granted.

Forbidden: modifying App/API/OpenAPI/schema/fixtures/Gateway/Core/Web/package; developing or executing QR/homography tools; capture, experiments or failure investigation; Bundle 1.6/v3 migration; authoritative ROI; changes to M1/M2/M6/M7. No source fixes, runtime execution, service/API calls or device actions are authorized by this documentary review scope. Conflict or missing evidence is reported, not repaired or fabricated.

### G0 Exit and later gates

Exit after separately authorized execution: report path/symbol-specific evidence for the current v2/runtime unchanged boundary, with checked revision/file digests and explicit limitations; document the minimal future offline artifact contract for source JPEG path/SHA, identity, candidate QR quad/H/predicted window/manual comparison, status/reason, config SHA, `measurement_authority=false` and `quantification_allowed=false`; list conflicts/gaps and QRP-G1 prerequisites. Contract freezing here is a documentary review conclusion only, not publication of a new wire/schema, actual artifact computation, scientific validation or runtime acceptance. Missing values remain explicit and are not fabricated.

Submit the report and checks JSON at an exact revision to independent Review, then separate PM Gate. A distinct reviewer must review the G0 author's outputs. Execution is now authorized, but result acceptance remains pending actual evidence; G0 acceptance never authorizes G1 or Integration.

Business stage remains M1/M1-D05, progress 1/6, M2 NOT_STARTED, M6/M7 PARKED. D05 authoritative mapping is established in the later section and awaits downstream synchronization/Exit assessment. No M1 Exit, M2 dispatch, QR implementation or result acceptance is granted. Package bytes and accepted digest remain unchanged; package revision requires renewed binding/review.

## Automatic dispatch control repair

PLAN_ID: AUTO-DISPATCH-01
DELIVERABLE_ID: AUTO-DISPATCH-01-D01
TASK_ID: RUN-20260918-AUTO-DISPATCH-FIX
REQUIREMENT_IDS: AUTO-DISPATCH-REQ-01
STATUS: REGISTERED_FOR_EXECUTION
EXECUTION_OWNER: lfa-start(w15:p1)
DISPATCH_TRACK: PARALLEL_WORKSTREAM
WORKSTREAM: CONTROL_AUTO_DISPATCH
MAINLINE_IMPACT: NONE
EXECUTION_STATUS: AUTHORIZED
INTEGRATION_STATUS: NOT_AUTHORIZED_PENDING_DUAL_GATE
DEPENDENCIES: current user explicit control-repair authorization; exact ACTIVE ownership below; lfa-start records task before implementation. No M1 Exit or QR G0 execution dependency.

AUTO-DISPATCH-REQ-01 source is the current user instruction: repair PM stopping after acceptance, reuse review_dispatch.py, notify lfa-start idempotently after review+PM dual ACCEPTED, keep watch resident on activate.sh/lfa-team.sh creation and recovery, update pm/start prompts and a brief README, allow SHA256SUMS updates. This is a new control-plane execution requirement, not a business Gate or a reuse of QR plan requirements.

Exact implementation FILE_SCOPE: `herdr-team/review_dispatch.py`, `herdr-team/activate.sh`, `herdr-team/lfa-team.sh`, `herdr-team/prompts/pm.md`, `herdr-team/prompts/start.md`, `herdr-team/README.md`, `herdr-team/SHA256SUMS.txt`. Reuse the existing state machine, queue persistence/locking, watch and notification mechanism; no second scheduler or business-code edits. SHA256SUMS changes only cover the six authorized implementation/documentation paths; preserve unrelated entries. Keep a focused runnable regression check in the existing authorized Python file if no existing authorized test path is available; temporary isolated checks may run outside the repository.

Behavior/Exit: fresh same-revision independent review and PM both ACCEPTED trigger a durable idempotent notification to lfa-start to reevaluate and execute the next eligible authorized action. Repeated watch/reconcile and restart must not redispatch an already acknowledged acceptance; failed notification must remain recoverable, not be recorded as success. One Gate, stale revision, rejected/blocked/conflicted state or missing evidence never triggers advancement. Eligibility requires authorization, satisfied dependencies and conflict-free exact ownership. Prompts require continuing immediately when these conditions hold; stop only for real BLOCKED/CONFLICTED, missing authorization, unmet dependency or ownership conflict, recording the specific reason. No eligible action does not manufacture one or lift a Gate.

Creation and recovery paths in both shell entrypoints must ensure one live watch for the intended project/session, without duplicate watchers or killing unrelated processes. Verify dual-Gate delivery, duplicate/restart behavior, unsuccessful-send recovery, single-Gate/stale/blocked refusal, and watch startup/recovery using executable isolated checks and actual control CLI/process smoke evidence. Preserve existing review behavior. Record commands, actual outcomes, revision/digests and limitations in the existing lfa-start meeting/task records; do not manufacture live business acceptance to test dispatch.

Integration Gate: exact repair revision and requirement/evidence references -> independent Review -> separate PM acceptance before accepting this control repair. Execution authorization permits these control-file edits and isolated verification now, but never self-approval or changing business Gate decisions. lfa-start registers the task and executes immediately on PM notification; no further proposal-only pause. Existing TASK_BOARD/REVIEW_QUEUE/role status remain under START ownership; the existing lfa-start meeting may record this task's specification, trace and checks without duplicating ACTIVE ownership. This section is the direct requirement source; no INDEX edit is required or authorized by this task.

M1/M1-D05, D05 UNMAPPED, progress 1/6, M2 NOT_STARTED, M6/M7 PARKED and all QR G0 metadata/PLANNED outputs remain unchanged. QR G0 execution and all business/authoritative integration remain unauthorized. Automatic continuation is notification and eligibility evaluation, not a grant of permission or a rewrite of historical Gate evidence.

## M1-D05 mapping and G0 execution authorization

Latest explicit user instruction authorizes PM to complete M1-D05 authoritative requirement mapping, source references, Exit assessment and evidence-bound dual Gate processing. It separately authorizes execution of registered RUN-20260918T075255Z-QRP-G0-AUTH with only the two existing G0 evidence outputs ACTIVE. This supersedes prior registration-only/no-execution wording for G0; historical restrictions retain their original chronology. Existing six QR-G0-REQ requirements, accepted package digest, read inventory, documentary Exit and all prohibited operations remain binding.

M1-D05 mapping must cite authoritative requirements rather than promote finding IDs into requirements. Mapping is not acceptance: assess M1-D02/D03/D04 dependencies, current exact evidence, preservation limits and every HIGH finding's owner/hunk/dependency/Exit/review input. Independent Review and separate PM acceptance bind the submitted revision; unresolved requirements or evidence retain explicit failed/not-evaluated status. No fabricated Gate or implied M1 Exit.

User prohibitions: no QR/homography tool execution, no App/API/Core/Web modification, no G1 start and no Integration Gate approval. After valid dual acceptance the existing dispatcher evaluates only already-authorized eligible actions with satisfied dependencies and unique exact ownership. Business implementation is not authorized by this instruction; M2 execution, M6/M7 activation and integration remain outside scope.

### M1-D05 authoritative requirement mapping

These new trace IDs label existing authoritative requirements and this explicit user-authorized documentary assessment; they do not promote finding IDs, invent product requirements or publish wire changes. Applies only to M1 / M1-D05 / RUN-20260918T043217Z-REPAIR-BOUNDARY. Frozen source below is `docs/LFA_最新完整文档集合/11_DHEA原生Android研究v2公开契约.md`; the compatibility API draft explicitly excludes this v2 scope.

| REQUIREMENT_ID | Authoritative source and required obligation | D05 Exit/evidence | Finding context, not requirement identity |
|---|---|---|---|
| M1-D05-REQ-01 | Frozen source §Android连接与恢复: explicit imported connection, no embedded address/credential, no secret logs; AGENTS.md integrity/credential boundary | Credential-safe repair owner, exact hunk, dependency and executable future Exit without credential disclosure or rotation; report §3/§7 | A-SEC-01 |
| M1-D05-REQ-02 | AGENTS.md §Component scope: UnifiedAnalysisRequest and common DheaRuntime; frozen source §结果信封与持久化字段 and routes/idempotency: immutable identity/hash, frozen runtime, final replay | Report §4/§9.2 independent accepted authority, exact lifecycle/refusal matrix, owners/hunks/dependencies and future negative checks; not public DTO migration | RBL-01 |
| M1-D05-REQ-03 | AGENTS.md §Component scope/Integrity rules: Core owns complete-JPEG decode and ICC evidence, immutable original, unknown not fabricated; frozen source §结果信封与持久化字段 structured diagnostics | Report §5/§9.4 producer/consumer ICC union, explicit unknowns, collector independence, schema placement and future checks | RBL-03; A-DIAG-01 |
| M1-D05-REQ-04 | AGENTS.md §Mission and business context/Delivery priority: Web lookup by request_id; frozen source §逐阶段工作台研究契约: same execution, subject isolation, credential separation, artifact SHA/length | Report §6/§9.5/§10 exact lookup and four server/client gates with authority, ordering and failure outcomes; proposed additions remain future repair specifications, not already-frozen wire fields | RBL-02 diagnostic branch |
| M1-D05-REQ-05 | AGENTS.md §Build, trace and verify/Integrity rules; latest user authorizes requirement mapping, Exit assessment and dual Gate, not implementation | Report/manifest/patch bind exact revision and protected hunks, every HIGH has owner/dependency/Exit/review input; preserve unknown chronology and independently review outputs | RBL-04; all repair boundaries |
| M1-D05-REQ-06 | AGENTS.md §Mission and business context/Laboratory and investor evidence: real capture, request, Core execution, original SHA and truthful limits | Identify current-vs-historical evidence and route missing APK/runtime/device proof to D04/M3; no invented proof or M1 Exit; report §7/§8 and current inventory | RBL-02 live-evidence branch |

Trace: authoritative source section -> these IDs -> M1-D05 Exit -> existing repair-boundary task -> exact report/manifest/patch and independent review -> PM Exit disposition. START synchronizes INDEX, TASK_BOARD, meeting and existing dashboard projection; PM does not edit those owner-controlled records. D05 requirement mapping is established here; synchronized dispatch/acceptance waits for those records to match. M1-D02/D03/D04 remain separately assessed dependencies; this mapping does not accept them or close implementation HIGH findings.

### M1-D04 documentary prerequisite mapping and assessment

M1-D04-REQ-01 derives from AGENTS.md §Build, trace and verify and §Laboratory and investor evidence: inventory exact source/dirty hashes, APK, runtime/profile identity and available evidence without fabricating missing facts. M1-D04-REQ-02 derives from AGENTS.md §Integrity rules and §Current definition of done: distinguish host/synthetic/source evidence from current real-device/API/Core proof, preserve failures and explicit unknowns. These IDs apply exclusively to existing M1-D04 / RUN-20260918T043217Z-START, not D05 or future runtime tasks. Meeting inventory row M1-D04 and original MASTER_PLAN D04 Exit operationalize this documentary requirement; they are not independent product authority.

PM documentary assessment uses PROJECT_SNAPSHOT source/revision and historical-evidence inventory, AND-AUDIT source fingerprints/APK/focused host checks, API-AUDIT fingerprints/host checks/readiness limits, meeting M1-D04 inventory row and D05 report §7/§8. Their explicit absence of current deployed-runtime/config/device binding is a correctly recorded inventory gap to collect in M3, not grounds to demand an unauthorized runtime run to complete this documentary inventory. Historical API/device counts must not be promoted to current evidence. Acceptance still needs an exact source/report manifest and independent Review plus PM; no current hardware or implementation acceptance follows. START may synchronize these two IDs and submit the existing documentary inventory, with missing evidence UNKNOWN, for that bounded review.

## Single-annotator development reference plan revision

PLAN_ID=QR-PLAN-03; DELIVERABLE_ID=QR-PLAN-03-D01; TASK_ID=RUN-20260918-QR-SINGLE-ANNOTATOR-REVISION. Current user confirms only one real research operator/annotator and authorizes minimal documentary synchronization, independent Review and separate PM Gate. EXECUTION_STATUS=AUTHORIZED_DOCUMENTARY_REVISION_ONLY; MAINLINE_IMPACT=NONE; IMPLEMENTATION_AUTHORIZED=false; INTEGRATION_AUTHORIZED=false. This section registers the requested development branch, not completion or research execution. Original G1 independent-validation Exit remains FALSE/NOT_MET; original G2 dependency remains unsatisfied. QR-PLAN-02 documentary acceptance and its exact frozen revision remain historical evidence, not implementation permission.

| REQUIREMENT_ID | Current user requirement / documentary Exit |
|---|---|
| QR-SINGLE-REQ-01 | Record one actual PROJECT_LEAD operator/annotator; preserve original G1 independent Exit=FALSE; same-person repeat work is never independent annotation. |
| QR-SINGLE-REQ-02 | Proposed G1-D uses 12 establishment physical cards and 72 immutable original JPEGs, PROJECT_LEAD physical measurements and one complete manual annotation pass; unknown actual identities, paths, hashes, measurements and timestamps remain null until real evidence exists. |
| QR-SINGLE-REQ-03 | Randomly reannotate 18 of the 72 distinct JPEGs after at least 48 hours, hiding first-pass results; retain random selection/order provenance, actual paired timestamps, first/repeat versions and visibility limitations. This is within-person repeatability only. |
| QR-SINGLE-REQ-04 | Differences exceeding 1% of target-window short side are recorded as SELF_CORRECTION, never independent adjudication; define the error denominator and corner correspondence before data, preserve both originals and correction audit, do not turn 1% into an invented algorithm pass rate. |
| QR-SINGLE-REQ-05 | All downstream development artifacts carry annotation_mode=SINGLE_ANNOTATOR_DEVELOPMENT_REFERENCE, independent_annotation=false, measurement_authority=false, quantification_allowed=false, formal_reporting_allowed=false. |
| QR-SINGLE-REQ-06 | Define G1-D -> G2-D -> G3-D only. G2-D freezes development candidate templates/protection boundaries only; G3-D is isolated offline QR/homography candidate tooling only, with no measurement/refinement authority or promotion of manual QR placement to fixed precise geometry. No transition to G4 independent validation, App/API/Core integration or authoritative ROI. |
| QR-SINGLE-REQ-07 | Synchronize authoritative plan, requirements, Gates and ownership through a separately bound supplement and explicit precedence/unchanged inventory. Preserve old G0/G1/M1 evidence, old package MANIFEST and accepted 09; no deletion or silent historical status rewrite. |
| QR-SINGLE-REQ-08 | Submit exact new documentary revision plus checks and stable PM authority sources to non-author Review, then separate PM disposition. This instruction does not authorize G2-D/G3-D code or automatically dispatch research/capture; actual future inputs and outputs require exact ownership and execution registration. |

New authoritative supplement candidate: docs/QiuQiu_DHEA_Project_Document_Update_Package_v1.6/10_SINGLE_ANNOTATOR_DEVELOPMENT_REFERENCE_PLAN_v1.0.md. Once separately accepted, it supplies only the single-annotator development branch exception to old package06/09 independent-reference prerequisites; those prerequisites remain binding for independent-validation claims. It does not replace the original G1/G4 validation route, remove G5-v2 -> C1 or R3 -> R4, or alter frozen v2/runtime. START must link this exact supplement in requirements INDEX and control TASK_BOARD/Gate records, enumerate affected old plan sections and their retained-versus-development-only applicability, and retain old digests. No rewrite of frozen old package bodies is needed or authorized for this minimal additive synchronization. G1-D has a distinct future development Exit, never a synonym for original G1 success.

## v1.7 documentary synchronization authorization

PLAN_ID=QR-PLAN-04; DELIVERABLE_ID=QR-PLAN-04-D01; TASK_ID=RUN-20260918-V17-BASELINE-SYNC. User authorized the five-item documentary synchronization proposal with “安排”. EXECUTION_STATUS=AUTHORIZED_DOCUMENTARY_REVISION_ONLY; IMPLEMENTATION_AUTHORIZED=false; INTEGRATION_AUTHORIZED=false; MAINLINE_IMPACT=NONE. Source is docs/QiuQiu_DHEA_Capture_Product_Gate_End_to_End_Spec_v1.7_IMPLEMENTATION_BASELINE.md, reconciled against root AGENTS, frozen research-v2 and accepted supplement10. Do not repeat G0 or reopen unrelated historical M1 acceptance.

| REQUIREMENT_ID | Authorized change and documentary Exit |
|---|---|
| QR-V17-REQ-01 | Preserve accepted supplement10 and separate G1-D -> G2-D -> G3-D branch: one real PROJECT_LEAD, 12 cards/72 original JPEGs, random18 with each pair at least48h and hidden first results, SELF_CORRECTION only above1%, five fixed development/no-authority markers; original independent G1 FALSE/NOT_MET. |
| QR-V17-REQ-02 | Map v1.7 G1/G2/G3E/G4/G5/G6 to prior09 and R/C/A responsibilities without equating completed Gates or dropping G5-v2 -> C1, R3 -> R4 and separate Integration Gate. Distinguish design timing from experiment execution and post-validation authorization; no automatic downstream dispatch. |
| QR-V17-REQ-03 | Bundle1.6/capture3.0/result3.0 and related changes are migration targets, not already adopted runtime contracts. Current frozen research-v2 remains authoritative until explicitly accepted migration. No live DTO/schema/API/source edits. |
| QR-V17-REQ-04 | Replace blanket all-null hard-refusal wording with stage/dependency-specific refusal: measurement prerequisite failure blocks dependent measurements; valid existing features survive concentration/model incompatibility; missing/invalid values remain null with reasons, never zero. Preserve stage evidence and formal_reporting_allowed=false. |
| QR-V17-REQ-05 | Synchronize v1.7, requirements/spec navigation and control Gates/ownership; preserve original v1.7 input digest and historical accepted artifacts/digests. Submit exact stable authority revisions, revised spec, changed indexes and checks for non-author semantic Review, then separate PM Gate. Acceptance at most PLAN_ACCEPTED_DOCUMENTARY_ONLY. |

This new revision intentionally changes MASTER_PLAN/FILE_OWNERSHIP after QR-PLAN-03 acceptance. Its prior exact authority bindings remain historical; the new full authority revisions require fresh non-author Review, not reuse of old acceptance. Supplement10 and its checks remain unchanged and accepted for their bounded branch. No research images, measurements, randomization, annotation, capture, QR/H tools, business code, production or ten-point collection are authorized. G1-D future execution still requires real input/output registration and separate authorization. START owns documentary execution and existing Gate records; PM owns only these two authority revisions and later disposition.

## G1-D output ownership revision

TASK_ID=RUN-20260918-G1D-OWNERSHIP; DELIVERABLE_ID=G1D-OWNERSHIP-D01. User explicitly authorized “下一步单独授权新增输出ownership并审阅”. AUTHORIZATION=OWNERSHIP_REGISTRATION_AND_REVIEW_ONLY; MAINLINE_IMPACT=NONE. Input is TASK_BOARD section G1-D real input preparation inventory, RUN-20260918-G1D-INPUT-PREP, including its eight exact proposed paths and actual missing evidence. PM revises only MASTER_PLAN and FILE_OWNERSHIP; START records submission/checks and actual dispositions only in its existing external TASK_BOARD.

G1D-OWN-REQ-01: Register exactly the eight proposed evidence outputs to sole agent writer lfa-start(w15:p1), with real physical measurement and annotation responsibility retained by PROJECT_LEAD. ACTIVE identifies exclusive ownership only; it grants no present permission to create or populate these eight outputs. Creation/writes require later bounded execution authorization and actual evidence. No directory-wide permission or duplicate ACTIVE writer.

G1D-OWN-REQ-02: Preserve preparation findings: 45 historical candidate paths/43 distinct SHA do not establish admitted G1-D images; real operator/card/slot provenance, physical measurements and first-round annotations/times remain missing. No invented membership, original-byte edits, captures, annotations, random selection, research tools, code or Integration are authorized here. Original G1=FALSE/NOT_MET; G1-D incomplete. Retain annotation_mode=SINGLE_ANNOTATOR_DEVELOPMENT_REFERENCE, independent_annotation=false, measurement_authority=false, quantification_allowed=false, formal_reporting_allowed=false. Current Bundle1.5/frozen research-v2 and downstream dependencies remain unchanged.

G1D-OWN-REQ-03: Submit these two complete new authority revisions with exact SHA256/bytes for non-author lfa-review semantic review, then separate PM disposition. QR-PLAN-04 acceptance retains its historical six-file binding; this authorization intentionally creates new revisions of only its two authority files, not retroactive coverage by the old Review. The v1.7 body, QR-PLAN-04 checks and two indexes remain frozen. Preserve prior SHA/bytes in external TASK_BOARD and do not rewrite historical checks. Reviewer/PM dispositions and BTW-CHECK belong only to the external ledger; freeze both authority files after submission. Acceptance at most OWNERSHIP_ACCEPTED_DOCUMENTARY_ONLY, never G1-D execution or completion.

## Formal QR product identification scope correction

PLAN_ID=QR-SCOPE-05; DELIVERABLE_ID=QR-SCOPE-05-D01; TASK_ID=RUN-20260918-QR-PRODUCT-DECOUPLING. Source: user formal 范围修正通知, not a discussion draft. Current instruction removes the erroneous geometry prerequisite for product identification immediately; documentary candidate revision/registration still requires non-author Review and separate PM Gate. CURRENT_MILESTONE and frozen Bundle1.5/research-v2 remain unchanged. MAINLINE_IMPACT=NONE; BUSINESS_EXECUTION_AUTHORIZED=false; INTEGRATION_AUTHORIZED=false. Sole present work is scope correction and task registration candidates.

QR-SCOPE-REQ-01: Search current plan/task/control and downstream references for direct and transitive geometry prerequisites on QR Decode, Protocol Parse, Product Family Match and Shutter Gate. Classify current dependencies for revision candidates; historical Evidence/old Review retained verbatim; unknown ownership report-only; no out-of-scope writes. MASTER_PLAN earlier G5->C1 and C1+R4->A1->A2 graph governs the old full geometry/authoritative integration scope only, never a prerequisite for the newly separated product-only tasks. Earlier G3/G3-D offline QR/H wording governs geometry tooling only, not preview/product decoding. Full v3 migration remains separately gated.

QR-SCOPE-REQ-02: QR_PRODUCT_IDENTIFICATION_DEPENDENCY=REMOVED for 72-image annotations, 48-hour relabel, G2/G3E, observation-window Homography and formal ROI thresholds. GEOMETRY_DATASET_STATUS=NOT_COMPLETED_OR_UNCHANGED; 48-hour relabel status=NOT_COMPLETED_OR_UNCHANGED. Geometry research including G1/G1-D, G2/G2-D, G3E/G3-D, ground truth, A/B/C, refinement, thresholds and G4/G5/G6 is DEFERRED_SEPARATE_RESEARCH_TRACK. Preserve existing tasks and incomplete evidence, original G1 FALSE/NOT_MET and all five single-annotator markers. C remains QR_HOMOGRAPHY_DIAGNOSTIC_ONLY with measurement_authority=false, quantification_allowed=false. No new research authorization follows.

QR-SCOPE-REQ-03: Register separate candidates ANDROID_QR_PRODUCT_IDENTIFICATION_MINIMAL_SLICE, QR_PRODUCT_DECLARATION_CONTRACT and FINAL_JPEG_QR_PRODUCT_RECHECK. Each needs distinct PLAN_ID/DELIVERABLE_ID/TASK_ID, candidate owner and WRITE_OWNER, exact proposed files/protected files, inputs/outputs/evidence paths, dependencies, Exit and independent review. Authorized business files are NONE. Inspect actual file paths before proposing; unknown existing ownership must remain UNKNOWN rather than invented. Sequence is a candidate for separate PM registration, never automatic dispatch. Shared contract semantics may be a true dependency, geometry is not.

QR-SCOPE-REQ-04: Preserve the full user product-only target: same DHEA page, background CameraX QR_CODE decode; split at first colon only; exact v1/QIUQIU/DHEA validation for 1:QIUQIU:DHEA; hash actual decoded UTF-8 bytes; shutter disabled before product match; bind capture_session_id/camera_session_id/capture_attempt_id/verification_record_id; invalidate on exit/capture completion/camera rebuild/other product/new attempt; distinguish unreadable, malformed, unsupported version and mismatch. No counterfeit claim from unreadability, URL opening, inferred LOT/Serial/concentration/card identity. Original complete JPEG/SHA/upload unchanged. Declaration candidates bind evidence and sessions with LOT/Serial null. Core final-JPEG candidate verifies product family/declaration only, without QR ROI, Homography, T/C or 4PL changes. True-card/device evidence is required for future Exit; fixtures cannot substitute for all real verification. Carry all 15 user Exit candidates without claiming their execution.

QR-SCOPE-REQ-05: START produces candidate and checks at exact registered paths, records original user notice and search inventory with path/line/classification/before-after mapping. Preserve protected digests and prior authority prefix bindings; sync current TASK_BOARD/BLOCKERS interpretation without rewriting historical events. Submit exact four-file revision to non-author lfa-review, report the user full BTW-CHECK field set, and await separate PM Gate. No automatic business, G2/G3E/G4/G5/G6, ROI, Homography, quantification, ten-point, complete-v3, LOT/Serial/anti-counterfeit, production/clinical/regulatory execution.

## Management issue recording control repair

PLAN_ID=GOV-MGMT-01; DELIVERABLE_ID=GOV-MGMT-01-D01; TASK_ID=RUN-20260918-MANAGEMENT-RECORDING; REQUIREMENT_IDS=MGMT-REQ-01..05. Source: current user explicit authorization to repair Herdr team management recording. PARALLEL_WORKSTREAM=CONTROL_PLANE_ONLY; STATUS=REGISTERED_FOR_EXECUTION; OWNER=lfa-start(w15:p1). CURRENT_MILESTONE unchanged. No QR task review/reopening, business implementation, geometry research or integration authorization.

MGMT-REQ-01: Reuse BLOCKERS.md for current issue status/responsibility/release conditions, ROUNDS/20260918T043217Z-meeting.md for append-only factual events/receipts and DECISIONS.md for confirmed workflow decisions. No second ledger/system. PM is accountable for end-of-task management assessment; existing unique writer START records PM-provided facts in START-owned ledgers, with attribution and acknowledgement, not inferred PM acceptance.

MGMT-REQ-02: Every task terminal outcome including blocked, rejected, cancelled and completed requires management summary, even explicit NONE_OBSERVED with assessment scope/evidence. Issues require unique issue_id, factual evidence references, impact, severity, root_cause_status, separately labelled hypotheses, containment, improvement_candidate, owner, status, recurrence_count, related_task_ids and release_conditions. Stable IDs are allocated through the single ledger writer after checking existing IDs; recurrence means a new evidenced occurrence, not repeated polling or duplicated receipts. Unknown causes stay UNKNOWN; confirmed causes cite evidence. Never fabricate retrospective counts or cause.

MGMT-REQ-03: Trigger recording on authorization/ownership ambiguity, missing or stale revision/evidence, review rework, dispatch/receipt failures, repeated blocking, process bypass or unexpected protected-file change; ordinary wait timeout alone is not proof of execution failure. Severity derives from evidenced impact; nonblocking improvements do not block or expand unrelated authorized work. Capture facts during execution and require PM end-of-task assessment before closure. Fix candidates are not execution grants.

MGMT-REQ-04: Synchronize pm.md, start.md and TASK_TEMPLATE.md with summary fields and references to this single policy. COMMON.md change is unnecessary unless a concrete contradiction is reported for separate scope registration. Preserve existing traceability, ownership and independent dual Gate. Use one actual observed management gap to exercise the recording/receipt workflow; any scenario simulation must be labelled, not claimed as historical incident.

MGMT-REQ-05: Execute focused documentary checks and a real PM-to-START recording receipt; bind exact reviewed revisions and protected digests. Historical Evidence and old review entries remain unchanged, prior ledger content append-only. Non-author lfa-review reviews implementation and evidence, then PM separately assesses the same revision. No self-review or premature repaired/CLOSED claim. External review/PM receipts may append after frozen submission with immutable prefix binding. SHA256SUMS changes only for authorized changed prompt/template entries already covered by manifest.

Exact execution FILE_SCOPE and unique WRITE_OWNER=lfa-start(w15:p1): herdr-team/prompts/pm.md; herdr-team/prompts/start.md; herdr-team/.agent-control/TASKS/TASK_TEMPLATE.md; herdr-team/.agent-control/BLOCKERS.md; herdr-team/.agent-control/ROUNDS/20260918T043217Z-meeting.md; herdr-team/.agent-control/DECISIONS.md; herdr-team/.agent-control/TASK_BOARD.md; herdr-team/SHA256SUMS.txt. PM separately owns authority registration in MASTER_PLAN.md and FILE_OWNERSHIP.md. Evidence/checks use the existing ROUNDS file; no new artifact file needed. REVIEW_QUEUE uses only its existing START-owned review lifecycle, not policy implementation.

Protected paths: all paths outside exact scope; specifically Android_App/, IOS_App/, core/, python_gateway/, tests/, fixtures/, docs/, all existing .agent-control/EVIDENCE/, QR geometry outputs including absent G1-D files, review_dispatch.py, dashboard.py, COMMON.md and historical ledger prefixes. Prior QR-SCOPE-05 authority revisions remain historical exact-prefix bindings, not accepted coverage of this new revision.

Exit: all five requirements traced; complete issue fields and trigger policy; prompts/template agree on PM accountability and START writer; actual issue plus PM assessment/START receipt recorded without speculative cause; focused checks pass, protected files/history preserved; exact revision non-author CODE_REVIEW_ACCEPTED followed by separate PM_ACCEPTED with no blocking findings. Only this control-plane repair may then close; no business or QR authorization follows.

## QIUQIU DHEA product identification authorized execution

Source: current user attachment titled QIUQIU DHEA QR PRODUCT IDENTIFICATION END-TO-END, all sixteen sections and numbered acceptance/check lists, retained by START in current ROUNDS. BUSINESS_EXECUTION_AUTHORIZED=true; AUTHORIZED_GOAL=QIUQIU_DHEA_QR_PRODUCT_IDENTIFICATION_END_TO_END; CURRENT_ACCOUNTABLE_ROLE=PROJECT_LEAD; APPROVAL_REQUIRED_FOR_INVESTOR_MVP=NO; FORMAL_REPORTING_ALLOWED=false. This prospective authorization supersedes earlier product-only no-execution clauses, not historical evidence or geometry restrictions. Existing Herdr team/stable names retained. PM owns these two authority files; START records and dispatches; lfa-review performs one non-author exact-revision Review then lfa-pm one engineering Gate per revision. No renewed user authorization for bounded fixes or dependency-satisfied continuation.

QR_PRODUCT_IDENTIFICATION_DEPENDENCY=REMOVED; GEOMETRY_DATASET_STATUS=NOT_COMPLETED_OR_UNCHANGED; 48_HOUR_RELABEL_STATUS=NOT_COMPLETED_OR_UNCHANGED; GEOMETRY_RESEARCH_TRACK_STATUS=DEFERRED_SEPARATE_RESEARCH_TRACK. No G1-G6/72/48/Homography/ROI/T-C/4PL/iOS/Java/full-v3/19th-stage implementation. Preserve all historical Evidence, original JPEG, stored requests, old reviews and ledger prefixes. No authenticity, LOT/Serial/single-card inference, medical, clinical or production claim. Existing scientific execution may continue only through the unchanged DheaRuntime path after product success.

Requirement source mapping: QR-PC-REQ-01..15 map one-to-one to section six contract items1..15; QR-PC-CHECKS maps its entire validation list and Exit. QR-ANDROID-REQ maps all section seven implementation/state/parser/shutter/evidence/lifecycle/behavior/JPEG requirements; QR-ANDROID-CHECKS maps every listed automation/runtime check and Exit. QR-FINAL-REQ maps all section eight input/order/recheck/results/failure/artifact requirements; QR-FINAL-CHECKS maps its complete automation list and Exit. QR-E2E-REQ maps sections nine/ten integration and section fifteen closure items1..15. Cross-cutting sections one-five and eleven-sixteen apply to every node, not optional samples.

Node1 QR_PRODUCT_DECLARATION_CONTRACT: PLAN_ID=QR-PC-01; DELIVERABLE_ID=QR-PC-01-D01; TASK_ID=RUN-20260918-QR-PC; REQUIREMENT_IDS=QR-PC-REQ-01..15,QR-PC-CHECKS; OWNER=WRITE_OWNER=lfa-api; STATUS=AUTHORIZED_ACTIVE. DEPENDENCIES=current explicit authorization and conflict-free exact FILE_SCOPE below, no geometry dependency. Scope: python_gateway/dhea_input.py; python_gateway/dhea_export.py; python_gateway/dhea.py; core/product_identity.py (new shared product-only parser/registry/declaration contract); docs/api/api-reference.md; docs/api/schemas/dhea-product.schema.json (new narrow schema); docs/api/openapi-dhea-v2.json; fixtures/dhea-product/cases.json (new); python_gateway/tests/test_dhea_product_contract.py (new); python_gateway/tests/test_dhea.py. Do not change historical v2 schema/v3 generator or fixtures opportunistically. Inspect consumers and prefer separate product-only revision preserving old v2 acceptance explicitly; maintain V3_ACCEPTANCE_NOT_IMPLEMENTED. No product request may silently bypass final recheck before Node3 exists: explicit unimplemented/disabled acceptance boundary required. EXIT=all section-six items/checks and contract/schema/reference/fixture/runtime consistency, compatible old callers, rollback, focused tests, exact revision SHA/bytes, actual non-author CODE_REVIEW_ACCEPTED and separate PM_ACCEPTED. Android producer migration occurs in Node2 against frozen contract, not fabricated Node1 completion.

Node2 ANDROID_QR_PRODUCT_IDENTIFICATION_MINIMAL_SLICE: PLAN_ID=QR-ANDROID-01; DELIVERABLE_ID=QR-ANDROID-01-D01; TASK_ID=RUN-20260918-QR-ANDROID; REQUIREMENT_IDS=QR-ANDROID-REQ,QR-ANDROID-CHECKS,QR-E2E-REQ; OWNER=WRITE_OWNER=lfa-android; STATUS=REGISTERED; DEPENDENCIES=Node1 same-revision dual Gate/frozen contract only. Exact scope: Android_App/app/src/main/java/com/example/camera/NativeCameraManager.kt; Android_App/app/src/main/java/com/example/camera/PreviewGuidanceAnalyzer.kt; Android_App/app/src/main/java/com/example/ui/screens/CaptureScreen.kt; Android_App/app/src/main/java/com/example/ui/LfaViewModel.kt; Android_App/app/src/main/java/com/example/domain/model/Models.kt; Android_App/app/src/main/java/com/example/data/local/JournaledArtifactStore.kt; Android_App/app/src/main/java/com/example/network/DheaClient.kt; Android_App/app/src/main/java/com/example/network/DheaJson.kt; Android_App/app/build.gradle.kts; Android_App/gradle/libs.versions.toml; Android_App/app/src/main/java/com/example/camera/ProductGate.kt (new); Android_App/app/src/test/java/com/example/camera/ProductGateTest.kt (new); Android_App/app/src/test/java/com/example/network/DheaContractTest.kt; Android_App/app/src/test/java/com/example/camera/PreviewGuidanceAnalyzerTest.kt; Android_App/README.md. EXIT=all section-seven behavior/checks, focused native checks and debug build, immutable byte/hash evidence, exact revision non-author Review and PM Gate. Device evidence tracked separately DEVICE_EVIDENCE_PENDING until real user observations; device wait never blocks Node3. No agent physical operator or invented device result.

Node3 FINAL_JPEG_QR_PRODUCT_RECHECK: PLAN_ID=QR-FINAL-01; DELIVERABLE_ID=QR-FINAL-01-D01; TASK_ID=RUN-20260918-QR-FINAL; REQUIREMENT_IDS=QR-FINAL-REQ,QR-FINAL-CHECKS,QR-E2E-REQ; OWNER=WRITE_OWNER=lfa-api; STATUS=REGISTERED; DEPENDENCIES=Node1 frozen dual Gate, not Android device/G1-G6. Exact scope: core/dhea.py; core/dhea_diagnostics.py; core/product_identity.py; python_gateway/dhea.py; python_gateway/dhea_input.py; python_gateway/tests/test_dhea_product_contract.py; python_gateway/tests/test_dhea_product_recheck.py (new); tests/test_dhea_product.py (new); python_gateway/tests/test_dhea_diagnostics.py; docs/api/api-reference.md. Shared Node1 files retain same unique lfa-api writer, only after Node1 freeze; semantic changes require fresh contract Review/PM before consumers depend on them. EXIT=every section-eight check, persisted original JPEG independent decode, registry/declaration/bindings, 18-stage product results and null refusal, same runtime, real API/Core smoke, exact non-author Review then PM Gate.

START records per-node exact source/authority/evidence SHA/bytes, checks/build/smoke/Review/PM/device status and limitations in current ROUNDS/TASK_BOARD/REVIEW_QUEUE/BLOCKERS. New node evidence may use exact EVIDENCE/QR-PC-01-D01.json, EVIDENCE/QR-ANDROID-01-D01.json, EVIDENCE/QR-FINAL-01-D01.json owned by corresponding implementer; prior evidence read-only. Every completed requirement receives full BTW-CHECK plus actual PM terminal management assessment and START receipt. Missing evidence stays pending, not zero or pass. Additional necessary paths require PM exact registration before writes, not new user approval.

Integration follows frozen contract, Android and final recheck, automated complete-JPEG upload/storage/Core/result/diagnostics/App roundtrip, then real designated Android observations from sections seven/ten. User physical operation is external; DEVICE_EVIDENCE_PENDING is not code blocker. Fixture QR use records PRODUCT_FAMILY_TEST_FIXTURE=true, PHYSICAL_DHEA_CARD_ID=null, AUTHENTICITY_CLAIM=false. Final CLOSED requires all fifteen section-fifteen conditions, including real device evidence, original/SHA chain, no product HIGH/CRITICAL, three exact dual Gates and no prohibited claims. Allowed task states follow section thirteen. Device implementation/acceptance labels from section seven are evidence qualifiers, not additional task-state enums. Only section-twelve real blockers pause affected branches; others continue. Future-role gaps remain POST_FUNDING_GATE/current_mvp_blocking=false.

Authorization receipt: START confirmed the full original sixteen-section attachment is stored in ROUNDS/20260918T043217Z-meeting.md:2682-3551, with provenance at 2678-2680; UTF-8 bytes=26273; SHA256=b2162749c781991cbdd3a2a44577bda3b0059606d30058563098353905f04f8c; exact byte match and historical prefix preserved. START confirmed Node1 formally dispatched to lfa-api and Android's live conflict check for the eleven registered paths returned NONE. This receipt establishes source availability and dispatch only; no implementation, Review or PM acceptance is implied. Node2 and Node3 remain REGISTERED until Node1 dual Gate.

Node1 engineering Gate: PM_ACCEPTED by existing lfa-pm for QR-PC-01 / QR-PC-01-D01 / RUN-20260918-QR-PC, Evidence SHA256=129730595d1bc42ef226df6a50a60e6e03793abb07a7a64e250e11dcc90491db, bytes=22762. Existing lfa-review CODE_REVIEW_ACCEPTED and QR-PC-R1 closure apply to this exact revision. PM independently verified Evidence and all ten implementation SHA/bytes bindings and executed nine Gateway checks: legacy runtime/replay/409, product refusal before persistence/Core, malformed declarations, and six complete-v3 rejection checks; 9/9 PASS. Earlier PM parser checks 4/4 PASS are historical, not a rerun of the amended tests; amended tests independently passed Reviewer 4/4. All fifteen requirement mappings and CHECKS/Exit remain covered by the exact-revision review. Broader scientific-fixture result remains 13/14, cause UNCONFIRMED; this Gate does not claim that failure resolved or pre-existing. No product contract blocker remains; real-device, Android implementation and final-JPEG recheck remain unaccepted.

Prospective activation after the above Gate: Node2 QR-ANDROID-01 and Node3 QR-FINAL-01 STATUS=AUTHORIZED_ACTIVE, within their exact registered scopes. START now formally dispatches both existing owners concurrently; no replacement agents. Frozen product declaration/schema/registry semantics are unchanged. Shared Node1 implementation paths needed by Node3 retain lfa-api as sole writer, with fresh review for changed revisions; Node1 Evidence remains frozen. Each node still requires author Build/Trace/Verify, existing lfa-review and existing lfa-pm exact-revision Gates. Geometry remains deferred and device evidence does not block reachable implementation. This activation supersedes earlier REGISTERED/pending-activation statements prospectively only.

Node3 engineering Gate: QR-FINAL-01 / QR-FINAL-01-D01 / RUN-20260918-QR-FINAL STATUS=PM_ACCEPTED by existing lfa-pm, binding only Evidence c99cfa6d411f3181fe0453f0b34c786bf4ce44287e6c795e66b964369ee3a538 / 15214 bytes. Existing non-author Review at REVIEW_QUEUE592 onward accepted this same revision and closed QR-FINAL-R1..R4. PM independently verified all eleven implementation SHA/bytes, both pre-Gate authority bindings and frozen Node1 Evidence, then ran seven focused checks in 20.691s: actual QR decoding/protocol/identity/hash refusal, persisted complete-JPEG real-runtime execution with continuous replay/409 observation, unreadable scientific-null refusal, source-hash 422 before persistence/Core, and invalid-original diagnostic refusal; 7/7 PASS. Bindings remained unchanged after checks. Reviewer fifteen-check PASS and temporary generator byte-parity are distinct Reviewer evidence. Twelve author BTW-CHECK mappings plus this exact Review and PM execution satisfy Node3 technical Exit. Original scientific 13/14 cause remains UNCONFIRMED; fixture proves neither real card nor device. Node2 and Android-origin end-to-end integration remain pending; no final goal closure. Geometry remains deferred and nondependent. This append records Gate disposition after verification; frozen submission authority digests remain historical and are not rewritten.
