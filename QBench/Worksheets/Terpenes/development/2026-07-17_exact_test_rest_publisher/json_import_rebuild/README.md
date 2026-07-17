# Old-Sandbox one-tab JSON compatibility rebuild

Date: 2026-07-17

Classification:
**`unqualified_address_candidate_local_validation_passed_save_retry_pending`**

Manual testing established two separate findings:

1. the native-envelope candidate rendered successfully as a 40x26 worksheet
   with all 43 named cells; and
2. **Save As New Version** rejected the qualified named-cell definitions with
   `Invalid cell definition Data!A2 for field name terpenes_instrument_conc_01`.

The intended first analyte is D2, not A2. The compatibility conclusion is that
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

No QBench environment was accessed in this correction prompt. The regenerated
candidate was not uploaded or saved, so a successful Draft row and
saved/reopened export remain pending. Publisher gates remain closed.
