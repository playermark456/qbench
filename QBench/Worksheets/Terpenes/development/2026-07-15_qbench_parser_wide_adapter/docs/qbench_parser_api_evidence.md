# QBench parser API evidence

## Evidence status

`runtime-contract evidence status = missing_exact_qbench_runtime_contract`

`qbench_native_status = blocked_missing_qbench_runtime_contract`

## Repository evidence found

| Claimed API or field | Evidence source | Exact observed code or field | Confidence | Implementation consequence |
|---|---|---|---|---|
| Parser library URL | `QBench/Docs/qbench_open_questions.md`; `QBench/FILE_PARSER_INDEX.md` | `importScripts('https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js');` visible for parser ID 46 | Medium: visible read-only summary only | The template records this URL, but no candidate wrapper is emitted. |
| Code parser exists in Sandbox | `QBench/FILE_PARSER_INDEX.md` | Parser ID 46, Cannabinoid Potency Parser, type Code | Medium | Existing parser proves QBench has code parser capability, not the Terpenes runtime API. |
| Parser export unavailable | `QBench/FILE_PARSER_INDEX.md`; `QBench/Docs/qbench_open_questions.md` | No parser-specific export/download control visible | High from repository notes | Cannot prove entry-point, input, output, write, or error APIs from repository alone. |

## Evidence not found

| Missing API evidence | Status | Consequence |
|---|---|---|
| Parser entry-point function | Not found | No paste-ready QBench parser candidate created. |
| Input file object shape | Not found | Wrapper cannot safely read text/bytes in QBench. |
| Text/byte access method | Not found | Wrapper cannot prove UTF-8/BOM handling in QBench. |
| Output API | Not found | Wrapper cannot safely return parser output. |
| Worksheet destination/write API | Not found | Wrapper cannot target Instrument Import blocks. |
| Error-reporting API | Not found | Wrapper cannot prove controlled failure behavior. |
| File-extension registration | Not found | `.txt` acceptance remains installation evidence to collect. |
| Assay attachment behavior | Not found | Sandbox parser assignment cannot be documented as exact UI behavior. |
| Return-vs-write parser behavior | Not found | No direct QBench wrapper emitted. |
| Transactional writes | Not found | Native status remains blocked. |
| JavaScript Number write semantics | Not found | Native status remains blocked until numeric writes are proven. |
| Specific batch worksheet tab/range targeting | Not found | Wrapper cannot safely write A:AE and AH:BE. |

## Preflight record

Direct PATH checks failed for `git --version`, `node --version`, and
`py --version`. Bundled Codex runtime tools were available:

| Tool | Version |
|---|---|
| Git | `git version 2.53.0.windows.3` |
| Node.js | `v24.14.0` |
| Python | `Python 3.12.13` |

Controlled dependency hashes:

| Dependency | Raw checkout SHA-256 | Canonical LF SHA-256 | Controlled outcome |
|---|---|---|---|
| Prompt 3 Test candidate | `90686b980882b221008f281be33984dc5232e2f3d2632300db3f4a27b529640a` | `90686b980882b221008f281be33984dc5232e2f3d2632300db3f4a27b529640a` | Accepted |
| Prompt 4 Batch candidate | `f779d0175a7aec09eb5f57a778fde91cccf07bb7078a9573132547ee158da151` | `e5c80b1213396cab4932e267fd786c6986c933d4b404f11daa5c5aba0629758e` | Accepted by canonical LF hash |
| Prompt 4 layout config | `7f1270063f689f9cac94ee22e4f69b0ea7953a6f5dc86e1f6b4c00bb4bed7ef0` | `fe137404165a044907a7fe31a7cc386f53f402bb643dd94bf2fbffe958571410` | Canonical matches Prompt 4 manifest |
| Prompt 4 import contract config | `7382a15789f8771b2888c908e69811898e5213454ec380d8efc68c0b7488b72a` | `b389c3d96447d6c3dfb5c879d3a624ce5f05bb39b16951305f609febe77f9a23` | Canonical matches Prompt 4 manifest |

The Prompt 4 Batch candidate is controlled by the canonical LF hash. The raw
Windows checkout hash mismatch is recorded and is not a dependency failure
because canonical LF SHA-256 matches the controlled value.

Baseline result summary:

| Package | Result |
|---|---|
| Prompt 2 validation/parser/tests | Passed; 27 tests; fixture 24/34/23 |
| Prompt 3 generator/validator/tests | Passed; generator hash matched; validator passed; 50 tests |
| Prompt 4 generator/validator/tests | Passed during controlled baseline build; 39 tests; canonical LF hash matched the controlled Prompt 4 hash |
| Prompt 4.5 JavaScript tests | Passed; 122 tests |
| Prompt 4.5 Python tests | Passed; 11 tests |

Sandbox validation evidence status in the generated manifest:

| Validation record | Status | Path | SHA-256 |
|---|---|---|---|
| Test Worksheet Sandbox validation | `not_recorded_in_repository` | `null` | `null` |
| Batch Worksheet Sandbox validation | `not_recorded_in_repository` | `null` | `null` |
| End-to-end QBench parser validation | `not_recorded_in_repository` | `null` | `null` |

Local untracked Sandbox notes are not used as generated evidence.
