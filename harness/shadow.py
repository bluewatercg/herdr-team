"""Read-only verification shadow for Herdr evidence and acceptance records."""
from __future__ import annotations

import hashlib
import json
import math
import mimetypes
from collections import defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
  import jsonschema
except ImportError:  # Schema validation is optional at runtime.
  jsonschema = None

STATUS_CLASSIFICATION = {
  "AUTHOR_COMPLETE": "DISPATCHABLE",
  "IMPLEMENTED_PENDING_REVIEW": "DISPATCHABLE",
  "REVIEW_PENDING": "DISPATCHABLE",
  "IMPLEMENTED_DEVICE_EVIDENCE_PENDING": "NOT_READY",
}
ACCEPTANCE_PRIORITY = {
  "PASS": 0, "PENDING": 1, "UNVERIFIED": 2, "FAIL": 3,
  "STALE": 4, "INVALID": 5, "CONFLICTED": 6,
}


def _float_text(value: float) -> str:
  if not math.isfinite(value):
    raise ValueError("JCS forbids non-finite numbers")
  if value == 0:
    return "0"
  text = repr(value).lower()
  coefficient, marker, exponent = text.partition("e")
  if not marker:
    return coefficient[:-2] if coefficient.endswith(".0") else coefficient
  exp = int(exponent)
  digits = coefficient.replace("-", "").replace(".", "")
  negative = coefficient.startswith("-")
  decimal = coefficient.lstrip("-").find(".")
  integer_digits = decimal if decimal >= 0 else len(digits)
  magnitude = integer_digits + exp
  sign = "-" if negative else ""
  if 0 < magnitude <= 21:
    if magnitude >= len(digits):
      return sign + digits + "0" * (magnitude - len(digits))
    return sign + digits[:magnitude] + "." + digits[magnitude:]
  if -5 <= magnitude <= 0:
    return sign + "0." + "0" * (-magnitude) + digits
  mantissa = digits[0] + (("." + digits[1:]) if len(digits) > 1 else "")
  scientific_exp = magnitude - 1
  return sign + mantissa + "e" + ("+" if scientific_exp >= 0 else "") + str(scientific_exp)


def jcs(value: Any) -> bytes:
  """Serialize JSON-compatible data using RFC 8785 ordering and number form."""
  def encode(item: Any) -> str:
    if item is None:
      return "null"
    if item is True:
      return "true"
    if item is False:
      return "false"
    if isinstance(item, str):
      return json.dumps(item, ensure_ascii=False, separators=(",", ":"))
    if isinstance(item, int) and not isinstance(item, bool):
      if abs(item) > 9007199254740991:
        raise ValueError("integer is not exactly representable as an IEEE-754 number")
      return str(item)
    if isinstance(item, float):
      return _float_text(item)
    if isinstance(item, list):
      return "[" + ",".join(encode(part) for part in item) + "]"
    if isinstance(item, dict):
      if not all(isinstance(key, str) for key in item):
        raise TypeError("JSON object keys must be strings")
      keys = sorted(item, key=lambda key: key.encode("utf-16be", "surrogatepass"))
      return "{" + ",".join(encode(key) + ":" + encode(item[key]) for key in keys) + "}"
    raise TypeError(f"unsupported JSON value: {type(item).__name__}")
  return encode(value).encode("utf-8")


def sha256_jcs(value: Any) -> str:
  return hashlib.sha256(jcs(value)).hexdigest()


def validate_schema(value: Any, schema: dict[str, Any]) -> list[str]:
  if jsonschema is None:
    raise RuntimeError("jsonschema is required for schema validation")
  validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
  return [error.message for error in sorted(validator.iter_errors(value), key=lambda error: list(error.path))]


def validate_registry(registry: dict[str, Any]) -> list[str]:
  ids = [item["criterion_id"] for item in registry.get("criteria", [])]
  return [] if len(ids) == len(set(ids)) else ["DUPLICATE_CRITERION_ID"]


def resolve_artifact(path_text: str, roots: Iterable[Path]) -> Path:
  path = PurePosixPath(path_text)
  if path.is_absolute() or ".." in path.parts or not path.parts:
    raise ValueError("ARTIFACT_PATH_ESCAPE")
  for configured_root in roots:
    root = configured_root.resolve(strict=True)
    candidate = root.joinpath(*path.parts)
    try:
      relative = candidate.relative_to(root)
      cursor = root
      for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
          raise ValueError("ARTIFACT_SYMLINK_REJECTED")
      resolved = candidate.resolve(strict=True)
      resolved.relative_to(root)
      return resolved
    except (FileNotFoundError, ValueError):
      continue
  raise ValueError("ARTIFACT_PATH_ESCAPE_OR_MISSING")


