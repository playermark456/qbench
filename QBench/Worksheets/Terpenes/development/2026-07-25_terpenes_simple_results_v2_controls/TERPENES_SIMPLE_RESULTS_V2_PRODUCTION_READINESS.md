# Terpenes Simple Results V2 Controls — Production-Readiness Audit

Date: 2026-07-25  
Audit mode: local implementation evidence plus read-only Sandbox reconciliation  
Final status: `PRODUCTION_IMPORT_LAYER_R2_READY_FOR_GIT`

## Executive decision

The earlier `PRODUCTION_IMPORT_LAYER_READY_FOR_GIT` decision applied to parser 43 Version 1, artifact SHA-256 `1c3b0badb33acee3152da95aa40fb8c4332aa465fd1733789456293e0a6c7189`, and Sandbox job 69. That evidence remains valid historical evidence, but the decision is superseded for the current local candidate.

Terpenes Simple Results V2 Controls revision `terpenes-simple-results-parser-v2-controls-r2` is locally validated as a corrected **Batch import and complete-run audit layer**. Revision r2 adds strict Results Test-context reconciliation, distinct physical-row enforcement, exact-byte source hashing, UTF-8 BOM rejection, and fatal UTF-8 validation. Its one controlled BATCH-65 Sandbox proof passed on 2026-07-27. After two failed automated quarantine Save attempts, the user completed one manual Save and Codex directly verified the exact inert configuration, unchanged proof objects, and no job 71. Revision r2 is now ready for the scoped Git follow-up as the import/audit layer only.

The one-tab Batch worksheet, focused tests, and historical controlled Sandbox execution establish the retained import boundary:

- one LabSolutions `.txt` input;
- strict parsing and validation of all 34 complete records;
- exactly 23 reportable terpene channels plus audit-only Dimethylacetamide;
- exactly two Sample records mapped by `Sample Information > Sample ID` to the matching QBench Test display IDs;
- all 34 records preserved in source order in the fixed Run Records audit area;
- one `QBBatchService` construction;
- one Results-only Batch update;
- exact read-after-write verification before success;
- no Test service, direct Test result write, status mutation, approval mutation, COA action, or METRC action.

Revision r2 may remain under Draft review. Its next boundary is the scoped 10-path Git follow-up, push, and additive Draft PR #14 comment. This readiness decision does **not** authorize Production deployment and does not classify the complete Terpenes review/release workflow as production-ready.

The following remain separate scopes:

1. analytical QC evaluation and staff disposition;
2. controlled individual-Test persistence, if required;
3. Test worksheet calculation/report presentation;
4. COA rendering;
5. METRC/profile-specific export.

The Batch Results worksheet is sufficient for the current import/audit phase. If the initial Production phase is intentionally limited to importing and reviewing the Batch/run record in QBench, the downstream scopes are not blockers to committing this implementation. They become deployment blockers before any workflow promises reviewed Test results, COA output, or METRC output.

## Evidence inspected

### Governing instructions and current state

- repository `AGENTS.md`;
- `QBench/Worksheets/Terpenes/AGENTS.md`;
- `QBench/Worksheets/Terpenes/TERPENES_CURRENT_STATE.md`;
- the local production-readiness prompt;
- `QBench/Worksheets/Terpenes/README.md`.

### V2 implementation and evidence

- `development/2026-07-25_terpenes_simple_results_v2_controls/src/terpenes_simple_results_parser_v2_controls.js`;
- `development/2026-07-25_terpenes_simple_results_v2_controls/scripts/build_terpenes_simple_results_parser_v2_controls.js`;
- `development/2026-07-25_terpenes_simple_results_v2_controls/dist/terpenes_simple_results_parser_v2_controls.js`;
- `development/2026-07-25_terpenes_simple_results_v2_controls/tests/test_terpenes_simple_results_parser_v2_controls.js`;
- `development/2026-07-25_terpenes_simple_results_v2_controls/TERPENES_SIMPLE_RESULTS_V2_CONTROLS_SPEC.md`;
- `development/2026-07-25_terpenes_simple_results_v2_controls/TERPENES_SIMPLE_RESULTS_V2_CONTROLS_VALIDATION.md`;
- `development/2026-07-25_terpenes_simple_results_v2_controls/SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V2_CONTROLS.json`;
- both V2 runtime fixtures.

### V1 regression dependencies

- the V1 parser source, builder, artifact, focused test, specification, validation record, original worksheet candidate, corrected worksheet candidate, and 310/311 runtime fixture under `development/2026-07-25_terpenes_simple_results_v1`.

### Analytical, QC, Test, report, and METRC evidence

