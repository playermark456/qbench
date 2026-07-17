# Saved Draft round-trip semantic comparison

Date: 2026-07-17

- Worksheet: `SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE`
- Saved version: `JSON Scalar 43 Field Base v1`
- Version state: `DRAFT`
- Candidate SHA-256: `e5ef20a5cec574dc292ed679867e01313233c92ceda9ef863bf98dd8d4485b80`
- Raw saved/reopened export SHA-256: `3589f2ace8afb96db96d4da638e9effc86bda404e03f97b85fca0e43aa349912`

The candidate and raw round-trip export have the same legacy
`table_config`/`qb_config` envelope. QBench regenerated the one renderer UUID
when the Draft was saved. After normalizing only that UUID, the parsed JSON
objects are identical. No other semantic difference exists.

| Contract check | Candidate | Saved/reopened export | Result |
|---|---:|---:|---|
| Logical Data worksheets | 1 | 1 | passed |
| Grid | 40x26 | 40x26 | passed |
| Visible anchors | 28 | 28 | passed |
| Named cells | 43 | 43 | passed |
| Unqualified cell values | 43 | 43 | passed |
| Unique addresses | 43 | 43 | passed |
| Exportable destinations | 43 | 43 | passed |
| Blank destinations | 43 | 43 | passed |
| Writable destinations | 43 | 43 | passed |
| Formula-owned destinations | 0 | 0 | passed |
| A2 destinations | 0 | 0 | passed |
| `sdf` / Pass/Fail / prohibited destinations | 0 | 0 | passed |

The prior qualified-address error was exactly:
`Invalid cell definition Data!D2 for field name terpenes_instrument_conc_01`.
It was never an A2 address. The saved Draft uses `D2` for the first analyte and
contains no A2 mapping.

Classifications:

- `json_import_saved_definition_contract=passed_43_of_43`
- `json_import_round_trip=passed`
- `destination_contract_proven=runtime_instantiation_passed_pending_read_only_api_confirmation`
- `atomicity_classification=api_patch_unresolved`
- `analyte_patch_key_contract=unresolved`

The separately authorized runtime instantiation passed the same contract at
43/43 and restored a 43/43 blank baseline. The operational publisher mapping
remains unpromoted pending read-only API confirmation.
