# M1-D05 repair boundary and preservation evidence

PLAN_ID: `M1`  
DELIVERABLE_ID: `M1-D05`  
TASK_ID: `RUN-20260918T043217Z-REPAIR-BOUNDARY`  
Disposition: `REPORT_READY_FOR_REVIEW`; preparation only. `M2=NOT_STARTED`.

## 1. Authority and non-implementation boundary

This report incorporates:

- API audit SHA-256 `75384511fe2867d60cd13f46355c860f37fb9eecd4c67854e60293b926f450af`.
- REVIEW-BASELINE lines 130-176, verified SHA-256 `3b6e390a8350b5847561f07181c2b984bb68cdf0ff1ca0c4724ef81a4efe64bc`.
- PM-SCOPE lines 171 onward, verified Markdown SHA-256 `9fc7c043e36a9f622a08d2fbda633be659754a269c76b5f4cec717cb1670a547`; companion JSON SHA-256 observed as `db71cea0c2cdf0928d1aaadcbb9d0ca14a5a587d13241e6734465150f8d5c511`.
- Coordinator dependency graph at meeting lines 89-110.

No business source, credential, service, device, build, formatter, linter, test, upload, install or capture action was authorized or performed. Proposed ownership below is not edit permission. Frozen Android Bundle 1.5 / `dhea-capture/2.0` remains unchanged; no v3 DTO, alias, compatibility fallback or new HTTP hop enters this repair.

## 2. Preserved old diff and hash manifest

Baseline: `410b17a00b63374f5d28a5531c478db8b30e8427` plus pre-existing dirty work.

- Exact protected patch: `RUN-20260918T043217Z-REPAIR-BOUNDARY-old-tracked.patch`
- Patch SHA-256: `c80055a2da264496b2998bc971f74afc07af69d6b9349da9c5ca79f657907325`
- Patch size: `11368` bytes
- Structured manifest: `RUN-20260918T043217Z-REPAIR-BOUNDARY-manifest.json`
- Credential scan: `PASS_NO_MATCH` for private-key PEM markers, AWS access keys, GitHub tokens, bearer tokens and credential assignments. No raw credential value was read or persisted.

The patch preserves exactly four dirty paths: `docs/api/api-reference.md`, `python_gateway/dhea.py`, `python_gateway/dhea_input.py`, and `python_gateway/tests/test_dhea.py`. `python_gateway/tests/test_dhea.py` changed concurrently before and after the initial preservation attempt; the artifacts were refreshed and bind the final observed bytes at verification. Future implementation MUST re-read every target and compare its hash before editing. RBL-04 remains conditional until PM/reviewer accept this preservation and hunk ownership.

## 3. Exact proposed hunk ownership

| File / symbol | Later owner | Proposed repair, after explicit M2 assignment |
|---|---|---|
| `python_gateway/dhea.py::DheaStore.__init__` | API | Add immutable accepted-binding object reference and SHA; transactional first-accept persistence; no reconstruction from current runtime. |
| `python_gateway/dhea.py::DheaService.accept` | API | Build first accepted binding from persisted Gateway facts and actual loaded runtime; retries use persisted bytes/binding only; final replay bypasses Core; legacy unverifiable retry fails closed. |
| `python_gateway/dhea.py::DheaService.validate_result` | API | Compare Core output to the accepted binding supplied for that execution, including exact source-map membership and values. |
| `core/dhea.py::DheaRuntime.analyze/_analyze` | API/Core | Accept one validated internal request and independently compare it to the immutable accepted binding and actual loaded runtime before decode. No duplicate image allocation beyond decode input. |
| `core/dhea.py::_analyze` ICC decode block | API/Core | Observe marker/extraction state before tag removal, retain no raw ICC, perform no transform/re-encode, and populate result evidence even without a collector. |
| `core/dhea_diagnostics.py::Diagnostics.decoded` | API/Core | Copy the same ICC evidence object to decoded-stage metrics; record load failures truthfully. |
| `python_gateway/dhea_diagnostics.py::BINDING`, `binding`, `publish`, `snapshot` | API | Publish the complete accepted binding plus execution identity; never make diagnostics authoritative. |
| `python_gateway/dhea.py::measurement_list`, `diagnostic_subject`, `workbench` | API/Web | Exact `request_id` parsing, target 403 code, and credential-free shell. Authentication remains before query validation. |
| `python_gateway/dhea_diagnostics.py::measurement_list` | API/Web | Add exact `m.analysis_id=?` as an AND predicate while retaining unconditional subject and expiry predicates. |
| `python_gateway/workbench.html::loadHistory/checkBinding/loadBundle` | API/Web | Operator request-ID lookup, clear stale selection, and verify complete same-execution binding before render/download. |
| `python_gateway/dhea_export.py::export` | API | Add query/schema/binding fields and diagnostic error contract, then regenerate v2 outputs only. |
| `docs/api/openapi-dhea-v2.json`, `docs/api/schemas/dhea-v2.schema.json` | API | Generated v2 artifacts; never hand-edit or regenerate v3 artifacts incidentally. |
| `docs/LFA_最新完整文档集合/11_DHEA原生Android研究v2公开契约.md`, `docs/api/dhea-v2-app-integration.md` | API | Document accepted binding, exact query, auth/error mapping, ICC paths and missing semantics. |
| `Android_App/.../ResearchResultPanel.kt::DevDiagnosticsCard` | Android | Typed ICC display with missing/partial/legacy precedence; replace obsolete `/api/v2/lfa/diagnostics` instruction with `/workbench` and bundle-addressed workflow. |
| Focused tests in `tests/test_dhea.py`, `python_gateway/tests/test_dhea.py`, `python_gateway/tests/test_dhea_diagnostics.py`, Android panel tests | owning role | Observable contract cases listed below; no broad suites during this preparation task. |

Current baseline hashes and clean/dirty status are authoritative only in the adjacent manifest. The proposed symbols are the ownership boundary, not authorization to edit overlapping dirty code.

## 4. M1-B01: independent accepted binding

### 4.1 Authoritative object

On first acceptance, Gateway creates one canonical RFC 8785 JSON `AcceptedAnalysisBinding` from facts it independently owns or has verified, before execution:

```text
schema_version = dhea-accepted-binding/1.0
request_id = persisted analysis_id
capture_bundle_id
original_sha256
metadata_sha256
image_object + immutable object byte length
metadata_object + canonical_metadata_object
research_profile_id + research_profile_sha256
curve_config_id + curve_config_sha256
template_id + template_sha256
curve_schema_sha256
source_artifact_sha256 (complete exact key/value map)
measurement_bundle_id
feature_schema_id = dhea-green-area/1.0
core_version = dhea-core/2.0
```

