# Terpenes Test Worksheet design

Date: 2026-07-14

## Source and safety

The candidate is generated from the immutable active Worksheet ID 42 export:

`QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_42__worksheet_export_spreadsheet__active__2026-07-04.json`

The generator preserves the workbook namespace, the existing worksheet IDs, tab names, and tab order. It writes a new candidate under `dist/` and leaves the source export untouched.

The current active export contains one stale conditional-formatting rule tied to Fail-style worksheet behavior. The generated candidate removes conditional formatting rules from the candidate only.

## Tabs

The candidate preserves exactly these tabs:

1. `Report`
2. `Data`
3. `Specifications`

No METRC tab is added in Prompt 3.

## Data tab

Columns D:Z are the 23-channel writable LabSolutions `Compound Results(Ch1) > Conc.` input surface in Prompt 2 config order.

Rows:

1. Headers and 23 analyte labels.
2. Writable instrument concentration inputs in D:Z.
3. Effective concentration formulas.
4. Result mg/g formulas.
5. Result percent formulas.
6. Internal analytical qualifier formulas.
8 onward. Control and audit block.

The default calculation and reporting gates are intentionally closed:

- `labsolutions_conc_unit = "ug/mL"`
- `labsolutions_conc_unit_confirmed = FALSE`
- `preparation_values_confirmed = FALSE`
- `df_application_mode = "capture_only_until_method_validated"`
- `below_loq_reporting_mode = "decision_required"`
- `loq_source_status = "decision_required"`
- `mu_source_status = "decision_required"`
- `batch_qc_disposition = "Hold"`
- `publish_ready = FALSE`

`calculation_ready` is separate from `reporting_ready`. The report can release only after calculation prerequisites are complete, batch disposition is `Accepted`, `publish_ready` is `TRUE`, and LOQ/MU decisions are confirmed.

## Calculation formulas

Each internal channel uses:

`effective concentration = instrument concentration * dilution multiplier`

The dilution multiplier is:

- `1` when `df_application_mode = "already_applied_by_labsolutions"`.
- `df` when `df_application_mode = "apply_in_qbench"`.
- blank when the mode is unresolved or invalid.

`result mg/g = effective concentration ug/mL * final volume mL / sample mass g / 1000`

`result percent = result mg/g / 10`

Blank instrument inputs produce blank channel outputs. Unconfirmed or invalid calculation configuration blocks numerical output.

## Specifications tab

Rows 5:27 preserve the 23 internal chromatographic channels. Columns A:E preserve the active worksheet purposes:

- A: Analyte
- B: Measurement Uncertainty (%)
- C: LOQ (mg/g)
- D: Result (%)
- E: Result (mg/g)

Prompt 3 adds support columns:

- F: Qualifier
- G: Internal Key
- H: COA Mapping Key

Rows 28:30 add controlled totals:

- Total Ocimene = cis-Ocimene + trans-Ocimene.
- Total Nerolidol = cis-Nerolidol + trans-Nerolidol.
- Total Terpenes = sum of the 23 internal numerical terpene channels, excluding rollup rows.

MU and LOQ values remain blank until approved sources are confirmed.

## Report tab

The Report tab is a compact `A1:E23` table:

- A: Analyte
- B: Result (%)
- C: Result (mg/g)
- D: LOQ (mg/g)
- E: MU (%)

The table contains the 21 default COA measurands in the required order plus Total Terpenes. Report result cells are formulas gated by `reporting_ready`. When `reporting_ready` is false, result cells stay blank.

The report uses Total Ocimene and Total Nerolidol rollups and keeps both percent and mg/g columns. It does not include a compliance status column.

## Named cells

The generated candidate preserves all 47 current compatibility named-cell system names from the active Worksheet ID 42 export, including the legacy `testterpenes` field.

It adds:

- Total result named cells for Ocimene, Nerolidol, and Total Terpenes.
- `report_header`, `report_content`, and `report_results`.
- Data-tab control/audit named cells.
- Data-tab ranges for instrument concentration, effective concentration, mg/g results, percent results, and qualifiers.

## Deferred work

Prompt 3 does not implement final METRC profile selection, METRC row generation, key/value-store configuration, parser configuration upload, QBench automation, COA source changes, protocol worksheets, report configuration changes, or production changes.
