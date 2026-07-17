# Unqualified-address JSON candidate validation

Result: **passed**

Candidate:
`SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json`

- exactly one legacy logical Data worksheet
- exact native legacy `table_config/qb_config` envelope preserved
- visible grid exactly 40 rows by 26 columns
- 28 required anchors and 30 total non-empty cells preserved
- exactly 43 independent scalar named cells; diagnostic `sdf` absent
- every JSON `qb_config.named_cells.<name>.cell` value is unqualified
- no JSON named-cell address contains `!`
- exactly 23 analytes at unqualified `D2` through `Z2`, in order
- `terpenes_instrument_conc_01=D2`, never `A2`
- remaining 20 destinations exactly cover `B12:B18`, `B22:B23`, and
  `B28:B38` as independent cells
- required spot checks passed: `_12=O2`, `_23=Z2`, `sample_mass_g=B12`,
  `batch_qc_disposition=B22`, `publish_ready=B23`, and
  `source_file_hash=B30`
- all 43 destinations resolve and remain blank, writable, non-formula,
  unique, and exportable
- no bracketed name, Pass/Fail, Dimethylacetamide, Peak Table destination,
  credential, token, signed URL, or customer-data marker
- comparison with the successfully rendered qualified-address candidate found
  exactly 43 differences, all limited to the named-cell `cell` strings
- grid, anchors, cell metadata, sizing, renderer UUID, and all other content
  are unchanged

Validator: `validate_candidate.py`

Candidate SHA-256:
`e5ef20a5cec574dc292ed679867e01313233c92ceda9ef863bf98dd8d4485b80`
