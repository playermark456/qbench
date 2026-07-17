# Scalar candidate mapping

Date: 2026-07-17

`config/field_mapping_scalar_candidate.csv` is the unpromoted 43-row candidate.
It preserves every source column, source header, source named range,
destination address, transfer type, constraint, row order, and status from
`config/field_mapping.csv`. Only the first 23 destination system names differ.

The candidate analyte names are exactly
`terpenes_instrument_conc_01` through `terpenes_instrument_conc_23`, in order,
at `Data!D2` through `Data!Z2`. The remaining 20 destination names and
addresses are unchanged.

Local candidate validation proves:

- exactly 43 mappings and 23 analytes;
- analyte suffixes exactly `01` through `23`, without gaps;
- 43 unique destination names and 43 unique destination addresses;
- analyte addresses exactly `Data!D2:Z2`;
- no bracketed destination name;
- no Pass/Fail destination;
- no Dimethylacetamide reportable destination;
- no Peak Table reportable destination.

The candidate was not promoted because the saved/reopened Phase 1A native
worksheet did not retain any of its seven representative named-cell
definitions. Operational `config/field_mapping.csv` and publisher code remain
unchanged, and the analyte PATCH-key contract remains unresolved.
