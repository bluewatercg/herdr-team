#!/usr/bin/env python3
"""Execute the approved HARNESS-VERIFICATION-SHADOW C01-C18 and QR smoke."""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

from shadow import (
  build_evidence_index,
  check_idempotency,
  classify_record,
  jcs,
  project,
  reduce_criterion,
  resolve_artifact,
  sha256_jcs,
  validate_acceptance,
  validate_registry,
  validate_schema,
  verify_artifacts,
)

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "herdr-team/herdr-team-remediation-v1.3"
FIXTURES = PACKAGE / "04_fixtures"
CONTRACTS = PACKAGE / "01_contracts"
QR_EVIDENCE = REPO / "herdr-team/.agent-control/EVIDENCE/QR-ANDROID-01-D01.json"
OUTPUT = REPO / "herdr-team/.agent-control/MACHINE/HARNESS-VERIFICATION-SHADOW/qr-android-projection.json"
QR_SHA256 = "34ff8fac1e19d73225ca0ac395fa82c1504457977de953df0ddeb95cf22f29a3"


def load(path: Path):
  return json.loads(path.read_text(encoding="utf-8"))


def schema(name: str) -> dict:
  return load(CONTRACTS / name)


def fixture(path: str):
  return load(FIXTURES / path)


def scenario_result(case: dict) -> str | int:
  kind = case["kind"]
  if kind == "schema":
    errors = validate_schema(fixture(case["input"]), schema(case["schema"]))
    return "VALID" if not errors else "INVALID"
  if kind == "legacy_status":
    classification, _, _ = classify_record({
      "task_id": "T", "deliverable_id": "D", "status": case["status"], "artifacts": []
    })
    return classification
  if kind == "acceptance":
    ids = [item["criterion_id"] for item in case["results"]]
    if len(ids) != len(set(ids)):
      return "DUPLICATE_CRITERION_RESULT"
    if any(item not in {"C01", "C02"} for item in ids):
      return "UNKNOWN_CRITERION"
    if any(item not in ids for item in case["required"]):
      return "REQUIRED_CRITERION_MISSING"
    if any(item["result"] in {"PASS", "FAIL"} and not item["evidence_refs"] for item in case["results"]):
      return "PASS_EVIDENCE_REQUIRED"
    return "VALID"
  if kind == "artifact":
    try:
      path = resolve_artifact(case["path"], [PACKAGE])
    except ValueError:
      return "ARTIFACT_PATH_ESCAPE"
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != case["sha256"] or len(data) != case["size_bytes"]:
      return "ARTIFACT_INTEGRITY_MISMATCH"
    if any(item not in {"C01", "C02"} for item in case["criterion_ids"]):
      return "CRITERION_BINDING_MISMATCH"
    return "VALID"
  if kind == "duplicate_evidence":
    index, conflicts = build_evidence_index([case["left"], case["right"]])
    return "EVIDENCE_ID_CONFLICT" if conflicts else ("DUPLICATE" if len(index) == 1 else "INVALID")
  if kind == "supersession":
    outcomes = set()
    for order in itertools.permutations(case["events"]):
      reduced = reduce_criterion(order)
      if reduced["status"] == "INVALID":
        outcomes.add("INVALID_SUPERSESSION")
      elif reduced["status"] == "CONFLICTED":
        outcomes.add(reduced["reason_codes"][0])
      else:
        outcomes.add(reduced["selected_event_id"])
    return outcomes.pop() if len(outcomes) == 1 else "PERMUTATION_VARIANCE"
  if kind == "revision_isolation":
    return len({(item["task_id"], item["revision"], item["criterion_id"]) for item in case["events"]})
  if kind == "idempotency":
    events = [
      {"idempotency_key": item["idempotency_key"], "payload_digest": item["payload_digest"]}
      for item in case["events"]
    ]
    return "IDEMPOTENCY_CONFLICT" if check_idempotency(events) else "IDEMPOTENT"
  raise ValueError(kind)