- `source/labsolutions_ascii_integration_spec.md`;
- `source/terpenes_worksheet_spec_v3.json`;
- `development/2026-07-14_config_parser_foundation/config/terpenes_qc.json`;
- `development/2026-07-14_batch_worksheet_candidate/config/terpenes_batch_import_contract.json`;
- active Terpenes Test worksheet export `terpenes__terpenes_test_ws_id_42__worksheet_export_spreadsheet__active__2026-06-30.json`;
- `development/2026-07-17_production_candidate/production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v4_binding_fix.json`;
- `development/2026-07-17_production_candidate/terpenes_deployment_contract.json`;
- `development/2026-07-17_production_candidate/live_reference_report_patterns.md`;
- the Phase 4A runtime/report and Phase 4B2 parser validation/Sandbox records;
- `QBench/ASSAY_ID_MAP.md`;
- `QBench/NAMED_CELL_INDEX.md`;
- `QBench/REPORT_RENDERING_MAP.md`;
- `QBench/AUTOMATION_INDEX.md`;
- `QBench/FILE_PARSER_INDEX.md`.

### Downstream persistence evidence

- the README, automation configuration, matching contract, idempotency contract, publish gate, success/failure results, and promotion-gap analysis under `development/2026-07-17_batch_to_test_automation`;
- the architecture, destination, atomicity, idempotency, security, rollback, publish-gate, and live-gap evidence under `development/2026-07-17_exact_test_rest_publisher`.

### Potency reference

- local `Potency parser.txt`, SHA-256 `61f91070e0b68b5c5c06de580efe0569d13075a032441968e9d43bec763c1d9e`;
- local `Cannabinoid Potency [Batch] Worksheet.json`, SHA-256 `f0af97d253a4ccca2d6fe577bb9eafd8ade3e305cf4b1257cfe7cbe149552f65`;
- local `Output (1).csv`, 155,634 bytes, SHA-256 `f4cb8e8d2d7008f7b2507378554dfa8cbff5bcdf166d00cde0747b3e9677cbdf`;
- repository active Cannabinoid Potency Batch worksheet ID 7 and Test worksheet ID 8 exports.

The Potency parser and Batch worksheet confirm the useful architectural boundary: a single parser-owned `Results` worksheet and a single Batch update. V2 deliberately strengthens that reference with closed candidate resolution, strict one-Batch cardinality, targeted ownership, full-run audit capture, and verified readback.

## Frozen baseline

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| V2 parser source | 48,889 | `374a0d6722c90a51abaea02a4989fc6927b212a66bcb45090158e1ea4ddab77d` |
| V2 builder | 5,379 | `81f1ac86d044605383e40a7aba4db2b0c44af28e57236fd0a411d857d911e3ba` |
| V2 browser artifact | 49,031 | `1c3b0badb33acee3152da95aa40fb8c4332aa465fd1733789456293e0a6c7189` |
| V2 worksheet candidate | 1,652,216 | `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3` |
| V2 focused test | 65,088 | `70adf74f1170e2e63bb899483129f34c2a43a73059a70d40a701ec07e5b8b218` |
| V2 specification | 6,850 | `b0de9ea38a13f0dc49b24bb156fea936e17c68da0ec31e87d2d356ef26a7afb5` |
| V2 validation record | 17,455 | `2b56aacbe8bb2e5a65b32e31d749ee7ee1580dcad09b91e42838d016e15aa338` |
| V2 310/311 regression input | 286,204 | `1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e` |
| V2 312/313 Sandbox-proof input | 286,204 | `6b6a208faa83a16e54aa7168467d2221fa23db8f8c6c8a82d183f2bb235ce2a7` |

Frozen QBench proof objects remain diagnostic evidence:

- V1 parser 42, worksheet 79, BATCH-62, and job 68;
- V2 parser 43, worksheet 80, BATCH-63, attachment 58, asset 78, and job 69;
- earlier parser 41, job 65, worksheet 78, BATCH-61, Tests 308/309, and attachment 53 remain protected diagnostic artifacts.

## Local validation repeated for this audit

Commands were run directly from:

`QBench\Worksheets\Terpenes\development\2026-07-25_terpenes_simple_results_v2_controls`

```text
node ..\2026-07-25_terpenes_simple_results_v1\tests\test_terpenes_simple_results_parser.js
```

Result: 97 total, 97 passed, 0 failed, 0 skipped.

```text
node tests\test_terpenes_simple_results_parser_v2_controls.js
```

Result: 123 total, 123 passed, 0 failed, 0 skipped.

`node --check` also passed for the V2 source, browser artifact, builder, and focused test. The V2 and repository Potency Batch worksheet JSON files parsed successfully. No build, dependency installation, formatter, coverage run, snapshot generation, or repository-wide test occurred.

## Answers to the production-readiness questions

### 1. Is V2 complete as a production Batch import and run-audit layer?

Yes.

The implementation is complete for the defined non-publishing import boundary:

- exactly one worksheet named `Results`;
- exact dimensions A:AY and rows 1:190;
- dynamic Test area rows 2:87;
- fixed Run Records audit area rows 91:190;
- strict one-file, complete-record, section, numeric, compound-count, controlled-analyte, candidate-ID, Test-resolution, one-Batch, worksheet, header, row-cardinality, and readback validation;
- dynamic Sample writes only for Sample records with a nonblank Sample ID;
- control and validation records validated and persisted only in Run Records;
- one Results-only Batch update and one verified readback.

