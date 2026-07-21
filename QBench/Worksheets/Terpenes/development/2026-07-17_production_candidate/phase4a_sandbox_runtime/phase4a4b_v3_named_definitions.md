# Phase 4A.4B Test v3 named definitions

Date: 2026-07-21

## Result

- Total named definitions: 44
- Writable scalar destinations: 43
- Report ranges: 1
- Unique destination addresses: 43 of 43
- Blank destination baselines: 43 of 43
- Exportable definitions: 44 of 44
- Formula-owned destinations: 0
- Duplicate destinations: 0
- Pass/Fail definitions: 0

The browser configuration view showed the 44 definitions before save. After list-based reopen, the saved Draft showed the same 44 definitions; QBench normalized their display order without changing their semantic content. The raw round-trip export's `qb_config` contract matches the V3 candidate.

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

The chromatographic destination surface remains 23 independent scalar definitions at `Data!D2:Z2`. The other 20 definitions remain the expected B-column preparation, disposition, and audit destinations.