def verify_contracts() -> None:
  for path in sorted(CONTRACTS.glob("*.json")):
    assert not validate_schema({}, load(path)) or path.name  # constructs and checks every schema
  pairs = [
    ("dispatchable-evidence-envelope.schema.json", "evidence/not-ready-envelope.json"),
    ("ledger-event.schema.json", "events/supersession-generation-1.json"),
    ("ledger-event.schema.json", "events/supersession-generation-2.json"),
    ("ledger-event.schema.json", "events/qr-android-evidence-observed.json"),
    ("dashboard-projection.schema.json", "projection/synthetic-not-ready.json"),
    ("dashboard-projection.schema.json", "projection/qr-android-real-not-ready.json"),
    ("task-acceptance.schema.json", "acceptance/unverified-valid.json"),
    ("criterion-registry.schema.json", "criterion-registry.json"),
  ]
  for schema_name, fixture_name in pairs:
    assert not validate_schema(fixture(fixture_name), schema(schema_name)), fixture_name
  registry = fixture("criterion-registry.json")
  assert not validate_registry(registry)
  acceptance = fixture("acceptance/unverified-valid.json")
  envelope = fixture("evidence/not-ready-envelope.json")
  not_ready_index, _ = build_evidence_index([envelope], roots=[PACKAGE], criterion_ids={"C01", "C02"})
  assert not validate_acceptance(acceptance, registry, not_ready_index)
  assert not verify_artifacts(envelope, [PACKAGE], {"C01", "C02"})
  for path in sorted((FIXTURES / "events").glob("*.json")):
    event = load(path)
    assert sha256_jcs(event["payload"]) == event["payload_digest"], path
  assert jcs({"b": 1, "a": -0.0}) == b'{"a":0,"b":1}'

  generation_1 = fixture("events/supersession-generation-1.json")
  generation_2 = fixture("events/supersession-generation-2.json")
  revision = generation_1["subject_revision"]
  dispatchable = json.loads(json.dumps(envelope))
  dispatchable["submission_status"] = "AUTHOR_COMPLETE"
  dispatchable["subject_revision"] = revision
  usable_index, _ = build_evidence_index([dispatchable], roots=[PACKAGE], criterion_ids={"C01", "C02"})
  projections = [
    project(registry, order, usable_index, subject_revision=revision, evidence_status="DISPATCHABLE")
    for order in itertools.permutations([generation_1, generation_2])
  ]
  assert projections[0] == projections[1]
  assert projections[0]["acceptance_status"] == "PASS"
  assert projections[0]["criteria"][0]["selected_event_id"] == generation_2["event_id"]
  assert projections[0]["criteria"][1]["status"] == "PENDING"

  missing = project(registry, [generation_1, generation_2], {}, subject_revision=revision)
  assert missing["acceptance_status"] == "UNVERIFIED"
  assert missing["criteria"][0]["reason_codes"] == ["EVIDENCE_UNUSABLE"]
  not_ready = project(registry, [generation_1, generation_2], not_ready_index, subject_revision=revision, evidence_status="NOT_READY")
  assert not_ready["acceptance_status"] == "UNVERIFIED"

  unrelated = json.loads(json.dumps(generation_2))
  unrelated.update(event_id="EV-OTHER", task_id="OTHER", subject_revision="sha256:" + "d" * 64, payload_digest="f" * 64)
  unrelated["payload"]["supersedes_event_id"] = None
  isolated = project(registry, [generation_1, generation_2, unrelated], usable_index, subject_revision=revision, evidence_status="DISPATCHABLE")
  assert isolated == projections[0]


def qr_smoke() -> dict:
  raw = QR_EVIDENCE.read_bytes()
  assert hashlib.sha256(raw).hexdigest() == QR_SHA256
  value = json.loads(raw)
  classification, evidence_id, reason_codes = classify_record(value)
  assert classification == "NOT_READY"
  assert evidence_id == "LEGACY:QR-ANDROID-01-D01"
  assert reason_codes == ["DEVICE_EVIDENCE_PENDING"]

  event = fixture("events/qr-android-evidence-observed.json")
  assert event["subject_revision"] == "sha256:" + QR_SHA256
  assert event["payload"]["classification"] == classification
  assert event["payload"]["evidence_id"] == evidence_id
  assert event["payload"]["reason_codes"] == reason_codes
  assert sha256_jcs(event["payload"]) == event["payload_digest"]

  projection = {
    "schema_version": "herdr-dashboard-projection/1.3",
    "task_id": value["task_id"],
    "subject_revision": "sha256:" + QR_SHA256,
    "ingestion_status": "VALID",
    "evidence_status": classification,
    "acceptance_status": "UNVERIFIED",
    "criteria": [{
      "criterion_id": "DEVICE_EVIDENCE",
      "required": True,
      "status": "UNVERIFIED",
      "generation": None,
      "selected_event_id": None,
      "superseded_event_ids": [],
      "evidence_refs": [evidence_id],
      "reason_codes": reason_codes,
    }],
    "diagnostics": [{
      "source_ref": "herdr-team/.agent-control/EVIDENCE/QR-ANDROID-01-D01.json",
      "code": "SUBMISSION_NOT_READY",
    }],
    "generated_from_event_digest": hashlib.sha256(
      f"{event['event_id']}  {event['payload_digest']}\n".encode()
    ).hexdigest(),
    "reducer_version": "shadow-reducer/1.0",
  }
  assert projection == fixture("projection/qr-android-real-not-ready.json")
  assert not validate_schema(projection, schema("dashboard-projection.schema.json"))
  assert projection["acceptance_status"] == "UNVERIFIED"
  assert projection["evidence_status"] == "NOT_READY"
  assert value["formal_reporting_allowed"] is False
  OUTPUT.parent.mkdir(parents=True, exist_ok=True)
  OUTPUT.write_text(json.dumps(projection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
  readback = load(OUTPUT)
  assert readback == projection
  assert readback["acceptance_status"] != "PASS"
  return readback


def main() -> int:
  verify_contracts()
  scenarios = fixture("scenarios.json")
  assert list(scenarios) == [f"C{number:02d}" for number in range(1, 19)]
  for scenario_id, case in scenarios.items():
    actual = scenario_result(case)
    print(f"{scenario_id}: {actual}")
    assert actual == case["expected"], f"{scenario_id}: expected {case['expected']}, got {actual}"
  projection = qr_smoke()
  print(f"QR-SMOKE: {projection['evidence_status']}/{projection['acceptance_status']}")
  print(f"QR-EVIDENCE-SHA256: {QR_SHA256}")
  print(f"PROJECTION: {OUTPUT.relative_to(REPO)}")
  print("SHADOW-VERIFY: PASS")
  return 0


if __name__ == "__main__":
  try:
    raise SystemExit(main())
  except Exception as error:
    print(f"SHADOW-VERIFY: FAIL: {error}", file=sys.stderr)
    raise
