# Authoritative OAuth endpoint discovery

Discovery date: 2026-07-17

The exact existing Sandbox API client named `Terpenes Sandbox REST Publisher`
was opened read-only. Its `Docs` link opened the Sandbox-hosted Swagger UI
identified as `QBench API 2.0` / `OAS3`. The expanded `AUTHENTICATION` section
documents:

- scheme and host: `https://ait-sandbox.qbench.net`;
- token path: `/qbench/api/v2/auth/token`;
- method: `POST`;
- request content type: `multipart/form-data`;
- required fields: `assertion` and `grant_type`;
- assertion representation: JWT;
- grant type: `urn:ietf:params:oauth:grant-type:jwt-bearer`.

The documentation form supplied a nonblank JWT assertion and did not require
`client_id` or `client_secret` as separate form fields. The local publisher
therefore constructs a short-lived HS256 JWT in memory with `iat`, `exp`, and
`sub` claims, where `sub` is the client ID and the signature uses the client
secret. Neither the assertion nor its subject value is retained in tracked
evidence.

The API client page showed `Server-Side Web Application` as the client type
and `v1` as the selected API version access. Its own documentation link still
authoritatively places authentication under the v2 auth route. This establishes
the token-route/API-access relationship without changing the existing v1 GET
templates.

No API client, scope, QBench object, or configuration was changed. The Swagger
`Execute` control was not used.