The successful Sandbox proof establishes persistence behavior in QBench Sandbox for the exact frozen artifact and worksheet. It does not establish QC acceptance, release approval, Test-result publication, COA output, or METRC output.

### 2. Does any current requirement require the parser itself to write individual QBench Test results?

No.

The controlling Simple Results requirements explicitly prohibit a Test service, direct Test result write, and Test status/completion/approval/review mutation. The current V2 parser meets that boundary. Existing Test worksheet, COA, and METRC requirements describe downstream consumers; they do not require the file parser itself to become that publisher.

Adding Test writes to this parser would combine validated import persistence with a separate, unproven release boundary and would invalidate the one-Batch-update architecture.

### 3. If results must reach COAs or METRC, what should perform that step?

Use a separately validated QBench-native Batch-to-Test workflow after Batch review. The repository’s intended native pattern is QBench’s Batch automation action that sets values on Test worksheets within the Batch, with each Test resolving its own source row by exact display ID—for example, a controlled `VLOOKUP({{test.id}}, …)` against the Batch Results table—then writing only approved destination named cells on the Test worksheet.

That downstream workflow is not yet production-qualified. Earlier evidence shows that the proposed one-field destination named-cell probe did not persist as required, and exact routing, complete field cardinality, atomicity, idempotency, and rollback still require a new isolated proof. The exact REST publisher is also not a qualified Production alternative because its live API, credential, atomicity, and operational contracts remain unresolved.

Therefore:

- for import/audit-only deployment, no Test publisher is required;
- before promising COA or METRC output, the smallest separate implementation is an exact-Test-ID QBench-native publisher into the validated Terpenes Test worksheet contract, with an independent Sandbox proof and release gate;
- the V2 parser must remain unchanged.

### 4. Which V2 columns are operational, audit-only, or reviewer-owned?

The exact A:AY schema is:

`Sample ID`, `Test ID`, `Product Matrix`, `LabSolutions Sample Name`, `Sample Type`, `Vial`, `Sample Amount`, `Dilution Factor`, `DF Application Mode`, `α-Pinene`, `Camphene`, `β-Myrcene`, `(-)-β-pinene`, `Delta-3-carene`, `α-Terpinene`, `cis-Ocimene`, `d-Limonene`, `p-Cymene`, `trans-Ocimene`, `Eucalyptol`, `γ-Terpinene`, `Terpinolene`, `Linalool`, `(-)-Isopulegol`, `Geraniol`, `β-Caryophyllene`, `α-Humulene`, `cis-Nerolidol`, `trans-Nerolidol`, `(-)-Guaiol`, `Caryophyllene Oxide`, `(-)-α-Bisabolol`, `Dimethylacetamide`, `Unknown Peak Count`, `Manual Integration`, `Integration Review Status`, `Source Instrument File`, `Source File Hash`, `Source Data File`, `Source Method File`, `Source Sequence File`, `Acquired At`, `Instrument Name`, `Detector ID`, `Detector Name`, `Parser Version`, `Compound Result Row Count`, `Peak Table Row Count`, `Reportable Compound Row Count`, `Source Row Hash`, `Import Status`.

| Columns | Classification | Ownership and use |
| --- | --- | --- |
| A:C | QBench operational context | QBench/dynamic context owns Sample ID, Test ID, and Product Matrix. Parser preserves them. |
| D:I | operational source/preparation context | Parser-owned identity, category, vial, sample amount, dilution factor, and DF application mode for matched Sample rows. These are imported facts, not review decisions. |
| J:AF | operational analytical result channels | The controlled 23 LabSolutions `Conc.` values. These are imported instrument concentrations, not final reviewed `%`/`mg/g` or regulatory disposition. |
| AG | audit only | Dimethylacetamide internal/audit channel; never reportable as a terpene. |
| AH:AI | audit and review-routing evidence | Unknown Peak Count and Manual Integration are parser-derived evidence requiring defined review policy. |
| AJ | parser-owned review-routing literal | Currently `Review Required` or `Not Reviewed`; it is not a reviewer signature, completed review, approval, or disposition. |
| AK:AX | provenance/audit | Instrument/source files, file and row hashes, acquisition/instrument metadata, parser version, and source-table row counts. |
| AY | import audit status | Parser-written literal `Imported`; not publish approval or regulatory disposition. |

No V2 column is a staff-owned approval field. The entire audit region A:AY on rows 91:190 is parser-owned. Future reviewer identity, review timestamp, rationale, QC evaluations, Batch disposition, and publish-ready fields must live in a separately designed review area or downstream review worksheet, not be overloaded into V2 parser-owned cells.

### 5. What review or acceptance rules are still missing?

The repository contains draft criteria, not a complete approved operational policy.

