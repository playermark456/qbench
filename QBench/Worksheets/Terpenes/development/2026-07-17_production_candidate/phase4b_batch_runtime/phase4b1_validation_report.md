# Phase 4B.1 Batch v2 validation report

Date: 2026-07-21

## Baselines

- `test_v4_binding_fix_runtime = passed`
- `coa_report_contract = passed_user_confirmed_live_template_operational`
- `sandbox_coa_preview = nonblocking_sandbox_report_template_error`
- `coa_live_template_functionality_source = user_confirmed_operational_knowledge`
- Codex did not access or validate live QBench.

## Passed gates

- Exact local Batch v2 SHA-256: passed.
- Local validators: passed, including 27/27 parser tests and 51/51 complete production-candidate tests.
- Dynamic Spreadsheet shell and user confirmation: passed.
- Native import, static render, exact tabs/dimensions, and draft save: passed.
- Round trip: `passed_with_expected_qbench_normalization`.
- Version 1 approval/activation and object Active state: passed; no Version 2.
- Isolated Assay, two Samples, two fresh Tests, and one isolated Batch: created and associations persisted.
- Parser landing ranges and AF/AG formula ownership: passed.
- Eight sanitized categories entered only in parser-writable cells.
- AF/AG classification and persistence: passed.
- Test Transfer inclusion/exclusion and 23-channel/preparation/audit mapping surface: passed.
- Both fresh Tests remained NOT STARTED and analytically unmodified.

## Runtime blocker

- Batch Review `all_publish_rows_valid` and `duplicate_test_id_count` displayed `#ERROR`.
- Test Transfer Publish Ready and Publish Message displayed `#ERROR` for both sample rows and blank template rows.
- The errors persisted after normal nonfinal save/reopen.
- The Batch v2 candidate was not modified, as required by the Phase 4B.1 prompt.
- No parser or ASCII upload occurred, and no Batch-to-Test write was attempted.

Phase 4B.2 is not ready to begin. A separately authorized Batch candidate correction and repeat of the affected static/round-trip/runtime gates is required.

`batch_v2_static_render = passed`

`batch_v2_round_trip = passed_with_expected_qbench_normalization`

`batch_v2_dynamic_manual_runtime_blocked_batch_review_test_transfer_formula_errors`
