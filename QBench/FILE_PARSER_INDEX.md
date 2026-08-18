# File Parser Index

## Production rescan 2026-08-16

Ten production parser configurations were verified read-only at `ait.qbench.net`: five active and five inactive; five Code and five No Code. No parser-specific export existed, so five complete visible Code-editor sources were captured, privacy-scanned, and hashed. No parser was previewed, run, retried, or given a file.

| ID | Parser | Type | Config | Trigger / file rule | Assay / destination | Current source or mapping evidence |
|---:|---|---|---|---|---|---|
| 50 | Terpenes Simple Results Parser V2 Controls | Code | Active | Batch attachment ending `.txt` | Terpenes; dynamic Batch `Results` | Active v2; full 1,274-line source, SHA-256 `0d8e998c017bd1b0888c1edf4b06cdc622c47e1a2c788e8b3ceead0951fb4841`; `node --check` PASS |
| 49 | ZZZ_SANDBOX_ONLY_Terpenes_Attachment_Context_Probe_2026-07-16 | Code | Inactive | Exact `Output_redacted_fixture.txt` Batch attachment | No assay; no worksheet write | v1 approved active inside inactive configuration; full 113-line source, SHA-256 `b78253516708c75444cfb4b1401c8d87bd206765851d9f8f56225dfe9478939f`; syntax PASS |
| 48 | ZZZ_SANDBOX_ONLY_Terpenes_Runtime_NoWrite_Probe | Code | Inactive | No configured trigger/file rule | No assay or target | v2/v1 drafts; full 53-line source, SHA-256 `eeb8c72a1c5bd995be44a648ed65f6a48fe6f66cddf89d3ccdb1b4479621b82d`; syntax PASS |
| 47 | Pest Myco Qualitative | No Code | Active | Batch attachment containing `.csv` | Pesticides; Populate Batch Worksheet; patch | 12 finder names; mapping rows not exposed without Edit |
| 46 | Cannabinoid Potency Parser | Code | Active | Batch attachment ending `.csv` | Cannabinoid Potency; dynamic Batch `Results` | Active v1; full 380-line source, SHA-256 `d66415468b309b82775a2af2e925a3ad0551bc667b34b0ac568d5b42ac452c33`; syntax PASS |
| 45 | Gene-up | Code | Inactive | Not configured | No target exposed | No versions; full 41-line base source, SHA-256 `1a5bf4c737e87cfcd4ffd2e3e7f4d29d854fe88c81b9e688c027a35fdfc9ff64`; syntax PASS |
| 41 | Heavy Metals DataManager | No Code | Active | Batch attachment containing `.txt`; tab separated | Heavy Metals; Populate Batch Worksheet; patch | 48 finder names; mapping rows not exposed without Edit |
| 25 | Cannabis Heavy Metals ICPMS File Parser | No Code | Inactive | Batch attachment containing `IC` | Heavy Metals; Populate Batch Worksheet; patch | 1 finder name |
| 22 | Heavy Metals File Parser - AMM | No Code | Inactive | Batch attachment ending `.csv` | Heavy Metals; Populate Batch Worksheet; patch | 1 finder name |
| 21 | Example [File Parser] | No Code | Active | Navigation upload; Test IDs in file; Excel | Populate Multiple Test Worksheets; no assay | 1 finder name |

IDs 48–50 are new relative to the seven-ID July production baseline. Parser 47 is a production object and is no longer omitted from the canonical main table. Parser 50 is active even though its source starts with an `SBX_ONLY` comment; names/comments are not runtime isolation.

Full evidence is in `QBench/Rescans/2026-08-16/File_Parsers/` and `QBench/Rescans/2026-08-16/parser_dependency_map.md`. The initial overlapping viewport extraction was rejected; the current hashes bind to the complete read-only select-all recapture recorded in `source_inventory.csv`. Parser result history, operational attachments, job IDs/logs, and individual No-Code finder mappings were intentionally not opened.

## Superseded pre-rescan summary

No parser-specific export/download control was visible during the earlier read-only inspection. The historical table below predates IDs 48–50 and omitted production parser 47 from its main rows.

As of 2026-07-16, `https://ait.qbench.net/` is the live tenant and is
read-only/reference-only for this work. The disabled Prompt 4.6 probe and its
exact-filename trigger remain inert. Future writable work moves to
`https://ait-sandbox.qbench.net/`, but existing objects in that older Sandbox
are not authoritative; GitHub-controlled parser code and mappings remain the
source of truth.

| Parser name | ID | Assay | Parser type | Active | Expected file type | Key fields / visible internals | Output destination / notes |
|---|---:|---|---|---|---|---|---|
| ZZZ_SANDBOX_ONLY_Terpenes_Attachment_Context_Probe_2026-07-16 | Intentionally omitted | None | Code | False | Exact `Output_redacted_fixture.txt` | Stage 2B fixed-allowlist presence/type probe; approved version remains marked active inside the disabled parser; exact Batch-attachment filename trigger remains inert. | One authorized Sandbox attachment-trigger job recorded `SUCCESS`, but persistent history exposed no console payload; no worksheet service or worksheet/results destination write. |
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
