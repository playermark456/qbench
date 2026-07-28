# Terpenes Simple Results V2 Controls Validation

## Final local status

`LOCAL_SIMPLE_RESULTS_V2_CONTROLS_VALIDATED`

This validation was local-only. No browser, QBench Sandbox, QBench Production, network, Git, GitHub, or PR action occurred.

## Read-only preflight

The authoritative state and required architecture references were inspected before implementation:

- `QBench/Worksheets/Terpenes/TERPENES_CURRENT_STATE.md`
- all source, build, test, specification, validation, runtime, parser-artifact, and corrected worksheet files in the frozen V1 directory
- `C:/Users/Mark Adams/Downloads/Potency parser.txt`
- `C:/Users/Mark Adams/Downloads/Cannabinoid Potency [Batch] Worksheet.json`
- `C:/Users/Mark Adams/Downloads/Output (1).csv`
- `C:/Users/Mark Adams/Downloads/terpene parser.txt`
- protected Terpenes multi-tab parser V2/V3 artifacts, worksheet-78 candidate, and C6 runtime source

The Potency references established the one-Batch-service/one-Results-payload persistence and fixed-row organization evidence. No Potency-specific calculations or cannabinoid fields were copied.

Preflight and post-validation protected hashes:

| Artifact | SHA-256 | Result |
|---|---|---|
| V1 browser parser | `bcec7bf0aa1f0b3edfab6ff2f6bcf370abf863226a81472714202aca5efbc871` | unchanged |
| V1 corrected worksheet | `f8d58b33024cce2bf90171df79c7f73e984674fa64b83f99e8030935f9030448` | unchanged |
| V1 runtime input | `1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e` | unchanged |
| protected multi-tab V2 parser | `c3f3ecccf346ce1a1338911ee3bcb45ab4c43342d93bcee7b74b2c70fc847e99` | unchanged |
| protected multi-tab V3 parser | `5a849a6cf3f78784f728cd89d6665310ddc04e299f769bd3ef5e646e31203e85` | unchanged |
| protected worksheet-78 candidate | `50fb7883a6932bc54b09f6997b91f01674e392696e82f77872935bb00576acda` | unchanged |
| protected C6 runtime source | `5de17d8f9eb21a8dfc068daf2297efb707a8b783f63393df432781e5e692e6aa` | unchanged |

Static V1 inspection confirmed one `QBBatchService` construction, one Batch update, one Results payload, no Test service/direct Test write, and read-after-write verification.

## V2 deliverables

Directory:

`QBench/Worksheets/Terpenes/development/2026-07-25_terpenes_simple_results_v2_controls`

| File | Bytes | SHA-256 |
|---|---:|---|
| `src/terpenes_simple_results_parser_v2_controls.js` | 48,889 | `374a0d6722c90a51abaea02a4989fc6927b212a66bcb45090158e1ea4ddab77d` |
| `scripts/build_terpenes_simple_results_parser_v2_controls.js` | 5,379 | `81f1ac86d044605383e40a7aba4db2b0c44af28e57236fd0a411d857d911e3ba` |
| `dist/terpenes_simple_results_parser_v2_controls.js` | 49,031 | `1c3b0badb33acee3152da95aa40fb8c4332aa465fd1733789456293e0a6c7189` |
| `SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V2_CONTROLS.json` | 1,652,216 | `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3` |
| `tests/test_terpenes_simple_results_parser_v2_controls.js` | 43,789 | `318519de29d8a534fe28d05b505a185739b307ee38e35bd42b6613366ad7da84` |
| `runtime/terpenes_simple_results_310_311_runtime_source.txt` | 286,204 | `1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e` |
| `TERPENES_SIMPLE_RESULTS_V2_CONTROLS_SPEC.md` | 6,850 | `b0de9ea38a13f0dc49b24bb156fea936e17c68da0ec31e87d2d356ef26a7afb5` |

The validation record itself is excluded from its embedded hash table; its final hash is recorded in the authoritative state.

## Worksheet validation

- Exactly one worksheet: `Results`.
- Exactly 51 columns through `AY`.
- Exactly 190 rows through row 190.
- `minDimensions` exactly `[51, 190]`.
- Row 1 and rows 2:87 are identical to the corrected V1 worksheet, including generic `tests[0]` through `tests[85]` context.
- Row 88 is blank.
- Row 89 is exactly `Run Records`, `Complete LabSolutions sequence audit`, then 49 blanks.
- Row 90 is the exact 51-column Unicode audit header specified in `TERPENES_SIMPLE_RESULTS_V2_CONTROLS_SPEC.md`.
- Rows 91:190 are initially blank and parser-owned.
- No configured cell or style address exceeds `AY190`.
- No formula or prohibited worksheet tab exists.

