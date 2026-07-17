# Native 43-field rebuild evidence

Date: 2026-07-17

Final classification: **`native_minimal_destination_probe_failed`**.

The isolated old-Sandbox Spreadsheet Worksheet
`SBX_ONLY_TERPENES_2026_07_17_NATIVE_43_FIELD_BASE` was built natively as a
40-row by 26-column minimal grid. Version 1, `Native 43 Field Base v1`, remains
Draft. The legacy single-table editor has no sheet-tab/name control, so the
logical `Data` grid is identified by the visible `Data` label in A1.

After save, navigation away, and reopen, the four scalar Phase 1 destinations
persisted exactly. QBench rejected the three required indexed named-cell keys
containing brackets. Otherwise-identical underscore diagnostic controls saved
and reopened, isolating the failure to the bracketed key syntax; those
diagnostic controls were removed before the final saved/reopened state.

Phase 1 therefore ended at 4/7. Per the stop gate, Version 1 was not approved
or activated, no Assay/Sample/Test was created, and Phases 2 and 3 were not
run. QBench's Export Spreadsheet control was invoked on the reopened Draft,
but no downloadable file was produced. No raw export or SHA-256 is claimed.

Publisher controls remain:

- `destination_contract_proven=false`
- `atomicity_classification=api_patch_unresolved`
- `analyte_patch_key_contract=unresolved`

No credential value was displayed. No OAuth token, REST API request, PATCH,
live-QBench access, analytical result, or Pass/Fail artifact occurred.
