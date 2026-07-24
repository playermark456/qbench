# Phase 4B.2 Sandbox first import

Status: `parser_sandbox_idempotency_passed`

The prior filename blocker is superseded.

- `artifact_validation_source = phase4b2_validation_report.md`
- `missing_artifact_validation_alias = nonblocking_prompt_filename_mismatch`

## Authorized artifact

- Parser artifact: 47,297 bytes.
- Parser SHA-256:
  `c67cc07c38fa50d46150f8b45de899a8e2a4bdb48db763edee73fc07cdfe849b`.
- Authoritative raw-source SHA-256:
  `bfd88621e2e8ab791e63ba38f07c9a1174f9600e1cf3f28d5b12ffbd08f2eb91`.
- Corrected Batch candidate SHA-256:
  `50fb7883a6932bc54b09f6997b91f01674e392696e82f77872935bb00576acda`.

## Controlled Sandbox execution

- The isolated Sandbox Assay was verified without modification.
- Its exact active Test and Batch Dynamic Spreadsheet versions were verified.
- No specification, protocol, control-group, resource-group, or extra worksheet
  was present.
- Collision checks passed for the two fresh Samples, the fresh Batch, and the
  exact parser name.
- Two fresh Samples and two fresh NOT STARTED Tests were created.
- One fresh Batch was created with only the two fresh Tests and the active
  Batch Version 2 worksheet.
- The ignored runtime TXT was generated from the authoritative raw source.
  Its SHA-256 was
  `3b6fda068e6861995f39ab60ed8a35e4a0a9f2378464fe81db3b88bc725e1b9d`.
- The runtime file differed from the authoritative source on exactly two
  `Sample ID` lines and no other lines.
- Exactly one coded parser object was created:
  `SBX_ONLY_TERPENES_MULTI_RECORD_PARSER_V1`.
- The exact parser source was verified before save at 47,297 bytes and the
  authorized SHA-256, then saved as one draft version and reopened.
- Exactly one runtime file was selected and exactly one Preview/import was
  submitted.
- The parser reported success:
  `Imported records=34 resolved=2 held=13 controls=19`.
- No parser error was reported and no retry or second import occurred.

## Landing validation completed before the controlled stop

- Instrument Import rows 2:35 contained exactly 34 records.
- Rows below the landing were blank in visible upper, middle, and row-201
  checks.
- The 57-column A:BE contract was present.
- All 34 rows contained the expected parser version and a source-row hash.
- The 23 analyte channels remained in the approved order.
- Visible analyte values were numeric or blank.
- AF/AG formula outputs remained active after the parser-owned A:AE and AH:BE
  update.
- AF status totals were Rejected=16, Review Required=8, and Valid=10.
- AG message totals were Sample type required=3, Integration review required=8,
  Import row valid=10, and QBench Test ID required=13.
- The live sample-type mapping matched the source classification baseline:
  Null=3, Blank plus Matrix Blank=3, System Suitability=3, Standard=6, CCV=3,
  LOQ=1, and Sample=15.
- All 34 Dimethylacetamide audit values were retained, including three numeric
  zeroes.
- The unknown-peak total was 138.
- Manual-integration state was retained as `No` for all 34 records.
- Exactly two mapped rows appeared in Test Transfer staging.
- The other thirteen Sample rows remained held and nineteen controls were
  excluded.
- Both mapped rows were correctly held at `Review Required` for staff
  integration review. No staff-controlled field was completed.
- Batch Review showed two populated publish rows, no duplicate Test IDs,
  QC data complete, integration review incomplete, unresolved QC
  configuration/review gates, Batch disposition Hold, and publish ready false.

## List-based persistence confirmation

Task C2E left the Batch page through the normal Batches list without clicking
Save. No unsaved-change warning appeared. The exact Batch was then reopened
from that list.

- `parser_sandbox_first_import = passed`
- `qbench_parser_update_persistence = passed_without_additional_ui_save`
- `manual_batch_save_security_rejection = nonblocking_browser_automation_limitation`

After list-based reopen:

- the exact Batch Version 2 Dynamic Spreadsheet remained attached;
- rows 2:35 still contained the same 34 records in source order;
- visible upper, middle, and row-201 checks below the imported set were blank;
- all 34 stable row keys, source-file hashes, parser-version values, and
  source-row hashes persisted;