Gateway persists canonical bytes, `binding_sha256`, and the object reference atomically with the measurement row. Blob/object reads verify stored byte length and SHA. The measurement row is authoritative for subject, expiry, object references and binding SHA; the immutable binding bytes are authoritative for accepted request/config identity. Diagnostics only copy this object and add `execution_id`; they are never authority.

The Core request carries both the typed accepted fields and `accepted_binding_sha256`. Gateway reconstructs it only from the persisted row, verified immutable objects and binding bytes. Incoming repeated POST fields may prove idempotency but never replace accepted authority. Core validates request against the independently supplied binding, then compares every configuration identity and the complete source-map membership/value set against its actual loaded `DheaRuntime`, before JPEG decode. Core does not query the database or own HTTP.

A required negative case holds accepted binding A fixed, supplies an otherwise valid request with B's `request_id`, bundle or metadata SHA, and proves refusal before decode/scientific stages. Comparing two copies derived from the same incoming request does not satisfy this case.

### 4.2 Lifecycle invariants

- First accept freezes the binding before execution and creates one `execution_id`.
- Completed/rejected replay returns persisted response bytes. No Core call, binding mutation or new `execution_id`.
- Failed retry first verifies the old accepted binding and exact runtime availability. If valid, it preserves request ID, capture identity, immutable object references and all frozen configuration; only then creates a new `execution_id`.
- A legacy completed/rejected row replays unchanged even without the new binding. It is never backfilled or re-executed.
- A legacy failed/processing row without a reconstructable verified binding cannot retry: `FROZEN_PROFILE_UNAVAILABLE`. No latest/default config fallback and no new execution.
- Diagnostics construction/publication failure cannot weaken any request/config comparison.

### 4.3 HTTP / wire / state / retry / replay matrix

| Class | Core/decode | HTTP | `wire_code` | `business_status` | `retryable` | `data` | Persisted effect | Retry/replay effect |
|---|---:|---:|---|---|---:|---|---|---|
| New valid accept | yes | 200 | Core result code | `completed` or scientific `rejected` | false | non-null Core result | Final response/object committed | Exact POST/GET returns same bytes; no execution |
| Existing final identity match | no | stored | stored | stored | stored | stored | None | Byte-identical replay; no new execution ID |
| Existing identity conflict from repeated POST | no | 409 | `IDEMPOTENCY_CONFLICT` | `rejected` | false | null | Existing row untouched | Correct original POST still replays/retries by stored state |
| Missing/corrupt binding or unavailable/mismatched frozen config before failed retry | no | 503 | `FROZEN_PROFILE_UNAVAILABLE` | `failed` | true | null | Existing failed row and frozen objects untouched | No execution ID; retry only after exact frozen runtime is available |
| Accepted internal request/binding mismatch, including swapped request/bundle/metadata | no | 503 | `FROZEN_PROFILE_UNAVAILABLE` | `failed` | true | null | Current execution records failed; accepted binding unchanged | Never scientific rejection; later retry still uses same binding and a new execution only after repair |
| Stored image bytes do not match accepted `original_sha256` | no | 200 | `IMAGE_HASH_MISMATCH` | `rejected` | false | non-null structured Core refusal | Final rejected response committed | Final replay only; no silent replacement or zero |
| Unexpected runtime exception after a valid binding | attempted as reached | 503 | `CORE_EXECUTION_FAILED` | `failed` | true | null | Failed response bound to current execution | Original POST may retry with same binding; new execution only |
| Interrupted persisted `processing` on restart | no automatic run | 503 | `EXECUTION_INTERRUPTED` | `failed` | true | null | Startup marks failed; binding unchanged | User-triggered original POST may retry after binding/runtime verification |
| Scientific geometry/signal refusal | yes | 200 | exact Core G/I/S/refusal code | `rejected` | false | non-null; missing metrics remain null | Final rejected result committed | Final replay only |
| Feature measured, concentration ineligible/model refusal | yes | 200 | exact Core code | `completed` | false | non-null; concentration null with reason | Valid feature retained | Final replay only; concentration failure never erases feature |

`IMAGE_HASH_MISMATCH` remains the existing structured Core refusal. This preserves current v2 external behavior; it MUST occur before image decode. Internal reason details such as `REQUEST_BINDING_MISMATCH`, `METADATA_HASH_MISMATCH`, `FROZEN_CONFIG_MISSING`, `FROZEN_CONFIG_MISMATCH`, `FEATURE_SCHEMA_MISMATCH` and `CORE_VERSION_MISMATCH` remain private diagnostic reason codes and MUST NOT create new public v2 codes.

Unknown retained for review: the current generic FastAPI `InputError` handler omits persisted request/capture identity. M2-D04 must return the 503 binding/config refusal through a measurement-aware service path so identity is retained without overwriting the authoritative prior result. Exact response-byte policy for repeated transient 503s is implementation-review material; the matrix above fixes observable status/state semantics.

## 5. M1-B03: ICC evidence contract

### 5.1 One observation, two paths

Core makes one immutable typed `icc_profile_evidence` object during original JPEG decode and places the same value at:

- Returned result: `data.diagnostics.image_decode_evidence.icc_profile_evidence`.
- Decoded stage: `stages[decoded].metrics.icc_profile_evidence`.

Result production is independent of the optional diagnostics collector. Gateway persists/replays the result unchanged. Diagnostics publication copies the value; it does not re-inspect the JPEG. Web consumes the decoded stage and checks it against the result value when both exist.

Required fields:

```text
embedded_icc_marker_present: boolean | null
icc_extraction_status: ABSENT | EXTRACTED | MALFORMED | DECODE_FAILED
icc_present: boolean | null
icc_byte_length: integer | null
icc_sha256: lowercase SHA-256 | null
icc_disposition: ABSENT | IGNORED_WITHOUT_TRANSFORM | NOT_EVALUABLE
icc_transform_applied: false | null
jpeg_reencoded: false | null
decoder_name: string | null
decoder_version: string | null
```

`icc_present=true` means Pillow successfully assembled non-empty ICC bytes. It does not mean a valid color profile or color accuracy. Embedded marker detection is separate: marker present plus extraction failure is `MALFORMED`, never verified absence. `icc_byte_length` and SHA are present only for `EXTRACTED`; raw ICC bytes are never returned or persisted. Decoder name/version are actual runtime values, never defaults.

