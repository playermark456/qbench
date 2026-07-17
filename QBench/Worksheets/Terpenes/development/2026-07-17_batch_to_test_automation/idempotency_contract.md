# Idempotency contract

Status: required behavior defined; not implementable with the inspected native
automation surface.

## Required state

Each Batch Publish row must persist at least:

- current reviewed `source_row_hash`;
- last successfully published `source_row_hash`;
- matched exact QBench Test ID;
- publish status;
- authorization status, reviewer, and review timestamp;
- publish timestamp or event reference.

The Prompt 3 Test Worksheet has `source_file_hash` but no named cell for the
Prompt 4.5 `source_row_hash`. These hashes are not interchangeable. The Batch
row therefore needs a durable automation-owned last-published hash, or a later
approved Test Worksheet contract must add a dedicated published source-row-hash
field.

## State behavior

| Current state | Required behavior |
|---|---|
| Never published; authorization off | No write; `Not Authorized` |
| Never published; authorized; one exact match; full preflight passes | One atomic input write; persist current hash as last-published hash; `Published` |
| Current hash equals last-published hash | No write; do not create a Test or append values; `Already Published - No Change` |
| Current hash differs after prior publish | No overwrite; set authorization to `Reauthorization Required`; `Source Changed - Review Required` |
| Changed hash explicitly reauthorized | Re-run full source, match, and destination preflight; one controlled replacement of writable inputs only; persist new hash |
| Missing or multiple match | No write and no last-published-hash change |
| Any source or destination validation failure | No partial write and no last-published-hash change |

## Formula preservation

Only the fields enumerated in `automation_mapping.csv` may be replaced. The
automation must not write `Data!D3:Z6`, `Data!B24:B27`, Specifications, Report,
or any report-display/calculated result. Duplicate execution must leave those
formulas byte-for-byte or semantically unchanged.

## Sandbox blocker

The inspected action does not expose:

- one-Test targeting;
- current-versus-last hash comparison;
- row-specific status/hash persistence;
- conditional no-op behavior based on destination state;
- an atomic multi-field write.

Idempotency and changed-source-hash validation were therefore not run. The
Prompt 4.6C duplicate attachment result is input-layer evidence only and is not
evidence of Batch-to-Test publishing idempotency.
