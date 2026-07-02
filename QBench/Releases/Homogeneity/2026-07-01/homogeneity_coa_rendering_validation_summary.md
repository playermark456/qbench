# Homogeneity COA Rendering Validation Summary

Worksheet JSON: `QBench\Releases\Homogeneity\2026-07-01\homogeneity_phase1_production_candidate__2026-07-01.json`

## Summary

- Errors: 0
- Warnings: 0

## Checks

| Check | Result | Detail |
|---|---|---|
| pass_fail still exists | PASS | {'cell': 'Data!B31', 'display_name': 'Pass/Fail', 'export': True} |
| report_results still exists | PASS | {'cell': 'COA!A1:G20', 'display_name': 'Homogeneity COA Output', 'export': True} |
| report_results range is COA!A1:G20 | PASS | COA!A1:G20 |
| report_results includes all 10 replicate rows | PASS | A11==Data!A12; A12==Data!A13; A13==Data!A14; A14==Data!A15; A15==Data!A16; A16==Data!A17; A17==Data!A18; A18==Data!A19; A19==Data!A20; A20==Data!A21 |
| Highest Reported Values row removed | PASS | ['', '', '', '', '', '', ''] |
| Average actual unit mass wording exists | PASS |  |
| Old Average actual mass wording removed | PASS |  |
| report_results range has no gray-filled cells | PASS |  |
| report_results range has no boxed grid borders | PASS |  |
| no obvious formula error literals | PASS |  |
| Homogeneity COA CSS exists in COA format\COA Body Source Code.txt | PASS |  |
| Homogeneity render_worksheet call preserved in COA format\COA Body Source Code.txt | PASS |  |
| COA does not calculate Homogeneity in COA format\COA Body Source Code.txt | PASS |  |
| Homogeneity COA CSS exists in qbench-coa-homogeneity-package\qbench-coa-homogeneity\coa\coa_source_8tile_homogeneity_full.html | PASS |  |
| Homogeneity render_worksheet call preserved in qbench-coa-homogeneity-package\qbench-coa-homogeneity\coa\coa_source_8tile_homogeneity_full.html | PASS |  |
| COA does not calculate Homogeneity in qbench-coa-homogeneity-package\qbench-coa-homogeneity\coa\coa_source_8tile_homogeneity_full.html | PASS |  |

## Notes

- The COA tab named cell remains `report_results` at `COA!A1:G20`.
- The worksheet remains the Homogeneity calculation source; COA source only renders and styles the named cell output.
- Header-line CSS targets both `tr:nth-child(7)` and `tr:nth-child(10)` so it tolerates QBench keeping or dropping blank worksheet rows.
