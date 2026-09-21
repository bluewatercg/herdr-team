#!/usr/bin/env bash
set -eu

MODE="dry-run"
if [ "${1:-}" = "--apply" ]; then
  MODE="apply"
elif [ -n "${1:-}" ]; then
  echo "Usage: $0 [--apply]" >&2
  exit 2
fi

PACKAGE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(pwd)
BACKUP_DIR=""
if [ "$MODE" = "apply" ]; then
  BACKUP_DIR=$(mktemp -d)
  trap 'rm -rf "$BACKUP_DIR"' EXIT
fi

required=(
  "herdr-team/prompts/pm.md"
  "herdr-team/prompts/start.md"
  "herdr-team/prompts/review-code.md"
  "herdr-team/README.md"
)
for path in "${required[@]}"; do
  if [ ! -f "$ROOT/$path" ]; then
    echo "Missing expected project file: $path" >&2
    exit 2
  fi
done

show_action() {
  printf '%-8s %s\n' "$1" "$2"
}

replace_marked() {
  target=$1
  snippet=$2
  old_begin=$3
  old_end=$4
  new_begin=$5
  relative=${target#$ROOT/}
  if grep -Fq "$new_begin" "$target"; then
    show_action "SKIP" "$relative already contains Revision 2 marker"
    return
  fi
  if [ "$MODE" = "dry-run" ]; then
    if grep -Fq "$old_begin" "$target"; then
      show_action "WOULD" "replace Slice 1 section in $relative"
    else
      show_action "WOULD" "append Slice 1 section to $relative"
    fi
    return
  fi
  backup="$BACKUP_DIR/$(basename "$target")"
  cp "$target" "$backup"
  tmp="$BACKUP_DIR/$(basename "$target").tmp"
  if grep -Fq "$old_begin" "$target"; then
    in_section=0
    inserted=0
    : > "$tmp"
    while IFS= read -r line || [ -n "$line" ]; do
      if [[ "$line" == *"$old_begin"* ]]; then
        cat "$snippet" >> "$tmp"
        in_section=1
        inserted=1
      elif [ "$in_section" = 1 ] && [[ "$line" == *"$old_end"* ]]; then
        in_section=0
      elif [ "$in_section" = 0 ]; then
        printf '%s\n' "$line" >> "$tmp"
      fi
    done < "$target"
    [ "$inserted" = 1 ] || { echo "Missing marker: $old_begin" >&2; exit 2; }
  else
    cat "$target" > "$tmp"
    printf '\n' >> "$tmp"
    cat "$snippet" >> "$tmp"
  fi
  mv "$tmp" "$target"
  show_action "REPLACE" "$relative"
}

sync_file() {
  source=$1
  target=$2
  relative=${target#$ROOT/}
  if [ -e "$target" ] && cmp -s "$source" "$target"; then
    show_action "SKIP" "$relative already matches package"
    return
  fi
  if [ "$MODE" = "dry-run" ]; then
    show_action "WOULD" "sync $relative"
    return
  fi
  mkdir -p "$(dirname -- "$target")"
  if [ -e "$target" ]; then
    cp "$target" "$BACKUP_DIR/$(basename "$target").existing"
  fi
  cp "$source" "$target"
  show_action "SYNC" "$relative"
}

sync_file "$PACKAGE_DIR/files/.agent-control/PM_REQUIREMENT_INTAKE.md" \
  "$ROOT/herdr-team/.agent-control/PM_REQUIREMENT_INTAKE.md"
sync_file "$PACKAGE_DIR/files/herdr_remediation/slice-1/SLICE_1_IMPLEMENTATION_PLAN.md" \
  "$ROOT/herdr-team/herdr_remediation/slice-1/SLICE_1_IMPLEMENTATION_PLAN.md"
sync_file "$PACKAGE_DIR/files/herdr_remediation/slice-1/SLICE_1_ACCEPTANCE.md" \
  "$ROOT/herdr-team/herdr_remediation/slice-1/SLICE_1_ACCEPTANCE.md"

replace_marked "$ROOT/herdr-team/prompts/pm.md" \
  "$PACKAGE_DIR/snippets/pm.md.append.md" \
  "BEGIN HERDR SLICE 1: REQUIREMENT INTAKE" \
  "END HERDR SLICE 1: REQUIREMENT INTAKE" \
  "BEGIN HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE"
replace_marked "$ROOT/herdr-team/prompts/start.md" \
  "$PACKAGE_DIR/snippets/start.md.append.md" \
  "BEGIN HERDR SLICE 1: INTAKE DISPATCH GUARD" \
  "END HERDR SLICE 1: INTAKE DISPATCH GUARD" \
  "BEGIN HERDR SLICE 1 REVISION 2: INTAKE DISPATCH GUARD"
replace_marked "$ROOT/herdr-team/prompts/review-code.md" \
  "$PACKAGE_DIR/snippets/review-code.md.append.md" \
  "BEGIN HERDR SLICE 1: INTAKE QA BOUNDARY" \
  "END HERDR SLICE 1: INTAKE QA BOUNDARY" \
  "BEGIN HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE QA BOUNDARY"
replace_marked "$ROOT/herdr-team/README.md" \
  "$PACKAGE_DIR/snippets/README.md.append.md" \
  "BEGIN HERDR SLICE 1: REQUIREMENT INTAKE OVERVIEW" \
  "END HERDR SLICE 1: REQUIREMENT INTAKE OVERVIEW" \
  "BEGIN HERDR SLICE 1 REVISION 2: REQUIREMENT INTAKE OVERVIEW"

if [ "$MODE" = "apply" ]; then
  rm -f "$ROOT/herdr-team/herdr_remediation/slice-1/PM_RI_001.yaml"
  echo
  echo "Applied Slice 1 Revision 2. Temporary backups were kept outside the repository."
else
  echo
  echo "Dry run only. Re-run with --apply after reviewing package content."
fi
