# Exact-Test REST API publisher for reviewed Terpenes Batch results

Date: 2026-07-17

Status: **The isolated unqualified-address JSON candidate passed its saved
43/43, raw round-trip, Approved/Active, normal Assay/Test instantiation,
runtime export, representative-value persistence, and restored 43/43 blank
baseline gates. The separately authorized read-only API phase made one OAuth
token POST to the package's same-origin token-path contract; the Sandbox
returned HTTP 404, so no GET or write request occurred**.

This package implements a controlled, Sandbox-only publisher for reviewed
Terpenes Batch rows. It routes only by exact QBench Test ID, builds the complete
Batch plan before any write, patches one exact Test Worksheet at a time, and
verifies all mapped values, formulas, and unrelated cells after each write.
It never writes a Test result, Pass/Fail field, full worksheet replacement,
COA, or METRC artifact.

## Current controlled stop

The prior lock conclusion is superseded by
`approval_attempt_procedural_error_unnecessary_lock_handling`. A worksheet
review lock is not required for approval in this Sandbox, and no administrator,
different account, or QBench support was required. The user manually approved
the exact `JSON Scalar 43 Field Base v1`; Codex verified the same single
Version 1 as Approved/Active and confirmed no Version 2 exists.

The isolated Assay association persisted, a fresh normal Assay-created Test
retained the full 40x26 grid before and after list-based reopen, and the
runtime export exposed all 43 exact destination columns. Five representative
values persisted, B22/B23 stayed blank, and only those five values were
cleared. A final save, leave, and reopen proved all 43 destinations blank.
Therefore
`destination_contract_proven=runtime_instantiation_passed_pending_read_only_api_confirmation`.

The read-only API origin preflight subsequently passed byte-for-byte for
`https://ait-sandbox.qbench.net`. One non-retried token POST to
`/qbench/api/v1/oauth/token` returned HTTP 404 with JSON content. No access
token was returned, persisted, or displayed, and no authenticated GET was
sent. The token path remains unproven; alternative paths were not guessed or
probed. Current API classification:

- `oauth_token_endpoint_404_controlled_stop`
- `read_only_api_identity=not_run_oauth_failed`
- `read_only_api_worksheet_contract=not_run_oauth_failed`
- `analyte_patch_key_contract=unresolved`
- `atomicity_classification=api_patch_unresolved`

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

- exactly one authorized OAuth token POST returned HTTP 404; no GET, PATCH,
  PUT, DELETE, or non-token POST was attempted;
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
  classification for the preserved 0/7 scalar attempt; its Version 1 remains Draft, was not
  approved or activated, and Version 2 was not created;
- the isolated one-cell persistence diagnostic used **Add Named Cell**, real
  keystrokes, Tab/blur events, a unique system name, and a blank writable B2;
  the row was visibly present before Create, but the reopened 6x5 Draft had
  zero named cells and no visible validation message;
- the current version-creation control visibly produced a Draft row, then
  reopened with zero named-cell rows;
- the user subsequently created `sdf` at `A1` in the exact native scalar Draft,
  clicked **Save Draft**, refreshed, and confirmed it persisted; Codex also
  independently reopened that exact Draft and saw `sdf`, a blank Display Name,
  and Exportable enabled;
- QBench native named-cell persistence is therefore `operational`; the earlier
  environment-blocker and support-review conclusions are superseded;
- the Codex row `terpenes_codex_save_control_20260717` at `B2` was visibly
  complete before **Save Draft** but disappeared after refresh and list-based
  reopen while `sdf` remained;
- `codex_named_cell_save_control_failed` is the current controlled-stop
  classification, `browser_control_authoritative=false`, and Probes B/C plus
  all further Codex-controlled worksheet construction remain skipped;
- the native-envelope candidate rendered successfully as a 40x26 grid with 43
  named cells, but **Save As New Version** rejected its sheet-qualified JSON
  cell definitions with `Invalid cell definition Data!D2 for field name
  terpenes_instrument_conc_01`; the error was never an A2 address;
- the logical first-analyte mapping is `Data!D2`, the old-Sandbox JSON cell is
  `D2`, and no A2 destination exists; compatibility evidence from `sdf -> A1`
  and the active one-tab Terpenes export establishes that legacy JSON cells
  must be unqualified;
- `json_import_rebuild/` now keeps the logical mapping sheet-qualified while
  serializing exactly 43 unqualified scalar cells such as `D2`;
- comparison against the successfully rendered candidate proves exactly 43
  address-string changes and no grid, anchor, metadata, UUID, or content
  changes;
- the regenerated candidate passed local validation with SHA-256
  `e5ef20a5cec574dc292ed679867e01313233c92ceda9ef863bf98dd8d4485b80`;
- the user imported the corrected candidate into the exact isolated Sandbox
  Worksheet, saved `JSON Scalar 43 Field Base v1`, and manually approved it;
  Codex verified the exact single Version 1 as Approved/Active;
- browser verification before refresh and after list-based reopen proved the
  exact title and breadcrumb, 40x26 grid, 28 anchors, and all 43 unqualified,
  blank, writable, unique, non-formula, exportable destinations;
- the raw saved/reopened Export Spreadsheet SHA-256 is
  `3589f2ace8afb96db96d4da638e9effc86bda404e03f97b85fca0e43aa349912`;
  semantic comparison passed after normalizing only QBench's regenerated
  renderer UUID;
- `json_import_saved_definition_contract=passed_43_of_43`,
  `json_import_round_trip=passed`,
  `runtime_test_worksheet_contract=passed_43_of_43`, and
  `destination_contract_proven=runtime_instantiation_passed_pending_read_only_api_confirmation`;
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

- The only accepted base URL is `https://ait-sandbox.qbench.net`.
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
3. Retain the exact Approved/Active Version 1, saved round trip, runtime CSV
   hash, and final 43/43 blank Test baseline. Do not upload another candidate,
   create Version 2, or edit the proven definition.
4. Retain the direct-approval correction: future Sandbox worksheet approvals
   must use the normal Approve action without creating or depending on a lock.
5. Add formulas or the complete Prompt 3 layout only in a separately
   authorized version and repeat the Assay-created Test proof after each stage.
8. Record internal synthetic identifiers only in a local ignored evidence
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
