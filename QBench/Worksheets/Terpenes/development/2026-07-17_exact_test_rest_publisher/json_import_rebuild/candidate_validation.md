# JSON candidate validation

Candidate:
`SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json`

Result: **passed**

- valid JSON with required top-level `config`, `qb_config`, and `data`
- exactly one worksheet named `Data`
- exactly 40 rows and 26 columns
- exactly 43 named cells and 23 analyte named cells
- analyte names exactly `terpenes_instrument_conc_01` through
  `terpenes_instrument_conc_23`
- analyte addresses exactly `Data!D2` through `Data!Z2`
- all 43 system names and addresses unique
- all addresses resolve inside the Data grid
- all destinations blank, writable, non-formula, and `export: true`
- no bracketed destination name and no `sdf`
- no Pass/Fail or result-status field
- no Dimethylacetamide or Peak Table reportable destination
- no merged cells, images, conditional formatting, hidden/frozen rows or
  columns, or formulas
- fresh UUID namespace and worksheet ID; neither is reused from a reference
- no credentials, tokens, signed URLs, or customer data

Validator: `validate_candidate.py`

Candidate SHA-256:
`7cfeeee00403e8c3fa7bf7ec4c2726e25f63cc1f4b867bc1f06550f612ef8f70`
