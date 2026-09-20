# Baseline review meeting response

TASK_ID: RUN-20260918T043217Z-REVIEW-BASELINE
RUN_ID: 20260918T043217Z
Reviewer: lfa-review
BASE_HEAD: 410b17a00b63374f5d28a5531c478db8b30e8427
Baseline: BASE_HEAD plus pre-existing dirty work recorded by PM; audited file SHA-256 values are in RUN-20260918T043217Z-REVIEW-BASELINE-checks.json.
Review status: BASELINE_REVIEW_REPORTED
Implementation acceptance: NOT_REVIEWED
End-to-end CODE_REVIEW_ACCEPTED: NOT_GRANTED

## Meeting opinion

Frozen Android Bundle 1.5/public research v2 is a coherent scope for bounded audit and later repair. READY was supplied as verified dispatch evidence; this review did not rerun the HEAD/gate check. Current round has no implementation diff. Earlier onboarding conflicts are historical and the latest PM scope ruling controls. Neither historical CLOSED claims nor completion of this baseline review approves the requested live loop.

The frozen contract explicitly permits diagnostic request_id=analysis_id. capture_bundle_id owns public lookup/idempotency; analysis_id identifies the accepted result; execution_id distinguishes executions. References: 11号公开契约:32–39,66–95,163–173; python_gateway/dhea.py:124–198; python_gateway/dhea_diagnostics.py:75–78. This mapping is not a defect. New internal request semantics must not silently alter these public identities.

## High-priority findings

### RBL-01 — HIGH — Required internal request is not integrated

Evidence: python_gateway/dhea.py:173–182 passes stored bytes, expected hash and an optional diagnostic collector to core/dhea.py:371–385. Capture/request identity and frozen profile binding currently live in the optional collector or Gateway/runtime state, not a required internal request validated by Core. core/contracts.py:94–109 is a separate prototype AnalysisRequest with optional template/manual annotations; its existence does not satisfy the assigned UnifiedAnalysisRequest requirement.

Impact: the explicit internal acceptance item remains incomplete. This finding does not assert that current image hashing or frozen retry checks are absent: dhea.py:132–137,203–215 and core/dhea.py:422–425 provide those guards.

Required repair input: PM/API must specify the actual required internal request fields, lifetime/ownership of its request identity, capture binding, original JPEG/SHA, applicable frozen profile/source digests, and mismatch/refusal behavior. Route the real Gateway invocation through that contract into the common DheaRuntime.analyze behavior. Identity must remain available when diagnostics fail. No alias-only/rename-only fix. Do not import manifest, Base64 transport or profile fields from api-reference.md:364 by assumption: that document explicitly excludes research v2 at line 9. In-process byte transport need not acquire a new HTTP hop.

Required review proof: real runtime invocation, hash/config/identity mismatch refusal, valid input without optional diagnostics, retry preserving frozen identity/config, unchanged public v2 schema and valid feature preservation on concentration refusal. Exact implementation diff and executable outputs required.

Disposition: OPEN_DELIVERY; proposed continuation of B-PM-03, not a safe-dispatch veto.

### RBL-02 — HIGH — Current end-to-end acceptance lacks bound runtime evidence

Evidence: four historical JSON artifacts listed by PM were freshly parsed and SHA-256 checked; all match the onboarding hashes. That validates inventory integrity only. PM snapshot:39–49,60–62 records no demonstrated current APK/deployed runtime binding; fresh AND/API reports were absent from EVIDENCE at this inspection. No current live loop was executed by this reviewer.

Required review proof: a manifest linking BASE_HEAD plus dirty source hashes, APK SHA/version and designated device observation, deployed source/profile/dependency identity, original local and persisted JPEG byte hashes, capture_bundle_id, analysis_id/diagnostic request_id and execution_id. Attach real multipart request/response evidence without credentials; App persisted result/recovery display; Web stages and downloaded artifacts bound to the same execution. Include actual bottom-to-top ROI/quad mapping and 256×24 canonical order, Green/profile/baseline, T/C and research 4PL or explicit refusal. Historical cohorts may contribute only through demonstrated provenance; do not relabel them fresh tests.

Web acceptance must state how an operator resolves the given request_id to the bundle-addressed frozen-v2 diagnostics. An explicit binding alone does not demonstrate operator lookup. Do not invent a new public endpoint without a scoped decision.

Disposition: OPEN_DELIVERY; B-PM-02. No conclusion that historical tests failed or current code is broken.

### RBL-03 — HIGH — ICC presence/disposition evidence is lost before diagnostic capture

Evidence: core/dhea.py:443–450 removes image.info.icc_profile before calling decoded; core/dhea_diagnostics.py:140–144 records dimensions, media type, size and EXIF but no ICC presence/disposition. The original byte stream is separately hashed and read from immutable storage; this is not evidence that stored JPEGs were altered.

Required repair/review proof: capture actual ICC presence and chosen no-transform disposition before in-memory removal, retain original bytes/hash, expose truthful stage evidence. Cover JPEGs with and without ICC, and the supported/refused decoder outcomes. No fabricated profile classification and no App/API colour conversion. Preserve historical raw JPEGs.

Disposition: OPEN_DELIVERY; B-PM-04.

### RBL-04 — HIGH for overlapping repairs — Existing dirty work is protected, not part of this round's diff

Evidence: onboarding JSON and DECISIONS.md:31–34 list four tracked dirty files plus untracked v3 and iOS work. Fresh read-only hunk inventory confirms python_gateway/dhea.py insertion at current 437–438; dhea_input.py insertion at 14 and 65–75 and replacement at 292–293; api-reference.md insertion at 3–4. The TODO document has extensive pre-existing changes. Unknown owner is not evidence of unauthorized work.

Required before any overlap: preserve the exact relevant pre-existing diff in credential-safe storage, record complete audited file hashes, obtain explicit hunk ownership via start/PM, and separate old from new changes. Hashes alone cannot reconstruct a lost diff. The current review changed no business source and therefore did not copy raw potentially credential-bearing diffs. Its hunk inventory is not an authorization to edit. Recheck a changed file baseline before a later repair.

Protect the complete untracked v3 schema/generator/fixtures/tests and IOS_App boundary listed in BLOCKERS.md:65–66, not merely the four tracked files. Do not revert, adopt v3, overwrite or regenerate protected artifacts as part of a v2 repair.

Disposition: OPEN_CONDITIONAL_OVERLAP; permits disjoint work and read-only audits.

## Laboratory and missing-data acceptance

