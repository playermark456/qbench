# QBench COA + MN OCM Homogeneity Project

This package collects the QBench worksheet templates, COA source code, report asset, examples, and validation utilities created for adding MN OCM Homogeneity reporting to the Adams Independent Testing COA.

## Quick start

1. Review `START_HERE.md` first.
2. Upload the 8-tile hex image in `assets/hexagon-grid-8tile-1336x618.png` to QBench report config attachments.
3. Use `coa/coa_source_8tile_homogeneity_full.html` as the full COA source code replacement.
4. Import `worksheets/current/homogeneity_copy_paste_v6_two_target_COA_import_safe.json` into the Homogeneity worksheet template.
5. Use the scripts in `scripts/` to validate future JSON/source changes before importing into QBench.

## Current production-candidate files

- `worksheets/current/homogeneity_copy_paste_v6_two_target_COA_import_safe.json`
  - Copy/paste Homogeneity worksheet.
  - Supports one or two target cannabinoids.
  - Includes `pass_fail` and `report_results` named cells for COA rendering.

- `coa/coa_source_8tile_homogeneity_full.html`
  - COA source with Homogeneity as the 8th hex tile.
  - Removes the old inline `Homogeneity: Pass/Fail` text below the cannabinoid table.
  - Adds Homogeneity as a standalone report page using `report_results`.

- `assets/hexagon-grid-8tile-1336x618.png`
  - 8-tile hex image to upload to QBench report config attachments.
  - The COA source expects this exact filename unless edited.

## Required Homogeneity named cells

The COA source expects the Homogeneity worksheet to provide:

- `pass_fail` — drives first-page Homogeneity tile and overall pass/fail logic.
- `report_results` — rendered on the standalone Homogeneity page.
- `homogeneity_metrc` — compatibility field for old logic if needed.
- `target_cannabinoid_1`
- `target_cannabinoid_2`

## QBench Homogeneity workflow

1. Open the Homogeneity worksheet.
2. Paste the 10 Cannabinoid Potency batch result rows into the Paste tab.
3. Enter unit masses for all 10 replicates.
4. Enter Target Cannabinoid 1 and optional Target Cannabinoid 2.
5. Enter label cannabinoid content and optional label unit mass.
6. Review calculations and COA output.
7. Generate the COA; Homogeneity should appear as an 8th tile and as its own page.

## Folder overview

```text
coa/                 COA HTML/Jinja source files
worksheets/current/  Current production-candidate QBench worksheet JSON
worksheets/archive/  Prior generated versions kept for reference
assets/              Hex images and related report assets
examples/            Sample XLSX/PDF exports and previews
uploaded_sources/    User-provided source templates and reference files
scripts/             Validation/extraction helpers for Codex or local use
docs/                Notes on QBench, COA integration, and workflow
```
