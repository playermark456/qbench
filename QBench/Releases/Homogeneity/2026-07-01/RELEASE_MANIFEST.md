# Homogeneity Release Manifest

Release date folder: `2026-07-01`

## Contents

| File | Purpose |
|---|---|
| `homogeneity_phase1_production_candidate__2026-07-01.json` | Phase 1 production-candidate QBench worksheet JSON. |
| `phase1_validation_report.md` | Phase 1 worksheet validation report. |
| `validate_homogeneity_phase1.py` | Read-only validation script for the Phase 1 worksheet JSON. |
| `coa_compatibility_report.md` | Phase 2 COA compatibility findings. |
| `sandbox_import_test_checklist.md` | Phase 3 manual QBench Sandbox test checklist. |
| `homogeneity_coa_rendering_validation_summary.md` | Local validation summary for Homogeneity worksheet report-tab styling and COA CSS compatibility. |

## Scope

This release package is for QBench Sandbox testing only.

The worksheet JSON has been updated after Sandbox feedback so pasted Cannabinoid Potency values are treated as `ug/g`, converted to `mg/g`, and then used for `mg/container` Homogeneity calculations. Target label claims are pulled from visible QBench sample label fields where supported, with manual override cells retained for blank or unavailable label fields.

Latest local fix: `Paste!D4` was checked for the invalid `P25IF` corruption and now uses the corrected label lookup structure. Label source values of blank, `None`, or unresolved `${...}` placeholders are treated as blank while `Paste!P25:P36` remains the raw QBench sample label amount source table.

COA rendering update: the Homogeneity `report_results` worksheet range has been cleaned to remove spreadsheet-like fills and boxed borders, and the local COA CSS now neutralizes worksheet fills/gridlines while preserving simple header underlines.

No QBench changes were made by this package step.
No production QBench access was used.
No automation was built.
No COA source files were modified.
