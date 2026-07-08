# Homogeneity

- QBench assay ID: 11
- Assay code: HOM
- Method IDs: 
- Worksheet/template status: 73 Homogeneity [Test WS]; 7 Cannabinoid Potency [Batch] Worksheet; protocol worksheets 69-72
- Report named cells: see ../../NAMED_CELL_INDEX.md and ../../REPORT_RENDERING_MAP.md.
- Parser status: see ../../FILE_PARSER_INDEX.md.
- Automation status: see ../../AUTOMATION_INDEX.md.
- COA/report dependency: inspected assays list Certificate of Analysis Report as default; worksheet named cells feed report rendering.
- Input/source file type: see parser index where a parser exists.
- Known calculation notes: batch-to-test automations use VLOOKUP/XLOOKUP formulas where visible.
- Open questions: Homogeneity test worksheet opened to pending/draft by default; active version was selected for export.

## Export Spreadsheet files

- `QBench/Worksheets/Homogeneity/homogeneity__protocol_evaluation_reporting_ws_id_72__worksheet_export_spreadsheet__active__2026-06-30.json`
- `QBench/Worksheets/Homogeneity/homogeneity__protocol_pre_conditions_prep_ws_id_69__worksheet_export_spreadsheet__active__2026-06-30.json`
- `QBench/Worksheets/Homogeneity/homogeneity__protocol_run_potency_ws_id_71__worksheet_export_spreadsheet__active__2026-06-30.json`
- `QBench/Worksheets/Homogeneity/homogeneity__protocol_subsampling_ws_id_70__worksheet_export_spreadsheet__active__2026-06-30.json`
- `QBench/Worksheets/Homogeneity/homogeneity__test_ws_id_73__worksheet_export_spreadsheet__active__2026-06-29.json`
## Current Homogeneity reporting note

- Report-facing Homogeneity cannabinoid content is labeled `mg/unit`.
- `mg/unit` is equivalent to the prior mg/serving calculation for each tested unit: `mg/g x actual unit mass g`.
- Legacy internal named-cell system names containing `mg_container` are retained for COA and validation compatibility.
