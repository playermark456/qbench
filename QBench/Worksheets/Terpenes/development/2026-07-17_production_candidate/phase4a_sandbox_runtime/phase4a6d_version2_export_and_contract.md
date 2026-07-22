# Phase 4A.6D Version 2 export and contract

Date: 2026-07-21

## Attribution and provenance

- `user_created_version_2 = true`
- `user_corrected_store_binding = true`
- `codex_verified_export_and_runtime = false`
- Downloads source: `spreadsheet-export-template (37).json`
- Raw export storage: ignored and uncommitted under `phase4a_sandbox_runtime/raw/`
- SHA-256: `2d6c635d2609825596e4e671b265e73d8e949affc211bc20da7010eaffb08b04`
- The raw bytes were copied unchanged; the exported JSON was not modified.

## Exported definition contract

- Tabs and dimensions: Report 23 x 5, Data 40 x 26, Specifications 23 x 21
- Embedded formulas: 309
- Five-argument Key/Value calls: 44 (21 LOQ, 23 MU)
- Writable destinations: 43
- Named definitions: 44
- `report_results`: `Report!A1:E23`
- Store binding: matches the intended Sandbox V4 Terpenes store and does not match the former TEST store
- Embedded hierarchy: Terpenes -> Cannabis Concentrates -> analyte or component -> LOQ or MU
- Representative embedded values: Alpha-Pinene LOQ 10 / MU 5; Ocimene 1 MU 4; Ocimene 2 MU 8; Nerolidol 1 MU 7; Nerolidol 2 MU 11
- Unit hierarchy: absent
- `MU%` terminal field: absent
- Pass/Fail named cell, column, formula, or key: absent
- Automatic Publish and automatic QC Review: absent

## Semantic comparison

`version_2_round_trip = passed_with_expected_qbench_normalization`

The Version 2 export preserved tab order, dimensions, embedded formulas, all non-formula workbook content, styles, number formats, named definitions, `report_results`, destinations, scientific formulas, and analyte mapping. Accepted QBench normalization was limited to generated identifiers, minimum dimensions, viewport values, evaluated top-level formula-cache values, key ordering, and the embedded associated-store hierarchy.

## Reproducible local candidate

- Candidate: `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v4_binding_fix.json`
- SHA-256: `92c4e87a9e06157fe37b007e805ce9905f3e18ea4516a48211956a909062dc59`
- Original V4 historical candidate SHA-256: `53554a8dc167202da373e856df7c1905aab19d117353ec2899cc2de708447924`
- Deterministic delta: only the two mirrored `Specifications!U2` binding representations

The Sandbox binding comes from the ignored runtime profile. No production profile contains the Sandbox binding.
