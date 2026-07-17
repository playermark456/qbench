# Generated JSON import rebuild

Date: 2026-07-17

Classification: **`json_import_upload_blocked_browser_file_upload_unsupported`**

This directory contains the generated, locally validated candidate for the
isolated Sandbox Spreadsheet Worksheet:

`SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE`

The implementation path is generated JSON import, not manual entry of 43 named
cells. The candidate uses one `Data` worksheet, a 40x26 blank grid, fresh UUIDs,
and exactly 43 sheet-qualified named cells derived from the unpromoted
`config/field_mapping_scalar_candidate.csv`.

Known-good read-only schema references:

- `2026-07-16_full_sandbox_implementation/round_trip/2026-07-16_ait-sandbox_ws_id_62_version_1_draft_export_spreadsheet.json`
  - SHA-256: `2f3b2b17beae2c3361b2cfcccfde121aeb4ed32757127806864d2c2b2da63d19`
  - old-Sandbox round trip with 15 named cells
- `QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_42__worksheet_export_spreadsheet__active__2026-07-04.json`
  - SHA-256: `1ff46aadc31c32b8b176f3eb0091c8ae26d905271fcbc4f1a118a3776f7820e9`
  - Terpenes Test Worksheet and `qb_config.named_cells` reference

Local validation passed before any Sandbox upload action. The exact inactive
worksheet shell was then created and its title and breadcrumb were verified.
The in-app browser explicitly reported that file uploads are unsupported, so
the JSON was not attached or submitted. No Draft version exists and no
round-trip export was run. The completed candidate is ready for manual Sandbox
upload.

The existing native scalar diagnostic worksheet and its user-created `sdf`
control were not modified or deleted.

Controls remain:

- `destination_contract_proven=false`
- `atomicity_classification=api_patch_unresolved`
- `analyte_patch_key_contract=unresolved`
- scalar candidate mapping unpromoted
- no OAuth token, REST API request, PATCH, live-QBench access, approval,
  activation, analytical result, or Pass/Fail artifact
