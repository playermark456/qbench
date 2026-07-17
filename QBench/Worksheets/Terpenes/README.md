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

The original 2026-07-17 43-field design stopped before activation because the
UI inspection did not prove exact routing, cardinality guards, or atomic
multi-field preflight. QBench's official guide later supplied a per-Test
`VLOOKUP({{test.id}}, ...)` source pattern. Prompt 5A exercised that pattern
once with an isolated one-field probe, but the post-run Test Worksheet export
showed the destination named cell had not persisted. The result is therefore
`per_test_vlookup_error`, not proof of broadcast or unsupported routing. The
probe automation is inactive; zero Test values were written. See
`development/2026-07-17_batch_to_test_automation/README.md`.
