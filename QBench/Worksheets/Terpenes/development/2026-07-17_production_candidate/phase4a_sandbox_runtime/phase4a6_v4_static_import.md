# Phase 4A.6 V4 static-render A/B result

Date: 2026-07-21

The same unchanged V4 JSON was evaluated in two QBench worksheet shell types.

## Preserved negative-control event

`SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4` was created as a regular **Spreadsheet**. Its named definitions loaded, but the workbook collapsed to the one-cell fallback. The object remains inactive and unchanged: it has no saved version, approval, activation, Key/Value association, Assay, Sample, or Test.

The historical event is preserved, but its interpretation is corrected:

`v4_regular_spreadsheet_control = failed_expected_object_type_mismatch`

## Valid Dynamic Spreadsheet deployment

No suitable V4 Dynamic Spreadsheet was present in the refreshed Worksheets list. Codex created exactly one inactive shell named `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4_DYNAMIC`. The user performed the native **Import Spreadsheet** file selection and submission with the unchanged V4 JSON; Codex verified the resulting workbook.

- QBench type: **Dynamic Spreadsheet**
- Tabs, exact order: Report, Data, Specifications
- Dimensions: 23x5, 40x26, 23x21
- Embedded formulas: 309
- Writable destinations: 43
- Named definitions: 44
- `report_results`: `Report!A1:E23`
- One-cell fallback: absent
- Pass/Fail: absent

`user_performed_dynamic_v4_import = true`

`codex_verified_dynamic_v4_result = true`

`dynamic_spreadsheet_v4_control = rendered_successfully`

`v4_candidate_renderer_contract = passed_when_deployed_as_dynamic_spreadsheet`

`v4_static_failure_root_cause = qbench_object_type_mismatch`
