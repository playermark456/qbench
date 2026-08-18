# Fields and Data Types — 2026-08-16

The production Field and Data Type Settings page exposed 277 field-definition rows across 20 populated object types. Two additional panes, Default Test Comments and Default Test Results, contained no rows.

| Object type | Definitions | Required | Hidden in QBench UI |
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
| **Total** | **277** | **20** | **30** |

## Capture boundary

No Edit, New Field, Show, Hide, Clone, or workflow control was used. Field IDs, data types, writable/read-only state, validation, formula, option source, KV-store association, and parser/automation/report usage were not exposed without prohibited Edit actions. Protocol, Protocol Step, Resource, Report, and Stability panes were not offered by this settings screen.

`field_inventory.json` preserves the hierarchical capture and limitations. `field_inventory.csv` is the flat index. These are definitions only; no operational record values were opened.
