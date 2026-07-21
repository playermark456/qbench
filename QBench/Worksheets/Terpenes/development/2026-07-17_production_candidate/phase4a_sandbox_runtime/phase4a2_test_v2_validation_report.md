# Phase 4A.2 Test v2 validation report

Date: 2026-07-21

## Final classification

`test_v2_round_trip_passed_with_expected_qbench_normalization`

The v2 candidate passed exact-hash, collision, static-render, named-definition, save, Draft-row, list-reopen, visual persistence, and revised semantic round-trip gates. Phase 4A.3 established that QBench's editor-minimum, viewport, and evaluated top-level formula-cache changes are expected serialization normalizations when the authoritative embedded worksheet model remains exact.

## Gate results

| Gate | Result |
| --- | --- |
| Exact Sandbox origin | passed: `https://ait-sandbox.qbench.net` on every controlled page |
| Exact-name v2 collision search | passed: absent before creation |
| Failed v1 shell untouched | passed |
| Candidate SHA-256 | passed: `7aa7469ec7767a7c7b4b0aa40194e927244adc3278999e23151f4eeb134dd5a4` |
| Static tabs and order | passed: Report, Data, Specifications |
| Visible dimensions | passed: 23x5, 40x26, 23x21 |
| Report contract | passed |
| Data contract | passed |
| Specifications contract | passed |
| Representative formula presence | passed in exact candidate, rendered states, and saved embedded worksheet data |
| Named definitions | passed: 43 destinations plus `report_results`; 44 total |
| `report_results` | passed: `Report!A1:E23` |
| Save as inactive Draft | passed; visible Draft row existed |
| Reopen from Worksheets list | passed; visible layout and configuration persisted |
| Raw re-export preservation | passed; ignored exact bytes, SHA-256 `cf479247be1271d4e8559bb6991d9869a9b6c1324c83c32b227d68d42e7ef127` |
| Semantic round trip | passed with expected QBench normalization; authoritative embedded formulas remained 309/309 exact |

## Safety result

- No production QBench page or QBench API was accessed.
- No OAuth flow or token was used.
- The failed v1 shell and both local candidate JSON files remained unchanged.
- No version was approved or activated, and no assay was assigned.
- No Assay, Sample, Test, Batch, parser, or Key/Value Store fixture was created or changed.
- No customer record was opened.
- Nothing was published, marked QC Review, or assigned Pass/Fail.
- No username, internal numeric QBench identifier, raw export, cookie, token, signed URL, unredacted screenshot, or customer information is tracked.

The saved-definition gate is open for the separately authorized isolated Phase 4A.3 runtime proof. The local v2 candidate remains unchanged.
