# Native named-cell persistence diagnostic

Date: 2026-07-17

Final classification:
**`native_named_cell_save_environment_or_procedure_blocked`**.

Probe A used a completely unique system name in a new isolated native
Spreadsheet Worksheet. QBench's **Add Named Cell** control was used exactly
once. The three fields were entered with real keystrokes, each field was
blurred with Tab, Exportable was enabled, and focus was moved outside the row.
The complete row was visibly present before Create.

After the Draft version save completed, a full navigation back to the
Worksheets list, and reopen from that list, the 6x5 grid and A1 probe label
persisted but the named-cell list contained zero rows. No visible validation
or error message appeared.

Probe A therefore failed. The required stop gate prevented Probes B and C,
the no-leading-zero fallback, any further candidate-name test, and any new
seven- or 43-field worksheet construction.

This diagnostic does not prove that underscore names, `_01`, reused scalar
names, or the candidate mapping are unsupported. It proves only that the old
Sandbox could not be trusted to persist a newly created single native
named-cell definition through the explicitly exercised procedure in this run.

Controls remain:

- `destination_contract_proven=false`
- `atomicity_classification=api_patch_unresolved`
- `analyte_patch_key_contract=unresolved`
- `config/field_mapping_scalar_candidate.csv` remains unpromoted
- no token, REST API request, PATCH, live-QBench access, Assay, Sample, Test,
  analytical result, or Pass/Fail artifact occurred
