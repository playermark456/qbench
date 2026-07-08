# 2026-07-07 Homogeneity and COA Update

## Changes

- Updated the COA regulatory reference to the Minnesota Office of Cannabis Management (OCM) Cannabis Technical Authority v2.0, approved July 1, 2026.
- Changed Homogeneity report-facing display labels from `mg/container` to `mg/unit`.
- For Homogeneity, `mg/unit` is treated as the `mg/serving` value requested by OCM and is calculated as `mg/g x actual unit mass g`.
- Updated Homogeneity label-claim lookup to use per-serving/unit sample fields where available, with manual override required when no per-serving field is exported for the selected cannabinoid.
- Added COA sample image max-width and max-height constraints through `.sample-image-coa`.
- Added Quality Control Verified image max-width and max-height constraints through `.qc-verified-coa`.
- Added Cannabinoid Potency page-break protection and centering CSS.
- Removed row-number-based Homogeneity `tr:nth-child(...)` CSS from the current COA source.
- Restored the Homogeneity COA worksheet output to the original `COA!A1:G20` layout rhythm while preserving all 10 replicate rows.

## Files Modified

- `COA format/COA Body Source Code.txt`
- `COA format/COA Footer Source Code.txt`
- `qbench-coa-homogeneity-package/qbench-coa-homogeneity/coa/coa_source_8tile_homogeneity_full.html`
- `QBench/Releases/Homogeneity/2026-07-01/homogeneity_phase1_production_candidate__2026-07-01.json`
- `QBench/Releases/Homogeneity/2026-07-01/validate_homogeneity_phase1.py`
- `QBench/Releases/Homogeneity/2026-07-01/phase1_validation_report.md`
- `QBench/Releases/Homogeneity/2026-07-01/homogeneity_coa_rendering_validation_summary.md`
- `QBench/Releases/Homogeneity/2026-07-01/RELEASE_MANIFEST.md`
- `QBench/Releases/Homogeneity/2026-07-01/sandbox_import_test_checklist.md`
- `QBench/Worksheets/Homogeneity/README.md`
- `qbench-coa-homogeneity-package/qbench-coa-homogeneity/docs/CHANGELOG.md`
- `qbench-coa-homogeneity-package/qbench-coa-homogeneity/docs/homogeneity_workflow.md`

## Compatibility Notes

- Internal named-cell system names containing `mg_container` were intentionally left in place because COA integration, release validation, and historical references may depend on those system names.
- The Homogeneity first-page hex tile and standalone Homogeneity detail page remain driven by worksheet named cells.
- The COA continues to render Homogeneity through `QBTestService().render_worksheet(HOMOGENEITY_TEST, named_cell="report_results", ignore_empty_rows=true)`.
- The COA continues to render Cannabinoid Potency through `QBTestService().render_worksheet(CANNABINOIDS_TEST, named_cell="report_results", ignore_empty_rows=true)`.

## Validation Results

- Phase 1 Homogeneity validation script completed with exit code 0 and regenerated `phase1_validation_report.md`.
- JSON parsed successfully.
- Required named cells exist: `pass_fail`, `report_results`, and `validation_status`.
- `report_results` is `COA!A1:G20` and includes all 10 replicate rows.
- No duplicate named-cell system names were found.
- No `P25IF`, `Worst`, or report-facing `mg/container` labels remain in the release-candidate worksheet JSON.
- COA source checks confirmed image classes, Cannabinoid Potency page-break/centering CSS, and preserved worksheet render calls.

## Remaining QBench Sandbox Test Steps

1. Import the updated Homogeneity worksheet JSON in QBench Sandbox.
2. Attach the worksheet to the Homogeneity assay/test.
3. Confirm required named cells are visible: `pass_fail`, `report_results`, and `validation_status`.
4. Enter or paste a representative 10-replicate Homogeneity dataset.
5. Confirm Total THC and Total CBD helpers convert ug/g to mg/g with `/1000`.
6. Confirm individual cannabinoid mg/unit calculations use converted mg/g times actual unit mass.
7. Generate a COA preview.
8. Confirm the Homogeneity hex tile remains present and correct.
9. Confirm the Homogeneity detail page renders all 10 replicate rows with `mg/unit` labels.
10. Confirm the sample image and Quality Control Verified image do not push or clip first-page content.
11. Confirm Cannabinoid Potency remains together and Total THC/Total CBD alignment is improved.
