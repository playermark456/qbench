# Prompt 4.6C Sandbox validation results

## Completed validation

- Created an isolated Sandbox-native worksheet with Run Setup, Instrument
  Import, QC Review, and Publish tabs.
- Verified the saved and reloaded worksheet definition has 57 Instrument Import
  columns, 23 analyte columns in AH:BD, and worksheet-owned formulas in AF2 and
  AG2.
- Approved and activated only the isolated worksheet version so it could be
  instantiated on the disposable Batch.
- Confirmed the worksheet has zero assay associations.
- Created the disposable Batch
  `SBX_ONLY_TERPENES_2026_07_16_NO_CODE_IMPORT_01` with the isolated worksheet
  and no assay, protocol, sample, or test.
- Created and activated the isolated No-Code parser with one exact-filename
  Batch attachment trigger and two accepted non-overlapping finders.
- Reloaded the parser and worksheet while configuring them; no pre-existing
  Terpenes object was modified or reused.
- Exported the created worksheet with QBench **Export Spreadsheet**, replaced
  runtime worksheet UUIDs with deterministic non-Sandbox UUIDs, and locally
  validated the sanitized export.
- Locally validated the canonical TSV: 57 columns, 24 Compound Results rows,
  34 Peak Table rows, 23 reportable rows, 23 numeric analytes,
  Dimethylacetamide numeric and audit-only, and AF/AG blank source placeholders.

## Canonical attachment run

The canonical file was attached manually in a normal browser because the Codex
in-app browser cannot choose a local file. The active exact-filename parser ran
once and QBench Parser History recorded `SUCCESS` for the Batch Worksheet data
target.

Observed after the parser completed and again after navigating away and
reopening the Batch:

- the two non-overlapping finders populated A2:AE2 and AH2:BE2;
- AF2 evaluated to `Valid` and AG2 evaluated to `Import row valid`;
- all 23 AH:BD analyte cells used QBench's native numeric cell type and matched
  the deterministic fixture values;
- Compound Results row count X2 was numeric `24`, Peak Table row count Y2 was
  numeric `34`, reportable row count Z2 was numeric `23`, and
  Dimethylacetamide count AA2 was numeric `100`;
- the exact source-row hash persisted in BE2;
- no `#REF!`, `#VALUE!`, or other spreadsheet error was visible;
- Publish remained blank and the Batch had no tests, samples, assay, or
  protocol.

The sanitized Export Spreadsheet artifact preserves the exact worksheet-owned
AF2 and AG2 formulas. The live canonical run confirms those formulas evaluated
correctly after parser population and reload. Duplicate and malformed runs are
tracked separately.
