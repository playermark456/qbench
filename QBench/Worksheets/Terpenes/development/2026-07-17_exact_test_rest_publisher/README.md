# Exact-Test REST API publisher for reviewed Terpenes Batch results

Date: 2026-07-17

Status: **local client-credential and destination-proof gates validated;
Sandbox API execution paused before the first token request**.

This package implements a controlled, Sandbox-only publisher for reviewed
Terpenes Batch rows. It routes only by exact QBench Test ID, builds the complete
Batch plan before any write, patches one exact Test Worksheet at a time, and
verifies all mapped values, formulas, and unrelated cells after each write.
It never writes a Test result, Pass/Fail field, full worksheet replacement,
COA, or METRC artifact.

## Current controlled stop

An ignored local secrets file now has all three required nonblank keys, and
the base URL passes the exact Sandbox allowlist. No value was printed, logged,
or persisted by the publisher. The actual saved/reopened Sandbox Test
Worksheet has not yet proven all 43 writable destinations. The repository
candidate passes the structural check with 43 of 43 targets writable, but it
has no saved/reopened Sandbox provenance. The active 2026-06-30 saved export
contains none of the 43 current destinations. Therefore:

- no OAuth token request, QBench API GET, or PATCH was attempted;
- no Sandbox object was created or modified;
- scalar persistence, rollback, and multi-field atomicity remain unclassified
  in QBench;
- `config/publisher_config.json` intentionally blocks publishing with
  `destination_contract_proven: false`, no locked destination-proof artifact,
  an unproven OAuth token endpoint, `api_patch_unresolved`, and empty
  expected-workflow identifiers.

Do not change those controls from repository evidence alone. They may be
changed only after the disposable Sandbox probes in `docs/atomicity_results.md`
and the saved Export Spreadsheet checks in `docs/field_mapping.md` pass.

## Safety defaults

- The only accepted base URL is `https://ait-sandbox.qbench.net/`.
- The default command is read-only; `publish` also requires `--execute`.
- Publishing requires the exact phrase
  `PUBLISH REVIEWED TERPENES BATCH <display-name>`.
- GET requests have a timeout and at most two retries.
- PATCH requests have a timeout and are never automatically retried.
- A timeout after PATCH submission is treated as ambiguous, verified by GET,
  rolled back when safe, and stops the Batch.
- Audit files hash Test, Sample, Batch, and reviewer identifiers and never
  include credentials, headers, cookies, signed URLs, or raw API error bodies.
- Client ID and Client Secret are loaded only from `--secrets-file`.
- The OAuth client-credentials response is accepted only as a short-lived
  Bearer token with a lifetime of at most one hour. It remains in memory and is
  never written to disk.
- Destination proof and token-endpoint proof must pass before credential
  loading or token exchange for any API command.
- Preflight failures create a sanitized no-plan audit before the CLI exits.
- Local `audit/` and secret files are ignored by Git.

## Commands

Local-only commands that never request a token:

```text
python terpenes_publisher.py --secrets-file <ignored-local-file> credentials-check
python terpenes_publisher.py prove-destination --worksheet-export <export.json> --provenance <provenance.json> --output <proof.json>
```

The proof output is written only when all 43 targets pass and the export has
valid saved/reopened synthetic-Sandbox provenance.

Run these commands only after completing and locking both pre-token proofs:

```text
python terpenes_publisher.py --secrets-file <ignored-local-file> inspect --batch-id <synthetic-batch-id>
python terpenes_publisher.py --secrets-file <ignored-local-file> dry-run --batch-id <synthetic-batch-id>
python terpenes_publisher.py --secrets-file <ignored-local-file> publish --batch-id <synthetic-batch-id> --execute
```

The checked-in `.env.example` contains only `QBENCH_BASE_URL`,
`QBENCH_CLIENT_ID`, and `QBENCH_CLIENT_SECRET` with blank values. Pass the
exact local filename to `--secrets-file`; never commit that file.

## Local validation

```text
python -m unittest discover -s tests -v
python validate_prompt_5b_package.py
```

Current result: 44 unit tests passed. The tests use only synthetic identifiers
and in-memory API behavior; they are not Sandbox success evidence.

## Release checklist for QBench Sandbox

1. Create a fresh task-only Terpenes Test Worksheet and Test.
2. Save, reopen, and Export Spreadsheet.
3. Prove all 43 mapping targets are present, unique, writable, non-formula,
   non-Pass/Fail destinations.
4. Record exact synthetic assay, workflow, worksheet, Batch, Sample, and Test
   identifiers in a local ignored evidence file.
5. Create the provenance JSON described in
   `docs/destination_contract_results.md` and generate the locked proof.
6. Confirm the documented same-host OAuth token path, then lock
   `token_endpoint_contract_proven` and `token_path` in configuration.
7. Supply Sandbox client credentials through the ignored secrets file.
8. Pause for explicit authorization before the first token request.
9. Run `inspect`, then review the sanitized audit.
10. Run the scalar and rollback probe manually as documented.
11. Run the multi-field invalid-field probe and classify atomicity.
12. Keep direct publishing blocked unless the classification is
   `api_patch_atomic`; otherwise stop and design staging-and-commit.
13. Run `dry-run` and review every old/new field value.
14. Publish one fresh synthetic Test, verify, and repeat the dry-run to prove
    `NO CHANGE`.
15. Publish a fresh three-Test synthetic Batch and stop on the first failure.
16. Do not promote to live QBench from this package.