B-PM-05 remains an evidence/binding dependency, not a requirement to invent or obtain unavailable instrument values before the reachable loop runs. Frozen contract:18,97–113 makes references optional and isolates validation from Core input. Repository acceptance still requires binding each available real reference to sample/value/unit/method/time/card/bundle/result/config and repeat captures. Unknown fields stay null, original results remain immutable, references use a separate traceable record. Current v2 validation fields do not by themselves establish the full requested laboratory association. PM/API must map missing fields to a companion evidence record or an explicitly scoped extension, without silently adding fields to frozen v2. No accuracy/tolerance claim is supported by this baseline review.

## Required independent review packet after repairs

- Assigned TASK_ID, exact before/after hashes and bounded diff relative to the captured dirty baseline; ownership of every protected overlap.
- Commands, environment/revision, exit results and raw credential-safe focused test outputs. Separate synthetic checks, historical results, host runs, real API traffic and device observations.
- Coverage of subject/auth isolation and diagnostic credential separation, multipart limits/schema/hash binding, immutable original replay, idempotency conflict/recovery, frozen profile refusal, stale execution/artifact binding, null/refusal and valid feature retention. Select existing focused regressions for touched paths; no passing-count claim without outputs.
- Runtime proof described in RBL-02; manual ROI/correction audit if used; no synthetic value or fixed zero standing in for unavailable measurements.
- Available laboratory/reference and repeated-capture comparison bindings; missing data and research limitations explicit.
- No credentials, destructive state operations, new production/clinical claims, or changes to active services under the audit assignment. Production YOLO, multi-device/general-background support, iOS and regulatory validation remain POST_FUNDING_GATE with current_mvp_blocking=false.

This is scoped source/contract review, not a complete security audit or certification that the repository contains no secrets. No live credentials were read or copied; no build, unit test, camera run, install or service change was performed.

## BTW-CHECK

| TODO_ID | Goal | Files changed | Build result | Requirement trace | Test result | Artifact evidence | Known limitations | Open post-funding gates | Current MVP blocker remaining |
|---|---|---|---|---|---|---|---|---|---|
| RUN-20260918T043217Z-REVIEW-BASELINE：核对会议范围身份与证据边界 | Restore authoritative scope | Review report/checks only | N/A review | meeting:51–56; latest PM ruling | Read-only authority inspection | meeting, snapshot, decisions, onboarding JSON | Gate verification supplied by start; no rerun | unchanged | RBL-02 |
| RUN-20260918T043217Z-REVIEW-BASELINE：评审契约内部请求与保护边界 | Inspect identity/internal/ICC/dirty boundaries | Review report/checks only | N/A review | frozen contract; meeting:14,40,56 | SHA-256 + JSON parse 4/4 matches; diff hunk inventory exit 0; no behavior tests | checks JSON; cited source lines | Source review does not prove runtime | unchanged | RBL-01/02/03 and conditional RBL-04; B-PM-05 evidence |
| RUN-20260918T043217Z-REVIEW-BASELINE：落盘报告高优先级发现并通知 | Publish findings and notify owners | This report, checks JSON, reviewer status | N/A review | meeting:20,54–56 | Report creation and notification receipts recorded by reviewer | EVIDENCE/RUN-20260918T043217Z-REVIEW-BASELINE*; AGENT_STATUS/lfa-review.json | Submission is not acceptance | unchanged | Findings remain open |

Ledger update proposal to start/PM: link this report from TASK_BOARD and REVIEW_QUEUE, mark baseline report submitted without CODE_REVIEW_ACCEPTED; synchronize RBL-01/02/03 to existing B-PM-03/02/04 and RBL-04 as a conditional protected-overlap blocker. Do not close those findings when marking the review-writing TODO complete. Shared ledgers are not rewritten by reviewer per meeting:20.

## Supplemental PM-SCOPE review under the same TASK_ID

Input: EVIDENCE/RUN-20260918T043217Z-PM-SCOPE.md and companion .json, supplied as REPORT_READY_FOR_REVIEW. Start reports its report SHA check passed; this reviewer does not repeat that check or interpret companion result=PASS as delivery acceptance. That PASS covers document coverage/identity checks only. Source comparison includes docs/QA.md:5–17,29–33,41–77,85–91.

| Criterion | Independent baseline disposition |
|---|---|
| A01 | Scope matches manual portrait capture and non-authoritative C/T guidance. Require actual device observation tied to APK. |
| A02 | Correctly requires camera/App/API original-byte hash chain; no re-encode or inferred provenance. |
| A03 | Correctly includes identity-preserving recovery and changed-content conflict; include response-loss and restart evidence, not only fresh success. |
| A04 | Correct frozen v2 multipart path and subject/hash bindings; sanitized traffic evidence required. |
| A05 | Correct requirement for actual accepted-input runtime integration and mismatch/refusal. RBL-01 remains open until a scoped implementation maps exact internal identity/config semantics. |
| A06 | Correct ROI/source/manual-disclosure requirement. Manual confirmation must remain auditable and AUTOMATED_PRODUCT_RESULT=false. |
| A07 | Correct bottom-to-top and 256×24 canonical order; source quad correspondence and actual artifacts must establish direction, not App labels. |
| A08 | Correct linked Green/profile/baseline evidence; retain actual versions and parameters. |
| A09 | Correct invalid-C refusal and null behavior; measured zero and missing data remain distinct. |
| A10 | Correct legitimate-curve, domain and research-only result/refusal requirement; no real-image result from synthetic calibration. |
| A11 | Correct same-result App response/recovery/display binding; source/build evidence alone cannot pass. |
| A12 | Binding/artifact/live-UI coverage is sound but needs an explicit operator lookup demonstration starting with request_id. Existing frozen routes are bundle-addressed. Add the request_id→analysis_id→bundle lookup scenario to later acceptance; do not presume a new endpoint. This is the RBL-02 review input, not a newly proven runtime bug. |
| A13 | Correctly retains explicit ICC presence/disposition as open delivery evidence; RBL-03 applies. |
| A14 | Correct full reference association and nullable unknowns. Historical QA suffixes/numbers are not current sample/card/bundle identities. |
| A15 | Correct per-capture scientific comparison and failure retention. Depend on verified same-card/sample identity, not availability of a laboratory concentration: unavailable lab values must not block collecting and comparing repeated captures. |
| A16 | Correct source/dirty/APK/runtime/config trace and limited feasibility conclusion. No present closure. |

