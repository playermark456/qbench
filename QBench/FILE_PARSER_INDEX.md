# File Parser Index

No parser-specific export/download control was visible during read-only inspection. Code/no-code details below are page-visible captures only.

| Parser name | ID | Assay | Parser type | Active | Expected file type | Key fields / visible internals | Output destination / notes |
|---|---:|---|---|---|---|---|---|
| Cannabinoid Potency Parser | 46 | Cannabinoid Potency | Code | True | .csv | Active version 1 imports `file_parser.js` 1.1.0 and `qbjs.js` 2.7.0; full source inspected read-only on 2026-07-15. | Current source uses `run`, `QB.files`, `QBBatchService`, and a dynamic Batch `Results` worksheet payload. This is tenant evidence, not the proposed Terpenes write contract. |
| Gene-up | 45 | Microbiology | Code | False | Not visible | Visible inactive template imports `file_parser.js` 1.1.0 and `qbjs.js` 2.7.0 and uses the `run`/`QB` base template. | No versions found; no export control visible. |
| Heavy Metals DataManager | 41 | Heavy Metals | No Code | True | .txt | No-code internals not exposed in detail view. | Heavy Metals import mapping, likely DataManager text output. |
| Cannabis Heavy Metals ICPMS File Parser | 25 | Heavy Metals | No Code | False | Filename text IC | No-code internals not exposed in detail view. | Inactive ICPMS parser. |
| Heavy Metals File Parser - AMM | 22 | Heavy Metals | No Code | False | .csv | No-code internals not exposed in detail view. | Inactive Heavy Metals parser. |
| Example [File Parser] | 21 | Other | No Code | True | .xlsx | Example parser only. | No assay dependency confirmed. |

## Rescan 2026-07-04

| Parser name | ID | Visible version/status | Export/download status | Notes |
|---|---:|---|---|---|
| Pest Myco Qualitative | 47 |  | No export/download control captured | No internals visible from parsed detail page |
| Cannabinoid Potency Parser | 46 | 1 - AIT-135 Cannabinoid Potency Parser - APPROVED (ACTIVE); active since 2026-07-10, rechecked 2026-07-15 | No export/download control captured | Complete active source inspected read-only; no source file downloaded |
| Gene-up | 45 | No Versions Found; inactive template rechecked 2026-07-15 | No export/download control captured | Visible current Code template inspected read-only |
| Heavy Metals DataManager | 41 |  | No export/download control captured | No internals visible from parsed detail page |
| Cannabis Heavy Metals ICPMS File Parser | 25 |  | No export/download control captured | No internals visible from parsed detail page |
| Heavy Metals File Parser - AMM | 22 |  | No export/download control captured | No internals visible from parsed detail page |
| Example [File Parser] | 21 |  | No export/download control captured | No internals visible from parsed detail page |
