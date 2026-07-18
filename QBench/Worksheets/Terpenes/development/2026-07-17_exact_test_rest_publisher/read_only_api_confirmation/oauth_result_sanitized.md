# OAuth result (sanitized)

- Origin preflight: `passed_exact_sandbox_origin`
- Credential loading: passed; three required keys were nonblank
- Credential values displayed: no
- Historical token request attempts: 1
- Current authoritative-route retry attempts: 1
- Method: `POST`
- Historical endpoint template: `/qbench/api/v1/oauth/token`
- Authoritative endpoint template: `/qbench/api/v2/auth/token`
- Exact origin: `https://ait-sandbox.qbench.net`
- Historical HTTP status: 404
- Authoritative retry HTTP status: 400
- Authoritative retry response content type: `application/json`
- OAuth result: `failed_authoritative_endpoint_http_400`
- Token type: not available
- Approximate expiration: not available
- Access token returned: no
- Token persisted or displayed: no
- Client assertion persisted or displayed by the runner: no
- Redirect followed: no
- Second authoritative-route retry attempted: no

Both raw token responses were suppressed and were neither displayed nor
written to evidence. The historical 404 is preserved in the versioned ledger.

During read-only Swagger inspection, an auto-generated documentation assertion
was inadvertently emitted once in transient tool output. It was not repeated,
saved, used for the controlled retry, or committed. The publisher and retry
runner did not display their locally generated assertion.
