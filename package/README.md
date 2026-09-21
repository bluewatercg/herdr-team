# Herdr Team Slice 1 Revision 2 Upgrade Package

> Status: `PROPOSAL`
>
> Implementation baseline: `false`
>
> Scope: PM Requirement Intake contract and prompt governance only

This package revises Slice 1 so unresolved discussion cannot be mistaken for a formal
task while preserving the existing six-role runtime chain.

It does not create a runtime role, seventh pane, `lfa-core`, Chronicle implementation,
automatic dispatch, or a mandatory Reviewer Gate. External decision-aid tools have no
authority effect and are not part of the permanent Prompt contract.

## Package contents

```text
files/.agent-control/PM_REQUIREMENT_INTAKE.md
files/herdr_remediation/slice-1/SLICE_1_IMPLEMENTATION_PLAN.md
files/herdr_remediation/slice-1/SLICE_1_ACCEPTANCE.md
snippets/pm.md.append.md
snippets/start.md.append.md
snippets/review-code.md.append.md
snippets/README.md.append.md
apply_slice1.sh
MANIFEST.sha256
```

`PM-RI-001` has one authoritative copy in the target `.agent-control` register. The
package intentionally contains no independent Intake YAML copy.

## Use

```bash
bash /path/to/package/apply_slice1.sh
bash /path/to/package/apply_slice1.sh --apply
```

The default is dry-run. `--apply` is explicit, idempotent, replaces marked prior Slice
1 sections, and keeps any temporary backups under `mktemp` rather than the repository.

Review the Git diff after application. Do not update the repository `SHA256SUMS.txt`
until final content review is complete.
