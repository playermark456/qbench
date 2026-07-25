# Terpenes Simple Results V1 local validation

## Final status

`SIMPLE_RESULTS_RUNTIME_INPUT_VALIDATED`

Validation date: 2026-07-25  
Scope: local immutable runtime-input construction and focused Node validation only

No browser, QBench, Sandbox, Production, network, Git, GitHub, or PR #14 action occurred.

## Dimension-fix reconciliation

The permanent focused suite now reconciles the original 45 Simple Results
architecture/runtime checks with the later worksheet dimension correction.
QBench's locally and live-established worksheet convention is
`minDimensions = [columns, rows]`.

- Preserved original diagnostic candidate:
  `SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1.json`
- Original SHA-256:
  `ce50d670be71fccf02912b30cacb918fd48916e8f154a164b095f8f0670a96be`
- Original `minDimensions`: `[87, 51]`
- Corrected import candidate:
  `SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1__dimension_fix.json`
- Corrected SHA-256:
  `f8d58b33024cce2bf90171df79c7f73e984674fa64b83f99e8030935f9030448`
- Corrected `minDimensions`: `[51, 87]`

The original and corrected JSON files have the same 766,266-byte length. Their
only semantic differences are
`config.worksheets[0].minDimensions[0]`, `87` to `51`, and
`config.worksheets[0].minDimensions[1]`, `51` to `87`. Binary comparison finds
exactly four changed bytes at offsets `614306`, `614307`, `614320`, and
`614321`.

The new persistent checks prove the two hashes and both dimension vectors;
`[columns, rows]` ordering; one `Results` tab; exact 51-column header and
87-row bounds through `AY87`; bounded cell/data/style/formula/image/reference
and named-cell addresses; generic A:C context and blank D:AY on rows 2:87; no
fixture-specific Test ID; the exact semantic and four-byte binary difference;
and the unchanged parser upload-artifact hash.

## Architecture result

- Worksheet tabs: exactly one, `Results`.
- Worksheet dimensions: 87 rows by 51 columns (`A:AY`).
- Context-owned range: `A:C`.
- Parser-owned range: `D:AY`, matched rows only.
- Dynamic context rows: 2:87, using `tests[0]` through `tests[85]`.
- Batch-service constructions per run: exactly one.
- Batch updates per run: exactly one.
- Dynamic update keys: exactly `["Results"]`.
- Worksheet calculations: `run_worksheet_calculations: true`.
- Test service operations: zero.
- Direct Test writes or lifecycle mutations: zero.
- Cross-tab reads/writes: zero.
- Repair or retry updates: zero.

## Exact Results schema

| Column | Header |
|---|---|
| A | Sample ID |
| B | Test ID |
| C | Product Matrix |
| D | LabSolutions Sample Name |
| E | Sample Type |
| F | Vial |
| G | Sample Amount |
| H | Dilution Factor |
| I | DF Application Mode |
| J | α-Pinene |
| K | Camphene |
| L | β-Myrcene |
| M | (-)-β-pinene |
| N | Delta-3-carene |
| O | α-Terpinene |
| P | cis-Ocimene |
| Q | d-Limonene |
| R | p-Cymene |
| S | trans-Ocimene |
| T | Eucalyptol |
| U | γ-Terpinene |
| V | Terpinolene |
| W | Linalool |
| X | (-)-Isopulegol |
| Y | Geraniol |
| Z | β-Caryophyllene |
| AA | α-Humulene |
| AB | cis-Nerolidol |
| AC | trans-Nerolidol |
| AD | (-)-Guaiol |
| AE | Caryophyllene Oxide |
| AF | (-)-α-Bisabolol |
| AG | Dimethylacetamide |
| AH | Unknown Peak Count |
| AI | Manual Integration |
| AJ | Integration Review Status |
| AK | Source Instrument File |
| AL | Source File Hash |
| AM | Source Data File |
| AN | Source Method File |
| AO | Source Sequence File |
| AP | Acquired At |
| AQ | Instrument Name |
| AR | Detector ID |
| AS | Detector Name |
| AT | Parser Version |
| AU | Compound Result Row Count |
| AV | Peak Table Row Count |
| AW | Reportable Compound Row Count |
| AX | Source Row Hash |
| AY | Import Status |

The worksheet candidate contains no formulas. A:C contain only the generic QBench dynamic `tests[i]` context expressions and no fixture-specific Test IDs. `AY` is the parser-written literal `Imported`.

## Analytical and mapping result