PM-SCOPE:45–49 preserves public identity ownership and genuinely requires internal integration; it neither accepts a renamed DTO nor imports the compatibility draft. Exact internal request identity lifetime, accepted metadata/config binding and mismatch policy remain inputs to the later repair specification, not missing prerequisites to this read-only audit. PM-SCOPE:71–75 correctly retains all pre-existing work and requires credential-safe diff preservation plus explicit hunk ownership before edits.

The five PM table entries match the supplied QA values. QA says they were user-relayed, original exports and measurement definitions were not received, image association is historical screenshot naming, manual coordinates were not visually validated, and concentration/assay/lot correspondence is unconfirmed. No current sample_id, physical_card_id or capture_bundle_id association is established. Keep supplied ratios unchanged; do not infer concentration, fit correction factors, create current bindings by filename/value similarity, or treat these rows as current A14/A15 completion. Missing source facts remain null. PM's provenance limitations are consistent with this source.

Supplemental conclusion: no new HIGH contradiction in the PM scope report was established. A12 needs the explicit lookup scenario above; A15 must preserve repeatability work independent of unavailable lab concentrations. Existing RBL-01/02/03 and conditional RBL-04 remain open. This accepts neither implementation nor the live loop; CODE_REVIEW_ACCEPTED remains NOT_GRANTED.

BTW-CHECK supplemental TODO_ID: RUN-20260918T043217Z-REVIEW-BASELINE：复核PM范围A01至A16并补充意见. Goal: independently check all sixteen requirements and laboratory provenance. Files Changed: this reviewer report and reviewer status only. Build Result: N/A. Requirement Trace: PM-SCOPE A01–A16, identity/lab/protection sections; frozen v2 contract; QA source. Test Result: read-only row/source comparison; no business/device tests. Artifact Evidence: this addendum and direct notification receipts. Known Limitations: no live runtime evidence, no laboratory bindings, no implementation diff. Open Post-Funding Gates: unchanged. Current MVP Blocker Remaining: RBL-01/02/03, conditional RBL-04, missing reference provenance as applicable; findings not closed by completing this review TODO.

## Subsequent review of PM lifecycle/configuration addendum

TODO_ID: RUN-20260918T043217Z-REVIEW-BASELINE：记录最新内部生命周期增补审阅版本

Reviewed input: EVIDENCE/RUN-20260918T043217Z-PM-SCOPE.md, SHA-256 `842de7d7745ce9256aff8327ea975b22ed09ee23e5299e35fb6a664054c9925b`; read snapshot #237E. Scope of this subsequent review is lines 92–126 only: Independent baseline review integration; Internal identity lifecycle and configuration refusal requirements; Web operator and laboratory evidence additions; Reviewer follow-up clarification. These sections arrived after the earlier A01–A16 review. Neither the initial checks JSON nor the earlier review is retroactively claimed to cover them.

Disposition: the new acceptance wording addresses the previously requested lifecycle and configuration clarification. Internal request_id uses the Gateway-persisted analysis_id and remains required independently of diagnostics. Final-result replay does not execute Core; failed-analysis retry retains accepted capture/request identity and frozen configuration, with a distinct execution identity for each real run. Core validates required bindings against authoritative expected identity/content and the actual loaded configuration before measurement; unavailable/mismatched configuration cannot fall back to latest. Exact internal fields and externally visible refusal mapping still require the later bounded repair specification. No incompatible public DTO, transport or endpoint is authorized.

The A12 operator lookup requirement now explicitly includes request_id→analysis_id→bundle resolution, actual UI steps and wrong/no-match handling. The A15 clarification explicitly permits same-card T/C/refusal repeatability without laboratory concentration; identity/provenance remain required. QA historical rows remain unbound and cannot become current reference records by inference. No additional HIGH contradiction is identified in these newly reviewed acceptance sections.

This is review of requirements only. RBL-01/02/03 and conditional RBL-04 remain open pending implementation/evidence; implementation remains NOT_REVIEWED and end-to-end CODE_REVIEW_ACCEPTED is NOT_GRANTED. No full audit, business test, runtime execution or historical-check rewrite was performed.

BTW-CHECK: Goal record the newly reviewed PM version/sections; Files Changed this reviewer report only; Build Result N/A; Requirement Trace PM-SCOPE:92–126 and this TASK_ID; Test Result targeted document comparison and sha256sum exit 0 for version identification only; Artifact Evidence this section and direct start/PM notification; Known Limitations no implementation acceptance or behavior proof; Open Post-Funding Gates unchanged; Current MVP Blocker Remaining existing open findings. No shared-ledger mutation by reviewer.

## M1-D03 report-based repair boundary review

PLAN_ID: M1. DELIVERABLE_ID: M1-D03. TASK_ID: RUN-20260918T043217Z-REVIEW-BASELINE. Disposition: REPORT_BOUNDARY_REVIEW_REPORTED, not repair authorization or implementation acceptance.

Reviewed inputs: API-AUDIT SHA-256 `75384511fe2867d60cd13f46355c860f37fb9eecd4c67854e60293b926f450af` and AND-AUDIT SHA-256 `f21c13ab6359b558ac17c05ba136b66a451f68c1597d247d577c3fc221124c3d`. API sections 103–202 supply proposed boundaries; Android findings at 20–21 supply consumer/security dependencies. These are later inputs, not material seen in initial baseline inspection. API's reported 46 passing tests and Android's reported 34/34 plus APK are role host evidence only; no suites were repeated here. M1-D05's concrete repair specification and protected-diff preservation are still separate inputs, not assumed complete or reviewed.

### M1-B01: authoritative binding and complete refusal mapping required in M1-D05

API-AUDIT:107–157 correctly requires real invocation, persisted analysis_id, diagnostics-independent identity, frozen retries and actual loaded config comparison. Its field inventory alone does not define the independent authority used by Core to reject a wrong bundle or metadata digest. The repair specification must name the persisted accepted record/immutable object, how its integrity is verified, how a request is compared with it, and which component owns that trusted comparison. Copying the same request values into an expected object is not independent validation. Core need not acquire database or HTTP responsibilities. Require a negative case that swaps an otherwise valid request/bundle/metadata binding while holding the trusted accepted binding fixed.

Freeze or reconstruct the complete accepted config from its immutable integrity root. A runtime-derived config tuple is acceptable for first acceptance only when persisted/bound before execution; using the current runtime to recreate an old retry's expected config defeats the guard. M1-D05 must cover old records that lack a reconstructable binding: preserve stored final replay; refuse an unverifiable failed retry rather than migrate it to today's config. Validate source-hash map completeness as well as values, and retain actual-loaded config comparison even when diagnostics construction/publication fails.

