# Exact-Test REST API publisher for reviewed Terpenes Batch results

Date: 2026-07-17

Status: **local implementation validated; Sandbox API execution stopped before
the first request**.

This package implements a controlled, Sandbox-only publisher for reviewed
Terpenes Batch rows. It routes only by exact QBench Test ID, builds the complete
Batch plan before any write, patches one exact Test Worksheet at a time, and
verifies all mapped values, formulas, and unrelated cells after each write.
It never writes a Test result, Pass/Fail field, full worksheet replacement,
COA, or METRC artifact.

## Current controlled stop

No `QBENCH_SANDBOX_TOKEN` or `QBENCH_BASE_URL` was present during Prompt 5B.
The actual saved Sandbox Test Worksheet has also not proven all 43 writable
destinations, and the REST representation for the 23-cell analyte range is not
yet proven. Therefore:

- no QBench API GET or PATCH was attempted;
- no Sandbox object was created or modified;
- scalar persistence, rollback, and multi-field atomicity remain unclassified
  in QBench;
- `config/publisher_config.json` intentionally blocks publishing with
  `api_patch_unresolved`, empty expected-workflow identifiers, and
  `destination_contract_proven: false`.

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
- Preflight failures create a sanitized no-plan audit before the CLI exits.
- Local `audit/` and secret files are ignored by Git.

## Commands

Run these commands from this directory after completing the Sandbox prerequisites:

```text
python terpenes_publisher.py inspect --batch-id <synthetic-batch-id>
python terpenes_publisher.py dry-run --batch-id <synthetic-batch-id>
python terpenes_publisher.py publish --batch-id <synthetic-batch-id> --execute
```

Credential loading order:

1. `QBENCH_SANDBOX_TOKEN` environment variable;
2. an ignored local secrets file passed with `--secrets-file`.

The checked-in `.env.example` contains variable names only. Never store a real
token in this directory outside an ignored file.

## Local validation

```text
python -m unittest discover -s tests -v
python validate_prompt_5b_package.py
```

Current result: 34 unit tests passed. The tests use only synthetic identifiers
and in-memory API behavior; they are not Sandbox success evidence.

## Release checklist for QBench Sandbox

1. Create a fresh task-only Terpenes Test Worksheet and Test.
2. Save, reopen, and Export Spreadsheet.
3. Prove all 43 mapping targets are present, unique, writable, non-formula,
   non-Pass/Fail destinations.
4. Record exact synthetic assay, workflow, worksheet, Batch, Sample, and Test
   identifiers in a local ignored evidence file.
5. Supply a Sandbox-only token at runtime.
6. Run `inspect`, then review the sanitized audit.
7. Run the scalar and rollback probe manually as documented.
8. Run the multi-field invalid-field probe and classify atomicity.
9. Keep direct publishing blocked unless the classification is
   `api_patch_atomic`; otherwise stop and design staging-and-commit.
10. Run `dry-run` and review every old/new field value.
11. Publish one fresh synthetic Test, verify, and repeat the dry-run to prove
    `NO CHANGE`.
12. Publish a fresh three-Test synthetic Batch and stop on the first failure.
13. Do not promote to live QBench from this package.
