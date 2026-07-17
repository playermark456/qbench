# Sandbox failure and controlled-stop results

No token or Sandbox API request was made. The current pre-token gate stops
because the saved 43-field destination proof and official OAuth endpoint
contract are absent. The credential presence check passed without exposing any
value. Atomicity proof is also absent.

## Destination proof controlled stop

The repository candidate is structurally complete and reports 43 of 43 targets
as writable, but lacks saved/reopened Sandbox provenance. The older active
saved export contains none of the 43 current destinations. Neither result can
produce a passing proof artifact.

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
