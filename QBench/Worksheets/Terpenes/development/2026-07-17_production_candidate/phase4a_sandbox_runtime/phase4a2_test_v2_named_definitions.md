# Phase 4A.2 Test v2 named definitions

Date: 2026-07-21

## Result

- Total named definitions: 44
- Writable scalar destinations: 43
- Report ranges: 1
- Unique destination addresses: 43 of 43
- Exportable definitions: 44 of 44
- Formula-owned destinations: 0
- Duplicate destinations: 0
- Blank input destinations before runtime data: 43 of 43
- Pass/Fail definitions: 0

The browser configuration view retained the same 44 entries before save and after reopening the saved Draft. The raw round-trip export's complete `qb_config` object is exactly equal to the local candidate's `qb_config` object.

## Representative definitions

| System name | Address | Display name | Result |
| --- | --- | --- | --- |
| `terpenes_instrument_conc_01` | `Data!D2` | alpha-Pinene | exact |
| `terpenes_instrument_conc_12` | `Data!O2` | gamma-Terpinene | exact |
| `terpenes_instrument_conc_23` | `Data!Z2` | alpha-Bisabolol | exact |
| `sample_mass_g` | `Data!B12` | Sample Mass | exact |
| `batch_qc_disposition` | `Data!B22` | Batch QC Disposition | exact |
| `publish_ready` | `Data!B23` | Publish Ready | exact |
| `source_file_hash` | `Data!B30` | Source File Hash | exact |
| `report_results` | `Report!A1:E23` | empty by design | exact |

The 23 chromatographic destinations remain `Data!D2:Z2` as independent scalar definitions. The remaining 20 destinations remain the expected independent B-column preparation, disposition, and audit cells.