def verify_artifacts(envelope: dict[str, Any], roots: Iterable[Path], criterion_ids: set[str]) -> list[str]:
  diagnostics: list[str] = []
  manifest_rows = []
  for artifact in envelope.get("artifacts", []):
    try:
      path = resolve_artifact(artifact["path"], roots)
    except ValueError as error:
      diagnostics.append(str(error))
      continue
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != artifact["sha256"] or len(data) != artifact["size_bytes"]:
      diagnostics.append("ARTIFACT_INTEGRITY_MISMATCH")
    guessed = mimetypes.guess_type(path)[0] or "application/octet-stream"
    if guessed != artifact["media_type"]:
      diagnostics.append("ARTIFACT_MEDIA_TYPE_MISMATCH")
    if any(item not in criterion_ids for item in artifact["criterion_ids"]):
      diagnostics.append("CRITERION_BINDING_MISMATCH")
    manifest_rows.append(f"{artifact['sha256']}  {artifact['path']}\n")
  revision = "sha256:" + hashlib.sha256("".join(sorted(manifest_rows)).encode()).hexdigest()
  if envelope.get("artifact_set_revision") != revision:
    diagnostics.append("ARTIFACT_SET_REVISION_MISMATCH")
  return sorted(set(diagnostics))


def validate_acceptance(acceptance: dict[str, Any], registry: dict[str, Any], evidence: dict[str, dict[str, Any]]) -> list[str]:
  diagnostics: list[str] = []
  criteria = {item["criterion_id"]: item for item in registry["criteria"]}
  results = acceptance.get("acceptance_results", [])
  ids = [item["criterion_id"] for item in results]
  if len(ids) != len(set(ids)):
    diagnostics.append("DUPLICATE_CRITERION_RESULT")
  if any(item not in criteria for item in ids):
    diagnostics.append("UNKNOWN_CRITERION")
  if any(item["required"] and item["criterion_id"] not in ids for item in registry["criteria"]):
    diagnostics.append("REQUIRED_CRITERION_MISSING")
  expected_ref = "sha256:" + sha256_jcs(registry)
  if acceptance.get("criterion_registry_ref") != expected_ref:
    diagnostics.append("CRITERION_REGISTRY_REF_MISMATCH")
  if acceptance.get("task_id") != registry.get("task_id"):
    diagnostics.append("TASK_BINDING_MISMATCH")
  for result in results:
    refs = result.get("evidence_refs", [])
    if result["result"] in {"PASS", "FAIL"} and not refs:
      diagnostics.append("PASS_FAIL_EVIDENCE_REQUIRED")
    if result["result"] == "PASS" and (result.get("reason_code") is not None or result.get("reason") is not None):
      diagnostics.append("PASS_REASON_FORBIDDEN")
    if result["result"] in {"FAIL", "UNVERIFIED"} and not result.get("reason_code"):
      diagnostics.append("REASON_CODE_REQUIRED")
    for ref in refs:
      state = evidence.get(ref)
      if state is None:
        diagnostics.append("EVIDENCE_UNAVAILABLE")
        continue
      item = state.get("envelope", state)
      if item.get("task_id") != acceptance.get("task_id") or item.get("subject_revision") != acceptance.get("subject_revision"):
        diagnostics.append("EVIDENCE_BINDING_MISMATCH")
      if result["result"] == "PASS" and (state.get("usable") is False or state.get("classification") not in {None, "DISPATCHABLE"}):
        diagnostics.append("EVIDENCE_UNUSABLE")
      if result["criterion_id"] not in {criterion for artifact in item.get("artifacts", []) for criterion in artifact.get("criterion_ids", [])}:
        diagnostics.append("CRITERION_BINDING_MISMATCH")
  repair = acceptance.get("repair", {})
  if repair.get("status") == "NOT_REQUIRED" and (repair.get("current_round") != 0 or repair.get("finding_refs")):
    diagnostics.append("REPAIR_STATE_INVALID")
  if repair.get("status") == "EXHAUSTED" and (repair.get("current_round") != repair.get("max_rounds") or not repair.get("finding_refs")):
    diagnostics.append("REPAIR_STATE_INVALID")
  if repair.get("current_round", 0) > repair.get("max_rounds", 0):
    diagnostics.append("REPAIR_STATE_INVALID")
  regression = acceptance.get("regression", {})
  if not regression.get("required"):
    if any(regression.get(key) is not None for key in ("scope", "result", "reason", "reason_code")) or regression.get("evidence_refs"):
      diagnostics.append("REGRESSION_STATE_INVALID")
  else:
    if regression.get("scope") != "FULL" or regression.get("result") is None:
      diagnostics.append("REGRESSION_STATE_INVALID")
    if regression.get("result") in {"PASS", "FAIL"} and not regression.get("evidence_refs"):
      diagnostics.append("REGRESSION_EVIDENCE_REQUIRED")
    if regression.get("result") in {"FAIL", "UNVERIFIED"} and not regression.get("reason_code"):
      diagnostics.append("REGRESSION_REASON_REQUIRED")
    if regression.get("result") == "PASS" and (regression.get("reason_code") is not None or regression.get("reason") is not None):
      diagnostics.append("REGRESSION_PASS_REASON_FORBIDDEN")
  return sorted(set(diagnostics))


