# Report Dependency Map — 2026-08-16 Production Snapshot

## Current report configurations

| ID | Configuration | Active version | Primary dependency model |
|---:|---|---|---|
| 26 Certificate of Analysis Report | Active | v24, `Terpenes final` | Assay routing plus named-cell worksheet rendering |
| 44 Homogeneity | Active | v2, `3.0` | Direct Homogeneity and Potency worksheet-value reads |
| 20 1Certificate of Analysis Report | Inactive | v1 still marked approved active | Full Test-worksheet rendering |

## Report 26 routing and worksheet dependencies

The captured active v24 Body embeds the following assay map:

| Report key | Assay ID |
|---|---:|
| Cannabinoids | 2 |
| Terpenes | 8 |
| Heavy Metals | 3 |
| Mycotoxins | 5 |
| Pesticides | 4 |
| Residual Solvents | 7 |
| Foreign Material | 12 |
| Water Activity | 9 |
| Homogeneity | 11 |
| Aspergillus | 14 |
| Salmonella | 15 |
| STEC | 16 |
| Listeria | 17 |
| Total Aerobic Microbial | 18 |
| Total Yeast and Mold | 19 |
| Enterobacteriaceae | 20 |
| General Microbial placeholder | -1 |

Pesticides Quantitative assay ID 21 is absent. Terpenes preparation and general Microbial mappings also use `-1` placeholders in the source's protocol-step/assay maps.

Observed rendering calls:

- `QBTestService().render_worksheet(..., named_cell="report_results", ignore_empty_rows=true)` for Cannabinoids, Terpenes, Homogeneity, Heavy Metals, Mycotoxins, Pesticides, Residual Solvents, and Foreign Material.
- `QBOrderService().render_test_worksheets_summary(...)` for the routed microbial set plus Water Activity assay ID 9, with `report_header` and `report_content`.
- `get_worksheet_value("pass_fail")` for result-tile state.
- `total_thc_report_result`, `total_thc_mg_per_serving_report_result`, and `total_thc_mg_per_container_report_result` for Cannabinoid display.

The Terpenes section has dedicated fixed-layout CSS, 40/15/15/15/15 column widths, wrapped cells, and a final 96% table width intended to prevent printable-page overflow. The Body contains four `mce-pagebreak` markers: before Terpenes, before Homogeneity, before the microbial/heavy-metals/mycotoxins group, and before Pesticides. The last marker is inside the Pesticides conditional; Residual Solvents/Foreign Material follow without a separate marker, so that break is absent when Pesticides is absent. These establish source-level break intent, but runtime page placement is not proven without a generated preview.

## Report 44 dependencies

The standalone Homogeneity source:

- identifies Cannabinoids as assay 2 and Homogeneity as assay 11;
- reads `homogeneity_metrc` first with `pass_fail` fallback, contrary to the canonical requirement that `pass_fail` drive first-page status;
- reads direct Potency cells `Report!B2:B4` and `Report!E2:E4` first;
- falls back to `report_left_total_label`, `report_left_total_mg_container`, `report_left_total_mg_serving`, `report_right_total_label`, `report_right_total_mg_container`, and `report_right_total_mg_serving` only when the direct values are falsey;
- renders literal `0.0` in the four left/right mg/serving and mg/container columns when both lookup paths are blank, creating a missing-data-as-zero risk;
- defines `page-break-before: always` for its `.page-break` class, but no element uses that class; `page-break-inside: avoid` applies to the detail block.

Report 44 does not call `render_worksheet`. Report 26 separately renders the Homogeneity `report_results` named range. The canonical correction target for report 44 is therefore explicit: use `pass_fail` as authoritative status and render `report_results` through `QBTestService().render_worksheet(..., named_cell="report_results", ignore_empty_rows=true)` for the standalone table/page. No report source was changed in this phase.

## Report 20 dependency

The legacy inactive configuration calls `QBTestService().render_worksheet(TEST_ENTRY)` without a named-cell restriction. It therefore depends on the complete Test worksheet rendering behavior rather than a compact named range.

