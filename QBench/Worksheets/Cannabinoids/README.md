# Cannabinoid Potency

- QBench assay ID: 2
- Assay code: CP
- Method ID: MTH-CP-01
- Worksheet/template status: Cannabinoid Potency Test Worksheet and Cannabinoid Potency Batch Worksheet
- Report named cells: see `../../NAMED_CELL_INDEX.md` and `../../REPORT_RENDERING_MAP.md`.
- Parser status: see `../../FILE_PARSER_INDEX.md`.
- Automation status: see `../../AUTOMATION_INDEX.md`.
- COA/report dependency: worksheet named cells feed the Certificate of Analysis report.

## Homogeneity dependency

The Cannabinoid Potency Batch Worksheet is the preferred copy/paste source for the Homogeneity Test Worksheet. Preserve row alignment between:

- Sample ID
- QBench Test ID
- cannabinoid result columns
- optional `True Mass per Unit`

Do not sort or independently reorder the True Mass column after the batch rows are generated.

## Optional True Mass per Unit field

QBench Test additional field:

- Label: `True Mass per Unit`
- Identifier: `true_mass_per_unit`

The batch candidate exposes this as column `AH` using the corresponding `tests[n]` Test context. The value is intentionally optional:

- numeric value: display the number;
- blank, `none`, unresolved, or nonnumeric value: display a blank cell;
- no batch validation or Pass/Fail dependency is added.

The intended workflow is:

1. Technician records True Mass per Unit on each individual Cannabinoid Potency Test when applicable.
2. The Batch Worksheet displays it in column AH.
3. Staff copy columns A:AH into the Homogeneity Paste tab.
4. Homogeneity uses the mass according to its selected Mass Entry Basis.

See `development/2026-07-20_true_mass_optional/` for the deterministic patcher, candidate archive, validation evidence, and Sandbox checklist.

## Promotion boundary

The optional True Mass candidate must be imported into an inactive QBench Sandbox Batch Worksheet and tested with populated, blank, and nonnumeric field values before replacing or activating the current worksheet.

## Historical Export Spreadsheet files

- `QBench/Worksheets/Cannabinoids/cannabinoid_potency__cannabinoid_potency_batch_ws_id_7__worksheet_export_spreadsheet__active__2026-06-30.json`
- `QBench/Worksheets/Cannabinoids/cannabinoid_potency__cannabinoid_potency_test_ws_id_8__worksheet_export_spreadsheet__active__2026-06-30.json`
