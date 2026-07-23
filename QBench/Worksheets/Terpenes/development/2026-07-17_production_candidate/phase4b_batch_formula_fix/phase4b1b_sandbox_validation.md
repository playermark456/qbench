# Phase 4B.1B/B3B Sandbox validation - pre-transfer runtime passed

Date: 2026-07-22
Sandbox only: `https://ait-sandbox.qbench.net`
Final classification: `batch_v2_dynamic_formula_fix_passed_ready_for_parser_and_transfer_validation`

## Reclassification

The approved and active Batch Version 2 was instantiated on a fresh isolated Batch with two fresh, intentionally analytically blank Tests. The exact eight-row manual fixture persisted after normal save/reopen. AF/AG recalculated, all six controls were excluded from Test Transfer, and only Sample A and Sample B were included.

The earlier `controlled_blocker_test_transfer_lookup_fields_blank_for_filtered_sample_rows` conclusion is superseded. The blank Test Transfer D:Z analytical fields and associated preparation/audit staging fields are expected before parser execution and Batch-to-Test transfer. They are not failed lookups.

`AZ` Analytical Values Complete, `BA` Source/Audit Complete, and `BB` Row Prerequisites Complete therefore remain `false` pre-transfer. B12 correctly remains `false`, and BD correctly reports `Analytical values incomplete`. B13 = `0` and B14 = `2` prove the duplicate-ID and populated-row formulas are working. The absence of `#ERROR` proves the Version-2 formula correction passed.

## Preserved runtime observations

- Batch Review B12: `false`.
- Batch Review B13: `0`.
- Batch Review B14: `2`.
- Batch Review B18: `false`.
- Batch Review B19: `Run setup incomplete`.
- Sample A BC/BD: `FALSE` / `Analytical values incomplete`.
- Sample B BC/BD: `FALSE` / `Analytical values incomplete`.
- `pretransfer_test_transfer_state = expected_incomplete_until_parser_and_transfer`.
- `batch_formula_fix = runtime_passed`.
- `formula_error_count = 0`.

## Validation scope and outcome

1. Active Version 2: Approved/Active Dynamic Spreadsheet; Version 1 remains Approved and preserved; no Version 3 exists.
2. Formula correction: quoted Test Transfer references persisted, the former circular dependency is absent, and no formula errors were observed.
3. Fresh fixtures: two collision-free synthetic Samples each created one NOT STARTED Test; the fresh Batch contains only those Tests. Internal identifiers are intentionally omitted.
4. Manual fixture: Null, Blank, Standard, CCV, LOQ, QC, Sample A, and Sample B were entered only in parser-writable cells.
5. AF/AG: formula-owned/read-only and recalculated. Null retained `Sample type required`; the other rows retained their expected pre-transfer review state.
6. Filtering: all six controls were excluded; only Sample A and Sample B were included.
7. Batch Review: B12/B13/B14 and B18/B19 remained valid non-error values with the observed pre-transfer results above.
8. Test Transfer: BC/BD remained valid non-error pre-transfer values; no Batch-to-Test transfer was executed.
9. Save/reopen: all eight rows, classifications, filtering, and observed non-error values persisted.
10. Fresh Tests: remained NOT STARTED and analytically unmodified.
11. No parser, ASCII upload, transfer, Pass/Fail, completion, publication, release, QC Review, METRC action, or cleanup occurred.
12. Environment boundary: Sandbox UI only during the runtime task; no live QBench, QBench APIs, OAuth, or browser developer tools were used.

## Local B4 reconciliation

- Reclassified the prior false blocker without changing the worksheet, formulas, candidate JSON, or Sandbox data.
- Focused tests cover both pre-transfer and post-transfer staging expectations.
- Version-2 saved-export SHA-256: `9f001553950403101be8f55e0ac592d77ea32105b76afaaa7c1374a3095c3aea`.
- Candidate round trip: `passed_with_expected_qbench_normalization`.
