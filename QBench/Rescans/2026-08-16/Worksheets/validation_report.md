# Phase 2 Worksheet Evidence Validation

## Overall assessment: Share with caveats

The worksheet metadata inventory and its 2026-07-04 reconciliation are internally consistent and ready to use as metadata evidence. Phase 2 is not complete as a native-definition rescan: all 161 required **Export Spreadsheet** targets remain blocked, so no current structural comparison can be supported.

## Question validated

Does the 2026-08-16 evidence completely and consistently identify the visible production worksheet objects, their versions and active states, their required native-export targets, and their metadata changes from the authoritative 2026-07-04 scan—without presenting metadata as worksheet-structure evidence?

## Sources and boundary

- Current source: `worksheet_detail_capture.json` and `../worksheet_version_inventory.csv`, captured 2026-08-16 from the production host recorded as `ait.qbench.net`.
- Export-attempt evidence: `export_attempts.json`.
- Prior source: `QBench/Rescans/2026-07-04/worksheet_rescan_metadata.json`, supported by the prior `rescan_summary.md`, `worksheet_change_log.md`, and 136 retained export files.
- Secondary canonical references: `QBench/SYSTEM_MAP.md`, `QBench/Docs/qbench_export_status.md`, and `QBench/NAMED_CELL_INDEX.md`.

The prior metadata file is the comparison baseline at worksheet-ID and version-ID grain. Canonical indexes were used only as secondary context because they are export-backed and predate the current scan. No source DOCX was read, copied, or included in this Phase 2 validation.

## Validation results

| Check | Result | Evidence |
|---|---|---|
| JSON parsing | Pass | Both current JSON artifacts and the prior metadata JSON parsed successfully. |
| CSV parsing | Pass | Current version inventory parsed to 700 rows; change summary parsed to 148 rows. |
| Worksheet uniqueness | Pass | 148 unique worksheet IDs; no duplicate object rows. |
| Version uniqueness | Pass | 700 unique version IDs and 700 unique worksheet/version keys. |
| JSON-to-CSV version coverage | Pass | Identical 700-key sets. |
| JSON-to-CSV field agreement | Pass | 7,000 checks across 10 fields per version row; 0 mismatched rows. |
| Per-object version counts | Pass | All 148 object counts equal the grouped version-row counts. |
| Active-version consistency | Pass | At most one active version per object; all object-level active IDs agree with version rows. |
| Export-policy consistency | Pass | Per-object required counts sum to 161 and agree with version rows. |
| Change-ledger coverage | Pass | Exactly one change row for each of the 148 current worksheet IDs. |
| Host/URL scope | Pass | All 700 detail URLs use the exact production host and worksheet-ID-only route. |
| Structural boundary | Pass | All 148 change rows say `not_performed_native_exports_blocked`; no artifact path is populated. |

No validation assertion failed.

## Calculation spot-checks

- Population bridge: 139 prior objects + 9 new − 0 missing = 148 current objects.
- Version bridge: 623 prior versions + 65 added on shared objects + 12 on new objects − 0 removed = 700 current versions.
- Change partition: 9 new + 22 active-changed + 1 active-gained + 116 metadata-unchanged = 148 objects.
- Export targets: 137 active approved + 7 latest draft/no-active + 17 newer non-active = 161 required targets.
- No-active partition: 7 latest-draft targets + 1 rejected-only object + 3 no-version objects = 11 objects.
- Worksheet types: 118 Dynamic Spreadsheet + 29 Spreadsheet + 1 QWML = 148.
- Version statuses: 530 APPROVED + 64 DRAFT + 36 OBSOLETE + 23 PENDING + 47 REJECTED = 700.

## Explicit edge cases

- IDs 41, 68, and 149 have zero versions. ID 68 is QWML and has no **Export Spreadsheet** control.
- ID 76 had no prior versions and now has two approved versions, including active v2; it also has the only observed display-name change.
- ID 111 has no active version and a rejected default/highest version; no export is required under the stated policy.
- ID 10 is the only object with two newer non-active targets above its active version: approved v27 and draft v28.
- All 139 prior worksheet IDs and all 623 prior version IDs remain present.

## Privacy and sanitization checks

Six Phase 2 text artifacts were scanned before this report was added. Sensitive-value patterns returned zero matches for email addresses, JWT-like values, bearer credentials, private-key headers, common cloud access keys, credential/token assignments, authentication query parameters, and Google authentication endpoints. No DOCX file is present in the Phase 2 worksheet directory.

Two PNG screenshots exist under `Screenshots/Worksheets/8/` (101,299 bytes total). Visual review found only the cropped worksheet export menu and the cropped version/status area; no login form, account identity, credential, cookie, token, URL, or session material is visible.

These checks are designed to detect likely secret or authentication material; they do not turn configuration metadata into non-sensitive public data.

## Material blocker

**High impact:** 0 of 161 required native exports were produced. The visible **Export Spreadsheet** control did not emit a downloadable file through the available authenticated browser tooling in the two representative attempts. `export_attempts.json` records zero QBench mutations, no use of **Export to Excel**, and no manual reconstruction.

Until native exports are obtained, do not infer or claim current:

- worksheet cells or values;
- formulas or calculated behavior;
- named-cell existence, targets, or uniqueness;
- sheet/tab structure or dimensions;
- formatting, protection, or rendering behavior; or
- structural equality with the 2026-07-04 exports.

## Required caveat for downstream use

The evidence is metadata-complete but native-export-blocked. It is suitable for inventory, version-state, and change-triage work only. Any worksheet-definition, COA dependency, parser mapping, formula, or named-cell conclusion requires a current native **Export Spreadsheet** file or a separately documented QBench view that directly exposes the specific structure.