The source JPEG bytes and `original_sha256` remain immutable. No ICC transform, JPEG re-encode or app-side color processing is introduced. `jpeg_reencoded=false` describes the original analysis input; separately encoded diagnostic previews do not contradict it and cannot replace the original.

A successful `Image.open` is not a successful decode. If `image.load()` fails, no decode PASS or normal result evidence is emitted: the decoded stage, when a collector exists, is FAIL/ERROR with `DECODE_FAILED`; the existing image refusal path remains authoritative. No result is fabricated when `data` is null.

### 5.2 Android typed semantics and precedence

Android reads the new result path first. Legacy `diagnostics.image.icc` is used only when the entire new object is absent and every legacy field required for a displayed assertion has the expected JSON type. If both paths exist, new path wins; disagreement is shown as `UNKNOWN/NOT_REPORTED` plus diagnostic inconsistency, never silently merged.

- Whole object missing: all ICC/transform/re-encode/decoder claims `UNKNOWN/NOT_REPORTED`.
- Partial object, explicit null, invalid enum, string boolean, invalid SHA/length, or inconsistent field combination: affected claim `UNKNOWN/NOT_REPORTED`.
- Explicit typed `icc_present=false` plus `ABSENT` establishes absence.
- Explicit typed false is distinct from missing. Missing must never render `PASS: ICC_ABSENT`, `NO`, or `Pillow`.
- `MALFORMED` is not absence; `EXTRACTED` proves extraction only, not profile validity.

Android owns this parsing/display repair and the stale route text in `ResearchResultPanel.kt`: the operator instruction must point to `/workbench`, then the exact request-ID/bundle workflow, not nonexistent `/api/v2/lfa/diagnostics`. API owns the actual workbench route.

Focused producer/consumer cases: extracted ICC, explicit no ICC, marker-present malformed/split ICC, missing object, partial object, wrong JSON types, legacy-only complete evidence, conflicting new/legacy evidence, collector absent, collector publication failure, and full-decode failure. Synthetic ICC proves extraction handling only, not profile validity or color accuracy.

## 6. M1-B02: exact request-ID diagnostic lookup

This extension is already `IN_SCOPE_FOR_M1_SPEC_AND_M2_D05_REPAIR`; it is not re-decided here.

```http
GET /api/v2/lfa/measurements?request_id=<analysis_id>&limit=2&offset=0
```

- `request_id` means persisted `analysis_id` only: one lowercase canonical UUID value, maximum 36 bytes.
- Empty, malformed, uppercase/noncanonical, too long or repeated values return HTTP 422 / `DIAGNOSTICS_QUERY_INVALID`.
- Diagnostic authentication executes before query validation.
- Missing/invalid diagnostic credential: 401 / `UNAUTHENTICATED`.
- Ordinary App/result credential: 403 / `DIAGNOSTICS_FORBIDDEN`. This is the authoritative frozen research-v2 contract. Current `FORBIDDEN`/403 is an explicit M2-D05 wire migration affecting handler, schema/docs and endpoint tests; it MUST NOT change incidentally inside parser work.
- `request_id` combines with `bundle`, `device_model`, `device_instance_id`, `status`, `limit` and `offset` using AND. Conflicts return zero rows; no fallback/fuzzy/alternate result.
- Caller-supplied pagination is retained. Workbench explicitly sends `limit=2&offset=0` with no stale device/status filters to detect impossible duplicates.
- `subject_hash=?` and `expires_at>now` remain unconditional storage predicates. Zero rows intentionally conflates nonexistent, other-subject and expired records; it reveals no distinction. Bundle-addressed resource 404/410 behavior remains separate.
- More than one exact row is an integrity error and must not select either.

### 6.1 Same-execution browser proof

Starting only from operator-supplied request ID, workbench must clear any previous selection/artifacts, resolve exactly one list row, then fetch the existing bundle `/stages` and `/artifacts` resources. Before render or download it verifies equality across list/result/stages/artifacts for:

```text
request_id = analysis_id; execution_id; capture_bundle_id;
original_sha256; metadata_sha256;
research_profile_id/SHA; curve_config_id/SHA; template_id/SHA;
curve_schema_sha256; complete source_artifact_sha256 map;
measurement_bundle_id; feature_schema_id; core_version
```

Zero, multiple, stale selection, wrong execution, expired/other-subject, or any binding mismatch clears the UI and blocks artifact requests. A retry changing `execution_id` cannot combine old stages with new artifacts.

### 6.2 Shell and token boundary

Target shell is static and credential-free. `GET /` and `/workbench` returns no private data and MUST NOT inject a configured/default bearer into HTML, DOM, JavaScript, URL, storage or logs. The operator supplies a diagnostic token into page memory; it is used only in Authorization headers and cleared on reload. Diagnostic credentials remain separate from App/result credentials.

Current source has token auto-selection/injection. This is a source-based boundary concern, not proof of live credential disclosure. Shell/token inspection is credential-safe evidence only; no live secret was read, no leak is claimed, and no rotation/production-permission action is authorized. Future proof uses a non-secret sentinel in an isolated app instance plus static source/APK checks; a real credential must never be embedded in source, rendered shell or APK. Removing source bootstrap alone is insufficient if build injection still embeds a secret.

Affected maintained artifacts: `python_gateway/dhea.py`, `dhea_diagnostics.py`, `workbench.html`, `dhea_export.py`, v2 OpenAPI/schema, frozen contract and app integration guide. v3 outputs remain untouched.

## 7. Approved dependency graph and shared mutation order

| Deliverable | Owner | Prerequisite | Observable exit |
|---|---|---|---|
| M2-D01 | Android | M1 Exit and explicit assignment | Source/APK contain no embedded credential; explicit local configuration survives; credential-safe proof only. |
| M2-D02 | API/Core | M1 Exit; approved Core hunks | Same ICC evidence in result and decoded stage without collector dependency; original bytes/hash retained; malformed/decode failure truthful. |
| M2-D03 | Android | D02 producer contract | Typed missing/null/invalid/legacy UI behavior and corrected operator route; focused consumer checks. |
| M2-D04 | API/Core | M1 Exit; accepted preserved Gateway baseline and M1-B01 | Independent binding and full runtime comparison; complete matrix verified; legacy final replay and unverifiable retry behavior proven. |
| M2-D05 | API/Web; Android guidance already in D03 | D04 and M1-B02 disposition | Exact request-ID lookup, auth/subject/expiry/filter integrity, `DIAGNOSTICS_FORBIDDEN`, credential-free shell, v2 schema/docs and browser proof. |
| M2-D06 | PM + independent review | D01-D05 proof and exact integrated diff | HIGH findings disposition and repair integration accepted; no live/device inference. |

