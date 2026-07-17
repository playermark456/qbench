# Read-only API confirmation preflight

- Origin preflight: `passed_exact_sandbox_origin`
- Exact allowed origin: `https://ait-sandbox.qbench.net`
- Allowed methods: one `POST` to the token endpoint, followed only by `GET`
- Token endpoint template: `/qbench/api/v1/oauth/token`
- Test endpoint template: `/qbench/api/v1/test/{test_id}`
- Test Worksheet endpoint template: `/qbench/api/v1/test/{test_id}/worksheet`
- Expected Worksheet: `SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE`
- Expected Version: `JSON Scalar 43 Field Base v1`
- Expected Assay: `SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_ASSAY`
- Expected Sample: `SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_RUNTIME_SAMPLE`
- Expected destination keys: the 43 ordered system names in
  `config/field_mapping_scalar_candidate.csv`
- Expected runtime baseline: 43/43 destinations blank

The exact Test identifier is loaded only from ignored local runtime evidence.
It may exist in process memory and ignored raw evidence, but it is never
printed or committed.

## Pre-dispatch stop conditions

- any credential key is missing or blank;
- the raw base URL is not byte-for-byte equal to the exact allowed origin;
- the runtime export does not identify exactly one Test with the expected
  Assay and a 43/43 blank destination baseline;
- a URL is not HTTPS on the exact allowed host and default TLS port;
- a URL contains user information, a query, or a fragment;
- a redirect is returned;
- a proxy would be used;
- the method is PATCH, PUT, DELETE, HEAD, OPTIONS, or non-token POST;
- the endpoint is not one of the three templates above;
- OAuth fails or returns a non-Bearer/invalid-lifetime token;
- the Test GET cannot prove the exact Test and Sample identifiers plus the
  expected Assay title;
- any response would require guessing an undocumented endpoint.

TLS certificate verification uses the platform trust store. Redirects and
environment proxies are disabled. Token exchange is attempted once. GET retry
is bounded to one retry and only for transient status or transport failure.