- Complete LabSolutions records parsed: 34.
- Controlled Compound Results rows per record: 24.
- Controlled reportable Terpenes analytes per record: 23.
- Dimethylacetamide audit rows per record: 1.
- Candidate rule: category `Sample` plus nonblank `Sample Information > Sample ID`.
- QBench Test display-ID source: exact LabSolutions Sample ID.
- C6 candidate IDs: exactly `["308", "309"]`.
- Rows staged from the C6 fixture: exactly 2.
- Other/control/validation records validated and skipped: 32.
- Low/Medium/High validation labels are controls for persistence in V1.
- P1 and P2 each matched every hard-coded expected 23-analyte test vector.
- Dilution Factor is captured; `DF Application Mode` is `already_applied_by_labsolutions`; no parser calculation applies the factor again.
- Manual integration recognizes LabSolutions `M` tokens and explicit manual labels.
- Unknown Peak Count and integration-review evidence are retained.

## Read-after-write result

After the sole update callback, the parser performs one second dynamic worksheet retrieval. It verifies:

- every parser-owned D:AY value on every matched row;
- numeric equality with equivalent numeric-string representations accepted;
- unchanged A:C on all rows;
- unchanged unmatched rows;
- unchanged formulas, images, and dollar references;
- unchanged unique candidate Test-ID row mapping;
- candidate and verified-row count equality.

Missing, changed, no-op, context-mutating, row-removing, and unmatched-row-mutating readbacks all fail with `RESULTS_WORKSHEET_UPDATE_NOT_PERSISTED`. `QB.success` is called only after successful verification. No failed readback triggers another update.

## Immutable staged runtime input

The byte-level source is the protected file:

`C:\Users\Mark Adams\Documents\GitHub\qbench\QBench\Worksheets\Terpenes\development\2026-07-15_qbench_native_parser_probe\runtime\terpenes_c6_308_309_runtime_source.txt`

- SHA-256: `5de17d8f9eb21a8dfc068daf2297efb707a8b783f63393df432781e5e692e6aa`
- Bytes: 286,204
- Encoding: strict UTF-8 without BOM
- Line endings: CRLF only
- Final newline: CRLF retained

The new immutable staged input is:

`C:\Users\Mark Adams\Documents\GitHub\qbench\QBench\Worksheets\Terpenes\development\2026-07-25_terpenes_simple_results_v1\runtime\terpenes_simple_results_310_311_runtime_source.txt`

- SHA-256: `1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e`
- Bytes: 286,204
- P1 contracted Sample ID: `308` to `310`
- P2 contracted Sample ID: `309` to `311`
- Changed byte positions: `124301`, `124302`, `133048`, and `133049`
- Changed-byte count: exactly 4
- Inserted or deleted bytes: 0

Restoring only those two context-bound Sample ID values makes the target text
identical to the protected source. Record count, record order, Sample Names,
Sample Types, Vial values, sections, tabs, whitespace, blank lines, source
paths, dates, times, units, line endings, BOM state, encoding, and final
newline behavior are unchanged.

All 34 records parse and validate. Each retains 24 controlled Compound Results
rows, 23 ordered reportable analytes, and one Dimethylacetamide audit result.
An entire parsed-record comparison, excluding only the two contracted Sample
ID fields and their derived `source_row_hash` fields, is exact for every
record. The 23 analyte values, Dimethylacetamide values, Compound Results and
Peak Table counts, reportable counts, manual-integration evidence, unknown
peak counts, integration-review decisions, source filenames, acquisition
metadata, instrument metadata, and detector metadata are preserved.

The parser-consumed candidate set is exactly `["310", "311"]`. P1 is record
17 and the human-reviewed Source role for Test `310`; P2 is record 18 and the
human-reviewed Target role for Test `311`. The new source-file hash is expected
to differ from the protected input hash. Deterministic new Source Row Hashes
are:

- P1/Test 310: `4743eb576c968d981670da6cd4addb81cd417aedbaf1fc687d0d0a3b10e80721`
- P2/Test 311: `3c0bfcdd128a8678a18ce137d593fad7da500e1d16b48a6b312aa4a7b3207f8d`

The local Sandbox-state mock uses BATCH-62/internal Batch ID `62`, Sample
`AIT-SAMP-170`, Product Matrix `Cannabis Concentrates`, Test `310` in Results
row 2, and Test `311` in Results row 3. Both candidates resolve exactly once
and only to Batch `62`. A:C remain:

- row 2: `AIT-SAMP-170`, `310`, `Cannabis Concentrates`
- row 3: `AIT-SAMP-170`, `311`, `Cannabis Concentrates`

