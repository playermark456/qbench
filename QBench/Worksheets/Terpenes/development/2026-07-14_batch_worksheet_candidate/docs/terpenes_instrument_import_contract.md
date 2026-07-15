# Terpenes instrument import contract

Date: 2026-07-14

## Source

The controlled quantitative source is:

- LabSolutions section: `Compound Results(Ch1)`
- Field: `Conc.`

The Batch Worksheet must not use `Conc. %`, `Norm Conc.`, or Peak Table values as final quantitative results.

`Peak Table(Ch1)` is retained only for chromatographic audit and QC review. Unknown or blank Peak Table names may be retained for audit. They must not silently map to Other Terpenes.

## Row model

`Instrument Import` has 200 data rows. One row represents one injection or parsed LabSolutions result record.

Unknown and Dilution rows require a QBench Test ID. QC rows may have a blank QBench Test ID.

## Required structural rules

- `compound_result_row_count` must equal 24.
- `peak_table_row_count` must be numeric and zero or greater.
- `reportable_compound_row_count` must equal 23.
- AH:BD must contain the 23 Prompt 2 analytes in exact config order.
- Unknown and Dilution rows must have 23 actual numeric analyte values to become structurally publishable.
- Numeric zero is valid.
- Nonnumeric text remains invalid. Numeric-looking text such as `24`, `23`, or `34` is not silently accepted if QBench stores it as text.
- Dimethylacetamide must be numeric and retained for audit.
- `unknown_peak_count` must be numeric and zero or greater.
- Manual integration values are exactly `No` or `Yes`.
- When manual integration is `Yes`, an integration reason is required.
- Integration review status values are exactly `Not Reviewed`, `Reviewed`, or `Review Required`.
- Import validation status values are exactly `Valid`, `Review Required`, or `Rejected`.

## Numeric contract

Active comparator worksheets use the QBench-supported text cell type for batch import surfaces. The candidate therefore keeps the supported cell type and relies on `ISNUMBER` and `COUNT` formulas plus Sandbox testing to confirm numeric recognition.

The worksheet does not use `VALUE` or `IFERROR` to coerce or conceal import errors. Nonnumeric values in count/audit fields return controlled import messages and are not intended to produce spreadsheet formula errors.

## Source traceability

The required source fields for Publish transfer are:

- Source Batch ID
- Source Instrument File
- Source File Hash
- Source Data File
- Source Method File
- Source Sequence File
- Parser Version
- Imported At
- Instrument Name
- Detector ID
- Detector Name
- Source Injection ID
- Source Row Hash

## Out of scope

The import tab does not calculate final sample mg/g, percent, qualifiers, totals, COA results, LOQ conclusions, MU values, METRC fields, key/value-store fields, or automation outputs.
