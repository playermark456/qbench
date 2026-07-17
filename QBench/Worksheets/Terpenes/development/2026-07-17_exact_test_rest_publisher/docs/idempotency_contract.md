# Idempotency and source-hash contract

The controlled source is the reviewed **source-row hash**, not the source-file
hash mapped to `source_file_hash`.

The application binds authorization to
`terpenes_batch_publish_reviewed_source_row_hash` and consults both the Batch
last-published hash and an ignored local ledger keyed by SHA-256 Test evidence
ID.

| State | Action |
|---|---|
| authorization absent | `BLOCKED` |
| reviewed hash differs from current hash | `REAUTHORIZATION REQUIRED` |
| no prior hash, destination blank, full gate passes | `PUBLISH` |
| prior hash equals current hash and all 43 values match | `NO CHANGE`; no PATCH |
| prior hash equals current hash but destination differs | `BLOCKED` |
| prior hash differs from current hash | `REAUTHORIZATION REQUIRED` |
| destination nonblank without trusted prior state | `BLOCKED` |

After verified publish the local ledger records the hashed exact Test ID,
source-row hash, timestamp, and audit reference. It never stores a raw Test ID.

The official Prompt 5B endpoint set does not include a Batch worksheet write,
and the 43-field Test mapping has no committed source-row-hash destination.
Therefore the local ledger is defense-in-depth, not a live-promotion-quality
system of record. Loss of the ledger fails closed when destination fields are
nonblank. A durable QBench-native committed hash remains a promotion gap.

Local synthetic unchanged-hash/no-PATCH and changed-hash/reauthorization tests
passed. Sandbox results were not run.
