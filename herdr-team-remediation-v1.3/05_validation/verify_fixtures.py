#!/usr/bin/env python3
import hashlib
import itertools
import json
import mimetypes
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "04_fixtures"
CONTRACTS = ROOT / "01_contracts"
KNOWN_STATUSES = {
    "AUTHOR_COMPLETE": "DISPATCHABLE",
    "IMPLEMENTED_PENDING_REVIEW": "DISPATCHABLE",
    "REVIEW_PENDING": "DISPATCHABLE",
    "IMPLEMENTED_DEVICE_EVIDENCE_PENDING": "NOT_READY",
}
KNOWN_CRITERIA = {"C01", "C02"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode()


def validate_schema(schema_name, input_name):
    schema = json.loads((CONTRACTS / schema_name).read_text())
    value = json.loads((FIXTURES / input_name).read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(value)
    return "VALID"


def validate_acceptance(case):
    results = case["results"]
    ids = [item["criterion_id"] for item in results]
    if len(ids) != len(set(ids)):
        return "DUPLICATE_CRITERION_RESULT"
    if any(item not in KNOWN_CRITERIA for item in ids):
        return "UNKNOWN_CRITERION"
    if any(item not in ids for item in case["required"]):
        return "REQUIRED_CRITERION_MISSING"
    if any(item["result"] in {"PASS", "FAIL"} and not item["evidence_refs"] for item in results):
        return "PASS_EVIDENCE_REQUIRED"
    return "VALID"


def validate_artifact(case):
    path = (ROOT / case["path"]).resolve()
    if not path.is_relative_to(ROOT.resolve()):
        return "ARTIFACT_PATH_ESCAPE"
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != case["sha256"] or len(data) != case["size_bytes"]:
        return "ARTIFACT_INTEGRITY_MISMATCH"
    if any(item not in KNOWN_CRITERIA for item in case["criterion_ids"]):
        return "CRITERION_BINDING_MISMATCH"
    if mimetypes.guess_type(path)[0] != "application/json":
        return "ARTIFACT_MEDIA_TYPE_MISMATCH"
    return "VALID"


def reduce_supersession(events):
    by_id = {event["event_id"]: event for event in events}
    successors = {}
    for event in events:
        prior_id = event["supersedes"]
        if event["generation"] == 1:
            if prior_id is not None:
                return "INVALID_SUPERSESSION"
            continue
        prior = by_id.get(prior_id)
        partition = (event["task_id"], event["revision"], event["criterion_id"])
        if prior is None or partition != (prior["task_id"], prior["revision"], prior["criterion_id"]) or event["generation"] != prior["generation"] + 1:
            return "INVALID_SUPERSESSION"
        successors.setdefault(prior_id, []).append(event["event_id"])
    if any(len(items) > 1 for items in successors.values()):
        return "CONCURRENT_RESULT_CONFLICT"
    superseded = set(successors)
    tips = sorted(event_id for event_id in by_id if event_id not in superseded)
    return tips[0] if len(tips) == 1 else "CONCURRENT_RESULT_CONFLICT"


def evaluate(case):
    kind = case["kind"]
    if kind == "schema":
        return validate_schema(case["schema"], case["input"])
    if kind == "legacy_status":
        return KNOWN_STATUSES.get(case["status"], "UNKNOWN_STATUS")
    if kind == "acceptance":
        return validate_acceptance(case)
    if kind == "artifact":
        return validate_artifact(case)
    if kind == "duplicate_evidence":
        return "DUPLICATE" if canonical(case["left"]) == canonical(case["right"]) else "EVIDENCE_ID_CONFLICT"
    if kind == "supersession":
        outcomes = {reduce_supersession(list(order)) for order in itertools.permutations(case["events"])}
        return outcomes.pop() if len(outcomes) == 1 else "PERMUTATION_VARIANCE"
    if kind == "revision_isolation":
        return len({(item["task_id"], item["revision"], item["criterion_id"]) for item in case["events"]})
    if kind == "idempotency":
        digests = {}
        for event in case["events"]:
            prior = digests.setdefault(event["idempotency_key"], event["payload_digest"])
            if prior != event["payload_digest"]:
                return "IDEMPOTENCY_CONFLICT"
        return "IDEMPOTENT"
    raise ValueError(kind)


def verify_contract_fixtures():
    for schema_path in sorted(CONTRACTS.glob("*.json")):
        jsonschema.Draft202012Validator.check_schema(json.loads(schema_path.read_text()))
    pairs = [
        ("dispatchable-evidence-envelope.schema.json", "evidence/not-ready-envelope.json"),
        ("ledger-event.schema.json", "events/supersession-generation-1.json"),
        ("ledger-event.schema.json", "events/supersession-generation-2.json"),
        ("ledger-event.schema.json", "events/qr-android-evidence-observed.json"),
        ("dashboard-projection.schema.json", "projection/synthetic-not-ready.json"),
        ("dashboard-projection.schema.json", "projection/qr-android-real-not-ready.json"),
    ]
    for schema_name, input_name in pairs:
        validate_schema(schema_name, input_name)
    for path in sorted((FIXTURES / "events").glob("*.json")):
        event = json.loads(path.read_text())
        assert hashlib.sha256(canonical(event["payload"])).hexdigest() == event["payload_digest"], path
    evidence = json.loads((FIXTURES / "evidence/not-ready-envelope.json").read_text())
    manifest = "".join(f"{item['sha256']}  {item['path']}\n" for item in sorted(evidence["artifacts"], key=lambda item: item["path"]))
    assert "sha256:" + hashlib.sha256(manifest.encode()).hexdigest() == evidence["artifact_set_revision"]
    event_by_id = {
        event["event_id"]: event
        for path in sorted((FIXTURES / "events").glob("*.json"))
        for event in [json.loads(path.read_text())]
    }
    projections = {
        "projection/synthetic-not-ready.json": ["EV-090"],
        "projection/qr-android-real-not-ready.json": ["EV-QR-ANDROID-01-D01"],
    }
    for path, event_ids in projections.items():
        projection = json.loads((FIXTURES / path).read_text())
        rows = "".join(f"{event_id}  {event_by_id[event_id]['payload_digest']}\n" for event_id in sorted(event_ids))
        assert hashlib.sha256(rows.encode()).hexdigest() == projection["generated_from_event_digest"], path
    historical_qr = ROOT.parent / ".agent-control/EVIDENCE/QR-ANDROID-01-D01.json"
    assert hashlib.sha256(historical_qr.read_bytes()).hexdigest() == "34ff8fac1e19d73225ca0ac395fa82c1504457977de953df0ddeb95cf22f29a3"


def main():
    verify_contract_fixtures()
    scenarios = json.loads((FIXTURES / "scenarios.json").read_text())
    assert list(scenarios) == [f"C{number:02d}" for number in range(1, 19)]
    failed = []
    for scenario_id, case in scenarios.items():
        actual = evaluate(case)
        print(f"{scenario_id}: {actual}")
        if actual != case["expected"]:
            failed.append(f"{scenario_id}: expected {case['expected']}, got {actual}")
    if failed:
        print("\n".join(failed), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