API-AUDIT:145 leaves the exact external mapping open. M1-D05 needs a table per failure class containing HTTP status, wire_code, business_status, retryable, data nullability, persisted state, and replay/retry effects. Existing Core IMAGE_HASH_MISMATCH is a structured measurement refusal; current Gateway converts returned non-measurable data to rejected/HTTP 200, while raised exceptions become failed/503/CORE_EXECUTION_FAILED/retryable=true (python_gateway/dhea.py:178–193). FROZEN_PROFILE_UNAVAILABLE is already a pre-execution Gateway refusal. Reusing code names without choosing these semantics can silently change retryability or make an integrity fault a scientific rejection. Do not invent a new public code, expose internal details, or convert a config/binding failure into zero measurements. Concentration-only refusal must still retain valid features. Exact choices require contract review before implementation acceptance.

Disposition: unresolved repair-spec inputs under existing RBL-01/B-PM-03 HIGH; no newly verified implementation fix.

### M1-B02: exact request_id list filter is a diagnostic contract extension

API-AUDIT:190–202 is the smallest proposed route change, but unchanged route/payload does not mean unchanged contract. Frozen contract:162 and current allowlist at python_gateway/dhea.py:299 exclude request_id, so the existing server rejects it with DIAGNOSTICS_QUERY_INVALID/422. M1-D05 must explicitly scope the optional parameter and update the authoritative diagnostic contract and applicable query documentation/schema/export under protected ownership. Do not regenerate protected v3 artifacts by default.

Define request_id as the persisted analysis_id only, with exact UUID representation/validation, empty/malformed/duplicate rejection, no fuzzy/bundle fallback, and explicit interaction with other filters. Conservative rule: compose supplied filters with AND, retain pagination defaults, and have the workbench send request_id plus limit=2 with offset=0 and no stale device/status filters. Subject and expiry predicates remain unconditional. For the filtered list, zero items covers no match, wrong subject or expired rows without revealing which; bundle resource 404/410 semantics remain separately governed. Invalid authorized queries use DIAGNOSTICS_QUERY_INVALID/422. Match existing authentication-before-query-validation ordering, diagnostic-token-only access, no-store and in-memory bearer handling. Never permit App credentials merely because they display analysis_id.

One contract discrepancy must be explicitly resolved in M1-D05: diagnostic_subject currently returns FORBIDDEN/403 for ordinary App tokens (dhea.py:274–275), while frozen diagnostic documentation names DIAGNOSTICS_FORBIDDEN/403 (contract:173). The report does not settle that wire mapping. Record the chosen contract disposition; do not silently change it as an incidental filter edit. Endpoint-level tests must cover missing/invalid/App/diagnostic credential classes, subject isolation, expiry and duplicates; browser evidence must show wrong/no-match cannot open a previous selection, and retry execution changes cannot mix stage/artifact snapshots.

Targeted inspection also shows a default diagnostic-token selection and workbench injection mechanism at dhea.py:251–252,282–284. No configured credential value or credential file was read. [INFERENCE] if an active token is delivered in the unauthenticated shell, independent diagnostic auth cannot be claimed merely from checks on list routes. M1-D05 must establish the served-shell access boundary and absence of bearer disclosure, using credential-safe evidence, before accepting the new lookup workflow. Do not rotate/read live credentials under this review. This is a boundary concern for the auth review, not a claim that live exposure was demonstrated.

Disposition: scoped contract/auth questions under RBL-02 plus the existing credential boundary; no implementation or live exposure conclusion.

### M1-B03: ICC must reach both result and stage consumers

API-AUDIT:163–186 selects data.diagnostics.image_decode_evidence.icc_profile_evidence, which matches Android's preferred read path. Current Core's returned diagnostics dictionary and optional core.dhea_diagnostics collector are separate: core/dhea.py:391–415 creates result diagnostics, :448–450 removes the tag then emits decoded, and :455–456 writes only image dimensions/orientation. Changing decoded stage metrics alone will not populate Android's result. M1-D05 must assign one observed ICC evidence value to returned diagnostics independently of collector availability, pass matching evidence into the decoded stage, preserve it through Gateway persistence/replay, and identify the Web consumer. No historical result backfill or re-execution may masquerade as original evidence.

Specify decoder_name/version placement consistently with the chosen path, actual boolean types, and each field's missing/null/malformed handling. Android's current optBoolean coercion/defaults (ResearchResultPanel.kt:138–148) mean fixing only an absent whole object is insufficient: a present partial object or a string boolean can still fabricate ABSENT/NO. Require explicit typed evidence for each assertion; unknown decoder must not default to observed Pillow. Define handling of the legacy diagnostics.image.icc fallback rather than silently presenting conflicting paths. Missing, partial and invalid fields show UNKNOWN/NOT_REPORTED; an explicit observed false remains distinguishable.

Define whether icc_present means successfully extracted ICC bytes or any embedded ICC markers. Malformed/split ICC that Pillow cannot assemble must not be promoted to verified absence. A successful Image.open is not successful full decode; no decode PASS on subsequent load failure. Scope jpeg_reencoded=false to preservation of original JPEG, since diagnostic previews may be encoded separately. Retain original hash/bytes, no color transform, no raw ICC publication, and truthful refusal outcomes. With/without ICC, missing/partial evidence, malformed evidence and decode failure are the focused producer/consumer proof cases. Synthetic ICC bytes establish extraction/handling only, not profile validity or color accuracy.

Related Android consumer text at ResearchResultPanel.kt:180 points to /api/v2/lfa/diagnostics, whereas the published workflow uses /workbench and bundle-addressed routes. Include correcting this consumer instruction in the bounded A12/A-DIAG ownership decision, or explicitly leave it as an open delivery mismatch. Do not claim the report's exact producer/UI path is complete while that guidance sends the operator elsewhere.

Disposition: coordinated RBL-03/B-PM-04 and A-DIAG-01 HIGH producer/consumer scope. A-SEC-01 remains separate: removing source bootstrap must preserve existing configuration; injecting a real secret at build time still embeds it in the APK. Credential rotation/production permission changes are not authorized by this report review.

### Evidence and handoff

These are M1 report-boundary questions for M1-D05, not an independent implementation audit or an authorization to widen business edits. Keep existing RBL findings and Android HIGH findings open; protect existing diffs and agree path/hunk ownership. Later review needs the exact M1-D05 spec, failure mapping, query/auth contract, ICC producer/consumer assignment and preserved baseline before judging a repair diff. No repeated full baseline audit is requested.