Dynamic ownership is `A:C` QBench context and matched-row `D:AY` parser-owned. Audit ownership is all `A:AY` for rows 91:190.

## Exact 34-record fixture

Runtime input:

`runtime/terpenes_simple_results_310_311_runtime_source.txt`

SHA-256:

`1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e`

Every record passed the controlled 24-compound, 23-reportable-analyte, and one-Dimethylacetamide-audit contract.

| Order | Category | Sample Name | Original Sample ID | Audit row | Dynamic row |
|---:|---|---|---|---:|---|
| 1 | Null | Blank001 | Null | 91 | — |
| 2 | Blank | Blank | blank | 92 | — |
| 3 | System Suitability | System Suitability 1 | blank | 93 | — |
| 4 | System Suitability | System Suitability 2 | blank | 94 | — |
| 5 | System Suitability | System Suitability 3 | blank | 95 | — |
| 6 | Null | Blank001 | Null | 96 | — |
| 7 | Standard | Std 1 | 10 µg/mL label | 97 | — |
| 8 | Standard | Std 2 | 25 µg/mL label | 98 | — |
| 9 | Standard | Std 3 | 50 µg/mL label | 99 | — |
| 10 | Standard | Std 4 | 100 µg/mL label | 100 | — |
| 11 | Standard | Std 5 | 300 µg/mL label | 101 | — |
| 12 | Standard | Std 6 | 1000 µg/mL label | 102 | — |
| 13 | Blank | Blank | blank | 103 | — |
| 14 | CCV | CCV | blank | 104 | — |
| 15 | LOQ | LOQ | blank | 105 | — |
| 16 | Matrix Blank | P0 | Matrix Blank | 106 | — |
| 17 | Sample | P1 | 310 | 107 | 2 |
| 18 | Sample | P2 | 311 | 108 | 3 |
| 19 | Validation | P3 | Low 3 | 109 | — |
| 20 | Validation | P4 | Low 4 | 110 | — |
| 21 | Validation | P5 | Low 5 | 111 | — |
| 22 | Validation | P6 | Medium 1 | 112 | — |
| 23 | Validation | P7 | Medium 2 | 113 | — |
| 24 | Validation | P8 | Medium 3 | 114 | — |
| 25 | CCV | CCV | blank | 115 | — |
| 26 | Validation | P9 | Medium 4 | 116 | — |
| 27 | Validation | P10 | Medium 5 | 117 | — |
| 28 | Validation | P11 | High 1 | 118 | — |
| 29 | Validation | P12 | High 2 | 119 | — |
| 30 | Validation | P13 | High 3 | 120 | — |
| 31 | Validation | P14 | High 4 | 121 | — |
| 32 | Validation | P15 | High 5 | 122 | — |
| 33 | Null | Blank001 | Null | 123 | — |
| 34 | CCV | CCV | blank | 124 | — |

Category counts: Null 3; Blank 2; System Suitability 3; Standard 6; CCV 3; LOQ 1; Matrix Blank 1; Sample 2; Validation 13.

Audit rows written/read back were exactly 34/34. Rows 125:190 remained blank. Dynamic rows written/read back were exactly 2/2. Candidate IDs were exactly `["310", "311"]`; both resolved to fixture Batch internal ID `62`; Test 310 mapped only to row 2 and Test 311 only to row 3. No control or validation record reached a dynamic Test row.

Every dynamic and audit `Source File Hash` matched the runtime hash. Dynamic Source Row Hash retained the V1 content-derived value. Audit Source Row Hash was verified as `SHA-256(source_file_hash + ":" + record_order)`. Every staged row used parser version `terpenes-simple-results-parser-v2-controls` and import status `Imported`.

## Update and stale-clearing proof

Static and mocked execution proved:

- one `QBBatchService` construction;
- one call to `QBBatchService.update`;
- data ID `62` in the fixture;
- exactly one `qb_dynamic_spreadsheet_data` key, `Results`;
- matched dynamic and fixed audit changes in that same Results payload;
- `run_worksheet_calculations: true`;
- unchanged `WORKSHEET_FORMULAS`, `WORKSHEET_IMAGE_DATA`, and `WORKSHEET_DOLLAR_REFERENCES`;
- no Test service, direct Test write, or second update.

The stale fixture placed values at `A125`, `K125`, and `AY130`. Only those nonblank cells were staged blank; an already blank `B125` was not staged; no dynamic row, row 89, row 90, or cell outside rows 91:190 was cleared.

## Readback proof

Successful persistence verified two dynamic rows and 34 audit rows before `QB.success()`. Focused negative tests proved controlled failure with `RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED` for:

