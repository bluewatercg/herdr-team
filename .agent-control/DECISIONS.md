# DECISIONS

## PM-ONBOARD / 20260918T043217Z

- Activation RUN_ID is 20260918T043217Z. The activation explicitly embeds ROUNDS/20260918T042918382640886Z.md as its brief source. Record SOURCE_BRIEF_RUN_ID=20260918T042918382640886Z; these are distinct identifiers, not evidence that the runs are identical. The source .panes file is empty; current role status and live Herdr inventory establish current role locations instead.
- Current scope is the user-authorized Android → standard API → Core → DHEA research result → App → Web Investor MVP audit. iOS implementation, production generalization and YOLO remain POST_FUNDING_GATE.
- Controlled capture conditions may be used only with explicit observed evidence. No assumptions that current images have stable edges, lighting, angle, crop or background.
- Do not adopt the uncommitted v3 contract as a completed cutover. Current Android emits v2; Gateway explicitly refuses v3 acceptance. This discrepancy requires scope/contract reconciliation before PM_GATE=READY.
- Historical CLOSED reports remain historical claims. No current project task is CLOSED without PM and independent code-review acceptance plus revision-bound evidence.

## lfa-start reconciliation / 20260918T043217Z

- Snapshot PM-ONBOARD-20260918T043217Z-410b17a0 and live Git HEAD both equal 410b17a00b63374f5d28a5531c478db8b30e8427. Activation RUN_ID matches; SOURCE_BRIEF_RUN_ID is distinct and its association is documented. Identity/HEAD prerequisites pass; Gate remains CONFLICTED, not READY.
- Pre-dispatch coordination only: request existing v3 authorization, owner, affected-file boundaries and source evidence from lfa-api/lfa-android and reconcile with lfa-pm. These requests do not create TASK_IDs, authorize implementation, or pause/overwrite existing independent work.
- Proposed round scope pending PM reconciliation: validate the user-authorized Android Investor MVP using the frozen accepted wire contract; do not presume uncommitted v3 is unauthorized, accepted, superseded or complete. If existing authorization requires v3, PM must record that evidence and the migration scope before dispatch.
- Resolve B-PM-03 by recording exact public identity fields and the internal Core request contract against the authoritative frozen schema. Do not silently substitute analysis_id/bundle identity for request_id or waive UnifiedAnalysisRequest acceptance.
- B-PM-02, B-PM-04 and B-PM-05 are outstanding delivery/evidence items. Ask PM to distinguish blockers of safe task assignment from completion criteria so the READY prerequisite does not require the implementation work it prevents assigning. No acceptance is waived and lfa-start does not change PM_GATE.
- Formal independent review must receive a TASK_ID, affected paths, immutable diff baseline plus pre-existing dirty-work boundary, and actual test/runtime evidence paths. PM_ACCEPTED and CODE_REVIEW_ACCEPTED remain absent.

## PM gate correction / PM-ONBOARD 10–12

- Accept lfa-start's distinction: READY is safe-to-dispatch, not delivery-complete. B-PM-02/04/05 become delivery/evidence work after dispatch is safe; none is waived or marked resolved.
- Uncommitted v3 files do not establish unauthorized work. Authorization, implementation and acceptance are separate facts. Await the already-requested API/Android ownership evidence without overwriting their work.
- B-PM-03 public mapping is specified, not guessed: frozen 11号契约 lines 33–37 and 66 define bundle lookup/idempotency and public analysis_id; line 169 explicitly defines diagnostic request_id=analysis_id. Future compatibility draft is a separate contract under api-reference.md line 9.
- UnifiedAnalysisRequest remains an explicit requested acceptance item. Its absence cannot be silently waived by the public alias. Define its internal integration/verification boundary once the authoritative round wire scope is reconciled; do not mutate frozen public metadata to resolve an internal requirement.
- Keep CONFLICTED pending B-PM-01 scope/ownership evidence and an explicit B-PM-03 internal acceptance boundary. No new implementation TASK_ID or progress approval is issued here.

