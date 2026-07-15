# Reviewed import to Publish mapping

The reviewed Publish adapter is a preview library only. It does not write to
QBench and does not begin Prompt 5 automation.

## Required inputs

A Publish preview is generated only when:

- QBench Test ID is nonblank.
- Row-specific review evidence keyed by `source_row_hash` is present.
- The review evidence has `explicitly_selected = true`.
- The review evidence has `import_validation_status = Valid`.
- The review evidence has `import_message = Import row valid`.
- All 23 analytes are JavaScript numbers.
- Sample mass and final volume are positive numbers.
- DF application mode is controlled.
- DF is valid when `apply_in_qbench` is selected.
- LabSolutions concentration unit is exactly `ug/mL`.
- Unit confirmed is TRUE.
- Preparation values confirmed is TRUE.
- Dimethylacetamide is numeric.
- Compound Results validation is complete.
- Integration Review Status is `Reviewed`.
- Source Row Hash is nonblank.
- Explicit QBench Test ID to Publish row mapping is present, unless the caller
  requests a Test-ID-keyed preview without worksheet ranges.

## Publish preview map

| Publish range | Source |
|---|---|
| D:Z | 23 analyte values |
| AA | sample mass |
| AB | final volume |
| AC | DF |
| AD | DF application mode |
| AE | LabSolutions Conc. Unit |
| AF | Unit Confirmed |
| AG | Preparation Values Confirmed |
| AH | Source Batch ID |
| AI | Source Instrument File |
| AJ | Source File Hash |
| AK | Source Data File |
| AL | Source Method File |
| AM | Source Sequence File |
| AN | Parser Version |
| AO | Imported At |
| AP | Instrument Name |
| AQ | Detector ID |
| AR | Detector Name |
| AS | Source Injection ID |
| AT | Source Row Hash |
| AU | Dimethylacetamide Conc. |
| AV | Compound Results Complete |
| AW | Integration Review Status |
| AX | Import Validation Status |

The adapter never writes AY or later formula/control columns and never writes
directly to the Test Worksheet.

Each patch records `expected_qbench_test_id`, `target_publish_row`, `range`, and
`source_row_hash`. Publish row mapping uses QBench Test ID only, never QBench
Sample ID.

Multi-row previews are atomic. If any selected row fails validation, has missing
or duplicate review evidence, lacks a Publish row mapping, maps to a duplicate
or out-of-range destination row, or shares a Test ID with another selected row,
the overall status is `blocked` and `patches` is empty.