def classify_record(value: Any, *, malformed: bool = False) -> tuple[str, str | None, list[str]]:
  if malformed or not isinstance(value, dict):
    return "MALFORMED", None, ["INVALID_JSON_OR_RECORD"]
  if value.get("record_kind") == "DISPATCHABLE_SUBMISSION":
    evidence_id = value.get("evidence_id")
    if not evidence_id:
      return "MALFORMED", None, ["EVIDENCE_ID_REQUIRED"]
    classification = STATUS_CLASSIFICATION.get(value.get("submission_status"), "UNKNOWN_STATUS")
    return classification, evidence_id, ([] if classification == "DISPATCHABLE" else ["SUBMISSION_" + classification])
  legacy = all(key in value for key in ("task_id", "deliverable_id", "status")) and ("implementation_files" in value or "artifacts" in value)
  if legacy:
    evidence_id = "LEGACY:" + str(value["deliverable_id"])
    classification = STATUS_CLASSIFICATION.get(value["status"], "UNKNOWN_STATUS")
    reason = "DEVICE_EVIDENCE_PENDING" if classification == "NOT_READY" else "SUBMISSION_" + classification
    return classification, evidence_id, ([] if classification == "DISPATCHABLE" else [reason])
  return "NOT_SUBMISSION", None, ["NOT_SUBMISSION"]


def build_evidence_index(envelopes: Iterable[dict[str, Any]], *, roots: Iterable[Path] | None = None, criterion_ids: set[str] | None = None) -> tuple[dict[str, dict[str, Any]], set[str]]:
  index: dict[str, dict[str, Any]] = {}
  digests: dict[str, str] = {}
  conflicts: set[str] = set()
  for envelope in envelopes:
    evidence_id = envelope["evidence_id"]
    digest = sha256_jcs(envelope)
    if evidence_id in digests and digests[evidence_id] != digest:
      conflicts.add(evidence_id)
      continue
    digests[evidence_id] = digest
    classification, _, reasons = classify_record(envelope)
    artifact_diagnostics = verify_artifacts(envelope, roots, criterion_ids) if roots is not None and criterion_ids is not None else []
    diagnostics = sorted(set(reasons + artifact_diagnostics))
    index[evidence_id] = {
      "envelope": envelope,
      "classification": classification,
      "diagnostics": diagnostics,
      "usable": classification == "DISPATCHABLE" and not diagnostics,
    }
  for evidence_id in conflicts:
    index[evidence_id] = {"envelope": None, "classification": "CONFLICTED", "diagnostics": ["EVIDENCE_ID_CONFLICT"], "usable": False}
  return index, conflicts


def check_idempotency(events: Iterable[dict[str, Any]]) -> set[str]:
  seen: dict[str, str] = {}
  conflicts: set[str] = set()
  for event in events:
    key, digest = event["idempotency_key"], event["payload_digest"]
    if key in seen and seen[key] != digest:
      conflicts.add(key)
    else:
      seen[key] = digest
  return conflicts


