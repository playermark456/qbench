# Field Index

Last verified in production on 2026-08-16.

The Field and Data Type Settings page exposed 277 definitions across 20 populated object types, including 20 required rows and 30 rows hidden in the QBench UI. The complete row-level index is `QBench/Rescans/2026-08-16/Fields/field_inventory.csv`; the hierarchical evidence and capture limitations are in `field_inventory.json` and the dated README.

| Object type | Definitions | Required | Hidden |
|---|---:|---:|---:|
| Order | 15 | 1 | 4 |
| Sample | 44 | 3 | 5 |
| Test | 13 | 0 | 1 |
| Source | 10 | 1 | 0 |
| Batch | 12 | 0 | 0 |
| Control | 4 | 0 | 0 |
| User | 5 | 0 | 0 |
| Assay | 27 | 0 | 10 |
| Panel | 2 | 0 | 0 |
| Customer | 15 | 3 | 4 |
| Invoice | 7 | 2 | 0 |
| Quotation | 10 | 3 | 0 |
| Supplier | 38 | 1 | 1 |
| Contact | 8 | 1 | 0 |
| Equipment | 19 | 1 | 3 |
| Document | 7 | 1 | 0 |
| Issue | 14 | 1 | 1 |
| Location | 6 | 1 | 0 |
| Inventory Item | 12 | 1 | 1 |
| Inventory Stock | 9 | 0 | 0 |

No Edit control was used. The UI did not distinguish system from custom definitions or expose field IDs, data types, validation, formulas, option sources, KV-store links, or automation/parser/report usage without prohibited actions. Those properties remain explicitly unverified.

## Phase 5 control-field observation

The control detail pages displayed `Concentration` as the selected data field for controls 2, 3, and 4. Control 1 displayed the exact spelling `Concentraiton`. Because the read-only field settings did not expose stable field IDs or deeper properties, this observation is not promoted to a field-definition mapping and the origin of the typo remains unverified. See `CONTROL_INDEX.md`.