BTW-CHECK: TODO_ID RUN-20260918T043217Z-REVIEW-BASELINE：审阅M1-D03拟修复边界并落盘; Goal review two role reports and their proposed repair boundaries; Files Changed this reviewer report only; Build Result N/A; Requirement Trace M1-D03 user assignment, API-AUDIT:103–202, AND-AUDIT:20–21, frozen diagnostic contract:159–173; Test Result read-only report/source-path comparison and report SHA inventory, no role test reruns; Artifact Evidence this M1-D03 section and direct start/PM notification; Known Limitations no M1-D05 concrete spec/diff or live auth/device proof reviewed, no embedded credential values read/copied; Open Post-Funding Gates unchanged; Current MVP Blocker Remaining original open HIGH findings and specified repair-boundary decisions. Implementation NOT_REVIEWED; end-to-end CODE_REVIEW_ACCEPTED NOT_GRANTED. Shared ledgers unchanged.

Subsequent PM input considered: PM-SCOPE section “M1-D03 scope ruling after both complete audits”, starting at line 157. The exact request_id diagnostic list extension is now IN_SCOPE_FOR_M1_SPEC_AND_M2_D05_REPAIR. Accordingly M1-B02 does not request another scope decision to draft it; its parameter/auth/error/schema and same-execution proof questions are concrete M1-D05 specification obligations within the accepted scope. This ruling authorizes preparation only, not implementation. Existing HIGH findings are M2 repair inputs and do not prevent M1 gap-audit completion. M1-D04 inventory, M1-D05 protected baseline/exact repair graph, and PM plus independent acceptance remain required for M1 Exit. Current status supplied by start: M1-D05 IN_PROGRESS, D02 EVIDENCE_READY, M2 NOT_STARTED. This reviewer creates no new repair assignment and does not clear protected overlap or grant M1 Exit through this report.

## M1-D05 independent specification and preservation review

TASK_ID remains RUN-20260918T043217Z-REVIEW-BASELINE; M1-D03 follow-up input, no repair assignment. Disposition: CHANGES_REQUESTED for the submitted D05 specification/preservation evidence. This does not require closing implementation HIGH before completing M1 gap auditing. M1 Exit and implementation acceptance are not granted.

Reviewed submission: report b03dbe6c37530755edc90b577dc249dbcc70f560a2f7328b3719e3a6a7a8495d; manifest 6c7b39167f29a9be97d4a938a357da2a2698734ab9e20ebe5384353f8cbc9918; patch c80055a2da264496b2998bc971f74afc07af69d6b9349da9c5ca79f657907325. REVIEW_QUEUE:9 and start identify these versions. Later PM assessment at PM-SCOPE:181–198, reported SHA 90429dbd7e0937d6ce7123e6e8b7391696f9ada704f82b23866c107bbe307002, supplies 3/3 digest matches, four-path temporary reconstruction and 12/12 current-file matches. Those are attributed PM checks, not repeated reviewer execution. Reviewer independently parsed manifest inventory and emitted only patch path headers, never patch hunk contents or credential values.

Ownership check: FILE_OWNERSHIP:16–20 gives the reviewer only this report and its checks JSON; the API owns the three submitted D05 artifacts exclusively. Their declared changed-file set matches their registered scope. The four source paths inside the preservation patch represent captured pre-existing work, not proof that this task wrote those source files. No task-specific before/after write provenance establishes every historical writer, so owner compliance of historical mutations is NOT_VERIFIED; no unauthorized writer is inferred. A demonstrated out-of-scope write, non-owner write or ACTIVE overlap mandates CHANGES_REQUESTED. This reviewer writes only its two registered paths and leaves all API artifacts unchanged.

### D05-R1 HIGH: submitted snapshot reconstruction does not preserve snapshot history

Report:29 and manifest:224 state that artifacts were refreshed after concurrent test-file changes. The manifest contains only the final snapshot, no ordered captures, retained original artifact reference or reconstructable transition. Meeting:94 and FILE_OWNERSHIP:26 explicitly forbid replacing preservation originals with a newer baseline. PM's successful final reconstruction cannot answer whether an earlier established baseline was overwritten. This is missing continuity evidence, not proof of irreversible loss or an identified unauthorized author.

Required revision: identify provisional versus established captures, ordered refresh events, original/final hashes and recoverable byte sources; preserve the submitted patch while documenting the history. If original bytes cannot be recovered, state that limitation and leave overlap uncleared; a hash alone is not recovery. API has been asked for existing evidence only, without new files or modifications. RBL-04 remains conditional and is not cleared.

### D05-R2 HIGH: transient failure and first-accept state remain externally unspecified

Report:99–109 and :217 defer repeated transient response-byte policy. This blocks exact-spec acceptance: after a frozen-config refusal the row is unchanged, but the immediate POST may return a different code from the next GET, which reads persisted response. Distinguish pre-execution refusal from an attempted execution that becomes failed, and first acceptance from failed retry/legacy rows. Specify POST status/body and identity, GET status/body, stored response/result objects, repeated POST eligibility, execution ID creation and restart outcome. Exact final replay remains unchanged. Serialization/transaction implementation may be deferred; observable persistence and replay cannot.

The accepted-binding architecture at :57–90 is directionally sufficient: Gateway's accepted row and verified immutable objects are authority, Core compares the independent binding and actual runtime, and final replay bypasses Core. Complete the verification order for first accept, bind request.accepted_binding_sha256 to verified canonical binding bytes and the row root, and check cross-consistency of row IDs/object references/digests with binding fields. A self-consistent but wrong binding object must not replace the accepted row identity. Add matrix outcomes for first-accept binding persistence/verification failure and output binding validation failure. The private METADATA_HASH_MISMATCH classification must specify verified canonical metadata-object hashing rather than merely comparing copied digest fields. These choices need no Core database or extra HTTP boundary.

### D05-R3 MEDIUM: proposed hunk inventory lacks four baseline entries

Independent set comparison finds proposed ownership entries absent from manifest.files: python_gateway/dhea_export.py; docs/LFA_最新完整文档集合/11_DHEA原生Android研究v2公开契约.md; docs/api/dhea-v2-app-integration.md; Android_App/app/src/main/java/com/example/ui/screens/ResearchResultPanel.kt. Supply baseline/current hashes and dirty status or exact accepted D04 references. Name concrete Android test paths before future scope registration. Do not create preservation files or grant business ownership through this report. Current manifest completeness cannot be claimed from its 12 matching entries.

