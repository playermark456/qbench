# Phase 3 full local validation report

Validation date: 2026-07-20

## Outcome

`calculation_contract = passed_authoritative_method_documentation_and_user_approved_reporting_rules`

`phase3_local_candidate_validation = passed`

The approved component-preprocessing rule, 41 calculation vectors, local Test candidate, and local Batch candidate passed the dedicated Phase 3 validator. No QBench environment or QBench API was accessed. No worksheet was imported, approved, activated, published, or assigned.

## Candidate artifacts

| Candidate | SHA-256 | Tabs and populated dimensions |
| --- | --- | --- |
| `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v1.json` | `275c8058cd597cfc688121bbdf50d1189897a088f455ff9e00e79a3fdf781a44` | Report 23x5; Data 40x26; Specifications 23x21 |
| `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v1.json` | `7c96c9e8bb300f5886a4f66971c6c22c3ae72ee9225134f737d6601a0bbc55b2` | Run Setup 25x3; Instrument Import 201x57; Batch Review 45x24; Test Transfer 87x56 |

The Test candidate has 44 named definitions: the exact 43 blank/writable/non-formula/exportable destinations plus `report_results = Report!A1:E23`. It retains 23 internal chromatographic channels, reports exactly 21 measurands plus Total Terpenes, and excludes component channels from the Report tab.

The Batch candidate has formula-owned AF/AG cells in all 200 Instrument Import data rows. Parser write ranges remain `A2:AE2` and `AH2:BE2`; AF and AG are excluded. Null, Blank, Standard, CCV, LOQ, and QC record types remain excluded from Test Transfer.

## Calculation-vector and formula validation

- 41 vector rows passed, including all 15 explicit combined-component boundary vectors and the required 13 minimum cases.
- Missing, blank, no-peak, zero, and negative component values produce `used_ug_g = 0` while retaining raw inputs separately.
- Positive values retain full precision; no component LOQ lookup or filter exists.
- Combined reportable results use the combined analyte LOQ only.
- One positive component uses that component's MU; two positive components use independent relative propagation; two zero components return blank; a positive contributor with missing MU is unresolved.
- Total Terpenes uses 21 unrounded reportable results and a strict `result_ug_g > LOQ_ug_g` inclusion test.
- Rounding appears only in final display formulas.
- All Test calculated cells and Batch AF/AG cells are protected/formula-owned.
- The CSV was opened through the bundled spreadsheet artifact runtime, inspected over `A1:R20`, rendered, and visually reviewed; zero formula-error tokens were found.

## Regression matrix

| Check | Result |
| --- | --- |
| Phase 3 deterministic rebuild | passed; candidate hashes unchanged |
| Phase 3 candidate/vector validator | passed; 41 vectors, 44 Test names, 200 AF/AG formula rows |
| Prompt 2 configuration/parser Python tests | 27/27 passed |
| Historical Test worksheet Python tests | 50/50 passed |
| Historical Test worksheet static/formula validator | passed; 265 formulas and `Report!A1:E23` |
| Historical Batch worksheet Python tests | 39/39 passed in an isolated manifest-byte validation workspace |
| Historical Batch worksheet static/formula validator | passed in the same isolated workspace; 1,180 formulas and 67 named cells |
| Wide-adapter Python tests | 13/13 passed |
| Wide-adapter JavaScript tests | 143/143 passed |
| Wide-adapter package validator | passed; 57 columns and two write blocks |
| Native-probe Python tests | 17/17 passed |
| Native-probe JavaScript tests | 48/48 passed |
| Native-probe package validator | passed; 45 artifacts |
| No-code parser package validator | passed; 57 columns, 23 numeric analytes, AF/AG excluded |
| Prompt 5 automation package validator | passed; 43 intended mappings and zero Test writes |
| Prompt 5B publisher tests | 46/46 passed |
| Prompt 5B package validator | passed; 115 generated-file hashes |

### Historical Batch newline note

The ordinary Windows checkout initially reported two false legacy Batch regression failures because `core.autocrlf=true` changes the raw byte hashes of dependencies whose 2026-07-14 manifest records a mixture of canonical-LF and preserved-CRLF files. The current Phase 3 changes do not modify any historical Batch dependency. The legacy suite and validator pass when run in an isolated scratch workspace assembled with each dependency's exact manifest-recorded bytes. No historical tracked file was changed or staged as part of that diagnostic.

## Sanitization and scope

- Candidate scans found no URL, QBench domain, signed URL, Authorization header, bearer token, client secret, access token, raw assertion, email address, worksheet query identifier, source worksheet-ID filename, or Pass/Fail token.
- Candidate UUIDs are fresh, unique, and disjoint from the structural references.
- The dedicated validator found no customer value or internal production QBench identifier.
- Controlled method documents and other raw evidence remain ignored and unstaged.
- `.env.local.txt` remains ignored and unstaged; it was not read or displayed.
- No live or Sandbox QBench access, token request, REST call, PATCH, automatic publication, automatic QC Review action, or Terpenes Pass/Fail artifact occurred.

## Next gate

The next controlled phase is isolated Sandbox import and saved/reopened validation, followed by instantiated runtime proof, Key/Value binding validation, COA preview, and transfer verification. This report does not authorize those actions.
