# PROJECT_SNAPSHOT

SNAPSHOT_ID: PM-QIUQIU-04-b3078300
RUN_ID: 20260918T043217Z
GENERATED_BY: lfa-pm
REPOSITORY_ROOT: /mnt/d/Project/Aventura/java_developer/AIPoweredHealthManager-lfa-reader
GIT_BRANCH: main
GIT_HEAD: b307830089b51aca793ca693e375c217ec8e45ea
WORKTREE_STATUS: DIRTY; pre-existing tracked/untracked work preserved; not accepted as a clean implementation baseline
SCOPE_VERSION: QIUQIU-04-DUAL-ANALYTE-BOUNDED-IMPLEMENTATION
CONTRACT_VERSION: frozen historical Android Bundle 1.5 / research v2 unchanged; distinct dual-reagent successor wire is an authorized implementation deliverable, not already accepted
SNAPSHOT_STATUS: IMPLEMENTATION_AUTHORIZED_PENDING_START; integration/device/review/PM acceptance ungranted
TASK_ID: TASK-QIUQIU-04; BUSINESS_REQUIREMENT_TRACE=QIUQIU_DHEA_COR_DUAL_ANALYTE_DELIVERY

## Current revision binding

Previous `PM-ONBOARD-20260918T043217Z-f952b0ac` is STALE for any new dispatch or acceptance. Its documentary decisions remain historical, tied only to `f952b0ac6942f8b5794c9a8ef0fcaae617e70d45`. The committed delta to the current HEAD is limited to `docs/technical/YOLO_OBSERVATION_WINDOW_API.md`, `research/validation_capture.html`, `research/validation_capture.py`, and `research/validation_report.html`; dirty working-tree changes remain unreviewed. All below pre-existing onboarding observations and approval descriptions refer to their recorded historical revisions, not a current implementation or device acceptance. Current Cor distinct-analyte behavior, geometry and new-sample evidence remain unverified.

The current user's DHEA/Cor dual-reagent instruction supersedes historical Cor-as-DHEA-family claims. On this HEAD PM_GATE grants only exact-path, sole-owner implementation after lfa-start START plus a verified decision event; see FILE_OWNERSHIP.md:579-610. Cor physical card layout/config and two new sample IDs are not evidenced, so numerical Cor template creation, integration/deployment, fresh device execution and scientific acceptance remain ungranted. The online Redmi K30 Pro and `artifacts/cor-dual-analyte-validation-20260923/` are designated candidates only; preserve every original JPEG and historical record. Historical documentary sections below are revision-scoped observations, not current dispatch or acceptance.
## Historical onboarding observations (STALE for current dispatch)

The activation explicitly supplies the earlier brief as source material. Its identifier remains distinct from this activation; no same-run equivalence is assumed. The source panes file is empty. Current AGENT_STATUS and live Herdr inventory identify lfa-pm w12:p1, lfa-start w15:p1, lfa-android w14:p1, lfa-api w13:p1, lfa-review w11:p1 and lfa-ios w16:p1.

CONTROLLED_CAPTURE_INVESTOR_MVP, DHEA only. Real Android capture → standard API → Core → research result → App → Web diagnostics is the goal. iOS implementation and production gates remain outside this round. Fixed capture profiles are permitted only with observed supporting evidence; present photo geometry/light/background stability is not presumed.

## Git and existing work

Latest five commits: 410b17a0 Android controlled capture/Gate closeout; f43f8668 gateway development-token policy; 3876f00b minimum_control_area/debug configuration; 88cb09fe camera guidance/focus; 944b50e8 nominal field/JPEG checks. Exact hashes and working-tree paths are in EVIDENCE/PM-ONBOARD-20260918T043217Z.json.

Pre-existing tracked edits: docs/DHEA_NATIVE_APPS_API_RECOGNITION_TODO_2026-09-15.md, docs/api/api-reference.md, python_gateway/dhea.py and dhea_input.py. Untracked work includes IOS_App, v3 specifications/schemas/fixtures/tests and dhea_v3_schema.py. Preserve all existing work. No business source was edited during this audit.

Root README.md does not exist. Read Android_App/README.md, CONTEXT.md, the authoritative requirements index and Android closeout report; repository AGENTS.md was provided in full context. Older component descriptions calling the gateway planned and iOS absent are stale relative to the directory inventory. Existence does not establish acceptance.

## Components and verification entry points

