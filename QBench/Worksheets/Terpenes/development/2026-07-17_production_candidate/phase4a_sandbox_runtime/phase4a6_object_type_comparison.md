# Phase 4A.6 V4 QBench object-type comparison

Date: 2026-07-21

The Sandbox Worksheets list established this deployment history:

| Candidate object | QBench type | Result |
| --- | --- | --- |
| V2 Test worksheet | Dynamic Spreadsheet | Rendered historical control |
| V3 Test worksheet | Dynamic Spreadsheet | Rendered and runtime-instantiated historical control |
| `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4` | Spreadsheet | Expected negative control: named cells loaded, workbook collapsed |
| `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS_V4_DYNAMIC` | Dynamic Spreadsheet | Report, Data, and Specifications rendered and round-tripped |

Both V4 observations used the exact unchanged candidate with SHA-256 `53554a8dc167202da373e856df7c1905aab19d117353ec2899cc2de708447924`. The differing outcome is attributable to the QBench shell type, not to the V4 JSON, five-argument formulas, Key/Value Store, named cells, styles, formulas, or dimensions.

`regular_spreadsheet_v4_control = failed_expected_object_type_mismatch`

`dynamic_spreadsheet_v4_control = rendered_successfully`

`v4_static_failure_root_cause = qbench_object_type_mismatch`
