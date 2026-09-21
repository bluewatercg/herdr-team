#!/usr/bin/env python3
"""Validate and append an authorized Jev/PM decision event.

Jev is advisory. Only an explicit PM authorization addressed to lfa-start can
be persisted as a decision event. The dashboard remains read-only.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

CONTROL = Path(__file__).resolve().parent / ".agent-control"
DEFAULT_LOG = CONTROL / "JEV_DECISIONS.jsonl"
REQUIRED_STRINGS = ("decision_id", "timestamp", "actor", "question", "status")
RESULTS = {"APPROVED", "REJECTED", "MODIFIED"}


def fail(message: str) -> None:
    raise ValueError(message)


def validate_record(value: object) -> dict[str, Any]:
    if not isinstance(value, dict):
        fail("record must be an object")
    record = value
    for key in REQUIRED_STRINGS:
        if not isinstance(record.get(key), str) or not record[key].strip():
            fail(f"missing decision metadata: {key}")
    for key in ("jev", "decision", "action", "authorization"):
        if not isinstance(record.get(key), dict):
            fail(f"missing decision structure: {key}")
    if not isinstance(record.get("context_refs"), list) or not record["context_refs"] or not all(isinstance(item, str) and item.strip() for item in record["context_refs"]):
        fail("context_refs must be a non-empty string list")
    if record["decision"].get("result") not in RESULTS:
        fail("decision.result must be APPROVED, REJECTED, or MODIFIED")
    auth = record["authorization"]
    expected = {
        "status": "AUTHORIZED_FOR_HANDOFF",
        "granted_by": "lfa-pm",
        "recipient": "lfa-start",
    }
    for key, expected_value in expected.items():
        if auth.get(key) != expected_value:
            fail(f"authorization.{key} must be {expected_value}")
    for key in ("task_id", "plan_id", "deliverable_id", "file_scope"):
        if not isinstance(record.get(key), (str, list)) or not record[key]:
            fail(f"{key} is required")
        if not isinstance(auth.get(key), (str, list)) or not auth[key]:
            fail(f"authorization.{key} is required")
        if auth[key] != record[key]:
            fail(f"authorization.{key} must match record.{key}")
    if record["actor"] != "lfa-pm":
        fail("actor must identify the PM decision maker")
    return record


def append_record(record: dict[str, Any], path: Path = DEFAULT_LOG) -> str:
    record = validate_record(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    with path.open("a+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        handle.seek(0)
        existing = handle.read().splitlines()
        for line_number, line in enumerate(existing, 1):
            if not line.strip():
                continue
            try:
                prior = json.loads(line)
            except json.JSONDecodeError as error:
                fail(f"existing log line {line_number} is malformed: {error.msg}")
            if not isinstance(prior, dict) or not isinstance(prior.get("decision_id"), str) or not prior["decision_id"].strip():
                fail(f"existing log line {line_number} is not a decision record")
            if prior["decision_id"] == record["decision_id"]:
                prior_bytes = (json.dumps(prior, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
                if prior_bytes != encoded:
                    fail("decision_id already exists with different content")
                return "IDEMPOTENT"
        handle.seek(0, os.SEEK_END)
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    return hashlib.sha256(encoded).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append one authorized Jev/PM decision event")
    parser.add_argument("--input", type=Path, help="JSON record path; stdin when omitted")
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    args = parser.parse_args(argv)
    try:
        raw = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
        result = append_record(json.loads(raw), args.log)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"jev_decide: {error}", file=sys.stderr)
        return 2
    print(json.dumps({"status": result, "path": str(args.log)}, ensure_ascii=False))
    return 0


def self_test() -> None:
    import tempfile
    base = {
        "decision_id": "JEV-TEST-1", "timestamp": "2026-09-21T00:00:00Z", "actor": "lfa-pm",
        "task_id": "TASK-1", "plan_id": "M1", "deliverable_id": "M1-D05", "file_scope": ["src/example.py"], "question": "continue?", "context_refs": ["TASK_BOARD.md#TASK-1"],
        "jev": {"output": "advice", "model": "test", "mode": "advisory", "confidence": 0.5},
        "decision": {"result": "APPROVED", "reason": "bounded", "scope": ["TASK-1"]},
        "action": {"type": "CONTINUE", "owner": "lfa-start", "next": "dispatch"},
        "authorization": {"status": "AUTHORIZED_FOR_HANDOFF", "granted_by": "lfa-pm", "recipient": "lfa-start", "task_id": "TASK-1", "plan_id": "M1", "deliverable_id": "M1-D05", "file_scope": ["src/example.py"]},
        "status": "OPEN",
    }
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "decisions.jsonl"
        assert append_record(base, path) != "IDEMPOTENT"
        assert append_record(base, path) == "IDEMPOTENT"
        changed = {**base, "decision": {**base["decision"], "reason": "changed"}}
        try:
            append_record(changed, path)
        except ValueError:
            pass
        else:
            raise AssertionError("conflicting duplicate was accepted")
        rejected = {**base, "decision_id": "JEV-TEST-2", "authorization": {**base["authorization"], "status": "ADVISORY"}}
        try:
            validate_record(rejected)
        except ValueError:
            pass
        else:
            raise AssertionError("non-authorizing handoff was accepted")
        corrupted = Path(directory) / "corrupted.jsonl"
        corrupted.write_text("{broken\n", encoding="utf-8")
        try:
            append_record({**base, "decision_id": "JEV-TEST-3"}, corrupted)
        except ValueError:
            pass
        else:
            raise AssertionError("corrupted log was appended")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
        print("self-test: OK")
    else:
        raise SystemExit(main())