API serializes shared Core mutations: D02 completes and is checked before D04 re-reads and edits `core/dhea.py`. D04 completes before D05 touches shared Gateway files. No concurrent editing permission is created. Android D01/D03 require one Android owner and their stated prerequisites.

M3 owns revision-bound live service/runtime/device evidence. M4 owns laboratory provenance, nullable real reference values and verified same-card repeatability. A15 does not require non-null laboratory concentration. Production YOLO, broad devices/backgrounds, regulation, clinical validation and formal production release remain `POST_FUNDING_GATE`, non-blocking for this preparation.

## 8. Risks and explicit unknowns

- No concrete M2 diff has been reviewed or accepted; all HIGH findings remain open.
- Current dirty files can continue changing. Every M2 owner must re-read and re-hash before editing.
- Database migration/transaction mechanics for the binding object remain implementation design, constrained by the authority and lifecycle above.
- Exact transient 503 response-byte persistence policy is noted in section 4.3 and requires implementation review; accepted identity/state semantics are fixed.
- Existing result schema does not yet declare the ICC fields; exact schema placement and validation are M2-D02 work.
- No live diagnostic credential disclosure was established. No live shell, token, service or APK was inspected in this task.
- No real-device, live API, ICC validity, color accuracy, laboratory or repeatability claim is made.

## BTW-CHECK

TODO_ID: `RUN-20260918T043217Z-REPAIR-BOUNDARY`  
Goal: Preserve overlapping dirty work and specify exact M2 repair boundaries without implementation.  
Files Changed: This report, protected old tracked patch, structured manifest only.  
Build Result: N/A; preparation task explicitly prohibited builds and business implementation.  
Requirement Trace: Formal task meeting lines 73-87; coordinator graph lines 89-110; PM-SCOPE lines 157-179 plus companion JSON; REVIEW-BASELINE lines 130-176; API audit SHA above.  
Test Result: No tests rerun by instruction. Evidence verification is limited to exact patch generation, SHA-256, credential-pattern scan, source/report comparison and report structural checks. Prior role-host test outputs are historical inputs only and are not re-claimed here.  
Artifact Evidence: This report; patch SHA `c80055a2da264496b2998bc971f74afc07af69d6b9349da9c5ca79f657907325`; adjacent structured manifest.  
Known Limitations: No implementation, behavioral test, live auth/service/device proof or reviewer acceptance; explicit unknowns in section 8.  
Open Post-Funding Gates: Production YOLO/generalization, broader devices/backgrounds, human factors, multi-lot/independent validation, regulation, clinical/commercial release and monitoring remain future gates.  
Current MVP Blocker Remaining: M1-D05 dual acceptance, M1 Exit, then open M2 HIGH repairs and later M3/M4 real evidence. `M2=NOT_STARTED`; RBL-04 remains conditional.

## 9. Clarification revision for PM and independent review R1-R5

This section is append-only relative to the independently reviewed original report: the first 23,391 bytes remain byte-identical with SHA-256 `b03dbe6c37530755edc90b577dc249dbcc70f560a2f7328b3719e3a6a7a8495d`. It addresses PM-SCOPE lines 181-198 (assessment SHA-256 `90429dbd7e0937d6ce7123e6e8b7391696f9ada704f82b23866c107bbe307002`) and REVIEW-BASELINE lines 178 onward. The submitted patch remains byte-for-byte unchanged: 11,368 bytes, SHA-256 `c80055a2da264496b2998bc971f74afc07af69d6b9349da9c5ca79f657907325`. This revision is specification evidence only; `M2=NOT_STARTED`, no M1 Exit or implementation permission is implied, and RBL-04 remains conditional.

### 9.1 R1 preservation chronology and limits

Ordered captures:

1. The first **provisional** patch was captured from BASE_HEAD plus the then-observed four dirty files. Exact bytes remain recoverable only from this role session's persistent evaluation-kernel variable `patch`: 11,943 bytes, SHA-256 `ecfbf13ff5789c9d67b7be3ba31355e1e56d68fa8cb7b2ba1baf66b208e2b2b1`. `artifact://54` is a rendered tool-output copy of the visible diff, 11,942 bytes, SHA-256 `a2aa2c079ef5fe57c89951b8bf0aa2688c57144179d022c66d5012be80ddfb5c`; it is not byte-identical and not an established preservation artifact. No repository path was registered for this provisional capture.
2. After a concurrent `python_gateway/tests/test_dhea.py` change, a second **provisional** refresh was captured. Exact bytes remain recoverable only from evaluation-kernel variable `patch_now`: 11,355 bytes, SHA-256 `87f416cb447a599899c23e53c02fb401903239df9e69284b26bc48bd06550c52`. It temporarily occupied the eventual patch path before ownership registration, then was superseded after a second detected change. It has no separate registered path.
3. After the second concurrent test-file change, the **established** capture was produced: 11,368 bytes, SHA-256 `c80055a2da264496b2998bc971f74afc07af69d6b9349da9c5ca79f657907325`. It is the only submitted preservation patch and is registered at `herdr-team/.agent-control/EVIDENCE/RUN-20260918T043217Z-REPAIR-BOUNDARY-old-tracked.patch`. `artifact://62` is only a rendered view. PM later reconstructed all four files from this patch and BASE_HEAD and matched the submitted manifest; that check is attributed, not rerun here.
4. The original report and manifest were finalized against the established capture, verified, submitted, independently reviewed, and only then registered `ACTIVE`. No established-patch write occurred after registration.

The first two exact patch byte strings are volatile session state, not durable registered artifacts; long-term recovery is not guaranteed. No byte-identical provisional manifest or prior provisional manifest SHA/length is known to survive. The historical manifest sequence is therefore `UNKNOWN`, and no hash alone is presented as recovery. Historical writer attribution is `NOT_VERIFIED`: the four source diffs are captured pre-existing/concurrent work, not evidence that this task wrote them and not evidence of unauthorized writing. RBL-04 remains conditional.

The D05 task's actual repository write set is the three registered paths only: this report, the manifest and the established patch. They are untracked, so Git has no committed task-before blobs and cannot supply a native before/after diff. Available write evidence is tool history, recorded byte counts/hashes, mtimes, the independently bound original report/manifest versions, the unchanged patch digest, and FILE_OWNERSHIP. This does not prove what unrelated external processes wrote.

### 9.2 R2 accepted binding verification and complete observable lifecycle

