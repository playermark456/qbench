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

`calculation_ready` is separate from `reporting_ready`. Sample mass and final volume must be numeric and greater than zero. If `df_application_mode = "apply_in_qbench"`, DF must also be numeric and greater than zero. When `df_application_mode = "already_applied_by_labsolutions"`, DF is not required and is not multiplied a second time.

The candidate also adds `analytical_results_complete` at `Data!B24`. It is true only when all 23 instrument concentration inputs and all 23 calculated mg/g results are numeric.

The report can release only after calculation prerequisites are complete, analytical results are complete, batch disposition is `Accepted`, `publish_ready` is `TRUE`, below-LOQ mode is one of the controlled report-release values, and LOQ/MU decisions are confirmed.

Controlled below-LOQ modes are:

- `decision_required`
- `display_less_than_loq`
- `display_numeric_result`

The final laboratory decision remains unresolved. The candidate supports both nondefault display modes only so Sandbox testing can confirm safe worksheet behavior.

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

Nonnumeric preparation inputs such as text mass, text volume, or text DF block calculation. Zero and negative mass, volume, or applicable DF also block calculation.

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

Rollups and totals are completeness-gated:

- Total Ocimene stays blank unless both component results are numeric.
- Total Nerolidol stays blank unless both component results are numeric.
- Total Terpenes stays blank unless all 23 internal channel results are numeric.

MU and LOQ values remain blank until approved sources are confirmed.

## Report tab

The Report tab is a compact `A1:E23` table:

- A: Analyte
- B: Result (%)
- C: Result (mg/g)
- D: LOQ (mg/g)
- E: MU (%)

The table contains the 21 default COA measurands in the required order plus Total Terpenes. Report result cells are formulas gated by `reporting_ready`. When `reporting_ready` is false, result cells stay blank.

Report Result (%) and Result (mg/g) columns are display formulas. If `reporting_ready` is true and the Specifications qualifier is `<LOQ`, the report displays `<LOQ` only when `below_loq_reporting_mode = "display_less_than_loq"`. If `below_loq_reporting_mode = "display_numeric_result"`, the report displays the numerical result. `Hold` and `Review Required` messages remain outside `report_results`.

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
