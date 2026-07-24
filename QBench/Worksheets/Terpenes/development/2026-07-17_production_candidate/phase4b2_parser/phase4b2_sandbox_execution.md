# Phase 4B.2 Sandbox parser execution

Date: 2026-07-23

Final classification: `qbench_parser_upload_artifact_missing`

## Controlled stop

Local preflight passed, but the required QBench-compatible upload artifact does
not exist in the authorized parser package. Per Task C2, execution stopped at
the upload-artifact gate before QBench Sandbox was opened and before any
Sandbox object was created or modified.

## Local preflight

- The authoritative raw bytes were found under the local filename
  `ASCIIData (1).txt`; the task text omitted the space before `(1)`.
- Raw source SHA-256:
  `bfd88621e2e8ab791e63ba38f07c9a1174f9600e1cf3f28d5b12ffbd08f2eb91`.
- The original raw file was read only and remained unchanged.
- Parser syntax checks passed for the core, adapter, and CLI.
- Focused parser tests passed: 17/17.
- Production-candidate compatibility suite passed once.
- Parsed records: 34.
- Category counts: Null 3; Blank 2; System Suitability 3; Standard 6;
  CCV 3; LOQ 1; Matrix Blank 1; Sample 15.
- All 34 records contained Sample Information, Original Files,
  Configuration, Peak Table(Ch1), and 24 Compound Results(Ch1).
- Output contract: 57 Batch columns, with exactly 55 parser-owned writes in
  A:AE and AH:BE.
- Formula-owned AF and AG were excluded from every parser write.
- The ordered 23-channel destination contract matched the active Batch
  candidate.
- Dimethylacetamide remained audit-only in AA.
- Peak Table data was retained for all 34 records.
- Unknown-peak audit total: 138.
- Manual-integration record count: 0.
- Numeric zero observations: 126. The focused negative and blank type tests
  passed; the authoritative source contained no negative or blank compound
  concentrations.
- Deterministic parsing, stable row keys, local idempotency, unmapped Sample
  holds, control exclusion, and the two-record synthetic mapping-overlay test
  passed.
- No Pass/Fail field or result was created.

## Upload-artifact gate

The authoritative local entrypoint is:

`QBench/Worksheets/Terpenes/development/2026-07-15_qbench_native_parser_probe/src/terpenes_multirecord_batch_cli.js`

Local entry function: `run(argumentsList)`.

Parser versions:

- Core: `terpenes-qbench-browser-core-v2`.
- Adapter: `terpenes-multirecord-batch-adapter-v1`.

Local accepted source extension: `.txt`.

Local expected output shape:

- one normalized object;
- `batch_headers`: 57 headers;
- `rows`: 34 normalized row objects for the authoritative source;
- each row contains a 57-value `batch_row` and 55 `write_cells`;
- optional local runtime mapping input is a separate ignored CSV overlay.

This CLI is not a QBench upload artifact. It imports Node-only modules
(`node:crypto`, `node:fs`, and `node:path`) and uses CommonJS `require`. The
browser-safe parser core and adapter expose parsing/normalization libraries,
but no QBench runtime entry function that receives `QB.files`, obtains the
Batch context, performs stable-key upsert/deduplication, writes A:AE and AH:BE,
and calls `QB.success()`.

The authorized package `dist` directory contains only earlier no-write,
context, and guarded patch probes. Its README explicitly states that it does
not contain a Terpenes Sandbox writer. None of those probes is a valid
multi-record Terpenes Batch parser artifact.

Therefore:

- upload artifact path: none;
- QBench parser entry function: none;
- QBench upload artifact version: none;
- QBench runtime output/write shape: not implemented;
- QBench input mode (one raw file versus raw file plus mapping): not
  established by an upload artifact.

No packaging format was improvised.

## Sandbox and downstream results

- Parser object creation: not attempted.
- Fresh Samples, Tests, and Batch: not created.
- Runtime mapping and runtime source: not generated.
- Runtime source SHA-256: not applicable.
- Instrument Import landing: not attempted.
- AF/AG runtime preservation: not evaluated.
- Test Transfer staging AZ:BD: not evaluated.
- Controlled second import: not attempted.
- Batch save/reopen and export: not attempted.
- Raw Batch export SHA-256: not applicable.

## Safety confirmations

- QBench Sandbox was not accessed.
- Live QBench was not accessed.
- No QBench API or OAuth flow was used.
- Browser developer tools were not used.
- No parser, worksheet, Sample, Test, Batch, assay, automation, QC Review,
  publication, release, completion, or METRC configuration was created or
  modified.
- No Batch-to-Test write occurred.
- No Test was analytically modified.
- Nothing was staged, committed, pushed, or sent to PR #14.

## Required next action

Create and locally validate a single QBench-native Terpenes parser upload
artifact that wraps the passed core and adapter, uses only the proven QBench
runtime contract, performs stable-key upsert/deduplication without writing AF
or AG, and defines whether runtime linkage is supplied as one generated
ignored `.txt` file or as a supported raw-plus-mapping input. Task C2 may be
resumed only after that artifact passes syntax and focused execution tests.
