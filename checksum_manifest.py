#!/usr/bin/env python3
"""Verify static release bytes; refresh explicitly after a change set is frozen."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile

# Static distribution scope, not the Jev process-depth trigger set.
STATIC_FILES = (
    ".agent-control/TASKS/TASK_TEMPLATE.md", "README.md", "preflight.sh",
    "activate.sh", "lfa-team.sh", "dashboard.py", "review_dispatch.py",
    "jev_decide.py", "jev_task_depth.py", "test_jev_depth.py",
    "verify_governance.py", "checksum_manifest.py", "harness/shadow.py",
    "harness/verify_shadow.py", "experiments/jev-intake-mvp/jev_intake_mvp.py",
    "prompts/COMMON.md", "prompts/api.md", "prompts/app-apk.md",
    "prompts/app-ios.md", "prompts/pm.md", "prompts/review-code.md", "prompts/start.md",
)


def static_files(root: Path) -> list[str]:
    return sorted(set(STATIC_FILES) | {p.relative_to(root).as_posix() for p in (root / "prompts").glob("*.md")})


def checked_path(root: Path, name: str) -> Path:
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or ".." in path.parts or "\\" in name
            or ":" in name or any(ord(c) < 32 for c in name) or path.as_posix() != name):
        raise ValueError(f"unsafe manifest path: {name!r}")
    target = root / name
    if any((root / Path(*path.parts[:i])).is_symlink() for i in range(1, len(path.parts) + 1)):
        raise ValueError(f"symlink in manifest path: {name}")
    if not target.is_file():
        raise ValueError(f"missing static file: {name}")
    return target


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(text: str) -> dict[str, str]:
    entries = {}
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        match = re.fullmatch(r"([0-9a-f]{64}) [ *](.+)", line)
        if not match:
            raise ValueError(f"malformed checksum at line {number}")
        sha, name = match.groups()
        if name in entries:
            raise ValueError(f"duplicate static file: {name}")
        entries[name] = sha
    if not entries:
        raise ValueError("empty checksum manifest")
    return entries


def check_manifest(root: Path) -> list[str]:
    try:
        entries = parse_manifest((root / "SHA256SUMS.txt").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [str(error)]
    errors = []
    required = set(static_files(root))
    for name in sorted(required - entries.keys()):
        errors.append(f"static file not covered: {name}")
    for name in sorted(entries.keys() - required):
        errors.append(f"file outside static scope: {name}")
    mismatches = 0
    for name, expected in entries.items():
        try:
            actual = digest(checked_path(root, name))
        except (OSError, ValueError) as error:
            errors.append(str(error))
            continue
        if actual != expected:
            mismatches += 1
            errors.append(f"checksum mismatch: {name}")
    if mismatches:
        errors.insert(0, f"checksum mismatches: {mismatches}/{len(entries)} files")
    return errors


def refresh_manifest(root: Path) -> None:
    # Read every required file before replacing anything; never skip missing files.
    entries = [(name, digest(checked_path(root, name))) for name in static_files(root)]
    base = subprocess.run(["git", "-C", str(root), "rev-parse", "--verify", "HEAD"],
                          check=True, capture_output=True, text=True).stdout.strip()
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    text = (f"# BASE_COMMIT: {base}\n# GENERATED_AT: {stamp}\n"
            "# CONTENT_SOURCE: WORKTREE; BASE_COMMIT is provenance, not acceptance or a clean-tree claim.\n")
    text += "".join(f"{sha}  {name}\n" for name, sha in entries)
    temp = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=root,
                                         prefix=".SHA256SUMS-", delete=False) as handle:
            temp = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        for name, sha in entries:
            if digest(checked_path(root, name)) != sha:
                raise ValueError(f"static file changed during refresh: {name}")
        os.replace(temp, root / "SHA256SUMS.txt")
    finally:
        if temp is not None:
            temp.unlink(missing_ok=True)


def self_test() -> None:
    sha = hashlib.sha256(b"hello").hexdigest()
    assert parse_manifest(f"# BASE_COMMIT: example\n{sha}  a.txt\n") == {"a.txt": sha}
    for text in ("# no entries\n", "bad  a.txt\n", f"{sha}  a.txt\n{sha}  a.txt\n"):
        try:
            parse_manifest(text)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid manifest accepted")
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for name in STATIC_FILES:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"hello")
        manifest = root / "SHA256SUMS.txt"
        original = "# BASE_COMMIT: example\n" + "".join(f"{sha}  {name}\n" for name in static_files(root))
        manifest.write_text(original)
        assert check_manifest(root) == []
        manifest.write_text(original.replace(f"{sha}  README.md\n", ""))
        assert "static file not covered: README.md" in check_manifest(root)
        manifest.write_text(original)
        (root / "README.md").write_bytes(b"changed")
        assert "checksum mismatch: README.md" in check_manifest(root)
        assert f"checksum mismatches: 1/{len(STATIC_FILES)} files" in check_manifest(root)
        (root / "README.md").unlink()
        try:
            refresh_manifest(root)
        except ValueError:
            pass
        else:
            raise AssertionError("refresh skipped missing file")
        assert manifest.read_text() == original
        for name in ("../escape", "/etc/passwd", "missing"):
            try:
                checked_path(root, name)
            except ValueError:
                pass
            else:
                raise AssertionError("unsafe or missing path accepted")
        (root / "link").symlink_to(root / "config.env")
        try:
            checked_path(root, "link")
        except ValueError:
            pass
        else:
            raise AssertionError("symlink accepted")
    print("checksum self-test: PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--refresh", action="store_true", help="replace manifest for the frozen worktree; grants no approval")
    mode.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    root = args.root.resolve()
    try:
        if args.refresh:
            refresh_manifest(root)
        errors = check_manifest(root)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(error)
        return 1
    for error in errors:
        print(error)
    if not errors:
        print(f"static checksums: PASS ({len(static_files(root))} files); not an approval")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