| Record/evidence | Draft evidence already present | Missing approved rule before release use |
| --- | --- | --- |
| Blank and Null | draft blank maximum `0.2 × LOQ` | distinguish Null, solvent Blank, sequence blank, and carryover blank; analyte scope; preceding-injection handling; response to failure; whether the first and terminal blanks have different purposes |
| System Suitability | draft retention-time drift ±0.5 min and resolution ≥1.0 | required injections/order; target peaks; response/area and replicate precision; calculation source; failure/reinjection rules; effect on the sequence |
| Standards | draft calibration correlation `r ≥ 0.99` | required levels/range; model and weighting; back-calculated accuracy; allowed exclusions; recalibration criteria; curve review and approval |
| CCV | initial accuracy ±15% and RSD ≤10%; unresolved bracket criterion | settle ±10% SOP text versus ±15% analysis-form conflict; cadence; which analytes must pass; bracketing logic; trend handling; sequence rejection/reanalysis consequences |
| LOQ | draft recovery 70–130% | number of replicates; precision criterion; analyte coverage; preparation requirements; acceptance aggregation; failed-analyte consequences |
| Matrix Blank | no final approved matrix-specific rule | contamination/interference threshold; whether `0.2 × LOQ` applies; analyte scope; carryover distinction; action on failure |
| Validation Low/Medium/High | categories and levels are retained in audit | recovery and precision criteria by level; required replicate count; allowed exclusions; whether records are method-validation-only or routine Batch acceptance controls; failure consequences |
| Manual Integration | detection only | required reason; before/after evidence; analyst identity; second-person reviewer; review timestamp; permitted integration changes; completion state before Batch disposition |
| Unknown Peaks | count only | significance threshold by area/height/concentration; retention-time handling; identification/escalation; allowable count; review evidence; effect on Batch disposition |

Additional release decisions still needed include the authoritative LabSolutions `Conc.` unit and dilution-factor treatment, final sample-preparation mass/volume authority, the CCV conflict, and the profile-specific METRC mapping/unit exceptions already documented.

Terpenes remains quantitative-only. These rules must not create analyte, Sample, COA, METRC, label-claim, or key-value-store pass/fail outputs. Internal QC language should use `within_criteria`, `outside_criteria`, and `review_required`, with Batch disposition limited to `Accepted`, `Hold`, or `Rejected`.

### 6. Where should review rules live?

Use four deliberately separated mechanisms:

1. **Objective formulas in a future review area:** deterministic calculations such as percent recovery, RSD, retention-time drift, resolution, blank-to-LOQ comparison, completeness, and proposed within/outside criteria. Keep these outside the parser-owned V2 range and do not make the parser depend on their same-update calculation.
2. **Staff-owned review fields:** integration rationale, unknown-peak assessment, analyst/reviewer identity, review timestamps, documented exceptions, and final Batch QC disposition.
3. **QBench automations:** notifications, task routing, and publish gating after the required fields and staff disposition exist. Automations should not invent analytical acceptance or repair parser results.
4. **Separately validated downstream process:** individual-Test persistence, Test worksheet calculations, COA rendering, and METRC/profile export.

The future review/release layer must use `publish_ready` only when Batch disposition is `Accepted` and all required analytical and audit fields are complete. It must not add a `pass_fail` field.

### 7. What production filename rule should replace the exact Sandbox filename?

Recommended QBench parser configuration:

- Trigger: `When file is added to Batch attachments`
- Filename Should: `Start With`
- Filename Text: `TERPENES_LABSOLUTIONS_`

Required laboratory filename convention:

```text
TERPENES_LABSOLUTIONS_YYYYMMDD_<sequence-id>.txt
```

Example:

```text
TERPENES_LABSOLUTIONS_20260725_GCFID01_RUN01.txt
```

The reserved, uppercase prefix scopes the trigger without hardcoding a single runtime fixture. The parser independently enforces exactly one selected `.txt` source. The SOP should restrict `<sequence-id>` to letters, digits, hyphen, and underscore; prohibit customer names and free text; require uniqueness; and require the file to be attached only to the intended Terpenes Batch.

The QBench UI’s exact visible operator label is `Start With`; `Equal`, `End With`, and `Contain` are also documented as available, but are not recommended for the Production convention.

### 8. What LabSolutions convention must bind the correct Test ID?

For every reportable Sample injection:

- `Sample Information > Sample ID` must be the exact QBench **Test display ID**;
- the value is treated as a trimmed string;
- no Sample display ID, Batch display ID, customer identifier, prefix, suffix, decoration, or locally assigned sequence number is allowed;
- leading zeros may be used only when they are part of the actual QBench Test display ID;
- each candidate Test display ID must occur once in the file;
- all candidate Tests must already exist, belong to exactly one Batch, belong to the same Batch, and appear exactly once in column B of that Batch’s Results worksheet.

`Sample Information > Sample Name` remains the LabSolutions run name such as P1/P2; it is not the Test-ID binding field.

