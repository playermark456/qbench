# Terpenes current authoritative state

## Repository

- Branch: `codex/terpenes-production-worksheets`.
- Draft PR: #14; not updated by this reconciliation.
- Current phase: one-time Batch formula-chain reconciliation before a narrow delta patch.

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
- `next_authorized_action = Phase 4B.2: parser execution; ASCII import; Instrument Import landing validation; population of Test Transfer staging fields; post-transfer readiness validation; controlled Batch-to-Test write; idempotency validation`.

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
