# Read-only API confirmation

Classification: `oauth_authoritative_endpoint_http_400_controlled_stop`

The exact-origin and local package preflights passed. The ignored runtime CSV
identified the previously proven isolated Test in memory, retained its exact
Assay association, and confirmed the 43/43 blank baseline.

The historical form-encoded request to `/qbench/api/v1/oauth/token` remains
recorded as HTTP 404. Read-only inspection of the exact existing Sandbox API
client and its QBench-hosted Swagger UI then proved the authoritative
`POST /qbench/api/v2/auth/token` multipart JWT-bearer contract.

After all local authentication and worksheet validators passed, exactly one
authorized retry was sent to that authoritative route. The Sandbox returned
HTTP 400 with JSON content. No access token was returned or stored by the
runner. Per the OAuth stop gate, no GET followed and no second retry occurred.

Therefore:

- `read_only_api_identity=not_run_oauth_failed`
- `read_only_api_worksheet_contract=not_run_oauth_failed`
- `destination_contract_proven=runtime_instantiation_passed_pending_read_only_api_confirmation`
- `analyte_patch_key_contract=unresolved`
- `atomicity_classification=api_patch_unresolved`

The endpoint is proven; the successful assertion/request acceptance contract is
not. A future separately authorized phase must resolve the HTTP 400 from an
authoritative QBench source or QBench support before another token request. It
must not probe alternate payloads.

No QBench object, worksheet, or analytical result changed. Across both
historical and current evidence there were two token POSTs, zero GETs, and zero
PATCH, PUT, DELETE, non-token POST, Publish, QC Review, or Pass/Fail actions.
