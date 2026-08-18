# Worksheet Metadata Comparison — 2026-08-16 vs 2026-07-04

## Result

The production worksheet inventory increased from 139 to 148 objects. All 139 prior worksheet IDs remain visible, 9 IDs are new, and no worksheet ID is missing. The captured version population increased from 623 to 700: 65 version IDs were added to existing objects and 12 belong to new objects. No prior version ID disappeared.

This is a metadata comparison only. All 161 native **Export Spreadsheet** targets are blocked, so current worksheet structure, formulas, named cells, formatting, and rendered ranges were not compared.

| Measure | 2026-07-04 | 2026-08-16 | Change |
|---|---:|---:|---:|
| Worksheet objects | 139 | 148 | +9 |
| Version records | 623 | 700 | +77 |
| Objects with an active approved version | 129 | 137 | +8 |
| Objects without an active version | 10 | 11 | +1 |
| Missing prior worksheet IDs | — | 0 | 0 |
| Removed prior version IDs | — | 0 | 0 |

## New worksheet objects

| ID | Name | List state | Version state |
|---:|---|---|---|
| 149 | ZZZ_SANDBOX_ONLY_Prompt_4_6_Runtime_Probe_2026-07-16 | Inactive | No version |
| 150 | Pest (Quantitative Flower) [Protocol WS] Preparation of Lab Control Samples \| Sample Preparation 1 | Active | Active v3 |
| 151 | Pest (Quantitative Flower) [Protocol WS] Preparation of Samples \| Sample Preparation 1 | Active | Draft v1; no active version |
| 152 | Pest (Quantitative Flower) [Protocol WS] Preparation of Standards \| Sample Preparation 1 | Active | Active v2 |
| 153 | Pest (Quantitative Flower) [Protocol WS] Preparation of Lab Control Samples \| Sample Preparation 2 | Active | Active v2 |
| 154 | Pest (Quantitative Flower) [Protocol WS] Preparation of Samples \| Sample Preparation 2 | Active | Active v1 |
| 155 | Pest (Quantitative Flower) [Protocol WS] Preparation of Standards \| Sample Preparation 2 | Active | Active v1 |
| 156 | Pest (Quantitative) [Protocol WS] Laboratory Control Requirements | Active | Active v1 |
| 157 | Pest (Quantitative) [Protocol WS] Calculations and Reporting of Results | Active | Active v1 |

The nine new objects contribute 12 version records. ID 149 is visible in production but its description labels it a disposable sandbox-only probe; that statement is reported as observed metadata, not interpreted as proof of origin or intended use.

## Active-version changes on existing objects

Twenty-two existing objects changed from one active version ID to another. One additional object, ID 76, gained its first active version.

| ID | Worksheet | Prior active | Current active |
|---:|---|---:|---:|
| 6 | Heavy Metals [Test] Worksheet | v32 / ID 537 | v34 / ID 675 |
| 7 | Cannabinoid Potency [Batch] Worksheet | v14 / ID 598 | v16 / ID 672 |
| 8 | Cannabinoid Potency [Test] Worksheet | v52 / ID 599 | v59 / ID 676 |
| 10 | Mycotoxin (Qualitative) [Test] Worksheet | v25 / ID 428 | v26 / ID 602 |
| 11 | Residual Solvents [Batch] Worksheet | v7 / ID 507 | v9 / ID 694 |
| 12 | Residual Solvents [Test] Worksheet | v35 / ID 515 | v41 / ID 697 |
| 14 | Pesticides (Qualitative) [Test] Worksheet | v26 / ID 634 | v29 / ID 681 |
| 16 | Pesticides (Quantitative) [Test] Worksheet | v6 / ID 593 | v7 / ID 682 |
| 28 | Water Activity [Test WS] | v13 / ID 594 | v15 / ID 690 |
| 31 | Foreign Material [Test WS] | v9 / ID 327 | v10 / ID 566 |
| 38 | Cannabinoid Potency {Protocol WS} Quality Control Requirements | v5 / ID 620 | v6 / ID 666 |
| 42 | Terpenes [Test] Worksheet | v4 / ID 313 | v14 / ID 691 |
| 43 | Terpenes [Batch] Worksheet | v2 / ID 95 | v5 / ID 657 |
| 73 | Homogeneity [Test WS] | v12 / ID 633 | v16 / ID 668 |
| 81 | Total Aspergillus Microbial Analysis [Test WS] | v25 / ID 613 | v27 / ID 689 |
| 83 | Salmonella Species [Test] Worksheet | v7 / ID 532 | v9 / ID 684 |
| 84 | STEC [Test] Worksheet | v5 / ID 522 | v7 / ID 685 |
| 87 | Listeria Monocytogenes [Test] Worksheet | v6 / ID 530 | v8 / ID 678 |
| 93 | Total Aerobic Count [Test] WS | v6 / ID 533 | v8 / ID 687 |
| 94 | Total Yeast and Mold {Test WS} | v6 / ID 524 | v9 / ID 688 |
| 95 | Enterobacteriaceae [Test] WS | v12 / ID 529 | v14 / ID 677 |
| 143 | Sample Dilution {Protocol WS} | v1 / ID 582 | v3 / ID 669 |

ID 76 changed from no versions to two approved versions, gained active v2 / version ID 654, and its display name changed from “Pest Myco (Qualitative) …” to “Pest Myco …”. The other 116 shared objects retained the same complete version-ID set and active-version state.

The largest version-count increases on shared objects are Terpenes [Test] ID 42 (+10), Cannabinoid Potency [Test] ID 8 (+7), Residual Solvents [Test] ID 12 (+6), Homogeneity [Test] ID 73 (+5), and Pesticides (Qualitative) [Test] ID 14 (+4).

## Newer non-active versions above the active version

Sixteen objects have one or more version numbers above their active version, producing 17 additional required export targets:

- ID 10: approved v27 and draft v28.
- IDs 6, 8, 12, 14, 28, 31, 42, 73, 81, 83, 84, 87, 93, 94, and 95: one newer draft each.

These are metadata states only. A newer approved version is not described as active unless the captured active flag says so.

## Objects without an active version

- Latest draft is the required export target: IDs 2, 4, 45, 59, 67, 114, and 151.
- Rejected-only/default state; no export required by policy: ID 111.
- No versions exist: IDs 41, 68, and 149.

ID 68 remains the sole QWML object. It has no versions and no **Export Spreadsheet** control. IDs 41 and 149 are spreadsheet-backed objects with no available version.

## Native-export blocker and downstream impact

The policy identified 161 targets across 144 objects: 137 active approved versions, 7 latest draft versions on no-active objects, and 17 newer non-active versions. The visible native control did not yield files through the available browser tooling in representative attempts, so 0 of 161 exports completed.

Consequently:

- no current worksheet JSON was reconstructed or inferred;
- no structural hash, sheet/tab, named-cell, formula, or rendered-range comparison is claimed;
- the 2026-07-04 exports remain historical evidence, not current-definition evidence for changed active versions; and
- `QBench/NAMED_CELL_INDEX.md` and export-backed canonical documentation cannot be reconciled from Phase 2 metadata alone.

The row-level basis for every classification is `Worksheets/worksheet_version_change_summary.csv`. The source-of-truth current metadata is `Worksheets/worksheet_detail_capture.json` plus `worksheet_version_inventory.csv`.