Control and validation records must use the approved LabSolutions category/sample-type convention and must not carry a QBench Test display ID. They remain validated and audit-only.

### 9. Is rerunning the parser intended, prohibited, or controlled?

Allowed only as a **controlled replacement**. It is not a routine duplicate-upload workflow.

The operator must:

- document the replacement reason;
- verify the Batch, attachment, Test set, and filename before upload;
- retain the earlier attachment and parser job as audit evidence;
- compare the new source hash to the earlier source hash;
- obtain the required review authorization when the hash changes;
- permit one attachment upload and one parser job;
- stop without retry if the upload/job receipt or terminal state is ambiguous;
- complete post-run Batch/run review before any downstream publication.

An unchanged duplicate input should normally be rejected operationally because it creates another persistent attachment and job without adding analytical information.

### 10. Are targeted stale clearing and readback sufficient for controlled reruns?

They are sufficient at the **technical parser layer**:

- all D:AY cells on each matched dynamic Test row are set, including explicit blanks;
- unmatched dynamic rows are preserved byte-for-byte;
- current audit records are rewritten deterministically in source order;
- only nonblank unused audit-capacity cells are cleared;
- A:C, headers, section labels, formulas, images, and dollar references are protected;
- readback verifies every staged cell, blank audit tail, unchanged context, unchanged unmatched rows, exact candidate count, and exact maps;
- failure emits `RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED`;
- no repair update or retry is attempted.

Readback does not replace the operational rerun controls above. V2 does not keep an approval ledger, compare the prior approved source hash, prevent duplicate attachments, record a replacement reason, or authorize changed analytical content.

### 11. What Production objects eventually need to be created or changed?

| Object/configuration | Import/audit phase | Later review/release phase |
| --- | --- | --- |
| Batch worksheet | Create a new Production-named dynamic Batch worksheet from the exact V2 candidate; do not overwrite Sandbox worksheet 80 or earlier worksheet 78 | Add a separate review area/workflow only after approved QC design; do not change V2 parser ownership |
| Code File Parser | Create a new Production Terpenes parser record | No Test-write capability should be added |
| Parser version | Upload the exact artifact hash as a new version; approve/activate only under a separately authorized Production change | Version any later parser corrections independently |
| Assay configuration | Bind to the verified Production Terpenes assay; repository mapping identifies Terpenes assay ID 8, but the tenant value must be revalidated before mutation | Add review/publish automations only after validation |
| Trigger | `When file is added to Batch attachments` | unchanged |
| Filename rule | `Start With` / `TERPENES_LABSOLUTIONS_` | unchanged unless a formal naming-policy version is approved |
| Batch worksheet assignment | Configure the new worksheet for new Production Terpenes Batches through the approved assay/Batch assignment procedure; do not silently retrofit existing Batches | define migration only if explicitly approved |
| Automation | none required for import/audit-only operation | separately validated QC notification/gating and exact-Test-ID Batch-to-Test publisher |
| Test worksheet | no change for import/audit-only operation | deploy the validated Test worksheet/report contract if COA/METRC is required |
| Report/COA | no change for import/audit-only operation | render the Test worksheet `report_results` range after exact Test persistence; preserve quantitative-only behavior |
| METRC/export | no change for import/audit-only operation | separately validate profile-specific units, Ocimene/Nerolidol rollups, p-Cymene mapping, missing analytes, below-LOQ behavior, and accepted-Batch gate |

Production object creation, activation, assignment, or configuration remains a separately authorized change. This local audit performed none of those actions.

### 12. What is the safest rollback plan?

1. Deploy as new, versioned Production objects; preserve current Production objects and their active versions.
2. Begin with a limited pilot Batch and no automatic Test publication.
3. If preflight fails before an attachment is uploaded, leave the new parser trigger inactive/unset and restore the prior Batch worksheet assignment for future Batches.
4. If an attachment triggers an incorrect import, disable the new trigger/parser for further inputs, preserve the attachment/job/worksheet evidence, place the Batch on Hold operationally, and do not delete or blanket-clear audit data.
5. Correct through a newly approved parser/worksheet version and either a fresh pilot Batch or one documented controlled replacement.
6. Never repair a readback failure with an untracked second update.
7. Because V2 performs no Test, COA, status, or METRC writes, the import-layer rollback requires no Test-result rollback. Any later publisher must have its own snapshot, idempotency, and rollback contract.

### 13. Exact PR #14 file allowlist

The following is the exact 21-path repository allowlist for the Simple Results lineage and this audit. Files already present on the branch remain part of the review scope; no inference is made about Git status because Git was not accessed.

#### Scoped line-ending rule

- `QBench/Worksheets/Terpenes/development/.gitattributes`

#### Authoritative state

- `QBench/Worksheets/Terpenes/TERPENES_CURRENT_STATE.md`

#### V1 foundation and reproducible regression evidence

- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v1/src/terpenes_simple_results_parser.js`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v1/scripts/build_terpenes_simple_results_parser.js`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v1/dist/terpenes_simple_results_parser_v1.js`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v1/tests/test_terpenes_simple_results_parser.js`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v1/TERPENES_SIMPLE_RESULTS_V1_SPEC.md`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v1/TERPENES_SIMPLE_RESULTS_V1_VALIDATION.md`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v1/SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1.json`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v1/SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1__dimension_fix.json`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v1/runtime/terpenes_simple_results_310_311_runtime_source.txt`

#### V2 production import-layer candidate and evidence

- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls/src/terpenes_simple_results_parser_v2_controls.js`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls/scripts/build_terpenes_simple_results_parser_v2_controls.js`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls/dist/terpenes_simple_results_parser_v2_controls.js`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls/tests/test_terpenes_simple_results_parser_v2_controls.js`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls/TERPENES_SIMPLE_RESULTS_V2_CONTROLS_SPEC.md`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls/TERPENES_SIMPLE_RESULTS_V2_CONTROLS_VALIDATION.md`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls/TERPENES_SIMPLE_RESULTS_V2_PRODUCTION_READINESS.md`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls/SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V2_CONTROLS.json`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls/runtime/terpenes_simple_results_310_311_runtime_source.txt`
- `QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls/runtime/terpenes_simple_results_v2_controls_312_313_runtime_source.txt`

Only these two V2 files are Production upload inputs:

- `dist/terpenes_simple_results_parser_v2_controls.js`;
- `SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V2_CONTROLS.json`, imported into a newly and clearly Production-named worksheet object after hash verification.

The source, builder, tests, specifications, validation/readiness records, and fixtures are repository evidence and reproducibility inputs, not files to upload as Production runtime data.

### 14. Which artifacts must not become Production deployment inputs?

Keep the following documented, preserved, and excluded:

- parser 41 and its V2/V3 multi-tab artifacts;
- worksheet 78 and `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v2_formula_fix.json`;
- BATCH-61, Tests 308/309, attachment 53, asset 73, job 65, and the immutable C6 308/309 source;
- V1 Sandbox objects parser 42, worksheet 79, BATCH-62, attachment 57, asset 77, and job 68;
- V2 Sandbox objects parser 43, worksheet 80, BATCH-63, attachment 58, asset 78, and job 69;
- all fixture-specific runtime inputs, including 310/311 and 312/313, as Production uploads;
- the original V1 worksheet with the intentionally preserved pre-correction dimension ordering;
- the V1 parser and corrected worksheet as Production deployment inputs now that V2 supersedes them;
- all earlier native-parser probes, no-code fallbacks, wide-import candidates, Instrument Import/Test Transfer candidates, failed worksheet imports, screenshots, downloaded round trips, and cleanup plans;
- the unqualified Batch-to-Test automation configuration;
- the unqualified exact REST Test publisher and its credentials/API experiments;
- old active Terpenes Test worksheet export ID 42 as a new deployment input;
- Test worksheet V4, report bindings, COA, and METRC mappings until their downstream phase is separately authorized and validated;
- Potency parser, Potency worksheets, and Potency raw output, which are architecture references only.

## Sandbox proof: what it establishes and what it does not

The V2 proof establishes:

- the exact artifact and worksheet imported successfully into isolated Sandbox objects;
- one attachment created one parser job;
- the job reached `SUCCESS`;
- exactly two dynamic Test rows and 34 Run Records rows persisted;
- all 190 × 51 cells were compared with zero semantic differences after normalizing only QBench’s displayed Windows-path escaping;
- context, unmatched rows, audit tail, headers, source hashes, row hashes, parser version, and import literals were exact;
- Tests remained not started with blank result/completion fields;
- no direct Test or COA mutation occurred.

It does not establish:

- approved QC acceptance criteria;
- staff review completion or Batch disposition;
- controlled Production parser/worksheet configuration;
- correct behavior for Production naming, permissions, concurrency, or operating volumes;
- individual Test worksheet persistence;
- Test worksheet calculations;
- COA rendering from the imported Batch data;
- METRC profile mapping/export;
- rerun governance beyond the technical overwrite/readback behavior.

## Superseded pre-proof next phase

This was the recommended next phase before r2 proof execution: upload the corrected artifact, SHA-256 `0cda871ea3510275bd37b8dff8ba3a173b2e97f2a80579a17b3a918a352bc062`, as parser 43 Version 2 and perform a fresh disposable Sandbox proof. That proof subsequently passed as documented in the 2026-07-27 addendum. The inert-quarantine gate also subsequently passed through one manual Save followed by Codex read-only verification.

Before any Production mutation:

1. approve the filename and LabSolutions Test-ID SOP;
2. name the new Production worksheet and parser objects without `SBX_ONLY`;
3. verify the Production Terpenes assay identity and new-Batch worksheet-assignment behavior read-only;
4. define pilot Batch selection, operator, one-upload limit, post-run comparison, Hold/rollback procedure, and success evidence;
5. verify the two upload-input hashes immediately before staging.

