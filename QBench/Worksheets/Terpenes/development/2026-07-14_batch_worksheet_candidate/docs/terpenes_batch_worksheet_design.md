# Terpenes Batch Worksheet design

Date: 2026-07-14

## Source and safety

The candidate is generated from the immutable active Worksheet ID 43 export:

`QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json`

The generator preserves the workbook namespace, records the source SHA-256, renames the source `Sheet1` tab to `Publish`, and preserves the source `Sheet1` worksheet ID for that tab. Repository search found no current named-cell, formula, automation, or index dependency that makes the `Sheet1` tab name unsafe to rename.

The source Publish-row capacity is 86 QBench test rows. The generated `Publish` tab preserves the source test display ID placeholders and product-matrix placeholders, while adding a QBench sample ID placeholder in column B.

## Tab design

### Run Setup

`Run Setup` is a compact field/value/notes table. It captures analytical batch ID, instrument, detector, method, sequence, analyst, run time, parser version, source package version, source manifest hash, and review fields.

`run_setup_complete` is formula-driven and conservative. It can become true only when the required run setup fields are present. It does not represent laboratory approval.

`run_setup_message` returns the first neutral missing-requirement message, such as `Analytical batch ID required`, `Instrument required`, `Source manifest required`, or `Run setup complete`.

### Instrument Import

`Instrument Import` is a fixed 200-row normalized import surface. Each row represents one injection or parsed LabSolutions result record. Leading columns A:AG match the required Prompt 4 order, analyte columns AH:BD hold the 23 Prompt 2 controlled Compound Results `Conc.` channels, and BE stores `source_row_hash`.

The import formulas check row structure, sample type, source traceability, Compound Results row counts, reportable analyte count, Dimethylacetamide audit retention, manual integration review, and integration review status. Numeric fields use the worksheet-supported text cell type documented from comparator worksheets; numeric recognition is enforced with `ISNUMBER` and `COUNT` formulas plus Sandbox testing.

### QC Review

`QC Review` contains a batch control block and a 23-analyte QC table. The table evaluates calibration r, initial CCV recovery, initial CCV RSD, blank fraction of LOQ, LOQ recovery, matrix spike recovery, duplicate difference, bracketing CCV recovery, retention-time drift, and resolution.

Allowed individual QC evaluation outputs are only:

- `within_criteria`
- `outside_criteria`
- `decision_required`
- `not_evaluated`
- `not_applicable`
- `review_required`

The known bracketing CCV discrepancy remains explicitly unresolved. The default `bracketing_ccv_criterion_status` is `decision_required`, the bracketing window is blank, and `qc_configuration_complete` remains false until the method owner decision is made.

### Publish

`Publish` is the controlled one-row-per-QBench-Test source surface for future Prompt 5 transfer. Columns D:Z contain the 23 instrument concentration values in Prompt 2 config order. The tab captures sample prep values, dilution mode, unit/preparation confirmations, source traceability, Dimethylacetamide audit value, Compound Results completion, integration review status, import validation status, batch QC disposition, row prerequisites, Publish Ready, and the first unmet neutral Publish message.

`Row Prerequisites Complete` is separate from `batch_publish_ready`; this prevents circular release logic. `Publish Ready` returns exact transferable text:

- `TRUE`
- `FALSE`
- blank for unused rows

`Publish Ready` can be `TRUE` only when row prerequisites are complete and `batch_publish_ready` is true.

## Release gates

`batch_publish_ready` requires:

- QC configuration complete.
- Integration review complete.
- QC data complete.
- QC review complete.
- All populated Publish rows structurally valid.
- Duplicate Test ID count equals zero.
- `batch_qc_disposition = Accepted`.
- Batch QC reviewer and reviewed-at fields present.

Defaults block release. Accepted disposition alone is insufficient.

## Exclusions

Prompt 4 intentionally does not create a Report tab, METRC tab, key/value-store tab, QBench automation, parser configuration, COA output, final mg/g result, percent result, qualifier, total, LOQ conclusion, or MU value.
