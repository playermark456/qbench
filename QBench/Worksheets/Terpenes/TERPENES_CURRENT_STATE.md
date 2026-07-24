# Terpenes current authoritative state

## Repository

- Branch: `codex/terpenes-production-worksheets`.
- Draft PR: #14; not updated by this reconciliation.
- Current phase: Phase 4B.2 Task C3 passed the controlled Sandbox parser idempotency check and completed the read-only Test Transfer prerequisite diagnosis.

## Passed Test baseline

- Object type: Dynamic Spreadsheet.
- Validated object: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4_DYNAMIC`, Active Version 2.
- Runtime: 43/43 destinations entered and persisted.
- Ocimene: 13 ug/g; MU display 6.083%.
- Nerolidol: 12.5 ug/g; MU display 7.000%.
- Total Terpenes: 204.7801 ug/g, 0.2047801 mg/g, and 0.02047801%.
- Report: 21 reportable analytes plus Total Terpenes. Pass/Fail is absent.
- Classification: `test_v4_binding_fix_runtime_passed_ready_for_coa_and_batch_v2_validation`.

## COA classification

- `coa_report_contract = passed_user_confirmed_live_template_operational`.
- The live-template functionality attribution is user-confirmed operational knowledge.
- `sandbox_coa_preview = nonblocking_sandbox_report_template_error`.

## Passed Batch baseline

- Object: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS_V2_DYNAMIC`, Dynamic Spreadsheet.
- Batch Version 1 passed static rendering, four-tab structure, save/reopen, semantic round trip, AF/AG ownership, parser landing ranges, control-row exclusion, and sample-row inclusion.
- Tabs/dimensions: Run Setup 25x3, Instrument Import 201x57, Batch Review 45x24, Test Transfer 87x56.

## Current Batch status and next action

