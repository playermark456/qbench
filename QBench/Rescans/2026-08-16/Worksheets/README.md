# Production Worksheet Rescan — 2026-08-16

This directory contains the worksheet-detail evidence captured from the Adams Independent Testing production tenant at `ait.qbench.net` in strictly read-only mode. The metadata capture is complete for all 148 worksheet objects visible during the scan. Native worksheet definition exports are not complete.

## Evidence status

| Evidence layer | Status | Coverage |
|---|---|---|
| Worksheet-object metadata | Complete | 148 of 148 visible objects |
| Version metadata | Complete | 700 version rows |
| Active-version identification | Complete | 137 active approved versions; 11 objects have no active version |
| Export-target identification | Complete | 161 required targets across 144 worksheet objects |
| Native **Export Spreadsheet** files | Blocked | 0 of 161 required exports downloaded |
| Worksheet structure, formulas, named cells, and rendered ranges | Not assessed | Requires native exports |

The native **Export Spreadsheet** control was present for spreadsheet-backed objects, but representative attempts did not emit a downloadable file through the authenticated in-app browser tooling. **Export to Excel** was not used, no worksheet JSON was reconstructed, and no substitute export format was created.

## Contents

- `worksheet_detail_capture.json` — object-level and version-level DOM metadata, selection state, export policy, and blocker details.
- `export_attempts.json` — two representative native-export attempts and the read-only safety assertions.
- `worksheet_version_change_summary.csv` — deterministic worksheet-ID reconciliation against the 2026-07-04 scan. Every current object has one row.
- `validation_report.md` — parsing, reconciliation, consistency, privacy, and scope-boundary checks.
- `../worksheet_version_inventory.csv` — the complete 700-row version inventory used for reconciliation.
- `../Screenshots/Worksheets/8/` — two tightly cropped representative screenshots showing the native export menu and the active-version selector. They are representative evidence only, not per-object screenshot coverage.

No native worksheet JSON belongs in this directory until QBench produces it through the **Export Spreadsheet** control. Prior exports under `QBench/Rescans/2026-07-04/Worksheets/` remain the latest native production definitions available for structural inspection; they must not be treated as proof of current structure when the active version changed.

## Captured population

- Worksheet types: 118 Dynamic Spreadsheet, 29 Spreadsheet, and 1 QWML.
- List state: 144 Active and 4 Inactive.
- Version statuses: 530 APPROVED, 64 DRAFT, 36 OBSOLETE, 23 PENDING, and 47 REJECTED.
- Export targets: 137 active approved versions, 7 latest draft versions on objects without an active version, and 17 newer non-active versions. The 17 newer targets occur on 16 objects because worksheet 10 has both a newer approved version and a still newer draft.

## Explicit exceptions

- IDs 41, 68, and 149 have no versions. ID 68 is the sole QWML object and has no native **Export Spreadsheet** control.
- ID 111 has no active version; its default/highest version is rejected, so the version policy does not require an export.
- IDs 2, 4, 45, 59, 67, 114, and 151 have no active version; the latest draft is the required target.
- ID 149 is a newly visible inactive production object whose own metadata labels it sandbox-only. It has no version.

## Comparison boundary

The comparison in this directory is metadata-only: object presence, names, types, version IDs/numbers/statuses, active flags, and export-policy classification. It does not claim that worksheet cells, formulas, named cells, layout, or rendered output are unchanged. Canonical indexes such as `QBench/NAMED_CELL_INDEX.md` are built from native exported JSON and therefore cannot be refreshed from this metadata capture alone.

The source DOCX files supplied separately by the user are not stored in this rescan directory and were not used for this Phase 2 reconciliation.
