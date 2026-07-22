# Phase 4A.6 V4 round trip

The verified Dynamic Spreadsheet was saved as exactly one Draft, reopened from the Worksheets list, and exported with QBench **Export Spreadsheet**.

- Object: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4_DYNAMIC`
- Version: `1 - Terpenes Production Candidate Test Worksheet v4 Dynamic`
- Saved state at the round-trip gate: `DRAFT`
- Raw ignored export: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4_DYNAMIC__saved_reopened_export_spreadsheet.json`
- Raw SHA-256: `3db41897b9d9fa8f134458c0dce66fdac097f0c9aca67474520feffae2cbfff1`

The accepted semantic comparator proved exact embedded formula data, non-formula data, tab order, dimensions, row/column metadata, styles, number formats, protection, 44 named definitions, `report_results`, and all 44 five-argument Key/Value calls.

Permitted QBench normalization was limited to three `minDimensions = [1,1]` values, six positive editor viewport dimensions, and 309 evaluated top-level formula-cache values. All 309 embedded formulas remained authoritative and exact.

`v4_dynamic_static_render = passed`

`v4_dynamic_round_trip = passed_with_expected_qbench_normalization`
