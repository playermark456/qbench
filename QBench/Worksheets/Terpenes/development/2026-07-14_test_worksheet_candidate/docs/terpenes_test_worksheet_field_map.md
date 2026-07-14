# Terpenes Test Worksheet field map

Date: 2026-07-14

## Data tab analytical surface

| Range | Purpose | Writable |
|---|---|---|
| `Data!A1:C1` | QBench metadata headers | No |
| `Data!A2:C2` | QBench test/sample/matrix placeholders | No |
| `Data!D1:Z1` | 23 LabSolutions analyte headers in Prompt 2 config order | No |
| `Data!D2:Z2` | LabSolutions `Compound Results(Ch1) > Conc.` inputs; must be actual QBench numeric values for calculation and completeness | Yes |
| `Data!D3:Z3` | Effective concentration formulas | No |
| `Data!D4:Z4` | Result mg/g formulas | No |
| `Data!D5:Z5` | Result percent formulas | No |
| `Data!D6:Z6` | Analytical qualifier formulas | No |

## Data tab named cells and ranges

| Named cell | Cell/range | Default |
|---|---|---|
| `qbench_test_id` | `Data!B9` | `=A2` |
| `qbench_sample_id` | `Data!B10` | `=B2` |
| `product_matrix` | `Data!B11` | `=C2` |
| `sample_mass_g` | `Data!B12` | blank |
| `final_volume_ml` | `Data!B13` | blank |
| `df` | `Data!B14` | blank |
| `df_application_mode` | `Data!B15` | `capture_only_until_method_validated` |
| `labsolutions_conc_unit` | `Data!B16` | `ug/mL` |
| `labsolutions_conc_unit_confirmed` | `Data!B17` | `FALSE` |
| `preparation_values_confirmed` | `Data!B18` | `FALSE` |
| `below_loq_reporting_mode` | `Data!B19` | `decision_required` |
| `loq_source_status` | `Data!B20` | `decision_required` |
| `mu_source_status` | `Data!B21` | `decision_required` |
| `batch_qc_disposition` | `Data!B22` | `Hold` |
| `publish_ready` | `Data!B23` | `FALSE` |
| `analytical_results_complete` | `Data!B24` | formula |
| `calculation_ready` | `Data!B25` | formula |
| `reporting_ready` | `Data!B26` | formula |
| `calculation_message` | `Data!B27` | formula |
| `source_batch_id` | `Data!B28` | blank |
| `source_instrument_file` | `Data!B29` | blank |
| `source_file_hash` | `Data!B30` | blank |
| `source_data_file` | `Data!B31` | blank |
| `source_method_file` | `Data!B32` | blank |
| `source_sequence_file` | `Data!B33` | blank |
| `parser_version` | `Data!B34` | blank |
| `imported_at` | `Data!B35` | blank |
| `instrument_name` | `Data!B36` | blank |
| `detector_id` | `Data!B37` | blank |
| `detector_name` | `Data!B38` | blank |
| `terpenes_instrument_conc` | `Data!D2:Z2` | writable input range |
| `terpenes_effective_conc` | `Data!D3:Z3` | formula range |
| `terpenes_results_mgg` | `Data!D4:Z4` | formula range |
| `terpenes_results_percent` | `Data!D5:Z5` | formula range |
| `terpenes_qualifiers` | `Data!D6:Z6` | formula range |

Controlled values for `below_loq_reporting_mode`:

- `decision_required`
- `display_less_than_loq`
- `display_numeric_result`

Only `display_less_than_loq` and `display_numeric_result` can allow `reporting_ready = TRUE`. The final laboratory decision remains unresolved.

`Data!D2:Z2` inputs are guarded by `ISNUMBER`. Blank inputs leave channel outputs blank. Nonnumeric inputs, including numeric-looking text if QBench stores it as text, leave effective concentration, mg/g, and percent blank and set the channel qualifier to `Review Required`.

## Specifications tab

| Range | Purpose |
|---|---|
| `Specifications!A5:A27` | 23 internal chromatographic channel labels |
| `Specifications!B5:B30` | Measurement Uncertainty, blank until approved source is confirmed |
| `Specifications!C5:C30` | LOQ, blank until approved source is confirmed |
| `Specifications!D5:D27` | Internal percent result formulas |
| `Specifications!E5:E27` | Internal mg/g result formulas |
| `Specifications!F5:F30` | Analytical qualifier formulas |
| `Specifications!G5:G30` | Internal keys |
| `Specifications!H5:H30` | COA mapping keys |
| `Specifications!D28:E28` | Total Ocimene formulas |
| `Specifications!D29:E29` | Total Nerolidol formulas |
| `Specifications!D30:E30` | Total Terpenes formulas |

## Report tab

| Named cell | Cell/range | Purpose |
|---|---|---|
| `report_header` | `Report!A1:E1` | Report table header |
| `report_content` | `Report!A2:E23` | Report content rows |
| `report_results` | `Report!A1:E23` | COA render range |

Report rows use the required 21-measurand display list plus Total Terpenes. Result cells are formula-driven and blank until `reporting_ready` is true.

Report result columns B and C are display-only formulas. They may display `<LOQ` only when `reporting_ready` is true, the Specifications qualifier is `<LOQ`, and `below_loq_reporting_mode = display_less_than_loq`. With `display_numeric_result`, the report displays numerical values. Numerical totals are calculated only in the Data and Specifications layers.

## Compatibility named cells

The 47 existing Worksheet ID 42 compatibility names are preserved exactly. Their current bare cell addresses continue to point at the D/E result-cell semantics in the Specifications tab. The legacy `testterpenes` name remains retained as a compatibility field with unknown business use.