| Component | Observed implementation | Build/test entry | Evidence status |
|---|---|---|---|
| Android_App | CameraX complete JPEG buffer copied without encoding; Journal/SHA; local Bundle 1.5; v2 multipart; bound server result panel; Preview/JPEG transform and nine-point round trip | Windows SDK/Gradle 9.3.1 via WSL, :app:assembleDebug; app/src/test camera, network and result-panel tests; instrumented/device acceptance separately | IMPLEMENTED_PENDING_EVIDENCE for this revision; no build/device check executed by PM |
| python_gateway | FastAPI DheaService, immutable blobs, persisted response, v2 POST/GET/validation/diagnostics/workbench; direct common runtime.analyze on stored original | python_gateway/pyproject.toml; python -m python_gateway.dhea; python_gateway/tests/test_dhea.py, test_dhea_diagnostics.py, test_dhea_v3_api.py and contract tests | IMPLEMENTED_PENDING_EVIDENCE; no current health check or API run by PM |
| core | DheaRuntime.analyze; JPEG/hash guards; EXIF transpose; ROI; 256×24 warp; Green profile, T/C and guarded research inverse; explicit null/refusal | root pyproject.toml, uv run python -m unittest discover -s tests -v; focused test_dhea.py | IMPLEMENTED_PENDING_EVIDENCE; numerical tests not rerun during read-only onboarding |
| IOS_App | Untracked Swift capture/client/store and Xcode project exist | Xcode project and build-and-install.sh require macOS/device/signing; no iOS tests identified in top-level inventory | DISCOVERED; deferred, no build executed or acceptance implied |

## Claims versus evidence

Historical docs/ANDROID_GATE_CLOSEOUT_2026-09-16.md claims CLOSED and P0=0. Four underlying evidence JSON files were read, parsed and hashed: capture distance confirmation, AND-02 device acceptance, API-03 diagnostics and CORE-02 JPEG decoding. They record real-device capture cohorts, 29/29 diagnostic retrieval and 490/490 artifact hashes. These are historical recorded outcomes, not freshly executed PM tests. Their top-level records contain no Git HEAD/commit binding. Artifact-by-artifact reproduction and installed APK/deployed-runtime revision matching remain unverified.

Android README has older 26/29 API-03 wording while later closeout/evidence record 29/29. Do not convert that stale documentation into a current failure or silently discard historical failures. The 80 mm failed capture remains excluded from the recorded 85–90 mm controlled profile.

Original JPEG: camera reads ImageProxy JPEG buffer directly; DheaService uses immutable storage and Core expected hash. Recompression is not present in the inspected extraction path. This is source evidence, not proof for every device record.

ICC: Core removes the in-memory ICC tag without colour conversion before decoded diagnostics. The inspected decoded metrics omit ICC presence/disposition. Original stored-byte preservation and explicit ICC evidence are separate acceptance checks; the latter is unresolved.

Preview/JPEG mapping: CoordinateTransform forward/reverse and nine-point max error guard are implemented. Historical evidence reports overlay acceptance and round-trip results. No present-device overlay/round-trip run was performed.

Core output: warp is 256×24; Green extraction, T/C and inverse paths are present. Direction uses two topology hypotheses with refusal if ambiguous. This remains RESEARCH_CANDIDATE and NOT_IMPLEMENTATION_BASELINE. Current correctness on a real bound laboratory cohort is not established by source inspection.

## Task and review state

Only the explicitly authorized PM-ONBOARD is recorded for this activation. TASKS contains a template, not an assigned implementation task. Initial TASK_BOARD and REVIEW_QUEUE were empty. Android/iOS/review preflight notifications are observations, not tests or approval. No PM_ACCEPTED or CODE_REVIEW_ACCEPTED exists for this round. No task is CLOSED by this snapshot.

## Interface conflicts and unknowns

1. Android emits local Bundle 1.5 / capture 2.0. Uncommitted v3 docs require 1.6 / 3.0 and prohibit new v2 acceptance. Current gateway explicitly refuses v3 with V3_ACCEPTANCE_NOT_IMPLEMENTED. Scope and migration ownership require reconciliation before READY.
2. No UnifiedAnalysisRequest symbol was found in core/ or python_gateway/. Current common DheaRuntime takes bytes/hash/diagnostics. Diagnostics request_id equals analysis_id; public routes identify bundle. Resolve exact requested acceptance against the frozen public schema, rather than silently renaming identity fields.
3. Present APK, deployed runtime and full App/Web/laboratory/repeatability evidence are not revision-bound in the inspected summaries.
4. Laboratory identity, method, timestamp and physical-card binding remain unknown for this round. Missing data must remain null.

## PM review

