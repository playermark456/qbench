# Homogeneity COA Rendering Validation Summary

Worksheet JSON: `QBench\Releases\Homogeneity\2026-07-01\homogeneity_phase1_production_candidate__2026-07-01.json`

## Summary

- Updated for the 2026-07-07 local Homogeneity/COA pass.
- Homogeneity `report_results` is restored to `COA!A1:G20`.
- The worksheet remains the Homogeneity calculation source; COA source only renders and styles the named-cell output.

## Checks

| Check | Result | Detail |
|---|---|---|
| `pass_fail` still exists | PASS | `Data!B31` |
| `report_results` still exists | PASS | `COA!A1:G20` |
| `replicate_results` still exists | PASS | `COA!A10:G20` |
| report output includes all 10 replicate rows | PASS | COA rows 11-20 map to Data rows 12-21. |
| Homogeneity labels use `mg/unit` | PASS | Report-facing labels and headers updated. |
| Homogeneity label claims use per-serving/unit sources | PASS | `Paste!P25:P36` uses per-serving placeholders where exported; unsupported targets require manual override. |
| Legacy `mg_container` system names retained | PASS | Internal names retained for compatibility. |
| Homogeneity row-number CSS removed | PASS | No `.ait-report-homogeneity-worksheet-container tr:nth-child(...)` styling remains. |
| Homogeneity render_worksheet call preserved | PASS | `QBTestService().render_worksheet(HOMOGENEITY_TEST, named_cell="report_results", ignore_empty_rows=true)` |

## Notes

- Header and summary styling now live in the worksheet COA tab instead of Homogeneity `nth-child` CSS.
- The report range preserves the original layout rhythm: summary rows at top, spacer rows, highest-value rows, spacer row, replicate header at row 10, and replicate rows 11-20.
- For Homogeneity, `mg/unit` is treated as the `mg/serving` value requested by OCM and is calculated as `mg/g x actual unit mass g`.
