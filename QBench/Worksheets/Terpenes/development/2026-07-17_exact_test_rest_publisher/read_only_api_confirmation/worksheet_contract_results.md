# API Worksheet contract result

Classification: `read_only_api_worksheet_contract=not_run_oauth_failed`

No GET response exists, so this phase makes no claim that the API exposes or
accepts any exact system-name key. The 43 expected keys are recorded in
`field_key_comparison.csv` as `not_exposed_by_get_contract` solely because the
GET contract was not reached; that is a controlled-stop bookkeeping state, not
an observation about a QBench GET response.

Counts:

- observed exact: 0
- missing: 0
- renamed: 0
- duplicated: 0
- present but unreadable: 0
- not exposed by GET contract: 43

The existing UI/runtime proof remains 43/43 blank. API blank values were not
observed because no GET occurred.

- `destination_contract_proven=runtime_instantiation_passed_pending_read_only_api_confirmation`
- `analyte_patch_key_contract=unresolved`
- `atomicity_classification=api_patch_unresolved`