TASK_ID: PM-ONBOARD
PM_REVIEW_STATUS: PM_BLOCKED
GIT_HEAD_REVIEWED: 410b17a00b63374f5d28a5531c478db8b30e8427 plus recorded dirty working tree
REQUIREMENTS_REVIEWED: activation acceptance, supplied AGENTS.md, current requirement index, v2 integration contract, v3 contract index and historical Android closeout
ACCEPTANCE_CRITERIA_RESULTS: onboarding fact inventory complete; actual end-to-end acceptance not established
IMPLEMENTATION_EVIDENCE: source paths and historical JSON inventory described above
MISSING_EVIDENCE: current revision/APK/runtime-bound live loop, ICC disposition, full laboratory binding and scientific repeatability
UNAPPROVED_SCOPE_CHANGE: not established; uncommitted status proves neither lack of authorization nor completed cutover. Existing v3 authorization and ownership evidence is pending role coordination.
CROSS_PLATFORM_INCONSISTENCY: Android v2 versus v3 target; iOS deferred, not an acceptance blocker
REQUIRED_CHANGES: deliver B-PM-02/04/05 and internal B-PM-03 through scoped tasks; protect pre-existing v3 edits. Safe-dispatch scope is frozen Bundle 1.5/public v2. READY does not mean end-to-end acceptance.

## Next coordination

Notify lfa-start of CONFLICTED gate and distinct activation/source-brief association. No formal meeting, implementation task or approval is issued by PM. Existing independent work must not be overwritten or paused by this snapshot.

Future gates: production YOLO/device/background generalization, iOS implementation, clinical/regulatory evidence. owner_role=FUTURE_ROLE_REQUIRED; approval_status=NOT_AVAILABLE_AT_CURRENT_STAGE; gate_class=POST_FUNDING_GATE; current_mvp_blocking=false. Specialist roles and required evidence are recorded in BLOCKERS.md.

## BTW-CHECK trace

| TODO_ID | Goal and evidence | Build/Test result | Limit |
|---|---|---|---|
| PM-ONBOARD 01 | git rev-parse confirmed root | command succeeded | no behavior change |
| PM-ONBOARD 02 | branch/HEAD/status/log captured in audit JSON | read-only commands succeeded | dirty tree retained |
| PM-ONBOARD 03 | project descriptions and rules read | inspection complete | root README absent |
| PM-ONBOARD 04 | all control ledgers and source brief read | inspection complete | initial ledgers were templates |
| PM-ONBOARD 05 | role states and four historical evidence JSON files inspected | JSON parse/hash succeeded | no current revision proof |
| PM-ONBOARD 06 | Android/API/Core/iOS source and build/test entry inventory | inspection complete | no build/test execution claimed |
| PM-ONBOARD 07 | source/contract/claim discrepancies recorded | reconciliation audit complete | findings remain DISCOVERED |
| PM-ONBOARD 08 | snapshot and PM_GATE | machine consistency check recorded in audit evidence after write | CONFLICTED is not approval |
| PM-ONBOARD 09 | blockers/decisions persisted; direct lfa-start notification | delivery receipt recorded separately | submission does not imply acceptance |

Files changed are confined to herdr-team/.agent-control PM records and evidence. Current MVP blocker remaining: evidence and contract findings above; production gates do not block current reachable work.

## Gate reconciliation / PM-ONBOARD 10–12

READY means the repository facts, authoritative round contract, existing-work ownership and safe task boundaries are explicit. It does not require that the work awaiting assignment already be implemented or verified. No end-to-end criterion is waived.

Frozen v2 contract evidence: docs/LFA_最新完整文档集合/11_DHEA原生Android研究v2公开契约.md lines 33–37 defines lookup/idempotency by capture_bundle_id, line 66 defines public analysis_id, and line 169 explicitly fixes diagnostic request_id=analysis_id. This alias is an explicit contract rule, not an inferred substitution. The current requested UnifiedAnalysisRequest requirement remains distinct and unresolved; do not waive it or add fields to frozen public v2. docs/api/api-reference.md line 9 excludes research v2 from its future compatibility-gateway contract.

At this reconciliation read, API and Android role files still contained STARTED without authorization/ownership evidence. lfa-start has requested that evidence directly. B-PM-01 remains a coordination dependency. PM_GATE remains CONFLICTED until authoritative scope and existing-work boundaries are explicit. B-PM-03 public identity mapping is documented; internal request acceptance must be assigned or resolved within the selected scope.

## Authoritative disposition after role evidence

The Android role reports no Android v3 changes, Bundle 1.5/public v2 still implemented, and v3 authorization/owner unknown after its read-only searches. These are received observations, not fresh PM tests. Existing v3 source/test/docs and recorded historical command results establish work exists, not authorization or cutover completion.

Current round contract: frozen 11号公开契约, Android Bundle 1.5/public v2. Separate v3 migration remains protected and excluded from default adoption. Unknown ownership prevents uncoordinated overlapping edits only; task assignment must bind an immutable baseline, preserve the existing diff and coordinate hunk ownership before overlap.

CURRENT_DISPATCH_STATUS: READY
CURRENT_ACCEPTANCE_STATUS: NOT_ACCEPTED
B-PM-01 dispatch scope is resolved. B-PM-03 public identities follow the frozen mapping; its required internal UnifiedAnalysisRequest integration remains delivery work. B-PM-02/04/05 remain delivery/evidence work. Earlier CONFLICTED and PM_BLOCKED observations describe the onboarding state before this ruling.

