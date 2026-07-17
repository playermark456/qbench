# JSON import compatibility result

Classification:
**`saved_definition_round_trip_passed_pending_runtime_instantiation`**

Manual testing of the prior native-envelope candidate proved that it rendered
the expected 40x26 grid and loaded all 43 named cells. That render is valid
structural evidence, but it is not saved-version evidence.

QBench rejected **Save As New Version** with:

`Invalid cell definition Data!D2 for field name terpenes_instrument_conc_01`

The error was never an A2 address. The logical contract maps the first analyte to
`Data!D2`; there is no A2 destination. The actionable compatibility finding is that the old
single-tab save validator rejects sheet-qualified JSON cell definitions.

The regenerated candidate uses 43 unqualified runtime cells while preserving
the successfully rendered worksheet structure. The user imported it into the
isolated Sandbox Worksheet and saved `JSON Scalar 43 Field Base v1` as Draft.
The visible Draft row, saved Draft editor, refresh, and list-based reopen all
proved the expected identity and persistence.

- Corrected JSON cells unqualified: 43/43
- First analyte: `D2`
- A2 mapping: absent
- Corrected Draft row visibly established: yes
- Grid before and after refresh/list reopen: 40x26
- Named cells before and after refresh/list reopen: 43
- Corrected saved/reopened export: yes
- Raw export SHA-256:
  `3589f2ace8afb96db96d4da638e9effc86bda404e03f97b85fca0e43aa349912`
- Semantic comparison: passed after normalizing only QBench's regenerated
  renderer UUID
- `json_import_saved_definition_contract=passed_43_of_43`
- `json_import_round_trip=passed`
- `destination_contract_proven=saved_definition_only_pending_runtime_instantiation`

The Draft was not approved or activated, no runtime Test was created, and the
operational mapping remains unpromoted.
