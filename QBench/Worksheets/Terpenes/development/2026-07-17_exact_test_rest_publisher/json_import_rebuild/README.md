# Corrected native-envelope JSON import rebuild

Date: 2026-07-17

Classification: **`corrected_native_legacy_candidate_local_validation_passed_not_uploaded`**

The prior import is invalid evidence. Manual review established that the failed
candidate was loaded into
`SBX_ONLY_TERPENES_2026_07_17_NATIVE_SCALAR_43_FIELD_BASE`, not the intended
`SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE`, and that QBench
loaded its 43 named-cell definitions while rendering a collapsed/default blank
cell instead of the intended 40x26 worksheet.

The corrected candidate is derived only from the fresh working-native Export
Spreadsheet file:

`source/2026-07-17_SBX_ONLY_TERPENES_NATIVE_SCALAR_43_FIELD_BASE_working_native_export_spreadsheet.json`

- Raw source SHA-256:
  `d86e05122bc9a7fc4b6937e5582d9ff469f15c234e606fc0c5bbdd7d7c3659e5`
- Source shape: legacy `table_config/qb_config`, one 40x26 native matrix,
  one diagnostic named cell `sdf / A1`

Unlike the failed newer-envelope candidate, the working native export has no
`config`, `config.style`, `config.worksheets`, worksheet UUID,
`minDimensions`, or top-level `data["Data"]`. The corrected candidate preserves
that exact legacy shape; absence replaces the failed file's incompatible
`style: null` and `[1, 1]` minimum dimensions.

The generator removes only the diagnostic named-cell definition, installs the
exact 43-field mapping, blanks all 43 destinations, and adds 28 required
visible anchors. It preserves every other native field and cell value. The
one renderer UUID embedded in all 1,040 native cell metadata records is
replaced consistently by one fresh UUID.

Corrected candidate:

`SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json`

- SHA-256:
  `54a65e029b9f1a038a21428cf40727896130db86041fafcc2d0bdf868e7fe35b`
- Grid: 40x26
- Required anchors: 28
- Total non-empty cells: 30 (28 required anchors plus two preserved native
  structural labels)
- Named cells: 43
- Analytes: 23 at `Data!D2:Z2`
- Destination result: 43/43 blank, writable, non-formula, unique, exportable

No corrected upload, save, Draft creation, or round-trip export occurred in
this prompt. The publisher gates remain closed:

- `destination_contract_proven=false`
- `atomicity_classification=api_patch_unresolved`
- `analyte_patch_key_contract=unresolved`
- no OAuth token, REST request, PATCH, live-QBench access, analytical result,
  approval, activation, or Pass/Fail artifact