#### 9.2.1 First-accept authority and verification order

Before creating an accepted row or `execution_id`, Gateway MUST perform this order:

1. Validate transport and frozen v2 metadata. Compute RFC 8785 canonical metadata bytes from the parsed metadata object; compute `metadata_sha256` from those actual bytes, not from an incoming/copied digest. Compute original JPEG byte length and SHA from the received immutable bytes and require equality with `metadata.original_sha256`.
2. Persist immutable image, raw metadata and canonical metadata objects; re-open each object and verify byte length/SHA. The canonical object bytes MUST equal the freshly computed canonical bytes, and hashing those verified bytes MUST reproduce `metadata_sha256`.
3. Resolve the exact loaded runtime configuration; never latest/default. Build canonical RFC 8785 accepted-binding bytes from verified row candidates, verified object facts and actual loaded runtime facts. Compute `accepted_binding_sha256` from those canonical binding bytes.
4. In one acceptance commit, persist row root identity (`subject_hash`, `request_id=analysis_id`, `capture_bundle_id`, image/metadata digests, immutable object references, frozen configuration IDs/hashes), binding object reference, binding byte length and `accepted_binding_sha256`. Re-open binding bytes; verify length/SHA; parse/canonicalize; require byte-identical canonical form.
5. Cross-check row root against binding field-by-field: request/bundle IDs, image SHA/length, metadata SHA, every private object reference, every frozen config ID/hash, complete source-map membership/values, measurement bundle, feature schema and Core version. A self-consistent binding that disagrees with the independently persisted row root is invalid and cannot replace the row.
6. Construct the internal request only from the verified row/objects/binding. Set `request.accepted_binding_sha256` to the verified binding-byte SHA. Core first checks request SHA against independently supplied canonical binding bytes, then typed request fields against that binding, then binding configuration against the actually loaded runtime, all before decode.
7. After Core returns, Gateway validates output identity/config fields against the same verified row and binding before storing a result. Diagnostics are not part of this authority chain.

Private mismatch reasons remain diagnostic only. `METADATA_HASH_MISMATCH` specifically means a mismatch involving SHA-256 freshly calculated over verified canonical metadata-object bytes, not two copied digest fields. First-accept persistence or verification failure rolls back the row/object-reference acceptance transaction; unreferenced immutable blobs MAY be garbage-collected later but are never treated as accepted evidence.

#### 9.2.2 POST, GET, replay, persistence and execution matrix

An **ephemeral** response is returned for one request but does not replace authoritative row response bytes. A **persisted** response is stored on the row and returned byte-for-byte by later GET/replay. Once a row exists, all service-generated responses carry its `request_id=analysis_id` and `capture_bundle_id`; repeated POST input never changes accepted identity.

| Case | Immediate POST | Subsequent GET | Repeated identical POST | Persisted row/result bytes and state | Execution/identity |
|---|---|---|---|---|---|
| First accept fails before atomic row acceptance: object/binding persistence, canonical verification or frozen config failure | 503 `FROZEN_PROFILE_UNAVAILABLE`, `failed`, retryable, `data=null`; no fabricated request ID | No row: normal subject-bound not-found | New first-accept attempt after exact prerequisite repair | Ephemeral response; no accepted row, binding, response or result object | No `execution_id`; no accepted identity; Core not called |
| First accept is atomically accepted, then pre-execution capacity/admission refusal | 503 `ANALYSIS_CAPACITY`, `failed`, retryable, `data=null`, accepted request/bundle IDs | Exact persisted 503 | Verify original inputs/binding; retry when capacity exists | Persist exact 503 as row response; state `failed`; result object null; immutable inputs/binding retained | Refused attempt has no execution; first admitted retry creates first `execution_id` |
| Failed retry cannot verify stored binding/config, including legacy failed/processing row without reconstructable binding | 503 `FROZEN_PROFILE_UNAVAILABLE`, `failed`, retryable, `data=null`, existing IDs if known | Existing persisted failed/interrupted bytes remain authoritative and may differ from ephemeral POST refusal | Repeats verification; no latest/default fallback | Ephemeral refusal does not overwrite row, prior response/result, binding or state | No new execution; Core not called |
| Verified failed retry receives pre-execution capacity refusal | 503 `ANALYSIS_CAPACITY`, `failed`, retryable, `data=null`, same IDs | Exact newly persisted 503 | Later identical original POST may retry | Persist 503; state remains `failed`; result null; immutable inputs/binding unchanged | No new execution for refusal; later admission creates one new ID |
| Admitted execution throws or output binding validation fails | 503 `CORE_EXECUTION_FAILED`, `failed`, retryable, `data=null`, same IDs | Exact persisted 503 | Re-verify then start a new execution; no reuse of failed output | Persist failed response bound to attempt; state `failed`; result object null; binding/inputs unchanged. Invalid output is never stored as result | Failed attempt has one `execution_id`; each admitted retry gets exactly one new ID |
| Restart finds persisted `processing` | No automatic POST | GET returns exact persisted startup replacement 503 `EXECUTION_INTERRUPTED`, failed/retryable | Original POST verifies then may retry | Startup atomically persists interrupted bytes and `failed`; binding/inputs unchanged | No startup execution; admitted retry gets new ID |
| Final completed or scientific-rejected row, including legacy final | Repeated POST returns exact stored HTTP/body after identity match | Exact stored bytes | Exact replay | Final response/result/state immutable | No Core call; no new execution |
| Repeated POST conflicts with accepted identity | Ephemeral 409 `IDEMPOTENCY_CONFLICT` | Existing persisted response unchanged | Correct original POST follows stored-state rule | No mutation | No execution |

A legacy row without persisted request identity is never assigned one retroactively. A retry never changes request ID, capture identity, object references, hashes or frozen configuration. Serialization and transaction mechanics may vary only if these observable outcomes remain exact.

### 9.3 R3 complete proposed-path baseline and Android tests

The original manifest `files` snapshot remains unchanged. The following supplemental proposed paths are all clean against BASE_HEAD; baseline and observed-current SHA-256 are identical:

| Path | BASE_HEAD/current SHA-256 | Dirty |
|---|---|---:|
| `python_gateway/dhea_export.py` | `a3bfe119ec611fc64485417bf11e371a090e9860c03a46c432c52206208a5a69` | no |
| `docs/LFA_最新完整文档集合/11_DHEA原生Android研究v2公开契约.md` | `1c648f525aa41bf2fc27e2bff762df00a8f52a53ae09f70a9ca319bc0e53720d` | no |
| `docs/api/dhea-v2-app-integration.md` | `16a9a6d3c3d13e1279f4d98426043e9712f3852c8ed3ca98bf29fbac6bdee23b` | no |
| `Android_App/app/src/main/java/com/example/ui/screens/ResearchResultPanel.kt` | `978a85b095f9f68c0b7c9f7785d278adb6a171706d1792048d7b79c40fc9fb76` | no |