- a no-op update;
- missing or duplicate audit records;
- changed audit or dynamic values;
- changed `A:C` context;
- a nonblank stale unused audit row;
- a changed row-90 header;
- changed formula/image/reference maps;
- a missing dynamic candidate row.

Every negative case performed one update at most, made no retry, and did not call `QB.success()`.

## Test executions

From the V2 directory:

```text
node tests\test_terpenes_simple_results_parser_v2_controls.js
```

Result: 93 total, 93 passed, 0 failed, 0 skipped.

From the V2 directory, the unchanged V1 suite was rerun with:

```text
node ..\2026-07-25_terpenes_simple_results_v1\tests\test_terpenes_simple_results_parser.js
```

Result: 97 total, 97 passed, 0 failed, 0 skipped.

No repository-wide test, dependency installation, formatter, package command, or network action occurred.

## Staging boundary

The candidate is locally ready for a separately authorized isolated V2 Sandbox staging phase. That future phase must use new worksheet, parser, Batch, Sample, Test, attachment, and job objects and must define its own mutation/retry budget. Nothing in this local validation states or implies that V2 has been uploaded, activated, attached, or executed in QBench.

## Immutable Batch-63 runtime binding validation

Final status:

`SIMPLE_RESULTS_V2_CONTROLS_RUNTIME_INPUT_VALIDATED`

This continuation was local-only. It relied on the authoritative staged contract already recorded in `TERPENES_CURRENT_STATE.md`; it did not open or access QBench. The staged objects remain worksheet `80`, parser `43`, BATCH-63/internal ID `63`, AIT-SAMP-171/internal ID `171`, Source Test `312`, Target Test `313`, dynamic Results rows `2` and `3`, and Run Records capacity rows `91:190`.

### Immutable transformation

Protected source:

`runtime/terpenes_simple_results_310_311_runtime_source.txt`

Source SHA-256:

`1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e`

The V2 source fixture remained byte-for-byte identical to the frozen V1 runtime fixture with the same SHA-256.

New immutable target:

`runtime/terpenes_simple_results_v2_controls_312_313_runtime_source.txt`

Target SHA-256:

`6b6a208faa83a16e54aa7168467d2221fa23db8f8c6c8a82d183f2bb235ce2a7`

Both source and target are exactly 286,204 bytes, valid UTF-8 without BOM, CRLF-only, and terminated by a final CRLF. Exactly two zero-based byte offsets differ:

| Offset | Old byte/value | New byte/value | Contract |
|---:|---|---|---|
| 124302 | `48` / `0` | `50` / `2` | P1 `[Sample Information]` Sample ID `310 → 312` |
| 133049 | `49` / `1` | `51` / `3` | P2 `[Sample Information]` Sample ID `311 → 313` |

No byte was inserted or deleted. The transformation was context-bound to the `[Sample Information]` sections for exact Sample Names P1 and P2; it was not a global numeric replacement.

### Record and analytical preservation

- All 34 complete records retained their original order and eight sections per record.
- Every record retained exactly 24 controlled Compound Results rows, 23 reportable analytes, and one Dimethylacetamide audit result.
- Sample Names, Sample Types, vials, source metadata, compound tables, peak tables, analyte values, Unknown Peak Count, Manual Integration, Integration Review Status, source files, acquisition data, instrument data, row counts, whitespace, tabs, blank lines, and line endings remained unchanged.
- After excluding only the P1/P2 contracted Sample IDs and source-hash-derived fields, every parsed record value was deeply identical to the protected 310/311 source.
- Category counts remained: Null `3`; Blank `2`; System Suitability `3`; Standard `6`; CCV `3`; LOQ `1`; Matrix Blank `1`; Sample `2`; Validation `13`.

### Role, candidate, and Batch resolution

The human-reviewed fixture roles remain:

- P1 / source record order `17` / Source / Test `312`;
- P2 / source record order `18` / Target / Test `313`.

The exact parser-consumed candidate set is the distinct strings `["312", "313"]`. Each appears exactly once in its contracted Sample ID field; contracted IDs `310` and `311` no longer appear; no third transfer-eligible Test ID exists.

The focused QBench-service mock resolved Test `312` exactly once to internal Batch ID `63` and Test `313` exactly once to internal Batch ID `63`. No alternate Batch resolved. Partial, unknown, ambiguous, duplicate-candidate, and multiple-Batch resolution paths failed closed before any update.

### Dynamic and audit mapping

The staged Batch-63 mock reproduces the live baseline:

- Results row `2` A:C is exactly `AIT-SAMP-171 / 312 / Cannabis Concentrates`;
- Results row `3` A:C is exactly `AIT-SAMP-171 / 313 / Cannabis Concentrates`;
- rows `4:87` are blank;
- row `88` is blank;
- row `89` is the exact Run Records section label;
- row `90` is the exact 51-column audit header;
- rows `91:190` begin blank;
- formula, image, and dollar-reference maps use the generic QBench worksheet contract.