- `batch_formula_fix_round_trip = passed_with_expected_qbench_normalization`.
- Corrected Version 2 candidate SHA-256: `50fb7883a6932bc54b09f6997b91f01674e392696e82f77872935bb00576acda`.
- Version 2 saved-export SHA-256: `9f001553950403101be8f55e0ac592d77ea32105b76afaaa7c1374a3095c3aea`.
- Version 2 is Approved/Active through user manual approval; Version 1 remains Approved and preserved but is no longer Active; no Version 3 exists.
- Batch Version 2 is an Approved/Active Dynamic Spreadsheet with an exact passed round trip, persisted quoted Test Transfer references, and the former circular dependency removed.
- Fresh Version-2 runtime fixtures were created in Sandbox: two NOT STARTED Tests and one Batch containing only those Tests. Internal object identifiers are intentionally not tracked.
- The exact eight-row manual fixture persisted after save/reopen. AF/AG recalculated, all six controls were excluded, and only Sample A and Sample B appeared in Test Transfer.
- The observed pre-transfer state is expected: B12 `false`, B13 `0`, B14 `2`, B18 `false`, B19 `Run setup incomplete`, and each sample row BC `FALSE` / BD `Analytical values incomplete`. The Tests were intentionally analytically blank; parser and transfer staging fields have not yet been populated.
- `pretransfer_test_transfer_state = expected_incomplete_until_parser_and_transfer`.
- `batch_formula_fix = runtime_passed` and `formula_error_count = 0`.
- Both fresh Tests remained NOT STARTED and analytically unmodified. No parser, ASCII upload, Batch-to-Test write, Pass/Fail, completion, publication, release, QC Review, METRC action, or cleanup occurred.
- `batch_runtime_validation = batch_v2_dynamic_formula_fix_passed_ready_for_parser_and_transfer_validation`.
- `parser_local_contract = passed`.
- `qbench_parser_write_contract = passed_authoritative_operational_live_parser`.
- `qbench_parser_artifact = locally_passed_ready_for_sandbox_creation`.
- `parser_sample_test_linkage = Sample ID to qbench_test_id with optional ignored runtime mapping overlay; validation labels are held from Test Transfer`.
- `parser_idempotency_contract = passed`.
- Task C2 local preflight reproduced the authoritative 34-record, 57-column, 55-write, 17/17-test baseline.
- The browser-runtime parser artifact is present at 47,297 bytes with authoritative SHA-256 `c67cc07c38fa50d46150f8b45de899a8e2a4bdb48db763edee73fc07cdfe849b`.
- Task C2D focused preflight passed 30/30 artifact checks and 6/6 adapter checks, including the one-update browser contract and synthetic runtime-source generator test.
- Sandbox Task C2D created exactly one parser, two Samples, two NOT STARTED Tests, one Batch, and submitted exactly one successful import. The parser reported 34 records, two resolved Sample rows, thirteen held Sample rows, and nineteen excluded controls.
- The live landing showed 34 Instrument Import rows, 57 columns, preserved AF/AG formula outputs, 23 analyte channels, 34 source-row hashes, an unknown-peak total of 138, and exactly two Test Transfer staging rows.
- Both staged rows remain correctly held for staff integration review. Batch disposition remains Hold and publish ready remains false. No staff-controlled field was completed.
- Task C2E left the Batch without Save and reopened it from the normal Batches list. All 34 rows, source order, parser-owned values, AF/AG computed outputs, audit totals, and two Test Transfer candidates persisted.
- The blocked Batch Save was never executed and was not retried. `qbench_parser_update_persistence = passed_without_additional_ui_save`.
- Task C3 reverified the ignored runtime source at SHA-256 `3b6fda068e6861995f39ab60ed8a35e4a0a9f2378464fe81db3b88bc725e1b9d`, confirmed exactly two Sample-ID-only changes from the authoritative raw source, and submitted exactly one user-authorized identical second import.
- The second import again reported 34 records, two resolved Samples, thirteen held Samples, and nineteen controls. Reopen comparison proved deterministic range replacement: 34 rows before and after, zero duplicate logical rows, rows 36:201 blank, ordered keys/hashes/parser versions unchanged, all 782 analytical cells unchanged and numeric, and all 34 AF/AG formulas preserved.
- `sandbox_parser_idempotency = passed_deterministic_range_replacement`.
- Both associated Tests remained NOT STARTED. AZ/BA/BB/BC remained valid false states, and BD remained neutral `Analytical values incomplete` text with no formula error.
- Both mapped source rows contain 23/23 analytical values and complete parser audit data. Transfer projections remain intentionally gated by expected staff integration review, final-volume/preparation confirmation, and Batch QC prerequisites; no parser or worksheet defect was found.
- `transfer_staging_classification = staff_staging_ready_expected_staff_review_preparation_and_batch_qc_prerequisites`.
- No third import, Batch-to-Test write, analytical Test modification, Pass/Fail, completion, publication, release, QC Review, METRC action, stage, commit, push, or PR update occurred.
- `artifact_validation_source = phase4b2_validation_report.md`.
- `missing_artifact_validation_alias = nonblocking_prompt_filename_mismatch`.
- The prior `required_phase4b2_qbench_artifact_validation_missing` blocker is superseded.
- `parser_sandbox_execution = parser_sandbox_idempotency_passed`.
- `manual_batch_save_security_rejection = nonblocking_browser_automation_limitation`.
- `next_authorized_action = staff_staging_ready`.

## Superseded conclusions — do not reuse

- Regular Spreadsheet collapse was an object-type mismatch.
- The wrong Test Key/Value binding caused the initial blank lookup.
- Old Tests do not migrate to new worksheet versions.
- Component MU is expected blank before positive component input.
- The Sandbox COA error is nonblocking.
- The stale Batch export hash `d7969c0708c64d2eef08d0b8ee600cbca5d232c39a05d61d7cea2910f4bdfbe7` is not authoritative.
- QBench did not rewrite a valid quoted `Test Transfer` reference; the source reference was already invalid.

## Permanent deployment guards

- Test and Batch must be Dynamic Spreadsheet.
- Create fresh runtime objects after approval/activation.
- Quote worksheet names containing spaces.
- Treat source-candidate and saved-export hashes as version-specific.
- Historical evidence may not override this current-state file.