Exact future Android test paths: `Android_App/app/src/test/java/com/example/ui/ResearchResultPanelTest.kt` covers typed ICC missing/null/partial/invalid/legacy/conflict states and corrected workbench guidance; `Android_App/app/src/test/java/com/example/network/DheaContractTest.kt` covers result-path wire parsing. No instrumentation-test path is proposed. These are inventory facts, not ACTIVE business ownership.

### 9.4 R4 ICC state union and concrete schema placement

New producer objects are complete; all listed fields are required. JSON `null` is explicit.

| Status | marker | `icc_present` | length/SHA | disposition | transform/re-encode | decoder |
|---|---|---|---|---|---|---|
| `ABSENT` | `false` | `false` | both null | `ABSENT` | both false | actual non-empty name/version |
| `EXTRACTED` | `true` | `true` | integer >0 and lowercase 64-hex SHA | `IGNORED_WITHOUT_TRANSFORM` | both false | actual non-empty name/version |
| `MALFORMED` | `true` | null | both null | `NOT_EVALUABLE` | both false | actual non-empty name/version |
| `DECODE_FAILED`, marker observation completed | observed boolean | null | both null | `NOT_EVALUABLE` | transform null; re-encode false | actual non-empty name/version when known, otherwise both null |
| `DECODE_FAILED`, marker not observed | null | null | both null | `NOT_EVALUABLE` | transform null; re-encode false | actual non-empty name/version when known, otherwise both null |

Empty extracted bytes are `MALFORMED`, never `EXTRACTED`. `ABSENT` requires completed marker inspection. `DECODE_FAILED` never asserts ICC presence/absence. `jpeg_reencoded=false` remains known because Core never rewrites input; transform is null because applicability was not evaluable.

`python_gateway/dhea_input.py::CORE_RESULT` gains `data.diagnostics.image_decode_evidence.icc_profile_evidence`, validated by a closed `oneOf` union of the rows above (`additionalProperties=false`, exact required names, positive length and SHA pattern). It is required when `data` is non-null and decode was attempted. A structured image refusal after marker observation/load failure carries the `DECODE_FAILED` object in non-null `data`; a refusal with `data=null` or before decode evidence exists carries no fabricated object. Historical results may omit it and consumers render unknown.

`core/dhea_diagnostics.py::Diagnostics.decoded` places the deeply equal object at stage ID `ORIGINAL_IMAGE`, `metrics.icc_profile_evidence`. `ABSENT`/`EXTRACTED` allow stage PASS; `MALFORMED` is WARN; `DECODE_FAILED` is FAIL/ERROR under existing vocabulary. The result object is created before optional collector publication; collector absence/failure cannot remove it. `python_gateway/dhea_diagnostics.py::STAGE` gains the typed conditional for `ORIGINAL_IMAGE`; generated v2 schema/OpenAPI expose the result and stage unions. Legacy precedence remains section 5.2.

### 9.5 R5 explicit public projection and field-to-response contract

The private accepted binding contains storage references (`image_object`, `metadata_object`, `canonical_metadata_object`, private binding object reference/length). These fields MUST NEVER appear in public diagnostics, list/result/stages/artifacts descriptors, HTML or downloads. Diagnostics publish a separately constructed `PublicExecutionBinding`, not a copy-minus-later operation:

```text
request_id, analysis_id, execution_id, capture_bundle_id,
original_sha256, metadata_sha256,
research_profile_id, research_profile_sha256,
curve_config_id, curve_config_sha256,
template_id, template_sha256, curve_schema_sha256,
source_artifact_sha256, measurement_bundle_id,
feature_schema_id, core_version, accepted_binding_sha256
```

Producer/response/equality contract:

| Field | Authoritative producer | Public locations | Required comparisons |
|---|---|---|---|
| request/analysis ID | accepted row | list item `request_id` + `analysis_id`; result `analysis_id`; stages/artifacts `binding.request_id/analysis_id` | all equal |
| `execution_id` | admitted diagnostic execution row | list item; result top-level diagnostic projection; stages/artifacts binding | all equal; null only for legacy/unavailable policy below |
| capture bundle | accepted row | list item; result; stages/artifacts binding | all equal |
| original/metadata SHA | verified row/object facts | list item; result; stages/artifacts binding | all equal |
| profile ID/SHA | accepted binding + loaded runtime | list item public binding; result `data`; stages/artifacts binding | all equal |
| curve ID/SHA, template ID/SHA, curve schema SHA | accepted binding + loaded runtime | list item public binding; result `data`; stages/artifacts binding | all equal |
| complete source-artifact SHA map | accepted binding + loaded runtime | list item public binding; result `data.source_artifact_sha256`; stages/artifacts binding | exact key set and values equal |
| measurement bundle, feature schema, Core version | accepted binding + loaded runtime | list item public binding; result `data`; stages/artifacts binding | all equal |
| accepted binding SHA | verified canonical binding bytes + row root | list item public binding; result top-level diagnostic projection; stages/artifacts binding | all equal; never substitutes for field comparisons |

`LIST_ITEM` gains `request_id`, `execution_id` and a typed `binding` public projection. `CORE_RESULT` gains missing `curve_config_sha256`, `template_sha256`, `curve_schema_sha256`; result top-level diagnostic projection gains `execution_id` and `accepted_binding_sha256` without changing frozen measurement science fields. `BINDING`, `DIAGNOSTICS`, `ARTIFACTS`, generated v2 schema/OpenAPI, frozen contract and app integration guide declare the same projection.

Legacy/missing policy: if any required public field is absent, null where prohibited, or inconsistent, workbench shows `LEGACY_BINDING_UNAVAILABLE`/`BINDING_MISMATCH`, clears selection and performs no byte download. It never backfills from current runtime or mixes executions. Zero exact matches keeps the existing privacy-preserving empty result. More than one `request_id` match returns observable HTTP 409 `DIAGNOSTICS_INTEGRITY_ERROR`, no selected row, no fallback and no stale display.