API role evidence subsequently received confirms the same unknown v3 authorization/owner and enumerates its protected paths. Existing core/contracts.py AnalysisRequest is not evidence that UnifiedAnalysisRequest or its required semantics is implemented. The future compatibility draft at api-reference.md 360–368 is not silently imported into research v2. B-PM-03 acceptance must explicitly map required internal request identity, capture identity, immutable JPEG/hash and applicable frozen configuration through the common runtime; preserve separation from public analysis_id ownership. No type alias, renaming-only change or untested equivalence satisfies this item. Keep it open for scoped implementation and independent review.

## Current candidate-only registration / 2026-09-24

`PLAN-QIUQIU-04` / `DELIVERABLE-QIUQIU-04` / `TASK-QIUQIU-04` remains bound to `b307830089b51aca793ca693e375c217ec8e45ea`. The current control-only overlay registers exactly 13 existing candidate paths: 6 `lfa-api`, 3 `lfa-android`, and 4 `lfa-test`. All are `CANDIDATE_NOT_ACTIVE`; no implementation, integration, review/PM acceptance, device execution, or evidence write is authorized. Historical bounded `AUTHORIZED_ACTIVE` rows remain preserved as history and do not grant current candidate execution. Cor template/config and fresh-device evidence remain `RESERVED_NOT_ACTIVE`; iOS `FILE_SCOPE=[]`.

## Current blocked projection / 2026-09-24

`PLAN-QIUQIU-04` / `DELIVERABLE-QIUQIU-04` / `TASK-QIUQIU-04` is `BLOCKED / NOT_DISPATCHED` at HEAD `b307830089b51aca793ca693e375c217ec8e45ea`. The 13 registered paths remain inactive candidates. Root `AGENTS.md` defines DHEA and Cor as current MVP products, but the executable successor wire, exact Cor physical configuration/source scope, and new-sample evidence write scope are not authorized or accepted. No implementation, integration, device execution, Review or PM acceptance is inferred.

## Cor physical-sample candidate / 2026-09-24

The user identifies capture bundle `1df42409-a789-47e4-9dc2-66bd270b603e` as a physical Cor reagent with an observation window and QR code. That identifier is not present in the current repository or latest exported Cor archive, so it is recorded as `CANDIDATE_IDENTITY_RECORDED_NOT_ACCEPTED`. It does not yet prove immutable JPEG/SHA binding, geometry, direction, T/C windows, implementation completion or device acceptance.

## QIUQIU-04 authorized implementation increment / 2026-09-24

At HEAD `b307830089b51aca793ca693e375c217ec8e45ea`, the user selected code/documentation implementation plus read-only evidence export for existing Cor bundle `1df42409-a789-47e4-9dc2-66bd270b603e`. The 13 candidate paths are now `AUTHORIZED_ACTIVE`, and `artifacts/cor-bundle-1df42409-a789-47e4-9dc2-66bd270b603e/` is active for export-only immutable evidence and a manifest. START delta `TASK-QIUQIU-04-START-DELTA-20260924-01` is recorded. Integration deployment, new shutter/sample execution, Cor numeric-template creation, Review and PM acceptance remain ungranted.

## QIUQIU-04 single Cor live trace / 2026-09-24

The user confirms the reagent below the camera is Cor and authorizes one App photo/upload to trace the API failure layer by layer. START delta `TASK-QIUQIU-04-START-DELTA-20260924-02` activates that single execution and evidence capture under the existing Cor bundle evidence directory. It does not grant deployment, Cor template creation, device acceptance, Review or PM acceptance.

## 2026-09-24 双产品交付快照（append-only）

- `IMPLEMENTATION_EXECUTION = DELIVERED_PENDING_INDEPENDENT_REVIEW`
- `NEW_SAMPLE_DEVICE_EXECUTION = COMPLETED_SINGLE_COR_CAPTURE_AND_UPLOAD`
- `REVIEW_AND_PM_ACCEPTANCE = NOT_GRANTED`
- `INTEGRATION_DEPLOYMENT = NOT_GRANTED`
- DHEA 与 Cor 已在当前源码中按独立产品身份兼容；Cor 不是 DHEA alias，也未创建独立拍摄链。
- 设备上安装的旧 APK 尚未包含 successor metadata 修复，因此真实上传在 Gateway 前置校验处以 `INVALID_PRODUCT_GATE_DECLARATION` 终止；当前源码已通过真实 JPEG 本地 API smoke 和聚焦测试。
- 证据目录：`artifacts/cor-bundle-1df42409-a789-47e4-9dc2-66bd270b603e/`。
