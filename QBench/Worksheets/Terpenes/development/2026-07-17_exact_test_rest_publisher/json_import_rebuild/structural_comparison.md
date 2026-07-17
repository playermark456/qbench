# Structural comparison: failed, working native, rendered qualified

Classification: **`qualified_address_native_envelope_rendered_save_rejected`**

| Property | Failed candidate | Working native export | Rendered qualified candidate |
|---|---|---|---|
| Envelope | newer config/qb_config/data | legacy table_config/qb_config | legacy table_config/qb_config |
| Top-level keys | ["config", "qb_config", "data"] | ["table_config", "qb_config"] | ["table_config", "qb_config"] |
| config.style type | null | absent | absent |
| config.style value | None | <absent> | <absent> |
| minDimensions | [1, 1] | <absent> | <absent> |
| Rows | 40 | 40 | 40 |
| Columns | 26 | 26 | 26 |
| Non-empty cells | 0 | 8 | 30 |
| Worksheet data dimensions | 40x26 | 40x26 | 40x26 |
| Worksheet data storage | config.worksheets[0].data | table_config.cell_settings | table_config.cell_settings |
| Top-level Data dimensions | 40x26 | absent | absent |
| Named-cell count | 43 | 1 | 43 |
| Namespace | fba1ba1a-6b6b-4101-be22-b4ef4935f65c | <absent> | <absent> |
| Worksheet ID | 148d340f-a118-495e-ac94-e9df7ab115a2 | <absent> | <absent> |
| Worksheet name | Data | <legacy single logical Data worksheet> | <legacy single logical Data worksheet> |
| tableHeight | 350 | <absent> | <absent> |
| tableWidth | 1588 | <absent> | <absent> |
| Worksheet style type | object | absent | absent |

## Failed-candidate defects

- Used the newer config/qb_config/data envelope instead of the working legacy table_config/qb_config envelope.
- config.style was null while the working native export has no config object or config.style field.
- minDimensions was [1, 1] despite serialized 40x26 arrays.
- The import loaded 43 qb_config.named_cells entries but rendered only a collapsed/default blank cell.
- The import was applied to the NATIVE_SCALAR worksheet instead of the JSON_SCALAR worksheet.

## Complete working-native to rendered-qualified difference

- Named cells: removed the sole diagnostic `sdf / A1` entry and replaced it
  with exactly the 43 Data-qualified entries from
  `config/field_mapping_scalar_candidate.csv`.
- Changed cell-value addresses (25): `A1, E1, F1, G1, H1, I1, J1, K1, L1, M1, N1, P1, Q1, R1, S1, T1, U1, V1, W1, X1, Y1, A12, A22, A28, A40`.
- Cell metadata identical after the required renderer-UUID substitution: `true`.
- Native default settings identical: `true`.
- Native plugin settings identical: `true`.
- No other `table_config` field changed.
- The single native renderer UUID was replaced everywhere by one fresh UUID;
  no source-specific UUID was copied.

The old Sandbox legacy export serializes one unnamed table and has no
`config`, `config.style`, `config.worksheets`, worksheet UUID,
`minDimensions`, or top-level `data["Data"]`. The rendered qualified candidate
preserves that exact single-table representation. This is intentional: the
failed candidate's invented newer envelope was the structural defect that
loaded named-cell configuration while collapsing the rendered sheet. Manual
testing later confirmed that this native-envelope file rendered correctly but
failed Save As New Version because its named-cell addresses were qualified.