Test `312` mapped exactly once to dynamic row `2`; Test `313` mapped exactly once to dynamic row `3`. Exactly two dynamic D:AY vectors were staged, matching the complete locally parsed P1 and P2 values with the new source hash. A:C and rows 4:87 remained unchanged.

All 34 records mapped exactly once and in source order to audit rows `91:124`; record order `1` mapped to row `91`, record order `34` mapped to row `124`, and rows `125:190` remained blank. P1/order `17` mapped to audit row `107` and dynamic row `2`; P2/order `18` mapped to audit row `108` and dynamic row `3`. The other 32 control and validation records appeared only in the audit region.

All shared P1/P2 D:AY values matched between the audit and dynamic representations under the controlled hash contracts. Dynamic Source Row Hash remained the parsed record-content hash. Audit Source Row Hash remained `SHA-256(source_file_hash + ":" + record_order)`. Every audit Source File Hash was the new runtime SHA-256, every audit Import Status was `Imported`, and every audit Parser Version was `terpenes-simple-results-parser-v2-controls`.

### Service, stale clearing, and readback

The unchanged generic parser constructed exactly one `QBBatchService` and performed exactly one Batch update with:

```text
data.id = "63"
qb_dynamic_spreadsheet_data = { Results: ... }
run_worksheet_calculations = true
```

The one Results payload combined both dynamic rows, all 34 current audit rows, and any targeted stale-audit clearing. It preserved `WORKSHEET_FORMULAS`, `WORKSHEET_IMAGE_DATA`, and `WORKSHEET_DOLLAR_REFERENCES`. No Test service was constructed, no direct Test write occurred, and no second Batch update occurred.

The stale fixture again populated only `A125`, `K125`, and `AY130`; exactly those nonblank unused-audit cells were targeted for clearing. Already blank cells were omitted. Rows `2:87`, row `89`, row `90`, and every cell outside rows `91:190` were excluded from stale-audit clearing.

Successful readback verified dynamic rows `2` and `3`, all 34 audit rows, blank rows `125:190`, unchanged A:C, unchanged rows `4:87`, unchanged rows `89` and `90`, and unchanged maps before `QB.success()`. Batch-63-specific negative checks covered missing and duplicate Test `312`/`313` rows; missing and duplicate audit records; changed audit, dynamic, or context values; returned stale audit data; changed audit header or maps; and a no-op update. Each failed with `RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED`, issued no retry, and did not call `QB.success()`.

### Focused test results

Unchanged V1 suite, run from the V2 directory:

```text
node ..\2026-07-25_terpenes_simple_results_v1\tests\test_terpenes_simple_results_parser.js
```

Result: 97 total, 97 passed, 0 failed, 0 skipped.

Extended V2 suite, run from the V2 directory:

```text
node tests\test_terpenes_simple_results_parser_v2_controls.js
```

Result: 123 total, 123 passed, 0 failed, 0 skipped. All previous 93 V2 checks remain present and passing; 30 new Batch-63 fixture-binding checks passed. The updated focused test file is 65,088 bytes with SHA-256 `70adf74f1170e2e63bb899483129f34c2a43a73059a70d40a701ec07e5b8b218`.

The generic parser source, build script, browser artifact, and worksheet candidate were not modified or rebuilt. Their protected hashes remained parser artifact `1c3b0badb33acee3152da95aa40fb8c4332aa465fd1733789456293e0a6c7189` and worksheet `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3`. The existing specification already explicitly states the generic Sample Information → Sample ID binding rule, audit-only control/validation behavior, and intentional Sample duplication between the audit and dynamic regions, so no specification change was required.

No browser, QBench Sandbox, QBench Production, network, dependency installation, Git, GitHub, PR #14, build, formatter, coverage, snapshot, repository-wide test, upload, attachment, or parser execution occurred.

### Next boundary

The exact filename for a separately authorized single controlled Sandbox execution is:

`terpenes_simple_results_v2_controls_312_313_runtime_source.txt`

Required SHA-256:

`6b6a208faa83a16e54aa7168467d2221fa23db8f8c6c8a82d183f2bb235ce2a7`

The next phase may configure parser `43` with the Batch-attachment trigger and this exact filename, attach this one immutable input to BATCH-63, and perform one controlled isolated V2 Sandbox execution. This local validation does not state or imply that the file has been uploaded, attached, or executed.

## Revision r2 PR-review hardening (2026-07-25)

Final local hardening status:

`LOCAL_PR_REVIEW_HARDENING_VALIDATED`