If COA or METRC output is required in the same release, pause Production deployment at this boundary and first implement the smallest isolated downstream phase:

- approved QC/reviewer workflow;
- exact-Test-ID Batch-to-Test publisher;
- validated Test V4 destination contract;
- `report_results` COA rendering;
- profile-specific METRC export and accepted-Batch gate.

## Activity boundary

The original audit created this readiness record and appended the authoritative current-state record only. The later local r2 hardening modified only the allowlisted V2 source, build script, browser artifact, focused tests, specification, validation record, this readiness record, and authoritative state. It did not modify the V2 worksheet, either runtime fixture, V1, package files, lockfiles, `.gitignore`, scoped `.gitattributes`, report, COA, or automation files.

No Git command, GitHub action, PR #14 access, browser action, QBench Sandbox action, QBench Production action, direct API action, or network action occurred.

## Revision r2 hardening addendum (2026-07-25)

The current local parser revision is `terpenes-simple-results-parser-v2-controls-r2`.

| Evidence | Bytes | SHA-256 |
|---|---:|---|
| Corrected parser source | 52,233 | `49cb728e0f06e9d12f154b5fdb9d2dac58a40cdc56bcf314b9ce6c26df0db136` |
| Corrected build script | 5,724 | `0cdbacfa7d4c1b454e9c6be972c891a3036285bb282a8e8802ba2859b180268d` |
| Corrected browser artifact | 52,375 | `0cda871ea3510275bd37b8dff8ba3a173b2e97f2a80579a17b3a918a352bc062` |
| Corrected focused test | 75,224 | `077710be872947aa95bcba14a66210e4d5894dbb5f10d335c60507f323fee13e` |
| Corrected specification | 8,282 | `b55fd323ca7290615c3ac6b8f0d129ec261bf22d6c969a70df57bd8dd745bcb9` |
| Corrected validation record | 22,796 | `3237d399efada1a0594a47037679fe24cff99ea04d6447327015243be58219d2` |

The V1 suite remains 97/97. The V2 suite is 145/145: all prior 123 checks plus 22 new adversarial hardening checks. The protected V2 worksheet remains SHA-256 `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3`; runtime fixtures remain `1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e` and `6b6a208faa83a16e54aa7168467d2221fa23db8f8c6c8a82d183f2bb235ce2a7`.

The exact PR allowlist was 21 paths because it included the scoped `QBench/Worksheets/Terpenes/development/.gitattributes`. Parser 43 Version 1/job 69 remains evidence only for the old artifact. Revision r2 subsequently passed its distinct BATCH-65 Sandbox proof and its parser-43 inert quarantine was later directly verified after one manual Save.

## BATCH-65 Sandbox proof and finalization boundary (2026-07-27)

The preceding `PRODUCTION_IMPORT_LAYER_R2_PENDING_SANDBOX_VALIDATION` and `PRODUCTION_IMPORT_LAYER_R2_PENDING_QUARANTINE_FINALIZATION` statuses remain historical context. The r2 proof passed, and the later manual quarantine Save was directly verified; this record is now advanced to `PRODUCTION_IMPORT_LAYER_R2_READY_FOR_GIT`.

- Frozen proof evidence: parser 43 Version 2 active; artifact SHA-256 `0cda871ea3510275bd37b8dff8ba3a173b2e97f2a80579a17b3a918a352bc062`; Batch Worksheet 80 Version 1 / SHA-256 `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3`; BATCH-65/internal ID 65; AIT-SAMP-172/internal ID 172; Source Test 314; Target Test 315; attachment 59 / asset 79; runtime SHA-256 `2019f6d543954ea5bccd485843329f3230aee944c4f82291c19b38eb1469d9fe`.
- Exactly one BATCH-65 attachment upload created exactly one parser-43 job. Job 70 reached `SUCCESS`, created `07/27/2026 11:45 AM` and completed `07/27/2026 11:48 AM`. It remains the newest parser-43 job; no later job appeared.
- Readback evidence is complete: every cell in dynamic rows 2 and 3 matched the local P1/Test-314 and P2/Test-315 A:AY vectors; visible and dollar-reference Test identities agreed; candidate rows were distinct; every cell in audit rows 91:124 matched the 34 source-ordered vectors; P1 was audit row 107 and P2 audit row 108; source hashes propagated exactly; and unmatched rows, row 88, fixed rows 89/90, and audit tail rows 125:190 remained unchanged.
- The parser boundary remains one Results-only Batch update with read-after-write verification before success, no Test service, no direct Test write, no Test Worksheet 77 payload, no second Batch update, and no repair retry. Test Worksheet 77 and Tests 314/315 remained unchanged and NOT STARTED with blank Test Results and dates.
- Local reconciliation after the proof returned V1 97/97 and hardened V2 163/163. Runtime fixture 312/313 remains SHA-256 `6b6a208faa83a16e54aa7168467d2221fa23db8f8c6c8a82d183f2bb235ce2a7`.
- The authorized final quarantine attempt changed Filename Text in the browser to `SBX_ONLY_R2_STAGING_INERT_0cda871ea3510275.txt`, but the single Configuration Save timed out at the browser-control layer. A reload restored `terpenes_simple_results_v2_controls_314_315_runtime_source.txt`; the change did not persist. No retry was made. Job 70 remained newest and attachment 59, BATCH-65, worksheet 80, Test Worksheet 77, and Tests 314/315 remained unchanged.
- Production mapping is recorded but not accessed: Production assay 8 Terpenes; existing Test Worksheet 42 (`Terpenes [Test] Worksheet`) remains unchanged; existing Batch Worksheet 43 (`Terpenes [Batch] Worksheet`) is the future target for a new worksheet version only. Production was not accessed or mutated.
- Follow-up PR accounting is unchanged until this blocker is resolved: the original commit scope is 21 paths; the r2 correction follow-up scope is 10 paths; the resulting unique PR path count is 22 because the 314/315 runtime fixture is the only new unique path, while the other nine paths were already in the original scope. The new scoped `-text` rule preserves that runtime fixture byte-for-byte.
- No Git, GitHub, PR, Production, direct API, or direct HTTP action occurred in this finalization attempt.

