# Phase 4B.2 parser contract

Classification: `parser_package_ready_for_sandbox_execution`

The authoritative multi-record parser is `QBench/Worksheets/Terpenes/development/2026-07-15_qbench_native_parser_probe/src/terpenes_multirecord_batch_cli.js`.

- Source is split at `[Header]`; each record must contain all eight controlled sections.
- Quantitative values come only from `Compound Results(Ch1) > Conc.`.
- All 24 controlled compound-result IDs are required: Dimethylacetamide (ID 1) is audit-only and IDs 2–24 are the ordered reportable Terpenes channels.
- Every Peak Table is retained for audit. Its variable row count is not used for quantitation.
- Each record normalizes to the 57-column Instrument Import contract. The writer emits only A:AE and AH:BE (55 columns) and never writes formula-owned AF or AG.
- `source_file_hash` and deterministic `source_row_hash` are populated. Repeated parsing of unchanged input produces identical normalized rows and row keys.
- Sample-to-Test linkage defaults to the LabSolutions Sample ID only for non-control, non-validation-label records. Low/Medium/High validation labels are held from Test Transfer. An optional ignored local runtime CSV may replace only the normalized `qbench_test_id` linkage.
- Controls remain excluded from Test Transfer. No Pass/Fail result is created.

The raw LabSolutions input and runtime mapping/output directory are not tracked.
