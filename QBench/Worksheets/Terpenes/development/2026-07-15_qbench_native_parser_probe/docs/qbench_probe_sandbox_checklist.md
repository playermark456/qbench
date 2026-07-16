# QBench Sandbox checklist

This checklist is for a future separately authorized stage only.

1. Confirm the browser URL is exactly `https://ait-sandbox.qbench.net/`.
2. Confirm the exact authorization phrase and any required Batch name or
   manual-ID decision are present.
3. Confirm the named Batch is disposable and Sandbox-only.
4. Confirm no production record, customer record, or live result is open.
5. Use only the generated artifact assigned to the authorized stage.
6. Keep parser versions draft/inactive unless that stage explicitly permits a
   temporary isolated activation.
7. Use only `Output_redacted_fixture.txt` where a fixture is permitted.
8. Capture sanitized counts, status, and safe property paths/types only.
9. Record every QBench object changed and stop after the single stage.
10. Update the same Draft PR with sanitized evidence.
11. Do not delete evidence until the method owner approves cleanup.

Never use this checklist against `https://ait.qbench.net/`; that is the live
tenant and is read-only/reference-only for this work. Treat all pre-existing
objects in the older Sandbox as non-authoritative until checked against the
GitHub-controlled worksheet candidates, parser code, mappings, and
specifications.

For the future disposable worksheet release: import the JSON, attach it only to
the authorized disposable Batch, confirm the required named cells, verify
formula sentinels and numeric counts, inspect read-only output, and never
promote it to production.
