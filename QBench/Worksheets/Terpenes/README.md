# Terpenes

- QBench assay ID: 8
- Assay code: TR
- Method IDs: 
- Worksheet/template status: 42 Terpenes [Test] Worksheet; 43 Terpenes [Batch] Worksheet
- Report named cells: see ../../NAMED_CELL_INDEX.md and ../../REPORT_RENDERING_MAP.md.
- Parser status: see ../../FILE_PARSER_INDEX.md.
- Automation status: see ../../AUTOMATION_INDEX.md.
- COA/report dependency: inspected assays list Certificate of Analysis Report as default; worksheet named cells feed report rendering.
- Input/source file type: see parser index where a parser exists.
- Known calculation notes: batch-to-test automations use VLOOKUP/XLOOKUP formulas where visible.
- Open questions: Default pages opened on draft for some worksheets; active exports captured.

## Export Spreadsheet files

- `QBench/Worksheets/Terpenes/terpenes__terpenes_batch_ws_id_43__worksheet_export_spreadsheet__active__2026-06-30.json`
- `QBench/Worksheets/Terpenes/terpenes__terpenes_test_ws_id_42__worksheet_export_spreadsheet__active__2026-06-30.json`

## Prompt 5 Batch-to-Test automation

The 2026-07-17 Sandbox attempt is blocked before activation. The native Batch
automation action can only copy to all Test Worksheets in the Batch and cannot
enforce exact QBench Test ID matching, exactly-one cardinality, or atomic
multi-field preflight. The isolated automation remains inactive with no saved
conditions/actions. See
`development/2026-07-17_batch_to_test_automation/README.md`.
