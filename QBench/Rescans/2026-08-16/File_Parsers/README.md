# File Parsers — Production Read-Only Snapshot

Captured from `https://ait.qbench.net/templates/file-parsers` on 2026-08-16/17 UTC. No parser history was opened and no parser, preview, file upload, or write path was executed.

## Inventory

- 10 parsers: 5 active and 5 inactive.
- Parser types: 5 Code and 5 No Code.
- Five complete Code-editor sources were captured through CodeMirror's read-only select-all text interface, hashed as exact persisted bytes, and passed `node --check`.
- Five No-Code configurations expose 63 finder names in total. Finder names were recorded, but opening an individual finder mapping would require a prohibited Edit action.

| ID | Parser | Type | Configuration | Version state |
|---:|---|---|---|---|
| 50 | Terpenes Simple Results Parser V2 Controls | Code | Active | v2 approved active; v1 approved |
| 49 | ZZZ_SANDBOX_ONLY_Terpenes_Attachment_Context_Probe_2026-07-16 | Code | Inactive | v1 approved active inside the inactive configuration |
| 48 | ZZZ_SANDBOX_ONLY_Terpenes_Runtime_NoWrite_Probe | Code | Inactive | v2 and v1 draft |
| 47 | Pest Myco Qualitative | No Code | Active | No version surface |
| 46 | Cannabinoid Potency Parser | Code | Active | v1 approved active |
| 45 | Gene-up | Code | Inactive | No versions; visible base editor source |
| 41 | Heavy Metals DataManager | No Code | Active | No version surface |
| 25 | Cannabis Heavy Metals ICPMS File Parser | No Code | Inactive | No version surface |
| 22 | Heavy Metals File Parser - AMM | No Code | Inactive | No version surface |
| 21 | Example [File Parser] | No Code | Active | No version surface |

IDs 48, 49, and 50 are new relative to the seven-ID July production baseline. Their `SANDBOX_ONLY` naming/source markers are present in the production tenant and must not be interpreted as proof that they are harmless: ID 50 is currently active.

## Source capture

The initial viewport-derived extraction was rejected because overlapping editor windows duplicated or truncated lines. The hashes below bind to the corrected full-editor recapture; `source_inventory.csv` records exact bytes, selected version, method, and syntax result.

| ID | Lines | SHA-256 |
|---:|---:|---|
| 50 | 1,274 | `0d8e998c017bd1b0888c1edf4b06cdc622c47e1a2c788e8b3ceead0951fb4841` |
| 49 | 113 | `b78253516708c75444cfb4b1401c8d87bd206765851d9f8f56225dfe9478939f` |
| 48 | 53 | `eeb8c72a1c5bd995be44a648ed65f6a48fe6f66cddf89d3ccdb1b4479621b82d` |
| 46 | 380 | `d66415468b309b82775a2af2e925a3ad0551bc667b34b0ac568d5b42ac452c33` |
| 45 | 41 | `1a5bf4c737e87cfcd4ffd2e3e7f4d29d854fe88c81b9e688c027a35fdfc9ff64` |

Parser 50 resolves candidate Test display IDs to exactly one shared Batch, reads the dynamic Batch `Results` worksheet, performs a single `QBBatchService.update` with calculation enabled, and then reads the worksheet back for verification. Its source enforces file/record/field limits and hashes both the source file and source rows. Parser 46 also updates the dynamic Batch `Results` worksheet through `QBBatchService.update`. Neither parser was executed during this scan.

See `../parser_dependency_map.md` for the downstream automation and report chains.

## Capture boundary

- Parser result history, job IDs, logs, attachments, and operational records were not opened.
- No Preview, Run, Retry, Reprocess, file selection, upload, Save, Set Active, or version action was used.
- No-Code finder destination mappings were not opened because the available control was Edit.
- Duplicate-file behavior, transactionality, rollback, retry semantics, and exact executed-version correlation remain unverified.
- Screenshots were omitted because the available full-page scope included account UI.
