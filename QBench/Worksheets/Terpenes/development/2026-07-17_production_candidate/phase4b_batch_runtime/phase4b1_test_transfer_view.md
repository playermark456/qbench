# Phase 4B.1 Test Transfer view

Date: 2026-07-21

## Passed surface checks

- Only Sample A and Sample B appeared in Test Transfer rows.
- Null, Blank, Standard, CCV, LOQ, and QC controls did not appear.
- The 23 instrument channels were present in the intended D:Z order.
- Preparation confirmation and source/audit metadata fields were present.
- Dimethylacetamide was present only as an audit field.
- No formula-owned Batch validation field was presented as an analytical Test input.
- No Pass/Fail, Publish instruction, or QC Review instruction was transferred.
- No Batch-to-Test write was executed.

## Controlled blocker

- Both sample rows correctly showed analytical/source prerequisites as false while the transfer cells were intentionally unpopulated.
- Publish Ready and Publish Message displayed `#ERROR` instead of a neutral false/hold message.
- Blank template rows also displayed the same Publish Ready/Message errors.
- The error persisted after save/reopen.

The candidate-inclusion and column-mapping surface passed, but the runtime readiness/message formula surface did not. Phase 4B.2 must not begin until a separately authorized candidate revision removes the runtime formula errors and repeats the affected gates.

`batch_v2_test_transfer_view = blocked_publish_ready_and_message_formula_errors`