### D05-R4 MEDIUM: ICC combinations and schema transitions are not yet exact

Keep collector-independent result evidence, matching stage evidence, typed Android unknowns, legacy precedence, original immutability and no-transform requirements. Report:125–141 permits nullable marker/presence/transform fields without a complete state table; :218 leaves schema placement to M2. Define allowed combinations for ABSENT, EXTRACTED, MALFORMED and DECODE_FAILED, including empty extracted bytes, marker uncertainty, length/hash, disposition and transform/re-encode assertions. Specify whether a structured image refusal carries observed ICC evidence when load fails versus when data is null. Name the actual decoded stage identifier, currently ORIGINAL_IMAGE, and concrete result/stage schema locations, requiredness and historical missing-object compatibility. These are consumer contracts, not deferred implementation mechanics.

### D05-R5 MEDIUM: same-execution comparison needs a field-to-response contract

Request-ID syntax, auth-first validation, subject/expiry predicates, AND filters, pagination, DIAGNOSTICS_FORBIDDEN migration and credential-free shell are specified adequately as target behavior. Report:177–185 nevertheless requires equality of execution/config fields across list/result/stages/artifacts that current LIST_ITEM and CORE_RESULT do not all carry. See python_gateway/dhea_diagnostics.py:20–43,75–78 and dhea_input.py:97–114. Specify each compared field's producer and response location, its equality partners, missing/legacy refusal and resulting v2 schema/doc changes. Do not silently expand the frozen measurement payload or expose private accepted-binding object references merely because :77 says diagnostics copy the object. Define an explicit public projection. Separate fetching an artifact manifest needed for comparison from downloading artifact bytes after validation; :187 must not make its own required comparison impossible. State the observable multiple-match integrity outcome and retain no fallback/stale display.

### Review disposition and proof

Keep the proposed serial Core/Gateway mutation order and separation of M2 repair from M3 live proof and M4 reference/repeatability. No M1-B01–03 implementation is accepted. Original RBL-01/02/03 and Android HIGH findings remain open, RBL-04 conditional, D04 runtime/device facts unknown or unaccepted. Required revisions above belong to the existing D05 preparation and must stay within its ownership or obtain registration first. Pending author chronology evidence can supplement this review; it is not assumed to exist or to resolve R1.

BTW-CHECK: TODO_ID RUN-20260918T043217Z-REVIEW-BASELINE：审阅D05保全与精确规格回收; Goal independently review M1-B01–03 and preservation; Files Changed reviewer report and checks JSON only; Build Result N/A; Requirement Trace meeting:83–104, FILE_OWNERSHIP:16–26, prior M1-B01–03 and latest user assignment; Test Result manifest JSON parse and patch-path/inventory set comparison, focused source/spec reads; PM reconstruction/digest checks attributed, not rerun; Artifact Evidence this section and companion follow-up entry; Known Limitations no historical writer attribution, prior snapshot continuity or runtime proof, no live credentials inspected; Open Post-Funding Gates unchanged; Current MVP Blocker Remaining existing HIGH and D04/D05 acceptance gaps. CHANGES_REQUESTED applies to exact-spec/preservation acceptance, not a new repair dispatch. M1 Exit NOT_GRANTED; implementation NOT_REVIEWED.

## M1-D05 clarification revision re-review

This is the same M1-D05 returning to the existing M1-D03 independent review; no new task or repair assignment. The control ledger/REVIEW_QUEUE and TASK_BOARD register `REPORT_READY_FOR_RE_REVIEW`. Re-review is bound to the complete clarified report SHA-256 `73a8658eebd14110a4f3951df080dfb1ca0e669d28ee0bd041489899a1500531` (42,641 bytes), manifest SHA-256 `72a818ce2be0b3eb86560cfe790b809aeeee1cbe3d3eacada9f3264ab5bec45f` (29,328 bytes), and unchanged patch SHA-256 `c80055a2da264496b2998bc971f74afc07af69d6b9349da9c5ca79f657907325` (11,368 bytes). The submitter declares the original report as an exact 23,391-byte `b03dbe6c` prefix and the original 7,960-byte `6c7b3916` manifest as recoverable/deep-equal; start did not rerun those checks. This attribution is not treated as acceptance evidence.

### Re-review disposition: CHANGES_REQUESTED; HIGH OPEN

R1 is improved but not closed. Section 9.1 and manifest `preservation_chronology` now distinguish two provisional captures from the established patch, preserve the established patch hash/path, state the missing durable provisional artifact paths, retain `historical_manifest_sequence=UNKNOWN`, `prior_snapshot_continuity=NOT_PROVEN`, and `historical_writer_attribution=NOT_VERIFIED`, and do not infer an unauthorized writer. The embedded original-manifest recovery/deep-equality claim, even if accepted as submitted evidence, establishes the original manifest contents, not durable byte recovery or historical continuity for the provisional patch captures. This is an honest limitation and the correct reason to keep protected-overlap status conditional; it does not satisfy a claim that continuity was proven. **R1 HIGH remains OPEN; RBL-04 remains CONDITIONAL.**

R2 is substantially specified and covers the required observable lifecycle: actual canonical metadata and JPEG hashing; immutable-object reopen/reverification; accepted-binding construction and row cross-check; execution creation only after verification; first-accept pre-row failure; accepted pre-execution capacity refusal; failed-retry unavailable binding/config; admitted execution/output-binding failure; restart interruption; final/legacy replay; and identity conflict. POST versus GET, persisted versus ephemeral bytes, retry eligibility, result nullability, IDs and no-latest/default fallback are stated. The authoritative row/binding verification order also addresses the prior copied-digest weakness. However, first-accept object/binding persistence, canonical verification and frozen-configuration failures are still collapsed into public `503 FROZEN_PROFILE_UNAVAILABLE`, while the matrix does not state whether those distinct causes share one externally observable wire code by contract or only share retryability. Before exact-spec acceptance, name the intentional public equivalence and retain distinct private diagnostics/audit outcomes; state the identity/body rule for every pre-row failure explicitly. Also preserve the existing requirement that `METADATA_HASH_MISMATCH` means a hash freshly computed over verified canonical metadata bytes. **R2 HIGH remains OPEN pending this narrow classification clarification; no implementation is accepted.**

R3 is addressed for specification scope: all four previously missing baseline entries now have BASE_HEAD/current hashes and clean status, and two concrete future Android JVM test paths are named without granting ownership. No implementation or test execution follows from this inventory.

