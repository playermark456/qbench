# Terpenes QBench parser and wide-row adapter candidate

Date: 2026-07-15

This repository-only package implements the Prompt 4.5 Terpenes parser core,
wide Instrument Import adapter, and reviewed Publish-preview adapter. It does
not modify QBench, Prompt 2, Prompt 3, Prompt 4, active/raw worksheet exports,
COA source, automations, protocol worksheets, METRC configuration, key/value
store configuration, production records, or Prompt 5.

## Status

`qbench_runtime_contract_status = insufficient_for_prompt_4_6`

`qbench_sandbox_probe_status = sufficient_to_begin_controlled_prompt_4_6_probe`

`qbench_native_status = blocked_missing_targeted_qbench_runtime_contract`

The pure JavaScript parser core and adapters are complete and locally tested.
The QBench Code File Parser wrapper is intentionally retained as
`src/qbench_file_parser_entry.template.js`. Official documentation and current
AIT tenant inspection now prove the base `run`/`QB`/`QBBatchService` model and
current `file_parser.js` 1.1.0 / `qbjs.js` 2.7.0 imports. Official QBJS v2.7.0
documentation makes `updateWorksheet` unsuitable for the proposed writer
because it completely replaces Batch worksheet data. `patchWorksheet` is the
preferred candidate for controlled Sandbox investigation because it updates
only included fields and preserves omitted data. Spreadsheet named-range and
array payloads, safe noncontiguous patching, current Batch context, numeric cell
semantics, atomicity/rollback, and supported debugging remain unproven.

The raw LabSolutions file will not contain a QBench Batch ID. A future parser
must obtain the current named Batch's internal ID from supported runtime or
attachment context; it must not infer the Batch from customer/sample data,
hardcode an ID, or require the instrument export to contain one.

Enough is documented for a future approved Prompt 4.6 effort to build a
no-write runtime probe and disposable scalar/range patch tests. This does not
authorize building or activating the final Terpenes writer or any production
action. Prompt 4.6 and Prompt 5 have not started.

## Contents

- `src/labsolutions_ascii_core.js` parses LabSolutions ASCII exports with no
  external dependencies.
- `src/wide_import_adapter.js` converts parsed injection files to Instrument
  Import A:BE logical rows and write plans. `source_row_hash` is source-derived
  only; QBench assignment context is excluded. Multi-file inputs require an
  explicit `filename` or `name`; invented source filenames are rejected.
- `src/reviewed_publish_adapter.js` creates a reviewed-row Publish D:AX preview
  patch only after row-specific review evidence, exact `ug/mL` unit
  confirmation, matching review-evidence identity, and explicit QBench Test ID
  to Publish-row mapping.
- `src/qbench_file_parser_entry.template.js` documents the blocked QBench
  wrapper integration points.
- `dist/` contains copied distribution JavaScript files, generated fixture JSON,
  TSV blocks, and `parser_adapter_manifest.json`.
- `tests/js/` contains Node standard-library tests.
- `tests/fixtures/` contains the copied redacted fixture and deterministic
  expected outputs.

## Fixture result

- Compound Results rows: 24
- Peak Table rows: 34
- Reportable terpene rows: 23
- Dimethylacetamide: retained as numeric audit-only value
- Instrument Import write blocks: `A:AE` and `AH:BE`
- Formula-owned Instrument Import columns excluded: `AF`, `AG`
- Publish preview range: `D:AX`
- Publish AF/AG/AV confirmation outputs: exact text `"TRUE"`
- Source row hash: `cef4d2a0c117ae168d6431c3e918668870546c6d165e36fc5f971515249f4546`
- JavaScript tests: 143
- Python package tests: 13

The parser never writes directly to the Test Worksheet, Publish, or QC Review.
The reviewed Publish adapter is a preview transformation only; it is not Prompt
5 automation.
