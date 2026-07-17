# Exact-Test REST API publisher for reviewed Terpenes Batch results

Date: 2026-07-17

Status: **the 43-row underscore scalar candidate is locally valid, but the new
native scalar worksheet failed its saved/reopened Phase 1A gate at 0/7;
paused before approval, activation, runtime instantiation, or the first token
request**.

This package implements a controlled, Sandbox-only publisher for reviewed
Terpenes Batch rows. It routes only by exact QBench Test ID, builds the complete
Batch plan before any write, patches one exact Test Worksheet at a time, and
verifies all mapped values, formulas, and unrelated cells after each write.
It never writes a Test result, Pass/Fail field, full worksheet replacement,
COA, or METRC artifact.

## Current controlled stop

An ignored local secrets file has all three required nonblank keys, and the
base URL passes the exact Sandbox allowlist. No credential value was printed,
logged, or persisted by the publisher. The earlier imported saved/reopened
Sandbox Worksheet definition and raw **Export Spreadsheet** file prove its 43
destinations are structurally present, unique, writable, and non-formula-owned.
That evidence does not prove the exact native runtime contract.

Runtime instantiation is now isolated as an import/schema compatibility
failure, not a general old-Sandbox engine failure. The retained earlier direct
Test and a second Test created normally from the imported Prompt 3 candidate
still display only QBench's blank 5-column by 5-row default. In contrast, the
new UI-built native control in `native_test_worksheet_probe/` instantiated its
exact six-row definition through a fresh Assay-created Test. The exact text and
numeric values persisted, both formulas evaluated correctly, and the sentinel
remained unchanged after save and reopen. Therefore:

- no OAuth token request, QBench API GET, or PATCH was attempted;
- `old_sandbox_test_worksheet_engine` is
  `operational_for_native_definitions`;
- `imported_prompt3_test_worksheet` is `compatibility_failure`;
- the exact native rebuild in `native_43_field_rebuild/` stopped at 4/7
  representative destinations because all three bracketed indexed names were
  rejected by the old-Sandbox native save path;
- `native_minimal_destination_probe_failed` is the current controlled-stop
  classification for the preserved bracket-name attempt;
- `config/field_mapping_scalar_candidate.csv` contains the exact 23 underscore
  analyte names `terpenes_instrument_conc_01` through `_23` plus the unchanged
  20 scalar destinations, and passes the local 43-row candidate validator;
- the separate native scalar worksheet retained its 40x26 grid but zero of
  seven representative named-cell definitions after save, navigation away,
  and reopen from the QBench Worksheet list;
- `native_scalar_minimal_destination_probe_failed` is the current
  controlled-stop classification; its Version 1 remains Draft, was not
  approved or activated, and Version 2 was not created;
- the earlier destination-proof objects and the native Worksheet, two
  versions, Assay, Sample, and Test are inventoried in separate sanitized
  evidence without internal IDs;
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

Current result: 46 unit tests passed. The tests use only synthetic identifiers
and in-memory API behavior; they are not Sandbox success evidence.

## Release checklist for QBench Sandbox

1. Retain the passing saved/reopened 43-field definition proof, the passing
   native Test-instantiation control, and both raw **Export Spreadsheet**
   hashes.
2. Retain `config/field_mapping_scalar_candidate.csv` as an unpromoted
   candidate; do not replace the operational bracketed mapping.
3. Resolve why the old-Sandbox save path reopened the underscore scalar probe
   with zero named cells, then repeat Phase 1A and require 7/7 before
   approving, activating, exporting, or creating an Assay/Sample/Test.
4. Only after Phase 1 passes, create Version 2 and prove the exact 43/43 saved
   definition and fresh runtime instantiation.
5. Add formulas and the complete Prompt 3 layout incrementally, repeating the
   Assay-created Test proof after each stage.
6. Record internal synthetic identifiers only in a local ignored evidence
   file, and update sanitized provenance without those identifiers.
7. Confirm the documented same-host OAuth token path, then lock
   `token_endpoint_contract_proven` and `token_path` in configuration.
8. Supply Sandbox client credentials through the ignored secrets file.
9. Pause for explicit authorization before the first token request.
10. Run `inspect`, then review the sanitized audit.
11. Run the scalar and rollback probe manually as documented.
12. Run the multi-field invalid-field probe and classify atomicity.
13. Keep direct publishing blocked unless the classification is
   `api_patch_atomic`; otherwise stop and design staging-and-commit.
14. Run `dry-run` and review every old/new field value.
15. Publish one fresh synthetic Test, verify, and repeat the dry-run to prove
    `NO CHANGE`.
16. Publish a fresh three-Test synthetic Batch and stop on the first failure.
17. Do not promote to live QBench from this package.