This section supersedes the implementation hashes and current-readiness statements above where they refer to the pre-hardening parser. The earlier Sandbox evidence remains historical and exact: parser 43 Version 1/job 69 used the 49,031-byte artifact with SHA-256 `1c3b0badb33acee3152da95aa40fb8c4332aa465fd1733789456293e0a6c7189`. That artifact and its successful proof are not recharacterized.

The corrected local artifact is parser revision `terpenes-simple-results-parser-v2-controls-r2`. It has not been uploaded to QBench and has not been validated in Sandbox. Its next required gate is parser 43 Version 2 plus a fresh disposable Sandbox proof.

### Corrected implementation

| File | Bytes | SHA-256 |
|---|---:|---|
| `src/terpenes_simple_results_parser_v2_controls.js` | 52,233 | `49cb728e0f06e9d12f154b5fdb9d2dac58a40cdc56bcf314b9ce6c26df0db136` |
| `scripts/build_terpenes_simple_results_parser_v2_controls.js` | 5,724 | `0cdbacfa7d4c1b454e9c6be972c891a3036285bb282a8e8802ba2859b180268d` |
| `dist/terpenes_simple_results_parser_v2_controls.js` | 52,375 | `0cda871ea3510275bd37b8dff8ba3a173b2e97f2a80579a17b3a918a352bc062` |
| `tests/test_terpenes_simple_results_parser_v2_controls.js` | 75,224 | `077710be872947aa95bcba14a66210e4d5894dbb5f10d335c60507f323fee13e` |

The artifact-only build command was:

```text
node scripts\build_terpenes_simple_results_parser_v2_controls.js --artifact-only
```

It rebuilt only the browser artifact and required the protected worksheet to equal the deterministic worksheet output before reporting it unchanged.

### Defect reproduction and corrections

The pre-hardening union index reproduced both reviewed unsafe states:

- visible `B2="999"` with dollar reference `B2="310"` allowed candidate Test `310` to plan against physical row 2;
- two distinct candidate IDs could be associated with one physical row through the union behavior.

Revision r2 replaces that behavior with one strict row-context function used for both initial planning and readback. On every dynamic row `2:87`, it trims visible column B and the exact B-cell dollar reference. Nonblank unequal values fail with `RESULTS_TEST_CONTEXT_MISMATCH`; equal values are accepted; a single nonblank source is accepted; two blanks mean no Test identity. Duplicate effective IDs across rows are rejected, and all candidate plans must use distinct physical rows or fail with `RESULTS_TEST_ROW_ALIAS`.

File ingestion now reads an `ArrayBuffer`, hashes its exact bytes before decoding, rejects leading bytes `EF BB BF` with `SOURCE_UTF8_BOM_NOT_ALLOWED`, and decodes with fatal UTF-8 validation. Invalid UTF-8 fails with `SOURCE_UTF8_INVALID`. Hashing, BOM rejection, and UTF-8 validation occur before Batch lookup, worksheet retrieval, or update. No line-ending normalization, BOM stripping, text re-encoding, or parser output participates in `Source File Hash`.

### Adversarial and regression validation

The 22 new focused checks prove:

- equal visible/reference IDs, visible-only IDs, and reference-only IDs are accepted;
- mismatches in either direction and mismatches on unused rows fail before update;
- physical-row aliasing fails before service/update/success;
- a readback-only context mismatch fails with `RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED`;
- valid Tests `312` and `313` still map to distinct rows 2 and 3;
- the CRLF 312/313 fixture produces exact-byte SHA-256 `6b6a208faa83a16e54aa7168467d2221fa23db8f8c6c8a82d183f2bb235ce2a7` in all dynamic and audit file-hash fields and in audit row-hash derivation;
- BOM and invalid UTF-8 inputs fail before Batch lookup/update;
- LF and CRLF byte sequences hash differently even when their parsed records are equivalent;
- dynamic and audit Parser Version values are exactly `terpenes-simple-results-parser-v2-controls-r2`;
- the one-service, one-Results-update, complete-readback, no-Test-write contract remains intact.

The frozen V1 suite was run from its directory:

```text
node tests\test_terpenes_simple_results_parser.js
```

Result: 97 total, 97 passed, 0 failed, 0 skipped.

The updated V2 suite was run from its directory:

```text
node tests\test_terpenes_simple_results_parser_v2_controls.js
```

Result: 145 total, 145 passed, 0 failed, 0 skipped. All prior 123 checks remain present and passing; 22 new hardening checks pass.

### Protected post-validation evidence

