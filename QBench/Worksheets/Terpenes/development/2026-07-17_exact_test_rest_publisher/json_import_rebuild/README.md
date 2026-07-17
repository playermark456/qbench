# Old-Sandbox one-tab JSON compatibility rebuild

Date: 2026-07-17

Classification:
**`runtime_instantiation_passed_pending_read_only_api_confirmation`**

Manual testing established two separate findings:

1. the native-envelope candidate rendered successfully as a 40x26 worksheet
   with all 43 named cells; and
2. **Save As New Version** rejected the qualified named-cell definitions with
   `Invalid cell definition Data!D2 for field name terpenes_instrument_conc_01`.

The error was never an A2 address. The intended first analyte is D2, and no A2
destination exists. The compatibility conclusion is that
this exact one-tab legacy worksheet requires unqualified JSON cell strings,
consistent with the working manual `sdf -> A1` control and the active Terpenes
Test Worksheet's unqualified named-cell addresses.

The logical mapping remains sheet-qualified in
`config/field_mapping_scalar_candidate.csv`:

- logical address: `Data!D2`
- old-Sandbox JSON cell representation: `D2`

The generator now strips only the `Data!` prefix when serializing the 43
independent scalar definitions under `qb_config.named_cells`. It does not
change the native envelope, grid, anchors, metadata, sizing, UUID, display
names, export flags, or cell contents.

Corrected candidate:
`SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json`

- SHA-256:
  `e5ef20a5cec574dc292ed679867e01313233c92ceda9ef863bf98dd8d4485b80`
- Grid: 40x26
- Required anchors: 28
- Total non-empty cells: 30
- Named cells: 43 independent scalars
- JSON address representation: 43/43 unqualified
- Analytes: `D2:Z2` in order
- Remaining destinations: individual cells in `B12:B18`, `B22:B23`, and
  `B28:B38`
- A2 mapping: absent

`address_format_comparison.md` proves exactly 43 differences from the
successfully rendered prior candidate and confirms every difference is a
qualified-to-unqualified `cell` string conversion.

The user imported the unqualified candidate into the isolated Sandbox
Worksheet. Browser verification proved the exact title and breadcrumb, a
visible `JSON Scalar 43 Field Base v1` Draft row, and the matching Draft in the
Configuration view. Before refresh and after a refresh plus list-based reopen,
the Draft retained the 40x26 grid, all 28 anchors, and 43/43 unqualified named
cells. All destinations remained blank, writable, unique, non-formula, and
exportable. The first analyte remained `D2`; no A2 mapping, `sdf`, Pass/Fail,
Dimethylacetamide, or Peak Table destination existed.

QBench's **Export Spreadsheet** action produced the unchanged raw file under
`round_trip/` with SHA-256
`3589f2ace8afb96db96d4da638e9effc86bda404e03f97b85fca0e43aa349912`.
After normalizing only QBench's regenerated renderer UUID, it is semantically
identical to the candidate. Therefore:

- `json_import_saved_definition_contract=passed_43_of_43`
- `json_import_round_trip=passed`
- `destination_contract_proven=runtime_instantiation_passed_pending_read_only_api_confirmation`

The prior lock-based stop is now classified as
`approval_attempt_procedural_error_unnecessary_lock_handling`. The user
manually approved Version 1; Codex verified that the exact single Version 1 is
Approved/Active and created no Version 2. The isolated Assay association and a
fresh normal Assay-created Test retained the full 40x26 definition through
list-based reopen. The runtime export passed 43/43, representative values
persisted, B22/B23 stayed blank, and the five probes were cleared back to a
43/43 blank baseline.

No credential was read and no OAuth token, REST request, PATCH, live-QBench
access, Publish, QC Review, or Pass/Fail artifact occurred. The operational
mapping remains unpromoted pending read-only API confirmation. See
`runtime_instantiation/` for the sanitized runtime evidence.
