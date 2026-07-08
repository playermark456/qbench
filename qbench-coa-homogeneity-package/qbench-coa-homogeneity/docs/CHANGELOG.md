# Changelog

## Current package

- Added Homogeneity as 8th COA hex tile.
- Added standalone Homogeneity COA page.
- Added 8-tile hex asset.
- Added two-target Homogeneity worksheet JSON.
- Added validation scripts and Codex project instructions.

## v6 import-safe worksheet

- Removed duplicate named-cell aliases that pointed to the same cells.
- Current import candidate is now `worksheets/current/homogeneity_copy_paste_v6_two_target_COA_import_safe.json`.
- Older v5 is retained in `worksheets/archive/` for reference.
## 2026-07-07 local COA and Homogeneity display update

- Updated current COA body styling for constrained sample and QC images, Cannabinoid Potency centering, and page-break protection.
- Removed row-number-based Homogeneity CSS from the current COA source copy.
- Updated Homogeneity release-candidate worksheet display labels from `mg/container` to `mg/unit`; calculation logic remains `mg/g x actual unit mass g`.
- Legacy internal `mg_container` named-cell system names remain unchanged for compatibility.
