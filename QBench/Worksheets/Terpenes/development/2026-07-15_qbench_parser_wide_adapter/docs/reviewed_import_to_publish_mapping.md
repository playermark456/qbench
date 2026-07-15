# Reviewed import to Publish mapping

The reviewed Publish adapter is a preview library only. It does not write to
QBench and does not begin Prompt 5 automation.

## Required inputs

A Publish preview is generated only when:

- QBench Test ID is nonblank.
- The source injection is explicitly selected.
- All 23 analytes are JavaScript numbers.
- Sample mass and final volume are positive numbers.
- DF application mode is controlled.
- DF is valid when `apply_in_qbench` is selected.
- Unit confirmed is TRUE.
- Preparation values confirmed is TRUE.
- Dimethylacetamide is numeric.
- Compound Results validation is complete.
- Integration Review Status is `Reviewed`.
- Import Validation Status is `Valid`.
- Source Row Hash is nonblank.

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