## PM scope ruling / 20260918T043217Z

- Evidence: Android role's read-only coordination report received for this RUN_ID confirms Bundle 1.5/public v2, no Android v3 worktree changes, v3 authorization=unknown and owner=unknown. Its source inspection and historical test-command references are role-reported evidence, not PM-executed tests or authorization evidence.
- This round uses the already-frozen research v2 contract (11号公开契约); Bundle 1.6/v3 remains a separate migration scope, neither adopted nor rejected as unauthorized. Preserve all pre-existing v3 work.
- Protected existing-work boundary: the four tracked files in the onboarding audit, plus v3 API/spec/generator/schema/fixture files, python_gateway/dhea_v3_schema.py and v3 tests. Before any task touches an overlapping file, record its exact pre-existing diff and coordinate ownership of the intended hunk; until then that overlap is task-blocked. No blanket permission to overwrite or revert those files.
- B-PM-01 safe-dispatch disposition: resolved for this round by frozen v2 scope and explicit exclusion/protection of v3 work. Unknown v3 authorship remains an open migration fact, not a blocker for disjoint v2 work.
- B-PM-03 disposition: public identities follow frozen v2 exactly; diagnostic request_id=analysis_id is expressly permitted by that contract. UnifiedAnalysisRequest remains a required internal integration and verification deliverable, owned by API-to-Core responsibility at later assignment. Preserve DheaRuntime.analyze and original bytes/hash; do not add draft fields to public v2 or waive the internal requirement. Any overlapping source edit requires the preceding boundary check.
- PM_GATE=READY means safe bounded assignment only. B-PM-02/04/05 and the internal B-PM-03 deliverable remain open. PM_ACCEPTED, CODE_REVIEW_ACCEPTED and end-to-end completion are not granted. lfa-start may now assign scoped tasks with immutable baseline and pre-existing-diff boundaries.

## Master plan reconstruction / 2026-09-18

- `herdr-team/.agent-control/MASTER_PLAN.md` is the sole authority for project milestones, current position, dependencies, next Gate and parked work. Specifications still own detailed behavior; evidence still owns proof.
- Current execution path is M0-M5 under frozen Android Bundle 1.5/public research v2. Current milestone is M1 baseline verification. Existing v3 work is preserved under M6 and is `PARKED`, not rejected, deleted, accepted or authorized for current dispatch.
- M6 may start only after M5 acceptance or a new explicit user-authorized milestone decision that records impact, cutover and rollback. M7 remains `POST_FUNDING_GATE` and cannot block M0-M5.
- Every formal task must carry exactly one active `PLAN_ID`, one matching `DELIVERABLE_ID` and one `TASK_ID`. `lfa-start` may not dispatch tasks without the full binding. `lfa-pm` may not accept work that is not traceable to its deliverable Exit.
- Non-blocking discoveries are assigned to a future deliverable or parked; they do not expand the current task. A milestone change requires updating MASTER_PLAN, DECISIONS, TASK_BOARD and Dashboard together.

## GOV-MGMT-01 authorized recording workflow

依据用户明确授权及MASTER_PLAN339-357，复用BLOCKERS保存issue当前责任、状态和解除条件，当前ROUNDS保存事实和回执，DECISIONS保存已确认流程决定。PM负责管理评估，START是八文件唯一writer；任务状态仍在TASK_BOARD。完整规则位于prompts/start.md的“管理问题记录规则”，PM提示与TASK_TEMPLATE引用它。这个已授权流程决定不等于修复验收；MGMT-20260918-001保持OPEN，等待精确revision的非作者Review及单独PM Gate。历史前缀和旧Evidence/Review不变，不扩大QR或业务权限。

## REMEDIATION-CONTRACT-FIRST-R01

