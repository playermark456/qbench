# Security model

## Credential boundary

The application accepts a Sandbox-only token from
`QBENCH_SANDBOX_TOKEN` or an ignored local secrets file. The sample environment
file contains variable names only. Root `.gitignore` patterns were added before
the runtime environment was checked for a credential.

The application never returns, prints, logs, screenshots, fixtures, or embeds
the token. It does not accept a token as a command-line argument because
command histories and process listings may expose it.

Windows Credential Manager is an acceptable operator-managed alternative, but
this implementation does not retrieve from it directly. An operator may load
the token into the environment immediately before running the process.

## Host and transport controls

- exact URL allowlist;
- HTTPS only;
- port 443 only;
- no userinfo, path, query, or fragment in the base URL;
- TLS verification enabled;
- redirects disabled;
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

The default configuration also rejects any Batch whose display name does not
begin with `SBX_ONLY_`, before worksheet content is processed. This task build
must not be used on ordinary or customer-like Sandbox data.
