# Jev Intake Precheck MVP

```yaml
status: EXPERIMENT_ONLY
authority_effect: NONE
model: jev-1.13.0
```

Read-only semantic experiment for `lfa-pm`. This directory does not modify Herdr
authority files, Requirement Intake, Task Board, PM Gate, Review Queue, prompts,
runtime roles, or dispatch state. Jev is a semantic sensor only; its output never
creates permission or execution authority.

## Boundaries

- Python 3.10+ standard library only; HTTP uses `urllib.request`.
- The API key is read only from `TYPESAFE_API_KEY`; it is never printed or persisted.
- Results are written only below `/tmp/herdr-jev-intake-mvp/` using secure atomic writes.
- The eight cases are synthetic/de-identified baselines. No production Chronicle,
  Requirement Intake, secrets, raw images, or complete repository context is sent.
- All `may_*` authority fields are hard-coded `false`; `authority_effect` is always
  `NONE`.
- No Gate, Review, Task, Dispatch, Agent, role, or pane is created.

## Checks

```bash
python3 herdr-team/experiments/jev-intake-mvp/jev_intake_mvp.py --self-test
python3 herdr-team/experiments/jev-intake-mvp/jev_intake_mvp.py \
  --cases herdr-team/experiments/jev-intake-mvp/cases.json \
  --output /tmp/herdr-jev-intake-mvp/offline-results.json \
  --offline-validate
```

Offline validation never fabricates Jev probabilities. It validates the case schema,
source normalization, secret policy, deterministic governance rules, and safe output
path without making a network request.

## Online experiment

Requires an existing environment variable, never a command-line key:

```bash
export TYPESAFE_API_KEY
python3 herdr-team/experiments/jev-intake-mvp/jev_intake_mvp.py \
  --cases herdr-team/experiments/jev-intake-mvp/cases.json \
  --output /tmp/herdr-jev-intake-mvp/results.json
```

The online path makes at most one sequential `POST /v1/systemone` request per case,
uses one Choice and four Noul questions in one `questions` map, applies bounded
retry only to transient failures, and records no raw request, response, header, or
key. Jev failures remain fail-safe and do not affect Herdr.

Exit codes: `0` normal, `2` input/argument error, `3` missing key, `4` API failure,
`5` invalid response, `6` dangerous false authorization or authority violation,
`7` unsafe output path.