Source: explicit user decision registered by PM at MASTER_PLAN.md:845-853. Proposed remediation implementation_allowed=false until lfa-pm approves the exact event, acceptance and projection contracts plus actual repository path mapping. Original owners complete versioned contracts and same-revision API/state conflict dispositions; START consolidates exact artifacts and observed schema/fixture validation; original independent Review assesses; PM approves or requires revision for that exact scope. Author completion, coordinator registration, Review, prior Shadow approval or narrative validation do not grant implementation permission.

Package must contain revision, exact paths/SHA256/bytes, requirement-to-event-to-acceptance-to-projection semantics, existing versus explicitly proposed paths, per-file FILE_SCOPE/sole WRITE_OWNER without wildcard or concurrent claims, exact schema/fixture paths and reproducible commands/results bound to submitted bytes. Changed bytes require renewed revision binding and applicable review. Unresolved conflicts or missing evidence retain implementation_allowed=false. This note grants no source/schema/runtime write scope. lfa-ios remains DEFERRED, FILE_SCOPE=[], no assigned writer or edit dispatch. Existing API plan revision, docs completion and separately bounded Android clarity implementation continue.

## Mainline preparation resumption / PM988-998

Confirmed user direction and MASTER_PLAN.md:988-998: remove the duplicate final-JPEG QR payload/product gate in the intended cutover while retaining authenticated server pre-capture product/configuration binding. QR geometry may assist Window localization; it must not reintroduce payload readability as identity acceptance. Runtime is unchanged and implementation_allowed=false; bypassing identity before server binding exists is not authorized.

Original API supplies stable R03 identities and independent EXIF/Window exact source/check scope; original Android supplies same-revision consumer/persistence dispositions; original Review evaluates contract/science and proposed checks separately from future runtime acceptance. Room and archive completion are not prerequisites for Core preparation. START returns concrete PM options with recommendations and keeps the existing task IDs/owners. No new agents or iOS work. Docs may correct only its two owned drafts; archive movement remains NOT_RELEASED_FOR_MOVE. MASTER_PLAN remains PM-owned.

## Exact pre-capture policies / PM1000-1012

LATE_COMMIT_POLICY=A; CONTROLLED_MVP_LOCAL_FREEZE_TRUST=ACCEPTED_FOR_CONTRACT. Complete JPEG and recoverable local freeze must precede the conservative deadline in the original process/clock scope. Shutter CAS alone is insufficient. R02 agreement permitting JPEG completion after deadline is not inherited and requires explicit revised owner disposition. Recovery preserves original bytes/binding/time facts and clock scope; no recreated shutter authority, invented OS-boot proof or hardware attestation.

REVOKE_CUTOFF_POLICY=A: accepted server commit preserves identical-binding measure/replay eligibility after confirmation revocation; revocation blocks new commits/bindings. Every request still checks authentication, authorization and exact binding/idempotency. Local freeze or unacknowledged send is not proof of server acceptance. Define ordering and lost-response recovery in the contract.

TTL_MS=30000 remains PROPOSED_NOT_FROZEN / NOT_EMPIRICALLY_VERIFIED. API reports actual source, assumptions and expiry/retake cost without new device work. Duplicate final-JPEG payload gate removal with server binding retained is settled. Technical fields/CAS/scientific residuals and same-revision dispositions remain required; runtime implementation_allowed=false. Independent EXIF/Window preparation/review continues without Room/archive/TTL completion.

## QIUQIU-04 shared measurement chain / 2026-09-24

Bound to PLAN-QIUQIU-04 / DELIVERABLE-QIUQIU-04 / TASK-QIUQIU-04, requirement QIUQIU-04-SHARED-CHAIN-01 and HEAD b307830089b51aca793ca693e375c217ec8e45ea. The user has ruled that DHEA and Cor have one capture/observation-window/quality/Green/Profile/T-C measurement chain; QR segment three distinguishes identity only. Preserve separate product_id/analyte_id and provenance without inventing a second science algorithm. `COR_PHYSICAL_CONFIGURATION_UNAVAILABLE` is the present safe refusal, not an inherent Cor measurement rule. Unknown geometry/template/sample evidence cannot be invented; T/C stays null when scientific evaluation fails. MASTER_PLAN.md#qiuqiu-04-shared-chain-requirement-revision--2026-09-24 supersedes the conflicting Exit rationale prospectively, retaining the earlier control record as history. Existing START/authorization was tied to its old Exit: revised implementation needs PM delta authorization and START delta dispatch by exact owner; neither is granted here. No integration, device execution, independent review, PM acceptance or iOS implementation is authorized by this decision.