| Protected artifact | SHA-256 | Result |
|---|---|---|
| V1 browser parser | `bcec7bf0aa1f0b3edfab6ff2f6bcf370abf863226a81472714202aca5efbc871` | unchanged |
| V1 corrected worksheet | `f8d58b33024cce2bf90171df79c7f73e984674fa64b83f99e8030935f9030448` | unchanged |
| V1 runtime input | `1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e` | unchanged |
| V2 worksheet | `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3` | unchanged |
| V2 310/311 runtime | `1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e` | unchanged |
| V2 312/313 runtime | `6b6a208faa83a16e54aa7168467d2221fa23db8f8c6c8a82d183f2bb235ce2a7` | unchanged |

No browser, QBench, Sandbox, Production, network, Git, GitHub, PR, dependency-installation, repository-wide-test, worksheet, fixture, V1, package, lockfile, or `.gitattributes` action occurred.

## Immutable Batch-65 r2 runtime binding (2026-07-26)

Final local binding status:

`LOCAL_R2_BATCH65_RUNTIME_BINDING_VALIDATED`

The user explicitly confirmed the fixture role contract before modification:

- P1 = Source Test `314`;
- P2 = Target Test `315`.

This continuation was local-only. It used the handoff contract for assay `21`, Batch Worksheet `80`, BATCH-65/internal ID `65`, AIT-SAMP-172/internal ID `172`, Results row `2` for Test `314`, and Results row `3` for Test `315`. Existing Test Worksheet `77` is protected fixture context only. It is not part of the Simple Results parser payload, was not mocked as a persistence destination, and was not read, written, updated, versioned, or claimed validated.

### Immutable runtime input

Source:

`runtime/terpenes_simple_results_v2_controls_312_313_runtime_source.txt`

New immutable input:

`runtime/terpenes_simple_results_v2_controls_314_315_runtime_source.txt`

| Property | Result |
|---|---|
| Source length | 286,204 bytes |
| Target length | 286,204 bytes |
| Target SHA-256 | `2019f6d543954ea5bccd485843329f3230aee944c4f82291c19b38eb1469d9fe` |
| Changed-byte count | 2 |
| UTF-8 BOM | absent |
| Line endings | CRLF only |
| Final bytes | CRLF |

The exact zero-based changed-byte offsets are:

| Offset | Old byte | New byte | Contract |
|---:|---|---|---|
| 124302 | `50` / `2` | `52` / `4` | P1 Sample ID `312 → 314` |
| 133049 | `51` / `3` | `53` / `5` | P2 Sample ID `313 → 315` |

No other byte differs. Parsing retained 34 complete records, 24 controlled compound-result rows per record, 23 reportable analytes per record, Dimethylacetamide audit values, Unicode labels, and the exact unchanged category counts: Null 3; Blank 2; System Suitability 3; Standard 6; CCV 3; LOQ 1; Matrix Blank 1; Sample 2; Validation 13.

The exact parser-consumed candidate set is `["314", "315"]`. Both values are strings and occur once in the contracted P1/P2 Sample ID fields. Tests `312` and `313` no longer occur as contracted Sample IDs.

### Batch-65 mapping and persistence proof

The local worksheet fixture reproduces:

- row `2` A:C = `AIT-SAMP-172 / 314 / Cannabis Concentrates`;
- row `3` A:C = `AIT-SAMP-172 / 315 / Cannabis Concentrates`;
- dollar references `B2 = 314` and `B3 = 315`;
- rows `2` and `3` as distinct physical rows;
- rows `4:87` blank.

Strict visible/reference reconciliation mapped Test `314` exactly once to row `2` and Test `315` exactly once to row `3`. Both candidates resolved only to internal Batch ID `65`. Unknown, ambiguous, partial, and multiple-Batch resolution paths failed before update.

All 34 records mapped once and in source order to audit rows `91:124`. P1 remained record order `17` and audit row `107`; P2 remained record order `18` and audit row `108`. Dynamic and audit Source File Hash values use exact byte hash `2019f6d543954ea5bccd485843329f3230aee944c4f82291c19b38eb1469d9fe`; audit Source Row Hash values use the controlled exact-hash-plus-record-order derivation. Dynamic and audit Parser Version values are `terpenes-simple-results-parser-v2-controls-r2`; Import Status is literal `Imported`.

The successful mock retained exactly one `QBBatchService` construction, one Batch update to `data.id = "65"`, exactly one `qb_dynamic_spreadsheet_data` key `Results`, and `run_worksheet_calculations: true`. It preserved A:C, unmatched rows, formulas, images, and dollar references. It included no Test Worksheet `77` payload, no Test service, no direct Test write, no second Batch update, and no retry.

Complete readback verified two dynamic rows, all 34 audit rows, blank unused audit capacity, unchanged context and maps, and persistence before `QB.success()`. No-op, missing-row, changed-context/reference, and changed-audit readback failures issued one update at most, did not retry, and did not call `QB.success()`.

