# Security model

## Credential boundary

The application accepts QBench client credentials only from an ignored local
file passed with `--secrets-file`. It requires nonblank `QBENCH_BASE_URL`,
`QBENCH_CLIENT_ID`, and `QBENCH_CLIENT_SECRET`. The local credential check
reports only key presence/nonblank status and the allowlist result. The sample
environment file contains blank variable names only, and root `.gitignore`
patterns cover `.env.local` and Windows-appended variants such as
`.env.local.txt`.

The OAuth exchange uses `grant_type=client_credentials`. The Client ID and
Client Secret exist only in process memory after file loading. A successful
response must contain a Bearer access token with a positive lifetime no longer
than 3,600 seconds. The token remains in memory and is never persisted.

The application never returns, prints, logs, screenshots, fixtures, or embeds
the credential values or access token. It does not accept them as command-line
values because command histories and process listings may expose them.

## Host and transport controls

- exact URL allowlist;
- HTTPS only;
- port 443 only;
- no userinfo, path, query, or fragment in the base URL;
- TLS verification enabled;
- redirects disabled;
- same-host relative OAuth token path only;
- no OAuth retry;
- limited GET-only retries;
- no PATCH retry.

## Log and evidence controls

Safe exception messages contain operation and HTTP status only. Response
bodies are suppressed. The sanitizer removes Bearer credentials and URLs.
Audit reports use truncated SHA-256 evidence IDs for Batch, Test, Sample, and
reviewer identifiers. Source hashes are retained because they are required
scientific/audit evidence; no source files or customer data are retained.

Real run output is written below ignored `audit/`. Each audit JSON and Markdown
report has a SHA-256 manifest. The local idempotency ledger stores only a
hashed Test evidence key, source hash, timestamp, and audit-manifest reference.

## Fail-closed behavior

Publishing is blocked if any credential, host, schema, identity, membership,
workflow, reviewer, source, destination, formula, atomicity, idempotency, or
rollback prerequisite is unresolved. No configuration option bypasses the
prohibition on Pass/Fail/result fields.

Before any token request, the application requires both a SHA-256-locked,
passing 43-field saved-Sandbox destination proof and an explicitly proven OAuth
token endpoint contract. The current configuration has neither, so API
commands stop before the secrets file is loaded or a token client is created.

The default configuration also rejects any Batch whose display name does not
begin with `SBX_ONLY_`, before worksheet content is processed. This task build
must not be used on ordinary or customer-like Sandbox data.