## Pagination, page setup, and assets

- Report 26 has automatic page numbering off while Footer CSS emits `Page x of y`.
- Report 44 has automatic page numbers enabled at Bottom Middle and also emits a CSS page counter, creating a duplicate-number risk.
- Report 20 has automatic page numbering off and no explicit break in captured source.
- All three use Letter 8.5×11-inch page setup, one-inch margins, and blank explicit header/footer size fields. Reports 26 and 44 have fixed source elements approximately 8.48–8.5 inches wide that can exceed the printable content width implied by those margins. Report 20 instead contains a 100.311%-wide table. All require PDF fit/clipping validation, but the fixed-inch risk applies only to reports 26 and 44.
- Report 26 exposes six safe report-attachment names, requests `AIT Watermark.png` plus `hexagon-grid-8tile-1336x618.png` by filename, and looks up the sample-level `sample_img` attachment. Other redacted blob/image references cannot be mapped to attachments from sanitized source alone.
- Report 44 exposes zero attachments but requests `AIT Watermark.png`; whether it resolves through another scope or disappears is unverified. Signature-image content was excluded and no attachment was downloaded.
- Report 20 iterates `sample.get_attachments()` and renders every returned sample attachment; it also renders the selected signature image.

## Date and timezone behavior

All three sources use QBench `local_time` for one or more displayed dates. Report 26 formats issuance, collection, and protocol-step completion as `%m/%d/%Y`, and received-by-lab as `%m/%d/%Y %I:%M %p`. Report 44 uses `%m/%d/%Y`. Report 20 uses `%m/%d/%y` for start/completion and `%m/%d/%Y` for issuance. The sources contain no timezone identifier or UTC offset.

The production General Settings page exposed no timezone label or matching control schema in read-only mode. Tenant timezone is therefore **not exposed / not verified**. Repository metadata showing `America/Chicago` is the scanner's local context and is not evidence of QBench report-rendering configuration.

## Historical range comparison and blockers

The 2026-07-04 native exports contain 486 named-cell definitions across 23 worksheets. Those ranges remain historical evidence only:

- Current report-critical worksheet versions have advanced.
- All current native Export Spreadsheet downloads are blocked in Phase 2.
- The July Terpenes worksheet has neither `report_results` nor generic `pass_fail`, even though report 26 v24 renders the former and uses the latter in tile/overall-status logic.
- The July Potency worksheet verifies `total_thc_report_result` but not report 26's newer `total_thc_mg_per_serving_report_result` or `total_thc_mg_per_container_report_result`; it also lacks generic `pass_fail`.
- Water Activity exposes `pass_fail_report` rather than `pass_fail`.
- Listeria lacks `pass_fail`.
- The original historical Homogeneity row shows `Report!A1:B1`, but the first authoritative 2026-07-04 rescan block verifies `homogeneity_metrc = COA!F1`, `pass_fail = Data!B31`, and `report_results = COA!A1:G20`. Three later exact copies of that rescan block are deprecated duplicates, not additional evidence. Current production worksheet v16 was not exported.
- Report 44's six semantic Potency fallback names are absent from the last verified exports. The source reads direct cells first, so absence of those names alone is not a runtime defect; neither lookup path proves current worksheet content.

No current named-cell address is inferred or reconstructed.

## Asset and privacy boundary

Report 26 exposes safe names for watermark, signature, header, grid, and quality-control assets. No attachment was downloaded. Signature content and uploader identities were omitted. Blob URLs and embedded image data were replaced in source, so blob-to-attachment identity remains unverified.

All nine persisted report source files reconcile to `Reports/report_source_inventory.csv` and to the explicitly labeled persisted byte/hash fields in `Reports/report_inventory.json`; separate pre-write character/hash fields preserve sanitizer provenance. Persisted source contains no literal email, phone, credential, token, authorization, or session values. Sanitizer field names/counts are not exposed values.

No report, preview, sample/Test selection, signature selection, or operational record was generated or opened.