### Focused test results

Frozen V1 suite, run from the V1 directory:

```text
node tests\test_terpenes_simple_results_parser.js
```

Result: 97 total, 97 passed, 0 failed, 0 skipped.

Hardened V2 suite, run from the V2 directory:

```text
node tests\test_terpenes_simple_results_parser_v2_controls.js
```

Result: 163 total, 163 passed, 0 failed, 0 skipped. All existing 145 checks remain present and passing; 18 new Batch-65 fixture-binding checks passed. The focused test file is 89,266 bytes with SHA-256 `d21b212d89e0bc7b61336b79c2ca2a0871d5aae1ee9b7e911aab92d525900389`.

### Protected evidence and next boundary

The parser source, build script, browser artifact, worksheet, specification, prior runtime fixtures, and Test Worksheet `77` were not modified. Protected hashes remained:

- parser source `49cb728e0f06e9d12f154b5fdb9d2dac58a40cdc56bcf314b9ce6c26df0db136`;
- build script `0cdbacfa7d4c1b454e9c6be972c891a3036285bb282a8e8802ba2859b180268d`;
- browser artifact `0cda871ea3510275bd37b8dff8ba3a173b2e97f2a80579a17b3a918a352bc062`;
- Batch worksheet `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3`;
- specification `b55fd323ca7290615c3ac6b8f0d129ec261bf22d6c969a70df57bd8dd745bcb9`;
- 312/313 runtime `6b6a208faa83a16e54aa7168467d2221fa23db8f8c6c8a82d183f2bb235ce2a7`.

No browser, QBench, Sandbox, Production, network, Git, GitHub, PR #14, build, dependency installation, upload, attachment, or parser execution occurred.

The exact filename for a later separately authorized one-upload Sandbox proof is:

`terpenes_simple_results_v2_controls_314_315_runtime_source.txt`

Required SHA-256:

`2019f6d543954ea5bccd485843329f3230aee944c4f82291c19b38eb1469d9fe`

That future proof must establish a read-only Test Worksheet `77` baseline for Tests `314` and `315` before execution and verify afterward that worksheet `77`, Test results, Test status, dates, completion, approval, and review state remain unchanged. This local validation does not state or imply that the new runtime input was uploaded, attached, or executed.

## BATCH-65 Sandbox proof evidence and quarantine-finalization block (2026-07-27)

The preceding local-only statement remains historical context. The isolated r2 proof was subsequently executed once in Sandbox and passed, with the following frozen evidence:

- parser 43 Version 2 active / artifact SHA-256 `0cda871ea3510275bd37b8dff8ba3a173b2e97f2a80579a17b3a918a352bc062`;
- Batch Worksheet 80 Version 1 / SHA-256 `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3`;
- BATCH-65/internal ID 65, Sample AIT-SAMP-172/internal ID 172, Tests 314/315 on distinct Results rows 2/3, and protected Test Worksheet 77;
- one attachment 59 / asset 79, exact runtime path `runtime/terpenes_simple_results_v2_controls_314_315_runtime_source.txt`, and SHA-256 `2019f6d543954ea5bccd485843329f3230aee944c4f82291c19b38eb1469d9fe`;
- one parser job 70, SUCCESS, created `07/27/2026 11:45 AM` and completed `07/27/2026 11:48 AM`.

Live verification matched every dynamic A:AY cell for P1/Test 314 and P2/Test 315, including matching visible/reference Test IDs, distinct physical rows, context preservation, exact-byte source-hash propagation, r2 identity, and Import Status. Every one of the 34 x 51 audit cells in rows 91:124 matched the local source-order expectation; P1 was audit row 107 and P2 audit row 108. Unmatched dynamic rows, blank row 88, fixed audit rows 89/90, and unused audit capacity 125:190 remained unchanged.

Test Worksheet 77 remained unchanged. Tests 314/315 stayed NOT STARTED with blank Test Results and dates. The executed parser retained one Results-only Batch update, complete readback before success, no Test service, no direct Test write, no Test Worksheet 77 payload, no second Batch update, and no retry.

Post-proof local validation returned V1 97/97 and V2 163/163. Artifact, worksheet, 314/315 runtime, and 312/313 runtime hashes matched their controlled values.

Finalization did not complete: the one authorized parser-43 Configuration Save intended to restore Filename Text to `SBX_ONLY_R2_STAGING_INERT_0cda871ea3510275.txt` timed out at the browser-control layer. Reload showed the proof filename still persisted. No retry occurred; job 70 remained newest and no QBench object changed. This validation record therefore preserves the proof evidence but does not claim Git or Production readiness.

