# Phase 4B.1 Batch Review runtime result

Date: 2026-07-21

## Passed observations

- `integration_review_complete` evaluated true.
- `qc_data_complete` evaluated true.
- `qc_configuration_complete` remained false because the documented method-owner decisions are unresolved.
- `qc_review_complete` remained false and the Batch QC disposition remained Hold.
- Control and sample input rows remained distinguishable through Instrument Import classification.
- No Pass/Fail appeared.

## Controlled blocker

After the eight-row manual probe:

- `all_publish_rows_valid` displayed `#ERROR`.
- `duplicate_test_id_count` displayed `#ERROR`.
- The same values persisted after a normal nonfinal save and reopen.

Candidate dependency review shows that these aggregates read Test Transfer BB/BD, while Test Transfer Publish Ready/Message logic reads Batch Review release state. This creates a runtime-sensitive cross-sheet dependency, including a direct release-state dependency from the publish-message path. The observed `#ERROR` state is recorded as a genuine Batch review/transfer-readiness contract defect; no formula was edited in Phase 4B.1.

`batch_v2_batch_review = blocked_persistent_cross_sheet_formula_errors`
