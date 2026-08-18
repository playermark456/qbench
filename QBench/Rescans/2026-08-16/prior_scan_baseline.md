# Prior-Scan Baseline for Reconciliation

This file records the deterministic offline baseline established before authenticated production access. It is not a claim about the current 2026-08-16 QBench state.

## 2026-07-04 worksheet rescan

- Worksheet pages discovered: 139
- Successful Export Spreadsheet JSON artifacts: 136
- Export failures: 3 (worksheet IDs 41, 68, and 76)
- Statuses among saved exports: 129 active/approved, 6 draft, 1 rejected
- Pages without an active-approved version: IDs 2, 4, 41, 45, 59, 67, 68, 76, 111, and 114
- Export structures: 107 dynamic and 29 legacy
- Comparison recorded at the time: 32 changed, 104 new, 0 unchanged
- Offline integrity recheck on 2026-08-16: all 136 metadata-referenced exports exist and parse; no orphan export was found
- Named cells: 486 definitions across 23 exports

The authoritative prior figures are in `QBench/Rescans/2026-07-04/worksheet_rescan_metadata.json` and `rescan_summary.md`. Intermediate repeated sections in the canonical indexes must not be treated as separate scans.

## Canonical baseline

- `ASSAY_ID_MAP.md`: 19 mapped assays (IDs 2–20)
- Known worksheet-assignment gaps: Moisture Analysis, Stability, and assay-level General Microbial Analysis
- `REPORT_RENDERING_MAP.md`: report templates 26 (COA active/default), 44 (Homogeneity active), and 20 (legacy inactive template with an approved active version)
- `AUTOMATION_INDEX.md`: 15 automations, 12 active and 3 inactive; the documented triggers are Data Modified
- `FILE_PARSER_INDEX.md` / 2026-07-15 parser snapshot: 7 production parsers, including 2 code parsers

## 2026-07-15 parser rescan

- Parser IDs: 47, 46, 45, 41, 25, 22, and 21
- Visible history jobs: 39 (38 SUCCESS, 1 IN_PROGRESS)
- Trigger in all visible rows: Attachment Added To Batch
- Destinations: 36 Batch Worksheet and 3 None
- The seven-file manifest under `QBench/Rescans/2026-07-15/File_Parsers/` passed a fresh SHA-256 verification on 2026-08-16
- Known gaps: failure/error-format evidence, logs and parsed preview, numeric-write evidence, atomicity/rollback behavior, retry behavior, multi-file grouping, and resolved Batch context

## Tooling cautions

`QBench/Rescans/2026-07-04/rescan_export_worksheets.py` must not be run unchanged. It hardcodes the old date and production URL, writes canonical documentation directly, compares against a limited filename pattern, and its index append operations are not idempotent. The current scan must use a dated output path, explicit version rules, privacy gates, and idempotent canonical updates.

`SYSTEM_MAP.md` contains four progressive 2026-07-04 sections. `NAMED_CELL_INDEX.md` contains the same 486-row rescan block four times. Current production reconciliation must distinguish these documentation duplicates from live QBench objects.

Historical documents inconsistently called `ait.qbench.net` Sandbox. Later repository evidence establishes `ait.qbench.net` as production/live read-only and `ait-sandbox.qbench.net` as Sandbox. This scan follows the prompt's explicit production-host definition.
