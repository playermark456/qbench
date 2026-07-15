# Terpenes Batch Worksheet design

Date: 2026-07-14

## Source and safety

The candidate is generated from the immutable active Worksheet ID 43 export:

`QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json`

The generator preserves the workbook namespace, records the source SHA-256, renames the source `Sheet1` tab to `Publish`, and preserves the source `Sheet1` worksheet ID for that tab. Repository search found no current named-cell, formula, automation, or index dependency that makes the `Sheet1` tab name unsafe to rename.

The source Publish-row capacity is 86 QBench test rows. The generated `Publish` tab preserves the source test display ID placeholders and product-matrix placeholders, while adding a QBench sample ID placeholder in column B.

## Tab design

### Run Setup

`Run Setup` is a compact field/value/notes table. It captures QBench batch ID, analytical batch ID, instrument, detector, method, sequence, analyst, run time, parser version, source package version, raw ASCII attachment reference, source manifest hash, and review fields.

`run_setup_complete` is formula-driven and conservative. It can become true only when the required run setup fields are present and `batch_assay_name` is exactly `Terpenes`. `run_column`, carrier gas, calibration ID, standard lot, and extraction solvent lot are retained as optional fields until a controlled source makes them mandatory. The formula does not represent laboratory approval.

`run_setup_message` returns the first neutral missing-requirement message, such as `QBench batch ID required`, `Instrument name required`, `Raw batch manifest hash required`, or `Run setup complete`.

### Instrument Import

`Instrument Import` is a fixed 200-row normalized import surface. Each row represents one injection or parsed LabSolutions result record. Leading columns A:AG match the required Prompt 4 order, analyte columns AH:BD hold the 23 Prompt 2 controlled Compound Results `Conc.` channels, and BE stores `source_row_hash`.

The import formulas check row structure, sample type, source traceability, Compound Results row counts, Peak Table row count, reportable analyte count, Dimethylacetamide audit retention, unknown peak count, manual integration review, and integration review status. Numeric fields use the worksheet-supported text cell type documented from comparator worksheets; numeric recognition is enforced with `ISNUMBER` and `COUNT` formulas plus Sandbox testing. Numeric-looking text in required count/audit fields is rejected rather than coerced.

### QC Review

`QC Review` contains a batch control block and a 23-analyte QC table. The table evaluates calibration r, initial CCV recovery, initial CCV RSD, blank fraction of LOQ, LOQ recovery, matrix spike recovery, duplicate difference, bracketing CCV recovery, retention-time drift, and resolution.

Allowed individual QC evaluation outputs are only:

- `within_criteria`
- `outside_criteria`
- `decision_required`
- `not_evaluated`
- `not_applicable`
- `review_required`

The known bracketing CCV discrepancy remains explicitly unresolved. The only controlled bracketing status values are `decision_required` and `confirmed`. The default `bracketing_ccv_criterion_status` is `decision_required`, the bracketing window is blank, and `qc_configuration_complete` remains false until the method owner decision is made.

`lcs_requirement_status` defaults to `decision_required`. If it is later set to `required`, configuration remains incomplete until controlled LCS acceptance criteria and worksheet implementation exist. If it is later set to `not_required`, the worksheet also requires a controlled-source reference and reviewer before configuration can complete.

### Publish

`Publish` is the controlled one-row-per-QBench-Test source surface for future Prompt 5 transfer. Columns D:Z contain the 23 instrument concentration values in Prompt 2 config order. The tab captures sample prep values, dilution mode, unit/preparation confirmations, source traceability, Dimethylacetamide audit value, Compound Results completion, integration review status, import validation status, batch QC disposition, row prerequisites, Publish Ready, and the first unmet neutral Publish message.

`Row Prerequisites Complete` is separate from `batch_publish_ready`; this prevents circular release logic. `Publish Ready` returns exact transferable text:

- `TRUE`
- `FALSE`
- blank for unused rows

`Publish Ready` can be `TRUE` only when row prerequisites are complete and `batch_publish_ready` is true.

## Controlled Publish column-contract decision

Publish column A is intentionally `QBench Test ID`, and Publish column B is intentionally `QBench Sample ID`. This is a controlled deviation from the original draft Prompt 4 column list because QBench Test ID is the Prompt 5 join key and the active source Test ID placeholder is preserved in column A.

The named-range and source-contract mapping is the authoritative Prompt 5 interface. The package does not claim exact column-order compliance with the earlier draft list.

## Release gates

`batch_publish_ready` requires:

- `Run Setup!B24 = TRUE`.
- Integration review complete.
- QC review complete.
- All populated Publish rows structurally valid.
- Duplicate Test ID count equals zero.
- Populated Publish row count greater than zero.
- `batch_qc_disposition = Accepted`.

`qc_review_complete` requires QC configuration complete, QC data complete, all 23 Overall Analyte QC Evaluation cells within criteria, and the QC reviewer/reviewed-at fields. `outside_criteria`, `decision_required`, `not_evaluated`, and `review_required` block release. Accepted disposition alone is insufficient.

## Exclusions

Prompt 4 intentionally does not create a Report tab, METRC tab, key/value-store tab, QBench automation, parser configuration, COA output, final mg/g result, percent result, qualifier, total, LOQ conclusion, or MU value.
