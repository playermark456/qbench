# Unqualified-address candidate round-trip result

Classification: **`runtime_instantiation_passed_pending_read_only_api_confirmation`**

The qualified-address native-envelope candidate rendered correctly, but QBench
rejected **Save As New Version** with `Invalid cell definition Data!D2 for
field name terpenes_instrument_conc_01`. The error was never an A2 address.
The unqualified candidate was regenerated and validated locally, then the user
imported it into the exact isolated Sandbox Worksheet.

The exact title and breadcrumb were verified. The Versions tab visibly showed
`JSON Scalar 43 Field Base v1` with status `DRAFT`. Before refresh and after a
refresh plus reopen from the Worksheets list:

- the grid was 40x26;
- all 28 visible anchors remained;
- all 43 named cells remained present, unique, unqualified, and exportable;
- all 43 destinations remained blank, writable, and non-formula;
- the first analyte remained `D2`, with no A2 mapping;
- `sdf`, Pass/Fail, Dimethylacetamide, and Peak Table destinations were absent.

QBench's **Export Spreadsheet** action produced the unchanged raw file:
`round_trip/SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE_v1_DRAFT_saved_reopened_export_spreadsheet.json`.
SHA-256:
`3589f2ace8afb96db96d4da638e9effc86bda404e03f97b85fca0e43aa349912`.

The raw export differs from the candidate only because QBench regenerated the
renderer UUID on save. After normalizing that UUID, the parsed JSON objects are
identical. Therefore:

- `json_import_saved_definition_contract=passed_43_of_43`;
- `json_import_round_trip=passed`;
- `destination_contract_proven=runtime_instantiation_passed_pending_read_only_api_confirmation`.

Atomicity remains `api_patch_unresolved` and the analyte PATCH-key contract
remains `unresolved`. The exact Version 1 is now Approved/Active, and the fresh
normal Assay-created runtime Test passed 43/43 before returning to a 43/43
blank baseline.