The parser stages all D:AY values on exactly rows 2 and 3, including the new
Source File Hash, deterministic Source Row Hash, Parser Version
`terpenes-simple-results-v1`, and Import Status `Imported`. Rows 4:87 remain
unchanged and blank. Controls are parsed and validated but are not candidates
and do not map to Results.

The successful mocked runtime constructs one `QBBatchService` and submits one
update with Batch ID `62`, exactly one
`qb_dynamic_spreadsheet_data.Results` payload, and
`run_worksheet_calculations: true`. It constructs no Test service, performs no
direct Test write, and performs no second Batch update. Readback verifies both
rows and preserves all A:C context. Missing or duplicate 310/311 rows,
alternate or partial Batch resolution, an unknown candidate, a no-op update,
a changed persisted value, and changed A:C context all fail closed.

This phase performed no browser, QBench, Sandbox, Production, network, Git,
GitHub, or PR #14 action. The new runtime input has not been uploaded or
executed.

## Focused test execution

Working directory:

`C:\Users\Mark Adams\Documents\GitHub\qbench\QBench\Worksheets\Terpenes\development\2026-07-25_terpenes_simple_results_v1`

Exact command:

`node tests\test_terpenes_simple_results_parser.js`

Result:

- Total: 97
- Passed: 97
- Failed: 0
- Skipped: 0

All 45 original checks remain present and passing. They continue to cover the
single-tab worksheet architecture, strict 34-record/24-compound/23-analyte
parsing, Dimethylacetamide and Unicode handling, Sample/Test mapping failures,
the single Batch-service/single Results-update boundary, cell ownership,
read-after-write failures and ordering, and the exact C6 fixture/hash/analyte
expectations.

Eight added dimension checks cover: exact original/corrected hashes and
`minDimensions`; columns-then-rows ordering; one Results tab with 51 headers
through AY and 87 rows; the AY87 address ceiling; generic A:C and blank D:AY;
the exact semantic-only difference; the exact four-byte binary difference; and
the unchanged parser artifact hash.

Forty-four additional staged-fixture checks cover the immutable 310/311 input,
the exact four-byte context-bound transformation, full analytical
preservation, the Source/Target role contract, BATCH-62-only resolution,
Results rows 2 and 3, A:C preservation, D:AY-only staging, untouched rows
4:87, control exclusion, the single Results-tab Batch update, readback
failures, source and row hashes, parser version, and the controlled `Imported`
literal.

Only this focused test file was run. No repository-wide test, package script,
dependency install, generator outside the isolated directory, or package
manager was used.

## New artifacts and hashes

| File | Bytes | SHA-256 |
|---|---:|---|
| `dist/terpenes_simple_results_parser_v1.js` | 41,416 | `bcec7bf0aa1f0b3edfab6ff2f6bcf370abf863226a81472714202aca5efbc871` |
| `runtime/terpenes_simple_results_310_311_runtime_source.txt` | 286,204 | `1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e` |
| preserved diagnostic `SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1.json` | 766,266 | `ce50d670be71fccf02912b30cacb918fd48916e8f154a164b095f8f0670a96be` |
| corrected `SBX_ONLY_TERPENES_SIMPLE_RESULTS_BATCH_WS_V1__dimension_fix.json` | 766,266 | `f8d58b33024cce2bf90171df79c7f73e984674fa64b83f99e8030935f9030448` |
| `src/terpenes_simple_results_parser.js` | 41,295 | `d0d55df9d870d8ec8a197259e3013e47063a1d2c2ad92ed1cfe0b440967bcc94` |
| `scripts/build_terpenes_simple_results_parser.js` | 4,651 | `33ea45546181d6552bbf4e07952a7c7cc1cb425962aa3abf6c7359b696eb4108` |
| `tests/test_terpenes_simple_results_parser.js` | 53,691 | `b87b98845979cfe99ada3f93184d84f82d79792ed1cd6dcca3fd6cef343a233b` |
| `TERPENES_SIMPLE_RESULTS_V1_SPEC.md` | 7,237 | `880f95b7ec55bd60096c41406026ed3716317d6ec7fe44dde821e2b5b19166a9` |

Fixture:

- `terpenes_c6_308_309_runtime_source.txt`
- Bytes: 286,204
- SHA-256: `5de17d8f9eb21a8dfc068daf2297efb707a8b783f63393df432781e5e692e6aa`

## Protected artifact proof

The following pre-implementation hashes were rechecked after build and test. Every value remained exact:

