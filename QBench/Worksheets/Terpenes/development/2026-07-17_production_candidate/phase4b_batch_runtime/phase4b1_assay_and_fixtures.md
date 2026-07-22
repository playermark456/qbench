# Phase 4B.1 isolated Assay and fixtures

Date: 2026-07-21

## Assay

- Created `SBX_ONLY_TERPENES_RUNTIME_ASSAY_BATCH_V2`.
- Associated only `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4_DYNAMIC` and `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS_V2_DYNAMIC`.
- Saved, navigated away, and reopened; both associations persisted.
- No Pass/Fail specification, parser automation, auto-Publish, auto-QC Review, or METRC action was added.

## Samples and Tests

- Created `SBX_ONLY_TERPENES_BATCH_SAMPLE_A` and `SBX_ONLY_TERPENES_BATCH_SAMPLE_B` with matrix Cannabis Concentrates.
- Exactly one fresh Test was created for each Sample.
- Both Tests instantiated the active Test V4 Dynamic Spreadsheet definition. The authoritative active definition is Version 2.
- Both Tests remained NOT STARTED and received no analytical data or version-update action.
- The previously validated Test runtime fixture was not reused or modified.

## Batch

- Created `SBX_ONLY_TERPENES_RUNTIME_BATCH_V2`.
- Associated only the two fresh Tests.
- The Batch instantiated the Batch v2 Dynamic Spreadsheet with all four expected tabs.
- No ASCII file or parser configuration was uploaded.
