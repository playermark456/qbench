# QBench native File Parser Sandbox probe

Date: 2026-07-15

This repository-only package prepares the controlled Prompt 4.6 QBench
Sandbox runtime probe. Stage 0 creates locally testable browser-safe parser
code, guarded stage scripts, a disposable Batch Spreadsheet Worksheet
candidate, mocks, tests, deterministic distributions, and sanitized evidence.

## Current status

- `stage_0_repository_preparation = passed`
- `stage_1_no_write_runtime = incomplete_retry_pending`
- `stage_2_batch_context = not_run`
- `stage_3_scalar_patch = not_run`
- `stage_4_range_patch = not_run`
- `stage_5_two_block_patch = not_run`
- `stage_6_failure_behavior = not_run`
- `stage_7_terpenes_fixture_probe = not_run`
- `qbench_sandbox_probe_status = stage_1_retry_pending`
- `qbench_native_status = blocked`

Stage 1 created the single controlled Sandbox-only parser configuration and an
inactive/DRAFT version under explicit authorization. The first Preview used
one controlled fixture and failed safely with `UNEXPECTED_PARSE_ERROR`. It
invoked no worksheet service and modified no worksheet or File Parser Results
destination. No trigger or assay was added, nothing was activated, no
worksheet was imported, and Stage 2A and Prompt 5 were not started.

The corrected retry accepts Array and FileList-like `QB.files` collections,
uses stable controlled validation codes, and emits sanitized step diagnostics.
The exact FileList cause remains a hypothesis until the retry runs.

## Package contents

- `config/` records probe limits, the controlled runtime contract, and a
  sanitized Sandbox-object evidence template.
- `src/` contains a browser/worker-safe LabSolutions parser core and guarded
  stage-specific probes.
- `scripts/` builds the disposable worksheet and distributions and validates
  the complete package.
- `tests/` contains JavaScript runtime mocks, security/write-guard tests,
  Python package tests, the controlled fixture copy, and expected payloads.
- `dist/` contains generated Stage 0 artifacts. It intentionally does not
  contain a Terpenes Sandbox writer.
- `docs/` contains the stage plan, Stage 0 evidence, safety review, cleanup
  plan, and future Sandbox checklists.

## Controlled dependency gate

- Prompt 3 Test candidate SHA-256:
  `90686b980882b221008f281be33984dc5232e2f3d2632300db3f4a27b529640a`
- Prompt 4 Batch candidate canonical-LF SHA-256:
  `e5c80b1213396cab4932e267fd786c6986c933d4b404f11daa5c5aba0629758e`
- Prompt 4.5 source fixture SHA-256:
  `ed796c690b972ca08f1976b1d8f7355d3e5140e73ffa912c441d6185a093283b`

Merged evidence establishes that the full-replacement Batch worksheet method
is prohibited and that the patch method is the only worksheet-write API that
may be investigated in later, separately authorized stages. Named-range,
array, numeric-cell, noncontiguous-write, failure, and rollback behavior remain
unproven until the corresponding Sandbox stages run.

## Stage 0 validation

Live Stage 0 counts from the final dependency and package reruns:

- Prompt 2 Python tests: 27 passed.
- Prompt 3 Python tests: 50 passed.
- Prompt 4 canonical-LF gate: 39 passed.
- Prompt 4.5 JavaScript tests: 143 passed.
- Prompt 4.5 Python tests: 13 passed.
- Prompt 4.6 JavaScript tests: 33 passed.
- Prompt 4.6 Python tests: 14 passed.
- Total automated tests: 319 passed.

Prompt 4's raw-byte validator is sensitive to Windows checkout line endings
for two local configuration files. Its final gate was run in an isolated copy
with those two dependencies normalized to the canonical-LF hashes recorded by
the Prompt 4.5 manifest; the controlled Prompt 4 candidate hash remained the
required `e5c80b...9758e` throughout. No Prompt 4 file was edited.

## Stage 1 correction validation

- Prompt 4.6 JavaScript tests: 44 passed.
- Prompt 4.6 Python/static tests: 16 passed.
- Prompt 4.6 total: 60 passed.
- Distribution and manifest generation: deterministic across repeated runs.

These are local correction tests only. They do not mark Stage 1 passed. The
corrected inactive/DRAFT parser must be retried with
`Output_redacted_fixture.txt` before Stage 1 can be resolved.

Run from this directory with Node.js and Python 3:

```powershell
node --test tests/js/*.test.js
python scripts/build_probe_worksheet_candidate.py
python scripts/build_qbench_probe_distribution.py
python scripts/validate_qbench_probe_package.py
python -m unittest discover -s tests
python -m py_compile scripts/build_probe_worksheet_candidate.py scripts/build_qbench_probe_distribution.py scripts/validate_qbench_probe_package.py
```

Run both generators twice and compare all generated artifact hashes to confirm
byte-identical output.

## Next action

Continue only under the existing Stage 1 authorization. Select the controlled
fixture for the corrected no-write Preview. Do not begin Stage 2A.
