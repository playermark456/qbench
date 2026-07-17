# Field mapping

`config/field_mapping.csv` is a controlled copy of the merged Prompt 5
`automation_mapping.csv` with all 43 rows preserved in order:

- 23 instrument-input analytes;
- 7 calculation/preparation controls;
- 11 source/instrument metadata values;
- Batch QC disposition;
- publish-ready control.

All mapping rows currently have status
`unverified_saved_sandbox_destination`.

## Important REST ambiguity

The merged Test Worksheet has one range named cell,
`terpenes_instrument_conc` at `Data!D2:Z2`. Prompt 5 expressed the 23 targets
as `terpenes_instrument_conc[1]` through `[23]` for automation design. The REST
contract supplied for Prompt 5B describes named-cell keys, but no Sandbox probe
has established whether QBench accepts those indexed keys or requires one
range value such as a 1x23 array.

The publisher supports either representation only after
`analyte_patch_key_contract` is set from empirical Sandbox evidence. Its default
is `unresolved`, which blocks PATCH.

## Saved worksheet proof required

Before runtime testing, Export Spreadsheet from the exact saved task-created
Test Worksheet and verify:

1. every scalar named cell exists once;
2. `terpenes_instrument_conc` covers exactly `Data!D2:Z2`;
3. each mapped target is writable and retains native numeric/text values;
4. no target contains a formula;
5. calculated `Data!D3:Z6`, readiness formulas, Specifications, and Report
   remain formula-owned and are not mapped;
6. Dimethylacetamide is not mapped;
7. Peak Table values are not mapped;
8. no Test Worksheet Pass/Fail named cell exists.

The repository candidate passes the structural base-name/cell comparison, but
that candidate is not proof of the actual saved Sandbox worksheet. Prompt 5A's
post-run Test Worksheet export lacked its intended destination named cell, so
repository-only evidence cannot clear this gate.