## Manual quarantine finalization and current decision (2026-07-27)

Two automated quarantine Save attempts failed without persisting the inert sentinel. The first timed out and read-only reload retained the proof filename. The separately authorized fresh retry was submitted exactly once at `2026-07-27T17:17:02.562Z`, timed out, and its single read-only reload also retained the proof filename. Neither failure created a parser job or changed a proof object.

The user later completed exactly one manual Configuration Save. Codex then verified read-only that parser 43 persisted:

- Trigger `When file is added to Batch attachments`;
- assay `SBX_ONLY_TERPENES_RUNTIME_ASSAY_BATCH_V2` / ID `21`;
- Filename Should `Equal`;
- Filename Text `SBX_ONLY_R2_STAGING_INERT_0cda871ea3510275.txt`;
- Version 2 APPROVED and solely active; Version 1 APPROVED and inactive.

History remained exactly 70 jobs, job 70 remained the newest parser-43 job and `SUCCESS`, and no job 71 appeared. BATCH-65, attachment 59 / asset 79, Tests 314/315, worksheet 80 dynamic and audit Results, and Test Worksheet 77 remained unchanged. Tests 314/315 remained `NOT STARTED` with blank Test-level Results, Start Date, and Complete Date.

Local verification reconfirmed parser artifact SHA-256 `0cda871ea3510275bd37b8dff8ba3a173b2e97f2a80579a17b3a918a352bc062`, Batch worksheet SHA-256 `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3`, and runtime 314/315 SHA-256 `2019f6d543954ea5bccd485843329f3230aee944c4f82291c19b38eb1469d9fe`. The exact scoped `-text` rule was present once and was not modified. Tested implementation content did not change; retained results remain V1 97/97 and hardened V2 r2 163/163.

Production was not accessed. The future Production mapping remains assay 8 Terpenes, Test Worksheet 42 preserved unchanged, and Batch Worksheet 43 as the future new-version target.

Current decision: `PRODUCTION_IMPORT_LAYER_R2_READY_FOR_GIT`.

The preceding `PRODUCTION_IMPORT_LAYER_R2_READY_FOR_GIT` and `PRODUCTION_IMPORT_LAYER_R2_CLEAN_PR_PENDING_REVIEW` statuses are historical. The r2 follow-up commit completed after the validated 22-path scope was transplanted to the clean feature-based branch. PR #14 remains Draft and is superseded because it contains 184 files against its configured base. PR #17 is technically clean against its feature base but is not release-safe because that base is unmerged Draft PR #13.

## Main-based replacement PR review boundary (2026-07-27)

Current readiness: `PRODUCTION_IMPORT_LAYER_R2_MAIN_PR_PENDING_REVIEW`.

The final replacement branch was created directly from `main` and contains exactly the 22 intended paths, with no PR #13 REST-publisher path. The hardened r2 Sandbox proof remains complete through parser 43 Version 2, BATCH-65, attachment 59, and job 70; parser 43 was returned to the inert sentinel filename. No additional Sandbox proof is required. Production was not accessed, and Production deployment remains separately controlled.

The next boundary is read-only technical review of the main-based Draft PR. The import/audit scope remains limited to the Batch Results and Run Records layer; QC disposition, downstream Test-result persistence, COA, and METRC remain separate scopes.

The main-based self-containment gate passed from this 22-path worktree: V1 `97/97` and hardened V2 r2 `163/163`, with no external legacy-file or PR #13 runtime dependency. Scoped `-text` rules preserve the four runtime fixtures, both parser artifacts, and all three byte-hashed worksheet candidates on Windows checkout. The parser, worksheet, and 314/315 runtime hashes remain the validated values above.
