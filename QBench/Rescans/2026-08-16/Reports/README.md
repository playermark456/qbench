# Reports — Production Read-Only Snapshot

Three visible report configurations were inspected without generating or previewing a report, selecting a sample/Test/signature, downloading an attachment, or changing QBench.

| ID | Report | Configuration | Current active version | Versions | Source |
|---:|---|---|---|---:|---|
| 26 | Certificate of Analysis Report | Active | 24 — Terpenes final | 24 | Sanitized Header, Body, and Footer captured |
| 44 | Homogeneity | Active | 2 — 3.0 | 2 | Sanitized Header, Body, and Footer captured |
| 20 | 1Certificate of Analysis Report | Inactive | 1 | 1 | Sanitized Header, Body, and Footer captured |

Report 26 advanced from active v20 in the 2026-07-04 baseline to active v24. Its complete version list includes draft and pending historical versions. Report 44 remains at active v2. Report 20 demonstrates that configuration status and version status are separate: its configuration is inactive while v1 is displayed as approved active.

## Source integrity, assets, and privacy

- Nine persisted source files are listed with exact byte counts, SHA-256 hashes, and redaction-marker counts in `report_source_inventory.csv`. `report_inventory.json` separately labels pre-write sanitized character/hash values and persisted-file byte/hash values; the persisted values reconcile to the files, including their terminal line feed.
- Report 26 exposes six safe report-attachment names. Its Body requests `AIT Watermark.png` and `hexagon-grid-8tile-1336x618.png` by exact filename and separately looks up the sample-level `sample_img` attachment. Report 20 iterates all sample attachments and renders the selected signature image. No attachment was downloaded, and `CoA Signatures.png` content was specifically omitted.
- Report 44 exposes no attachment while its Body requests `AIT Watermark.png`; a generated preview is required to determine whether the watermark resolves through another scope or is absent.
- Raw-capture sanitization metadata records three email matches and one phone match. The persisted evidence contains zero literal email or phone values; uploader identities, opaque blob URLs, embedded image payloads, and signature content were omitted or replaced.
- The report password field value was not inspected.

## Rendering, pagination, and timezone

- Report 26 calls `QBTestService().render_worksheet(..., named_cell="report_results")` for Cannabinoids, Terpenes, Homogeneity, Heavy Metals, Mycotoxins, Pesticides, Residual Solvents, and Foreign Material.
- Its microbial summary calls `QBOrderService().render_test_worksheets_summary(...)` with `report_header` and `report_content`; the routed summary set also includes Water Activity assay ID 9.
- Its embedded assay map routes Pesticides qualitative ID 4 but omits Pesticides Quantitative ID 21.
- Report 26 also reads `pass_fail`, historically verified `total_thc_report_result`, and the export-unverified `total_thc_mg_per_serving_report_result` and `total_thc_mg_per_container_report_result` names.
- Report 44 reads `homogeneity_metrc` first and `pass_fail` only as fallback. It reconstructs a Potency table by reading direct `Report!B2:B4` and `Report!E2:E4` cells first, then six export-unverified semantic fallback names. Missing direct and fallback numeric values render as literal `0.0` in the four left/right mg/serving and mg/container columns, which can make missing data look measured. This conflicts with the canonical Homogeneity contract: `pass_fail` must drive first-page status and `report_results` must render the standalone Homogeneity table/page.
- Report 20 renders a complete Test worksheet rather than a named range.
- Report 26 contains four `mce-pagebreak` markers: before Terpenes, before Homogeneity, before the microbial/heavy-metals/mycotoxins group, and inside the Pesticides conditional before Pesticides. Residual Solvents/Foreign Material follow without a separate marker, so that final break is absent when Pesticides is absent. Automatic page numbering is off, while Footer CSS emits `Page x of y`.
- Report 44 enables automatic page numbers at Bottom Middle and also emits a CSS page counter, creating a duplicate-number risk. Its `.page-break` class declares `page-break-before: always`, but no element uses that class, so no effective explicit break was found. Report 20 has no explicit break behavior in the captured source.
- All three use Letter 8.5×11-inch setup with one-inch margins and blank explicit header/footer size fields. Reports 26 and 44 contain fixed elements approximately 8.48–8.5 inches wide; report 20 instead contains a 100.311%-wide table. Each requires PDF preview/fit testing, but the fixed-inch overflow risk applies only to reports 26 and 44.
- Report 26 formats issuance, collection, and protocol completion as `%m/%d/%Y`, and receipt as `%m/%d/%Y %I:%M %p`. Report 44 uses `%m/%d/%Y`; report 20 uses `%m/%d/%y` for start/completion and `%m/%d/%Y` for issuance. No timezone identifier or UTC offset exists in the captured source.
- The production General Settings read-only surface exposed no timezone field. Tenant timezone therefore remains unverified; the local rescan timezone is not evidence of QBench rendering configuration.
- Report 26 contains dedicated fixed-layout/96%-width Terpenes table rules. Runtime pagination, counter placement, asset resolution, and printable fit remain unverified because no safe report preview was generated.

See `../report_dependency_map.md` and `../../../REPORT_RENDERING_MAP.md`.

## Capture boundary

- Reports generated: 0.
- Preview, sample/Test selection, signature selection, Save, Set Active, approval, upload, download, and Make Public controls were not used.
- Current worksheet named-cell ranges cannot be certified because Phase 2 native Export Spreadsheet downloads are blocked. The last verified Terpenes export lacks both `report_results` and generic `pass_fail`, although report 26 renders the former and uses the latter in tile/overall-status logic.
- Screenshots were omitted because the available full-page scope included account UI.