- the A:BE contract, A:AE and AH:BE parser ownership, and readonly AF/AG
  computed cells persisted;
- AF/AG retained their prior status/message totals and no `#ERROR`;
- analyte cells retained numeric cell types, numeric zeroes remained zero, and
  blanks remained blank;
- all 23 Terpenes channels remained in approved order;
- Dimethylacetamide remained audit-only, Peak Table audit data persisted, and
  the unknown-peak total remained 138;
- exactly two Sample rows remained mapped, thirteen remained held/unmapped,
  and all nineteen controls remained unlinked and excluded;
- exactly two Test Transfer candidates persisted;
- both candidates retained AZ=false, BA=false, BB=false, BC=false, and neutral
  BD text `Analytical values incomplete`;
- both associated Tests remained NOT STARTED.

At the C2E checkpoint, the blocked Save had never been executed or retried and
no second parser import had occurred. No worksheet edit, Batch-to-Test
transfer, Test worksheet edit, analytical Test write, Pass/Fail, completion,
publication, release, QC Review, METRC action, repository stage, commit, push,
or PR update occurred.

## Task C3 deterministic second import

The ignored runtime source was reverified before the second write:

- runtime SHA-256:
  `3b6fda068e6861995f39ab60ed8a35e4a0a9f2378464fe81db3b88bc725e1b9d`;
- authoritative raw-source SHA-256:
  `bfd88621e2e8ab791e63ba38f07c9a1174f9600e1cf3f28d5b12ffbd08f2eb91`;
- exactly two `Sample ID` lines differed and no other line differed;
- the runtime source remained Git-ignored.

The user explicitly authorized the second import with
`second-import-authorized`. Exactly one additional Preview/import was then
submitted from the same selected runtime file. It completed successfully and
reported `Imported records=34 resolved=2 held=13 controls=19`. There was no
retry, third import, or separate Batch Save.

After navigating away and reopening the Batch:

- the pre- and post-import row counts were both 34;
- populated logical rows remained 2:35;
- all rows 36:201 had blank `import_row_id` values;
- the duplicate logical-row count was zero;
- all 34 ordered stable row keys, source-file hashes, parser versions, and
  source-row hashes exactly matched the pre-import baseline;
- all 782 analytical cells, 34 records by 23 channels, exactly matched the
  baseline and retained native numeric cell types;
- AF and AG retained identical evaluated values and readonly formula ownership
  in all 34 rows;
- the category distribution was unchanged;
- exactly two Samples remained mapped, thirteen Sample rows remained held,
  and nineteen controls remained excluded;
- exactly two Test Transfer candidates remained, with no duplicate Test ID.

`sandbox_parser_idempotency =
passed_deterministic_range_replacement`.

## Task C3 controlled stop

Both mapped Instrument Import rows contained 23 numeric analytical values,
complete source/audit values, 23 reportable compound rows, numeric
Dimethylacetamide, and retained source-row hashes. Both remained
`Review Required` with `Integration review required`.

Test Transfer D:Z therefore remained intentionally gated and blank for both
candidates. Each candidate had zero numeric cells, 23 blank cells, zero text
or error cells, and AZ=`false`. Source/audit and preparation projections also
remained gated. BA and BB were `false`, Batch QC disposition remained `Hold`,
BC was the valid Boolean `false`, and BD was neutral text
`Analytical values incomplete`. All computed gate cells remained readonly and
no `#ERROR` appeared.

The first failing prerequisite was AZ, so BD matched the formula sequence.
The root outstanding work is staff-controlled integration review, final-volume
entry and preparation confirmations, followed by Batch QC disposition. The
parser-populated source fields were present; no parser patch or worksheet
formula patch is indicated.

- `parser_sandbox_idempotency = passed`
- `transfer_staging_classification =
  staff_staging_ready_expected_staff_review_preparation_and_batch_qc_prerequisites`
- `recommended_next_action = staff_staging_ready`

Both associated Tests remained NOT STARTED. No Batch-to-Test write, analytical
Test modification, Pass/Fail, completion, publication, release, QC Review,
third import, cleanup, repository stage, commit, push, or PR update occurred.
