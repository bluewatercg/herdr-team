#!/usr/bin/env python3
"""Execute the approved HARNESS-VERIFICATION-SHADOW C01-C18 and QR smoke."""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
import tempfile
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
QR_EVIDENCE = REPO / "herdr-team/.agent-control/EVIDENCE/QR-ANDROID-DEVICE-R03.json"
R03_INPUTS = REPO / "herdr-team/.agent-control/MACHINE/HARNESS-VERIFICATION-SHADOW/qr-android-r03-inputs.json"
OUTPUT = REPO / "herdr-team/.agent-control/MACHINE/HARNESS-VERIFICATION-SHADOW/qr-android-projection.json"
QR_SHA256 = "7cc1adfa48c948710755ba8a19cc131098aab1ba0a9c941206f9088a57b8468b"


def load(path: Path):
  return json.loads(path.read_text(encoding="utf-8"))


def _write_projection(projection: dict, output: Path) -> dict:
  """Atomically persist only a validated reducer projection."""
  errors = validate_schema(projection, schema("dashboard-projection.schema.json"))
  if errors:
    raise ValueError("INVALID_PROJECTION_SCHEMA: " + "; ".join(errors))
  if projection["acceptance_status"] == "PASS":
    raise ValueError("PROJECTION_ACCEPTANCE_PASS_FORBIDDEN")
  if "formal_reporting_allowed" in projection and projection["formal_reporting_allowed"] is not False:
    raise ValueError("FORMAL_REPORTING_FORBIDDEN")
  serialized = json.dumps(projection, ensure_ascii=False, indent=2) + "\n"
  output.parent.mkdir(parents=True, exist_ok=True)
  temporary: Path | None = None
  try:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=output.parent, prefix=f".{output.name}.", delete=False) as handle:
      temporary = Path(handle.name)
      handle.write(serialized)
      handle.flush()
      os.fsync(handle.fileno())
    os.replace(temporary, output)
    temporary = None
    readback = load(output)
    if readback != projection or json.dumps(readback, ensure_ascii=False, indent=2) + "\n" != serialized:
      raise ValueError("PROJECTION_READBACK_MISMATCH")
    return readback
  finally:
    if temporary is not None:
      temporary.unlink(missing_ok=True)


def write_projection(projection: dict) -> dict:
  return _write_projection(projection, OUTPUT)


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
  assert evidence_id == "LEGACY:QR-ANDROID-DEVICE-R03"
  assert reason_codes == ["DEVICE_EVIDENCE_PENDING"]

  inputs = load(R03_INPUTS)
  reduced = project(
    inputs["registry"],
    inputs["events"],
    inputs["evidence_index"],
    **inputs["project_arguments"],
  )
  assert reduced == load(OUTPUT)
  assert reduced["subject_revision"] == "sha256:216f8f35af950f475b16991ef7685c8617404668dad17e9dbc1a30b920e36aab"
  assert reduced["evidence_status"] == "NOT_READY"
  assert reduced["acceptance_status"] == "UNVERIFIED"
  assert reduced["criteria"][0]["evidence_refs"] == [evidence_id]
  assert reduced["criteria"][0]["reason_codes"] == reason_codes
  assert value["formal_reporting_allowed"] is False
  with tempfile.TemporaryDirectory() as directory:
    original_output = globals()["OUTPUT"]
    globals()["OUTPUT"] = Path(directory) / "projection.json"
    try:
      readback = write_projection(reduced)
      assert readback == reduced
      test_output = globals()["OUTPUT"]
      test_output.write_text("sentinel\n", encoding="utf-8")
      before = test_output.read_bytes()
      for rejected in (
        {**reduced, "acceptance_status": "PASS"},
        {**reduced, "formal_reporting_allowed": True},
        {**reduced, "criteria": []},
      ):
        try:
          write_projection(rejected)
        except ValueError:
          pass
        else:
          raise AssertionError("invalid projection was accepted")
        assert test_output.read_bytes() == before
    finally:
      globals()["OUTPUT"] = original_output
  return reduced


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