def reduce_criterion(events: Iterable[dict[str, Any]], evidence: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
  ordered = sorted(events, key=lambda event: event["event_id"])
  if not ordered:
    return {"status": "PENDING", "generation": None, "selected_event_id": None, "superseded_event_ids": [], "evidence_refs": [], "reason_codes": []}
  by_id: dict[str, dict[str, Any]] = {}
  duplicate_conflict = False
  for event in ordered:
    prior = by_id.get(event["event_id"])
    if prior is not None and sha256_jcs(prior) != sha256_jcs(event):
      duplicate_conflict = True
    else:
      by_id[event["event_id"]] = event
  if duplicate_conflict:
    return {"status": "CONFLICTED", "generation": None, "selected_event_id": None, "superseded_event_ids": [], "evidence_refs": [], "reason_codes": ["EVENT_ID_CONFLICT"]}
  successors: dict[str, list[str]] = defaultdict(list)
  invalid = False
  partition = None
  for event in by_id.values():
    payload = event.get("payload", event)
    current_partition = (event["task_id"], event.get("subject_revision", event.get("revision")), payload.get("criterion_id", event.get("criterion_id")))
    partition = partition or current_partition
    if current_partition != partition:
      invalid = True
    generation = payload.get("generation", event.get("generation"))
    supersedes = payload.get("supersedes_event_id", event.get("supersedes"))
    if generation == 1:
      invalid |= supersedes is not None
      continue
    prior = by_id.get(supersedes)
    if prior is None or supersedes == event["event_id"]:
      invalid = True
      continue
    prior_payload = prior.get("payload", prior)
    prior_partition = (prior["task_id"], prior.get("subject_revision", prior.get("revision")), prior_payload.get("criterion_id", prior.get("criterion_id")))
    prior_generation = prior_payload.get("generation", prior.get("generation"))
    if current_partition != prior_partition or generation != prior_generation + 1:
      invalid = True
      continue
    successors[supersedes].append(event["event_id"])
  if any(len(items) > 1 for items in successors.values()):
    return {"status": "CONFLICTED", "generation": None, "selected_event_id": None, "superseded_event_ids": sorted(successors), "evidence_refs": [], "reason_codes": ["CONCURRENT_RESULT_CONFLICT"]}
  if invalid:
    return {"status": "INVALID", "generation": None, "selected_event_id": None, "superseded_event_ids": sorted(successors), "evidence_refs": [], "reason_codes": ["INVALID_SUPERSESSION"]}
  tips = sorted(set(by_id) - set(successors))
  if len(tips) != 1:
    return {"status": "CONFLICTED", "generation": None, "selected_event_id": None, "superseded_event_ids": sorted(successors), "evidence_refs": [], "reason_codes": ["CONCURRENT_RESULT_CONFLICT"]}
  selected = by_id[tips[0]]
  payload = selected.get("payload", selected)
  evidence_refs = sorted(payload.get("evidence_refs", []))
  status = payload.get("result", "UNVERIFIED")
  reason_codes = sorted(filter(None, [payload.get("reason_code")]))
  criterion_id = payload.get("criterion_id", selected.get("criterion_id"))
  task_id = selected["task_id"]
  revision = selected.get("subject_revision", selected.get("revision"))
  def usable(ref: str) -> bool:
    state = evidence.get(ref, {}) if evidence is not None else {}
    envelope = state.get("envelope") or {}
    bindings = {item for artifact in envelope.get("artifacts", []) for item in artifact.get("criterion_ids", [])}
    return (state.get("usable", False) and envelope.get("task_id") == task_id
            and envelope.get("subject_revision") == revision and criterion_id in bindings)
  if status == "PASS" and (not evidence_refs or any(not usable(ref) for ref in evidence_refs)):
    status = "UNVERIFIED"
    reason_codes = ["EVIDENCE_UNUSABLE"]
  return {
    "status": status,
    "generation": payload.get("generation", selected.get("generation")),
    "selected_event_id": selected["event_id"],
    "superseded_event_ids": sorted(set(by_id) - {selected["event_id"]}),
    "evidence_refs": evidence_refs,
    "reason_codes": reason_codes,
  }


def project(registry: dict[str, Any], events: Iterable[dict[str, Any]], evidence: dict[str, dict[str, Any]], *, subject_revision: str | None = None, evidence_status: str = "UNAVAILABLE", diagnostics: list[dict[str, str]] | None = None) -> dict[str, Any]:
  task_id = registry["task_id"]
  revision = subject_revision or registry["task_contract_revision"]
  event_list = [event for event in events if event.get("task_id") == task_id and event.get("subject_revision") == revision]
  groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
  for event in event_list:
    payload = event.get("payload", {})
    if event.get("event_type") == "ACCEPTANCE_RECORDED":
      groups[(task_id, revision, payload["criterion_id"])].append(event)
  criteria = []
  for criterion in registry["criteria"]:
    row = reduce_criterion(groups.get((task_id, revision, criterion["criterion_id"]), []), evidence)
    criteria.append({"criterion_id": criterion["criterion_id"], "required": criterion["required"], **row})
  required_statuses = [row["status"] for row in criteria if row["required"]]
  acceptance = max(required_statuses, key=ACCEPTANCE_PRIORITY.get) if required_statuses else "UNAVAILABLE"
  idempotency_conflicts = check_idempotency(event_list)
  if idempotency_conflicts:
    acceptance = "CONFLICTED"
  rows = "".join(f"{event['event_id']}  {event['payload_digest']}\n" for event in sorted(event_list, key=lambda item: item["event_id"]))
  return {
    "schema_version": "herdr-dashboard-projection/1.3",
    "task_id": task_id,
    "subject_revision": revision,
    "ingestion_status": "CONFLICTED" if idempotency_conflicts else "VALID",
    "evidence_status": evidence_status,
    "acceptance_status": acceptance,
    "criteria": criteria,
    "diagnostics": diagnostics or [],
    "generated_from_event_digest": hashlib.sha256(rows.encode()).hexdigest(),
    "reducer_version": "shadow-reducer/1.0",
  }
