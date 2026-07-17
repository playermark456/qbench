# Complete Batch publish gate

No API write may occur until every candidate Publish row and every exact
destination Test has passed the complete plan.

## Source row requirements

- Publish row is nonblank and exact Test ID is present.
- Test ID occurs exactly once among Publish rows.
- Test ID occurs exactly once in selected Batch `test_ids`.
- Instrument Import has exactly one row with that exact Test ID.
- Instrument Import `AF` is `Valid`.
- Instrument Import `AG` is `Import row valid`.
- Publish and Instrument Import source-row hashes are nonblank and equal.
- All 23 reportable analytes are native numeric values and match in controlled
  order between Instrument Import `AH:BD` and Publish `D:Z`.
- Compound Results count is native numeric `24`.
- Peak Table count is native numeric `34`.
- reportable analyte count is native numeric `23`.
- Dimethylacetamide audit values are numeric and never mapped.
- sample mass and final volume are positive native numeric values.
- dilution mode is one of the two approved values, with positive DF when
  `apply_in_qbench` is selected.
- unit is exact `ug/mL`; unit and preparation confirmations are TRUE.
- required source, preparation, integration, and instrument metadata are
  complete.
- integration review is `Reviewed`.
- Batch QC disposition is `Accepted`.
- Publish validation and readiness controls pass.

Parser job `SUCCESS` is not a gate input.

## Reviewer binding

The runtime Batch Worksheet must contain these saved named ranges:

- `terpenes_batch_publish_authorization`;
- `terpenes_batch_publish_authorized_by`;
- `terpenes_batch_publish_authorized_at`;
- `terpenes_batch_publish_reviewed_source_row_hash`;
- `terpenes_batch_last_published_source_row_hash`.

Authorization must be exact `Authorized`, reviewer and timestamp must be
nonblank, and the reviewed hash must equal the current source-row hash. A
different hash produces `REAUTHORIZATION REQUIRED`, never an overwrite.

These ranges do not exist in the merged Prompt 5 Batch candidate. Their absence
is a required controlled stop until a separate saved Sandbox worksheet proves
the contract.

## Exact destination requirements

The exact GET Test response must match Test ID, selected Batch, Sample ID,
expected assay ID/name, and workflow. Every mapped target must be present,
unique, scalar at its intended cell, writable, and not formula-owned. Any
Pass/Fail-like named cell in the Test Worksheet blocks the entire plan.

Global runtime evidence must also prove the saved destination contract,
analyte PATCH representation, and `api_patch_atomic` before direct publish.

The 2026-07-17 underscore-scalar Phase 1A attempt does not clear this gate.
Although its local 43-row candidate mapping validates, the saved/reopened
native Draft retained zero of seven representative named-cell definitions.
It was not approved or activated, no Export Spreadsheet was run, and no
runtime Test was created. `destination_contract_proven` remains false and the
operational mapping was not changed.
