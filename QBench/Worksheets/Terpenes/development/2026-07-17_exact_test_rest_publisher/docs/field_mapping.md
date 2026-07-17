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

## Unpromoted scalar candidate

`config/field_mapping_scalar_candidate.csv` preserves all 43 ordered source
mappings, destination addresses, transfer types, constraints, and statuses.
It changes only the 23 analyte destination system names to exact independent
scalar names `terpenes_instrument_conc_01` through `_23` at `Data!D2:Z2`.
The remaining 20 rows are byte-for-field equivalent to the operational
mapping.

The candidate validator proves exactly 43 rows, exactly 23 analytes numbered
01 through 23, unique names and addresses, exact `Data!D2:Z2` analyte cells,
and no brackets, Pass/Fail, Dimethylacetamide, or Peak Table destination.

The candidate was not promoted. The new native scalar worksheet reopened with
zero of seven representative named-cell definitions, so
`config/field_mapping.csv`, publisher payload construction, and runtime
classification remain unchanged.

## Important REST ambiguity

The merged Test Worksheet has one range named cell,
`terpenes_instrument_conc` at `Data!D2:Z2`. Prompt 5 expressed the 23 targets
as `terpenes_instrument_conc[1]` through `[23]` for automation design. The REST
contract supplied for Prompt 5B describes named-cell keys, but no Sandbox probe
has established whether QBench REST accepts those indexed keys or requires one
range value such as a 1x23 array.

The 2026-07-17 native Phase 1 worksheet probe established a narrower editor
fact: the old-Sandbox native Worksheet save path retained the four scalar
controls but rejected the three representative bracketed named-cell keys.
Otherwise-identical underscore controls persisted and were removed after the
diagnostic. This proves the required indexed names cannot currently be built
through that native save path; it does not establish the REST PATCH-key shape.

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

The 2026-07-17 local proof run established:

- repository candidate: 43 targets found, 43 unique, 43 writable by exported
  cell metadata, zero formula-owned destinations, and zero Pass/Fail mappings;
- candidate result: not proven because saved/reopened Sandbox provenance is
  missing;
- active saved 2026-06-30 Test Worksheet export: zero of the 43 current
  destinations, so it cannot clear the gate;
- no proof artifact was generated and `destination_contract_proven` remains
  false.

See `destination_contract_results.md` for hashes, provenance requirements, and
the exact controlled stop. See `native_43_field_rebuild/` for the failed 4/7
native Phase 1 evidence. All 43 mapping-row statuses remain
`unverified_saved_sandbox_destination`.
