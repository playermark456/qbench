# Sandbox failure and controlled-stop results

No Sandbox API request was made. The runtime attempt stopped before request
because no Sandbox credential was available. Destination and atomicity proofs
were also absent.

## Required failure cases exercised locally

| Case | Local result |
|---|---|
| Batch not found | safe error; no PATCH |
| Test not found | `BLOCKED` |
| Test not in selected Batch | `BLOCKED` |
| duplicate Test ID in Publish | complete plan blocked |
| missing Test ID | row retained and blocked |
| missing source hash | blocked |
| authorization off | blocked |
| Import AF rejected | blocked |
| Import AG invalid | blocked |
| non-numeric analyte | blocked |
| incorrect counts | blocked |
| missing destination named cell | blocked |
| formula-owned destination | blocked |
| GET timeout | limited retries, sanitized error |
| timeout after PATCH submission | no retry, verify, rollback, stop |
| HTTP error | status-only sanitized error |
| success response with failed persistence | rollback, stop |
| changed source hash | `REAUTHORIZATION REQUIRED` |
| unchanged duplicate publish | `NO CHANGE`, no PATCH |
| later Test fails after prior success | prior success recorded; Batch stops |

Additional local checks reject Pass/Fail/result fields, formula-like input,
alternate hosts, missing runtime approvals, and unrelated-cell mutation.

Sandbox classification for every PATCH-dependent case remains **not run**.