No Production, Git, GitHub, PR, direct API, or direct HTTP action occurred in the proof-finalization attempt.

## Manual quarantine finalization and read-only verification (2026-07-27)

Final status:

`R2_QUARANTINE_FINALIZED_READY_FOR_GIT`

The earlier pending-quarantine state remains historical evidence. Two automated parser-43 quarantine Save attempts failed without changing the persisted server configuration:

1. The initial automated Save timed out at the browser-control layer; read-only reload showed `terpenes_simple_results_v2_controls_314_315_runtime_source.txt` still persisted.
2. The separately authorized fresh automated retry was submitted once at `2026-07-27T17:17:02.562Z`. It also timed out; the single authorized read-only reload again showed the proof filename. No automated retry, repair, or other mutation followed either timeout.

The user later completed exactly one manual parser-43 Configuration Save. Codex then performed a separate read-only Sandbox verification and directly observed the final persisted configuration:

- parser ID `43`;
- Version `2` / `terpenes-simple-results-parser-v2-controls-r2` APPROVED and solely active;
- Version `1` / `terpenes-simple-results-parser-v2-controls` APPROVED and inactive;
- Trigger `When file is added to Batch attachments`;
- assay `SBX_ONLY_TERPENES_RUNTIME_ASSAY_BATCH_V2` / ID `21`;
- Filename Should `Equal`;
- Filename Text `SBX_ONLY_R2_STAGING_INERT_0cda871ea3510275.txt`.

File Parser History remained exactly 70 jobs. Job `70` remained the newest parser-43 job and remained `SUCCESS`, created `07/27/2026 11:45 AM` and completed `07/27/2026 11:48 AM`; no job `71` appeared.

The read-only reconciliation found no proof-object change:

- BATCH-65 still contained exactly Tests `314` and `315`;
- attachment `59` / asset `79` remained the sole BATCH-65 attachment;
- worksheet `80` retained the proven dynamic rows `2` and `3`, including r2 Parser Version and literal `Imported`;
- audit rows `107` and `108` retained P1/Test `314` and P2/Test `315`, the exact runtime Source File Hash, r2 Parser Version, controlled Source Row Hash values, and literal `Imported`;
- Tests `314` and `315` remained `NOT STARTED` with blank Test-level Results, Start Date, and Complete Date;
- protected Test Worksheet `77` remained unchanged, including `<LOQ` for Nerolidol and Ocimene and `0` for Total Terpenes on both Tests.

Local hashes remained exact:

- parser artifact `0cda871ea3510275bd37b8dff8ba3a173b2e97f2a80579a17b3a918a352bc062`;
- Batch worksheet `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3`;
- 314/315 runtime `2019f6d543954ea5bccd485843329f3230aee944c4f82291c19b38eb1469d9fe`.

The exact `development/.gitattributes` rule for the 314/315 runtime fixture was present once and was not modified. Tested implementation content did not change, so the retained results remain V1 `97/97` and hardened V2 r2 `163/163`.

Production was not accessed. The recorded future Production mapping remains assay `8` Terpenes, Test Worksheet `42` preserved unchanged, and Batch Worksheet `43` as the future new-version target. The current readiness status is `PRODUCTION_IMPORT_LAYER_R2_READY_FOR_GIT`. The next boundary is to stage and commit the 10-path r2 follow-up scope, verify the preserved CRLF fixture bytes, push, and add an additive Draft PR #14 comment.

## Main-based self-containment validation (2026-07-27)

The focused suites now run from the main-based 22-path package without any persistent dependency on the historical parser-probe tree, production-candidate tree, exact-Test REST publisher, Git history, or another worktree. The V1 suite passed `97/97`; the hardened V2 r2 suite passed `163/163`; both had zero failures and zero skips. The V2 preflight protection block now verifies package-local V1/V2 hashes and architecture, and its meta-test rejects forbidden external dependency markers and out-of-package persistent fixture paths.

The scoped `development/.gitattributes` retains the four runtime-fixture `-text` rules and adds exact `-text` rules for both parser artifacts and all three byte-hashed worksheet candidates. The validated V2 parser artifact remains SHA-256 `0cda871ea3510275bd37b8dff8ba3a173b2e97f2a80579a17b3a918a352bc062`, the V2 worksheet remains `80fde1ebb3d4207a2fdcbe297c3b457906cca7355d12ff50baf3e1fca14bfeb3`, and the 314/315 runtime remains `2019f6d543954ea5bccd485843329f3230aee944c4f82291c19b38eb1469d9fe`.

Current readiness is `PRODUCTION_IMPORT_LAYER_R2_MAIN_PR_PENDING_REVIEW`. No additional Sandbox proof is required; Production was not accessed.
