# Prompt 4.6 staged authorization plan

Only Stage 0 is authorized by initial submission. Each later stage requires
the exact phrase below and ends with an immediate stop, sanitized evidence
update, QBench-object change list, observed result, and next authorization.

| Stage | Purpose | Exact authorization |
|---|---|---|
| 1 | No-write runtime Preview | `AUTHORIZE STAGE 1 — NO-WRITE QBENCH RUNTIME PREVIEW` |
| 2A | Read-only Batch-context Preview | `AUTHORIZE STAGE 2A — READ-ONLY BATCH-CONTEXT PREVIEW` |
| 2B | Optional temporary attachment-trigger context test | `AUTHORIZE STAGE 2B — TEMPORARY SANDBOX ATTACHMENT TRIGGER — BATCH: <EXACT DISPOSABLE SANDBOX BATCH NAME>` |
| 3 | Disposable scalar patch | `AUTHORIZE STAGE 3 — DISPOSABLE SCALAR PATCH — BATCH: <EXACT DISPOSABLE SANDBOX BATCH NAME> — MANUAL SANDBOX BATCH ID: ALLOWED|NOT ALLOWED` |
| 4 | Disposable range patch | `AUTHORIZE STAGE 4 — DISPOSABLE RANGE PATCH` |
| 5 | Disposable two-block patch | `AUTHORIZE STAGE 5 — DISPOSABLE TWO-BLOCK PATCH` |
| 6 | Disposable failure and rollback probe | `AUTHORIZE STAGE 6 — DISPOSABLE FAILURE AND ROLLBACK PROBE` |
| 7 | Redacted Terpenes fixture patch | `AUTHORIZE STAGE 7 — TERPENES REDACTED FIXTURE PATCH PROBE — BATCH: <EXACT DISPOSABLE TERPENES SANDBOX BATCH NAME>` |
| 8 | Finalize sanitized repository package | `AUTHORIZE STAGE 8 — FINALIZE PROMPT 4.6 REPOSITORY PACKAGE` |

General language such as “continue” does not authorize a live stage. A Batch
name or manual-ID decision may not be omitted where the phrase requires it.

All live activity is limited to `https://ait.qbench.net`. Production tenants,
records, samples, results, credentials, session data, direct HTTP writes,
request replay, and arbitrary API calls are permanently out of scope.
