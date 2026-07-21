# Phase 4A Test worksheet controlled import failure

## Classification

`phase4a_classification = blocked_test_import_collapsed_renderer`

## Expected imported definition

- Tabs in order: Report, Data, Specifications.
- Populated dimensions: Report 23x5, Data 40x26, Specifications 23x21.
- Exactly 44 named definitions: 43 writable destinations plus `report_results = Report!A1:E23`.
- Formula-owned/protected calculated cells and three-decimal display formatting.

## Observed unsaved editor state

The exact hashed Test candidate was selected and submitted through QBench's **Import Spreadsheet** dialog. QBench populated the named-cell configuration surface with sheet-qualified destinations beginning at `Data!D2`, proving that the configuration portion was read.

The Spreadsheet renderer did not render the candidate workbook. It showed only a single blank/default cell and no visible Report, Data, or Specifications tabs. The required 23x5, 40x26, and 23x21 grids therefore could not be established. This is the same failure class as a collapsed/default renderer, and it materially affects tabs, dimensions, formulas, styles, protection, and runtime viability.

## Controlled stop

The prompt requires an immediate stop when QBench strips or materially changes the worksheet structure. Therefore:

- **Save As New Version** was not clicked.
- No Test worksheet version exists from this run.
- No version was approved or activated.
- No manual repair or JSON change was attempted in Sandbox.
- No Key/Value fixture or runtime object was created.
- The Batch candidate was not imported.

`test_import = failed_collapsed_renderer`

`test_round_trip = not_run_import_invariant_failed`

`kv_runtime_binding = not_run_import_invariant_failed`

`test_runtime_instantiation = not_run_import_invariant_failed`

`batch_round_trip = not_run_import_invariant_failed`