| Protected file | Pre SHA-256 | Post SHA-256 |
|---|---|---|
| deployed V2 `dist/terpenes_multirecord_qbench_parser.js` | `c3f3ecccf346ce1a1338911ee3bcb45ab4c43342d93bcee7b74b2c70fc847e99` | same |
| V3 `dist/terpenes_multirecord_qbench_parser_c6_headerfix_v3.js` | `5a849a6cf3f78784f728cd89d6665310ddc04e299f769bd3ef5e646e31203e85` | same |
| immutable C6 input | `5de17d8f9eb21a8dfc068daf2297efb707a8b783f63393df432781e5e692e6aa` | same |
| worksheet-78/current Batch candidate `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v2_formula_fix.json` | `50fb7883a6932bc54b09f6997b91f01674e392696e82f77872935bb00576acda` | same |
| browser parser core | `d1843770db39cdc65ac20473773fe5891fceb63caeb9a18b91e7c1ccad88529b` | same |
| multi-record Batch adapter | `e54d77e0c5add16eb1a15fbed3563eb210ea49b6d55149a5939d5fb35c3a7f49` | same |
| existing runtime template | `755506555d824287a5909d0ca575d52c93af6f904c644b3edfae36f780f32256` | same |
| existing parser builder | `179c8b2b4f1b9dc2f25e79f8d4bbd14ea2f42f580513443dd94897103c8fc0cc` | same |
| existing focused parser test | `5bb7ac89182362942bc8b0cff3e30fa18607faf5cfc8e040494d25c815f685b4` | same |
| existing analytical core | `f73106170a9062f52b393ae2e64efcdc08a290c4605185030fb89ee3aec20e8e` | same |
| repository `.gitignore` | `b98f0afdafec7c10c40bc903d5d3f66bfa97546e708eed3a79b1925a6d34d21a` | same |

The working reference files also remained unchanged:

- `C:\Users\Mark Adams\Downloads\Potency parser.txt`: `61f91070e0b68b5c5c06de580efe0569d13075a032441968e9d43bec763c1d9e`
- `C:\Users\Mark Adams\Downloads\Cannabinoid Potency [Batch] Worksheet.json`: `f0af97d253a4ccca2d6fe577bb9eafd8ade3e305cf4b1257cfe7cbe149552f65`
- `C:\Users\Mark Adams\Downloads\terpene parser.txt`: `8c3cbaf4e144ca1a181fd9c4b6ef41f172114199a5b47969fa39c45ac3d1002d`

No package or lock file exists in this repository inventory, and none was created.

## Files inspected

- `QBench/Worksheets/Terpenes/TERPENES_CURRENT_STATE.md`
- `QBench/Worksheets/Terpenes/AGENTS.md`
- working Potency parser and Batch worksheet in Downloads
- `Output (1).csv` in Downloads, read-only
- `terpene parser.txt` in Downloads, read-only
- protected V2 and V3 Terpenes browser artifacts
- protected current Terpenes production-candidate Batch worksheet
- protected immutable C6 source
- current browser analytical core, adapter, runtime template, builder, and focused tests
- controlled Terpenes analyte configuration
- Phase 4B.2 parser contract and mapping

## Repository changes

Repository changes for this local runtime-input phase are exactly:

- new `runtime/terpenes_simple_results_310_311_runtime_source.txt`;
- modified `tests/test_terpenes_simple_results_parser.js`;
- modified `TERPENES_SIMPLE_RESULTS_V1_SPEC.md`;
- modified `TERPENES_SIMPLE_RESULTS_V1_VALIDATION.md`;
- appended `QBench/Worksheets/Terpenes/TERPENES_CURRENT_STATE.md`.

The parser source, builder, browser-upload parser artifact, both worksheet
candidates, protected diagnostic input/artifacts, package files, lockfiles, and
`.gitignore` were not modified.

## Staged Sandbox binding contract and next boundary

The already completed Sandbox staging established:

- worksheet `79`, active version `1`, one Results tab, `A:AY`, rows `1:87`;
- parser `42`, active version `1`, assay `21`, with Trigger and Filename Should
  unset and Filename Text blank;
- BATCH-62/internal Batch ID `62`;
- AIT-SAMP-170/internal Sample ID `170`;
- Source Test `310` in Results row 2;
- Target Test `311` in Results row 3.

This local phase did not inspect or change those QBench objects. The next
separately authorized boundary is to configure parser `42` with the
Batch-attachment trigger and exact filename
`terpenes_simple_results_310_311_runtime_source.txt`, then perform one
controlled isolated Sandbox upload/execution using the immutable file with
SHA-256
`1e5087715a9bcf216c2991cca53f41fb4ae84b4f9e80eea0e95d7618ec77a36e`.