Fetch gates are ordered: authenticate; exact list lookup with `limit=2`; require exactly one row; fetch result metadata and the `/stages` and `/artifacts` JSON manifests/descriptors only; validate schemas and every comparison above, including identical execution and descriptor SHA/size; only then enable `GET .../artifacts/{artifact_id}`. Each downloaded byte payload is independently checked against the already validated descriptor SHA/size and response `X-Content-SHA256`; mismatch blocks display/save with `ARTIFACT_INTEGRITY_FAILED`. Manifest retrieval is therefore necessary for validation and is distinct from artifact-byte download.

### 9.6 Revised risks and BTW-CHECK

Historical snapshot continuity remains unproven beyond the chronology above; writer attribution is `NOT_VERIFIED`. No implementation, behavior test, PM reconstruction rerun, live API, credential, build or device action occurred. Existing HIGH remain open; RBL-04 remains conditional.

BTW-CHECK: TODO_ID `RUN-20260918T043217Z-REPAIR-BOUNDARY`; Goal answer PM and independent R1-R5 clarification requests; Files Changed append-only report plus structured manifest revision, established patch unchanged; Build Result N/A; Requirement Trace PM-SCOPE:181-198 and REVIEW-BASELINE:178 onward; Test Result original report prefix/hash verified, original manifest recovery verification required, patch SHA/bytes unchanged, four missing paths hashed/status checked; Artifact Evidence this appended section and manifest revision history; Known Limitations no durable provisional manifest/patch paths, no historical writer attribution, no implementation/runtime proof; Open Post-Funding Gates unchanged; Current MVP Blocker Remaining independent/PM acceptance, M1 Exit, then separately authorized M2 repairs. `M2=NOT_STARTED`.

## 10. Final R5 clarification: manifest and byte gate ownership

This append-only clarification is bound to the independently re-reviewed revision: report 42,641 bytes / SHA-256 `73a8658eebd14110a4f3951df080dfb1ca0e669d28ee0bd041489899a1500531`, manifest 29,328 bytes / SHA-256 `72a818ce2be0b3eb86560cfe790b809aeeee1cbe3d3eacada9f3264ab5bec45f`, and unchanged patch 11,368 bytes / SHA-256 `c80055a2da264496b2998bc971f74afc07af69d6b9349da9c5ca79f657907325`. `REVIEW-BASELINE:242-266` is the final assessment; its withdrawal of the intermediate R1/R2 objections and its R1 limitation remain controlling. R1 continuity is `NOT_PROVEN`, writer attribution is `NOT_VERIFIED`, and RBL-04 remains `CONDITIONAL`. R2-R4 are specification-addressed and are not reopened.

The two gates have different owners, inputs and failure effects:

1. **Server manifest-return gate.** For each authenticated result, `/stages` JSON manifest and `/artifacts` JSON manifest request, Gateway independently loads the subject/expiry-bound accepted row, verified canonical accepted-binding bytes and row `accepted_binding_sha256`, and the currently admitted execution record. Before returning that response, Gateway constructs its public projection from those server-side authorities and compares every projected field, complete source-map membership/value, execution ID and artifact descriptor relationship against the stored response/manifest being emitted. It does not use, require or trust any manifest previously fetched by the client. Missing private authority, non-canonical/corrupt binding bytes, row/binding/execution disagreement or emitted-projection mismatch returns HTTP 503 `DIAGNOSTICS_INTEGRITY_FAILED`, with no manifest/descriptors or artifact bytes in the response. The server does not synthesize/backfill fields, switch execution or fall back to stale diagnostics.
2. **Client cross-response gate.** After authentication and the exact `request_id` list query returns exactly one row, the client may fetch the result plus `/stages` and `/artifacts` JSON manifests. Only after all four JSON responses exist and pass their schemas does the client compare their public projections and descriptor relationships locally. This comparison is not a prerequisite for fetching those JSON documents; it is the prerequisite for enabling any artifact-byte request. Missing/legacy public fields produce local `LEGACY_BINDING_UNAVAILABLE`; any cross-response field, execution, complete source-map or descriptor mismatch produces local `BINDING_MISMATCH`. Either outcome clears current selection/rendered artifacts, revokes download controls, performs no artifact-byte request, and permits no fallback or stale display.
3. **Server byte-download gate.** A later artifact-byte request independently repeats diagnostic authentication, subject/expiry/bundle checks and server accepted-authority comparison; it additionally requires exact execution ID, artifact membership, descriptor SHA/size/media and immutable object digest equality. Failure before bytes are opened returns HTTP 503 `DIAGNOSTICS_INTEGRITY_FAILED`; missing membership remains the existing subject-safe not-found outcome; stored bytes missing or digest/size mismatch returns existing `ARTIFACT_UNAVAILABLE` or `ARTIFACT_INTEGRITY_FAILED`. No bytes are returned on failure.
4. **Client downloaded-byte check.** Only after the client cross-response gate passes may bytes be requested. The client then compares received media type, length, payload SHA-256 and `X-Content-SHA256` against the already validated descriptor. Failure is local `ARTIFACT_INTEGRITY_FAILED`, blocks display/save and clears any object URL for that payload.

Accordingly, `public_diagnostics_projection.server_manifest_return_gate` is a server comparison against independently verified accepted authority; `client_cross_response_gate` occurs post-JSON-fetch and pre-byte-download. Neither gate makes an unavailable client-fetched manifest a server fetch prerequisite.

BTW-CHECK: TODO_ID `RUN-20260918T043217Z-REPAIR-BOUNDARY`; Goal close only final D05 R5 comparator/ownership ambiguity; Files Changed append-only report and structured manifest supplement, patch unchanged; Build Result N/A; Requirement Trace `REVIEW-BASELINE:242-266` and `checks.d05_clarification_re_review`; Test Result reviewed report/manifest revision retained as prefix/recoverable history and patch digest unchanged; Artifact Evidence this section and manifest gate fields; Known Limitations R1 continuity NOT_PROVEN, writer NOT_VERIFIED, no implementation/runtime/device proof; Open Post-Funding Gates unchanged; Current MVP Blocker Remaining independent/PM exact-spec acceptance and existing implementation HIGH. `RBL-04=CONDITIONAL`; `M2=NOT_STARTED`; M1 Exit NOT_GRANTED.

## 11. M1-D05-REQ-01 credential-bootstrap boundary and authoritative mapping

The previous revision specified the M2-D01 Exit but materially omitted the exact Android source and focused-test boundary needed to make that Exit executable: section 3 did not name the credential-bootstrap hunk, section 7 was generic, section 9.3 covered ICC/result parsing only, and section 6.2's sentinel/APK language applied to the Web shell. This documentary supplement records only that missing boundary. It is based on credential-safe source/symbol inspection and consultation with the existing Android owner; no credential value, live configuration, service, APK, network, device or rotation action was read or exercised.