R4 is addressed at specification level: the closed state table covers ABSENT, EXTRACTED, MALFORMED, empty extracted bytes, marker-observed/unobserved decode failure, nullability, disposition, transform/re-encode assertions, decoder evidence, result/stage placement at `ORIGINAL_IMAGE`, deep equality, refusal data policy and historical unknown compatibility. It remains a future implementation contract, not a passed behavior check.

R5 is substantially complete and now meets the requested field-to-response shape on paper. The explicit `PublicExecutionBinding` excludes private object references; producer authority, list/result/stages/artifacts locations, equality partners, source-map exactness, legacy refusal, multi-hit 409, manifest-before-byte gate and byte digest gate are specified. This resolves the previous ambiguity about copying accepted internal objects. Acceptance remains conditional on the narrow R2 classification clarification and later implementation proof: the revision does not establish that the current schemas or runtime emit these fields.

### PM four-item disposition

Chronology: partially addressed with explicit limits; continuity not proven. Transient POST/GET/state: substantially addressed, with the R2 public classification gap above. Four baseline paths/tests: addressed as inventory/specification. ICC state/schema: addressed as a closed specification contract. The clarification text is evidence for review only; no submitter statement, hash match or manifest entry is treated as implementation acceptance.

### Boundary and status

The unchanged patch remains preparation-only. `M2=NOT_STARTED`; no M1 Exit, business/source/docs/test implementation permission, runtime acceptance or end-to-end acceptance is granted. Existing RBL-01/02/03 and Android A-SEC-01/A-DIAG-01 remain open. This reviewer changed only the existing ACTIVE reviewer report and checks JSON; no D05 artifact, shared ledger, business file, credential or device state was changed.

BTW-CHECK: TODO_ID `RUN-20260918T043217Z-REVIEW-BASELINE：D05澄清版回到M1-D03独立复审`; Goal assess section 9 and manifest against PM four items and R1-R5; Files Changed existing reviewer report/checks only; Build Result N/A; Requirement Trace D05 report section 9, manifest chronology/lifecycle/ICC/projection, FILE_OWNERSHIP:16–20 and existing M1-D03 review; Test Result exact three supplied artifact SHA-256 checks, focused report/manifest reads, no start-reported original-prefix/manifest-deep-equality rerun; Artifact Evidence this section and companion checks entry; Known Limitations no implementation/runtime/device proof and provisional snapshot continuity not proven; Open Post-Funding Gates unchanged; Current MVP Blocker Remaining R1/R2 HIGH and RBL-04 conditional; `M2=NOT_STARTED`; M1 Exit NOT_GRANTED.

## M1-D05 second clarification re-review: R5 gate ownership

Same M1-D05, returned to the existing M1-D03 independent review and existing ACTIVE report/checks scope; no new task. The exact reviewed artifacts are report SHA-256 `73a8658eebd14110a4f3951df080dfb1ca0e669d28ee0bd041489899a1500531` (42,641 bytes), manifest SHA-256 `72a818ce2be0b3eb86560cfe790b809aeeee1cbe3d3eacada9f3264ab5bec45f` (29,328 bytes), and unchanged patch SHA-256 `c80055a2da264496b2998bc971f74afc07af69d6b9349da9c5ca79f657907325` (11,368 bytes). PM-SCOPE:210–220 and its JSON record PM's artifact hash/length, original-report-prefix, embedded-original-manifest recovery and `files` deep-equality checks; PM did not repeat patch reconstruction, and start did not execute those checks. They are attributed evidence, not acceptance.

### Independent disposition: CHANGES_REQUESTED; R5 remains open

**R1 — addressed as an explicit limitation, not cleared.** Section 9.1 and the manifest distinguish provisional and established captures, retain the established patch, and explicitly record volatile-only provisional sources, `historical_manifest_sequence=UNKNOWN`, `prior_snapshot_continuity=NOT_PROVEN`, and `historical_writer_attribution=NOT_VERIFIED`. This is sufficient evidence for M1 gap auditing because it does not overclaim continuity. It does not prove durable recovery or clear protected overlap; RBL-04 remains `CONDITIONAL`. No unauthorized writer is inferred.

**R2 — specification addressed.** Section 9.2 and the manifest give an observable first-accept authority/order and lifecycle matrix covering canonical metadata/JPEG hashing, object reopen, binding/row cross-checks, pre-row failure, accepted capacity refusal, failed-retry binding/config refusal, admitted execution/output-binding failure, restart interruption, final/legacy replay, identity conflict, POST/GET bytes, retry eligibility and execution identity. The same public code for the explicitly listed pre-row frozen-profile/persistence failures is an observable contract; no implementation acceptance is implied. The requirement that `METADATA_HASH_MISMATCH` be based on freshly hashed verified canonical metadata remains present.

**R3 — specification inventory addressed.** Four formerly absent baseline paths now have BASE_HEAD/current hashes and clean status, and two concrete Android JVM test paths are named. This neither registers business ownership nor proves the tests exist or ran.

**R4 — specification addressed.** The ICC union states legal ABSENT/EXTRACTED/MALFORMED/decode-failure combinations, empty extracted bytes, marker uncertainty, nullability, disposition, transform/re-encode claims, decoder evidence, `ORIGINAL_IMAGE` result/stage placement, deep equality, refusal behavior and historical unknown handling. This remains an implementation contract, not runtime proof.

**R5 — not addressed; the remaining blocker.** Section 9.5's fetch sequence is sound up to manifest retrieval: authenticate, exact list lookup, require one row, then fetch result/stages/artifacts JSON manifests before any artifact bytes. The public field allowlist, response locations, equality partners, legacy refusal and byte gate are also useful. However, manifest `public_diagnostics_projection.manifest_gate` is only `diagnostic auth + subject/expiry + exact bundle + complete public projection equality` and does not identify who performs that equality or against what authority. It is therefore ambiguous/circular: the client must fetch manifests to compare them, but “complete equality” could be read as a precondition that has to be satisfied before the manifests needed for comparison are available.

Required single clarification in the existing D05 report/manifest: separate the gates by owner and inputs. (1) **Server-side authority check:** Gateway compares each emitted result/stage/artifact manifest binding to the independently verified accepted row/binding and admitted execution authority before returning the manifest; server does not use client-fetched manifests as its own authority. (2) **Client-side cross-response check:** after the authenticated client fetches list, result, stages and artifacts manifests, it compares their declared public projections and descriptor relationships locally, before enabling byte downloads. State the exact failure response/state for server authority mismatch versus client cross-response mismatch, and retain no fallback/stale display. The structured `manifest_gate` must not make unavailable manifests a prerequisite to fetch those manifests.

