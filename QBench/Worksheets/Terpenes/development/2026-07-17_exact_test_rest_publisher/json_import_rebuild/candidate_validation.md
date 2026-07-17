# Corrected JSON candidate validation

Result: **passed**

Candidate:
`SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json`

- working-native source bytes match SHA-256
  `d86e05122bc9a7fc4b6937e5582d9ff469f15c234e606fc0c5bbdd7d7c3659e5`
- exact legacy `table_config/qb_config` envelope preserved
- one logical Data worksheet represented by the native single table
- visible grid exactly 40 rows by 26 columns
- 28 required anchors present at A1, D1:Z1, A12, A22, A28, and A40
- 30 total non-empty cells; the two additional values are unchanged native
  structural labels
- exactly 43 mapped named cells; diagnostic `sdf` absent
- all 43 addresses resolve and are blank, writable, non-formula, unique, and
  exportable
- exactly 23 analytes at `Data!D2:Z2`; no bracketed name
- no Pass/Fail, result-status, Dimethylacetamide, or Peak Table destination
- all native cell metadata, sizing, and plugin settings unchanged after
  normalizing the required fresh renderer UUID
- no newer `config.style`, worksheet-data, or top-level Data representation
  introduced; their absence exactly matches the working native export
- no source UUID, credential, token, signed URL, or customer-data marker

Validator: `validate_candidate.py`

Candidate SHA-256:
`54a65e029b9f1a038a21428cf40727896130db86041fafcc2d0bdf868e7fe35b`
