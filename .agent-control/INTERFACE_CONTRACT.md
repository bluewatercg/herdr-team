# INTERFACE_CONTRACT
VERSION: Android local 1.5 / public dhea-capture 2.0 observed; v3 migration unresolved
STATUS: DISCOVERED

Observed Android source: LfaViewModel creates Bundle 1.5; DheaClient emits dhea-capture/2.0 and validates dhea-result/2.0.
Observed Gateway source: POST /api/v2/lfa/measure accepts v2 and explicitly refuses v3 with V3_ACCEPTANCE_NOT_IMPLEMENTED. DheaService calls runtime.analyze(original_bytes, original_sha256, diagnostics=collector).
Observed Core: DheaRuntime.analyze exists; no UnifiedAnalysisRequest symbol found in core/ or python_gateway/. Diagnostics bind request_id=analysis_id; public lookup uses capture_bundle_id.
Uncommitted docs/api/dhea-v3-product-gate.md specifies Bundle 1.6, capture/result 3.0 and recovery-only v2. This is not the observed implemented contract. PM acceptance withheld pending reconciliation.