### Final status

Overall D05 remains `CHANGES_REQUESTED`, narrowed to R5 gate ownership/comparator wording. R1–R4 are specification-addressed with explicit limitations; this is not implementation, runtime, device or business acceptance. Existing HIGH findings remain open, D04 runtime/device facts remain unknown/unaccepted, RBL-04 remains conditional, `M2=NOT_STARTED`, and M1 Exit is not granted. Only this existing reviewer report/checks scope is changed; no D05 artifact, patch, shared ledger, business file, credential or device state is modified.

BTW-CHECK: TODO_ID `RUN-20260918T043217Z-REVIEW-BASELINE：D05 section9第二次独立复审`; Goal independently assess R1–R5 and PM's remaining R5 ambiguity; Files Changed existing reviewer report/checks only; Build Result N/A; Requirement Trace D05 section 9, manifest public projection, PM-SCOPE:210–220, existing M1-D03 review and ACTIVE ownership; Test Result exact submitted artifact versions bound by supplied hashes and focused reads; PM prefix/recovery/deep-equality checks attributed and not rerun; Artifact Evidence this section and companion checks entry; Known Limitations no implementation/runtime/device proof, R1 continuity not proven; Open Post-Funding Gates unchanged; Current MVP Blocker Remaining R5 clarification and existing HIGH; `RBL-04=CONDITIONAL`; `M2=NOT_STARTED`; M1 Exit NOT_GRANTED.

Review-history clarification: lines 242–264 are the final assessment of the same submitted revision, not a second D05 submission. They supersede the interim R1/R2 blockers and R5-sufficient assessment at lines 216–240 without deleting that history. R1 explicitly permits recording unavailable history while retaining conditional overlap; section 9.2's matrix already fixes the public failure code/body, so the earlier request to declare that mapping again was unnecessary. The remaining exact-spec finding is R5 MEDIUM: specify gate owner, comparator and ordering. Original implementation HIGH remain OPEN independently of this specification disposition.

## M1-D05 final R5-only clarification review

Same existing M1-D03 assignment. Independent disposition: `SPECIFICATION_ADDRESSED_WITH_LIMITATIONS`. R5 is closed at specification level for section 10 and the four structured gates. This supersedes the R5-only `CHANGES_REQUESTED` disposition at lines 242–266 for this new artifact revision; all earlier review history remains intact. R2–R4 are not reopened, and R1's explicit limitations remain.

Reviewed report SHA-256 `82098374c48dfd6bf97cf5e0f1b3b5bfae6fb5119fa66cff6a5cf2b789f0f36f`, submitted length 47,402 bytes; manifest SHA-256 `0f158adbaf9c5ff4360bb84c7e02c8a0dc9abc6af962e36b575c88c1b45399f6`, submitted length 71,512 bytes; unchanged patch SHA-256 `c80055a2da264496b2998bc971f74afc07af69d6b9349da9c5ca79f657907325`, submitted length 11,368 bytes. Reviewer independently checked all three complete hashes. Preservation checks supplied with this submission remain attributed to PM: exact 42,641-byte prior-report prefix, restoration of the prior 29,328-byte manifest and original 7,960-byte revision, and files deep equality. These checks were not repeated or attributed to start.

The report at section 10 and manifest `public_diagnostics_projection` now answer the final finding:

- `server_manifest_return_gate` names Gateway, independently verified accepted row/canonical binding and admitted execution authority, complete projection/source-map/descriptor comparison, and explicitly requires no client manifest. Integrity failure returns HTTP 503 `DIAGNOSTICS_INTEGRITY_FAILED` without manifests or bytes; section 10 forbids backfill, execution switching and stale fallback.
- `client_cross_response_gate` occurs after the single list hit and schema-checked result/stages/artifacts JSON retrieval, before artifact-byte requests. Missing legacy fields produce local `LEGACY_BINDING_UNAVAILABLE`; disagreement produces `BINDING_MISMATCH`. Section 10 requires clearing rendered artifacts and selection, disabling downloads and no stale display. Thus cross-response equality no longer blocks fetching its own inputs.
- `server_byte_download_gate` independently repeats server authority and execution/membership/descriptor/object checks. Section 10 distinguishes authority integrity failure, subject-safe absent membership, missing object and corrupt object outcomes, with no returned bytes on failure.
- `client_downloaded_byte_check` compares media type, length, payload SHA-256 and `X-Content-SHA256` to the validated descriptor; failure blocks display/save and clears the payload object URL. The old ambiguous manifest gate is explicitly marked superseded.

No remaining R5 specification change is requested. This judgment rests on the report/structured-gate comparison, not inherited PM acceptance. R1 continuity remains `NOT_PROVEN`, writer attribution `NOT_VERIFIED`, RBL-04 `CONDITIONAL`, original implementation HIGH `OPEN`, D04 runtime/device `UNKNOWN_OR_UNACCEPTED`, M2 `NOT_STARTED`, and M1 Exit `NOT_GRANTED`. No implementation, business repair or device acceptance is granted.

BTW-CHECK: TODO_ID `RUN-20260918T043217Z-REVIEW-BASELINE`; Goal independently resolve the same D05 final R5-only clarification; Files Changed existing reviewer report and checks only; Build Result N/A for specification review; Requirement Trace prior finding at 242–266, D05 section 10 and four public-diagnostics gates; Test Result three complete SHA-256 matches and focused specification comparison, companion JSON validation; Artifact Evidence this section and `d05_final_r5_re_review`; Known Limitations no implementation/runtime/device tests, PM preservation checks attributed; Open Post-Funding Gates unchanged; Current MVP Blocker Remaining original implementation HIGH, conditional preservation boundary and unaccepted D04 evidence, no remaining R5 specification objection.

Evidence attribution supplement: PM-SCOPE:230–238 and JSON `d05_final_r5_pm_assessment` record PASS for complete artifact hashes/lengths, both report prefixes of 42,641 and 23,391 bytes, strict recovery/hash/length of embedded 29,328-byte and 7,960-byte manifests, and files deep equality against both. PM executed these checks; start did not; reviewer did not repeat them or patch reconstruction. The independent gate comparison and explicit disposition above remain unchanged. Meeting handoff at ROUNDS/20260918T043217Z-meeting.md:194–200 was read and the same-task boundary retained.