## 2026-09-24 TASK-QIUQIU-04 实施交付边界决定（append-only）

1. 记录 `TASK-QIUQIU-04-DELIVERY-20260924-01` 为 `DELIVERED_PENDING_INDEPENDENT_REVIEW`，不等于 Review 通过或 PM acceptance。
2. DHEA 与 Cor 是两个产品/分析物；共享拍摄和科学处理框架不允许把 Cor 当作 DHEA alias，也不允许在缺少 Cor 物理配置时复用 DHEA 模板。
3. 产品身份由 App 预览门禁生成并绑定到原始 JPEG；Gateway 校验声明后路由；Core 不得从最终 JPEG 重扫 QR 决定产品。
4. 真实设备旧 APK 的 `INVALID_PRODUCT_GATE_DECLARATION` 必须保留为版本不一致证据；本地 successor smoke 不能冒充设备成功上传。
5. 新 APK 安装、真机重验、集成部署、独立 Review 与 PM acceptance 均需后续明确授权。

## PM-LEDGER-REQ-01 实施：控制账本唯一 writer / 2026-09-24（append-only）

Supersedes the writer assignment in the GOV-MGMT-01 section above（“START是八文件唯一writer”）。GOV-MGMT-01 的记录流程本身（issue 字段、recurrence_count、release_conditions、历史不改写）继续有效，只改 writer 身份。

- **WRITER**：`lfa-pm` 是控制账本的唯一 writer —— `MASTER_PLAN.md`、`TASK_BOARD.md`、`BLOCKERS.md`、`REVIEW_QUEUE.md`、`DECISIONS.md`、`FILE_OWNERSHIP.md`、`PM_GATE`、`PROJECT_SNAPSHOT.md`、`PM_REQUIREMENT_INTAKE.md` 及同族控制记录。实质授权来源是已登记的 `PM-LEDGER-REQ-01`（`MASTER_PLAN.md` PM control-ledger governance registration 节；`TASK_BOARD.md` 行 PM-GOV-01）。
- **`lfa-start`** 是执行与回执角色：核对绑定与 Gate、执行正式派单、回收事实与证据、向 PM 返回可归因回执。不写控制账本。
- **被关闭的缺口**：`PM-LEDGER-REQ-01` 登记时带 `IMPLEMENTATION_AUTHORIZED: false`，从未应用到 `prompts/*.md`，而 prompt 是运行时行为的唯一来源。结果 PM 在账本里宣布自己是唯一 writer，自己的 prompt 却禁止它写。这个矛盾就是实际观察到的派单堵塞的成因。
- **已实施于**：`prompts/pm.md`（新增「控制账本唯一 writer」节；四处反向断言改为正向）与 `prompts/start.md`（新增「控制账本写入边界」节；删除截断重复的 sole-writer 段；修正其余 START 写账本表述）。
- **保留的边界**：证据不得由作者自写；账本 append-only 并带 `previous_submission_sha256` 链；账本规则/Gate/状态语义的实质变更仍需非作者 Review 与单独 PM Gate。
- **PROVENANCE**：本次实施由外部助手在用户明确指示（“开始动”）下执行，**不是** `lfa-pm` 或 `lfa-start` 所为。在此记录以免隐藏该干预。改动哈希与变更记录见 `.agent-control/CHANGE_RECORD_2026-09-24.md`。
- **SCOPE_CLASS**: CONTROL_PLANE_ONLY。**MAINLINE_IMPACT**: NONE。未改变任何业务代码、里程碑、交付物、QR、geometry 或 Integration 状态。
