# OAuth 404 root cause

Classification:

`oauth_404_root_cause=incorrect_token_endpoint_path`

Sanitized comparison:

| Property | Failed historical request | Authoritative Sandbox contract |
| --- | --- | --- |
| Method | `POST` | `POST` |
| Endpoint template | `/qbench/api/v1/oauth/token` | `/qbench/api/v2/auth/token` |
| Content type | `application/x-www-form-urlencoded` | `multipart/form-data` |
| Fields | `grant_type`, `client_id`, `client_secret` | `assertion`, `grant_type` |
| Grant type | `client_credentials` | `urn:ietf:params:oauth:grant-type:jwt-bearer` |

The prior HTTP 404 occurred at the wrong route before credential validity could
be evaluated. It is historical evidence and is not reclassified as an invalid
client ID or client secret.

The exact path difference is both the API prefix/version segment and the auth
resource: `/qbench/api/v1/oauth/token` became
`/qbench/api/v2/auth/token`. Request-body construction also required correction
to the documented multipart JWT-bearer form.

Authoritative source: the exact Sandbox API client's `Docs` link and the
expanded `AUTHENTICATION` operation in the Sandbox-hosted `QBench API 2.0 OAS3`
Swagger UI.