### 11.1 A-SEC-01 exact future hunk and focused checks

After M1 Exit and an explicit M2-D01 assignment, the Android owner removes the complete constructor `init` bootstrap at `Android_App/app/src/main/java/com/example/network/DheaClient.kt::DheaClient.init` (currently lines 50-63). It MUST NOT replace it with another embedded default, `BuildConfig` or resource secret, compiled environment fallback, automatic write, or overwrite of an existing `connection.enc`. The same bounded repair preserves these existing paths and behavior:

- `DheaClient.isConfigured`: reports only whether an explicitly imported configuration exists.
- `DheaClient.importConfiguration(Uri)`: remains the sole provisioning entry and continues to accept only a content URI.
- `DheaClient.configuration(JSONObject)`: remains the common strict schema, origin and token validation boundary.
- `DheaClient.readConfiguration` and `DheaClient.key`: retain authenticated encrypted read/storage through AndroidKeyStore/AES-GCM and the existing not-configured refusal.
- `LfaViewModel.beginConfigurationImport` and `LfaViewModel.finishConfigurationImport(Uri?)`: preserve explicit-import operation ownership and current failure/state behavior.
- `QueueScreen.configurationLauncher`: preserves the `OpenDocument` content-URI import workflow and JSON media request.

The exact future focused test boundary is `Android_App/app/src/test/java/com/example/network/DheaClientConfigurationTest.kt`, owned by Android under the M2-D01 assignment, with synthetic non-secret input only:

1. `freshClientRequiresExplicitConfiguration`: a fresh client is not configured and creates no `connection.enc` before explicit import.
2. `explicitContentUriImportPersistsAcrossClientRecreation`: a valid synthetic `dhea-connection/1.0` content URI imports, makes `isConfigured()` true, and remains available through encrypted local storage after client recreation.
3. `invalidImportPreservesExistingConfiguration`: invalid import creates no configuration and never replaces an existing valid configuration.
4. `importedSentinelIsNotLogged`: captured logs contain no imported synthetic sentinel.

The exact future static/package gate boundary is `Android_App/app/build.gradle.kts::verifyNoEmbeddedDheaCredential`, dependent on the assembled target APK. It rejects (a) any production main-source `DheaClient` constructor/`init` path that constructs `dhea-connection/1.0` or writes `connection.enc` before explicit import and (b) the synthetic sentinel occurring in production main sources, generated `BuildConfig` or resources, assembled APK entries/classes dex, or captured logs. Its positive side proves the same sentinel remains usable only through explicit content-URI import and survives `DheaClient` recreation through encrypted local storage. No real credential/address, network request, multipart behavior, device action, credential disclosure/use/rotation belongs to this repair or proof. This task creates neither the test nor Gradle task and runs no build; both remain future M2-D01 boundaries only.

### 11.2 Authoritative requirement mapping

| Requirement | Authoritative obligation | D05 evidence and disposition |
|---|---|---|
| `M1-D05-REQ-01` | Frozen Android connection/recovery contract: explicit imported connection, no embedded address/credential or secret logging | Sections 3, 7 and 11.1 now identify Android owner, exact delete/preserve symbols, M1 Exit and explicit assignment dependencies, four executable future checks, and credential-safe source/APK proof. A-SEC-01 remains implementation `OPEN`; M2-D01 is not authorized. |
| `M1-D05-REQ-02` | Unified request and common `DheaRuntime`; immutable identity/hash, frozen runtime, idempotent final replay | Sections 4 and 9.2 specify accepted authority, owner/hunks, lifecycle/refusal matrix and negative checks without public DTO migration. RBL-01 remains implementation `OPEN`. |
| `M1-D05-REQ-03` | Core-owned complete-JPEG/ICC evidence, immutable original and truthful unknowns | Sections 5 and 9.4 specify producer/consumer union, collector independence, schema placement and checks. RBL-03/A-DIAG-01 remain implementation `OPEN`. |
| `M1-D05-REQ-04` | Request-ID Web lookup, same execution, subject/credential isolation and artifact integrity | Sections 6, 9.5 and 10 specify exact lookup and four gates with authority, ordering and refusals. RBL-02 diagnostic repair remains implementation `OPEN`. |
| `M1-D05-REQ-05` | Build/trace/verify integrity and exact dual-Gate review input | Sections 2, 3, 7-10, the adjacent manifest and unchanged patch bind owner/hunk/dependency/Exit/review input while preserving unknown chronology. RBL-04 remains `CONDITIONAL`. |
| `M1-D05-REQ-06` | Real capture/request/Core/original-SHA evidence and truthful limitations | Sections 7-8 route missing current APK/runtime/device evidence to D04/M3 and make no live-evidence or M1 Exit claim. |

This mapping is sourced from `MASTER_PLAN.md#m1-d05-authoritative-requirement-mapping` and does not promote finding IDs into requirements. The previous 47,402-byte report / SHA-256 `82098374c48dfd6bf97cf5e0f1b3b5bfae6fb5119fa66cff6a5cf2b789f0f36f` and 71,512-byte manifest / SHA-256 `0f158adbaf9c5ff4360bb84c7e02c8a0dc9abc6af962e36b575c88c1b45399f6` retain their historical `SPECIFICATION_ADDRESSED_WITH_LIMITATIONS` / R5-closed review disposition. That acceptance does not transfer to this supplement. The new exact report/manifest revision requires fresh independent review and separate PM disposition. The established patch remains byte-for-byte unchanged.

BTW-CHECK: TODO_ID `RUN-20260918T043217Z-REPAIR-BOUNDARY`; Goal repair only the omitted M1-D05-REQ-01 Android credential-bootstrap symbol/test boundary and map REQ-01..06; Files Changed append-only report and adjacent manifest, patch unchanged; Build Result N/A by documentary-only authorization; Requirement Trace `MASTER_PLAN.md#m1-d05-authoritative-requirement-mapping`, especially REQ-01, plus Android-owner credential-safe consultation; Test Result document structure, JSON, history recovery, exact hashes and mapping fields only; Artifact Evidence this section and structured manifest supplement; Known Limitations no implementation, source/APK behavioral proof, real credential inspection, runtime/device action or inherited acceptance; Open Post-Funding Gates unchanged; Current MVP Blocker Remaining fresh D05 dual review, RBL-04 conditional, implementation HIGH, D04 and no M1 Exit. `M2=NOT_STARTED`; `implementation_authorized=false`.
