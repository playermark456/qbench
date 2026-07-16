# QBench runtime probe results

## Stage 0

- Authorization: initial Prompt 4.6 submission.
- Repository preparation: completed.
- QBench accessed: no.
- QBench objects changed: none.
- Parser created, saved, previewed, run, or activated: no.
- Worksheet imported: no.
- Batch created or modified: no.
- Attachment selected, uploaded, or attached: no.
- Worksheet service invoked: no.
- Prompt 5 started: no.

## Stage 1 — initial attempt

- Authorization: `AUTHORIZE STAGE 1 — NO-WRITE QBENCH RUNTIME PREVIEW`.
- Evidence reference: `stage_1_initial_attempt_method_owner_report_2026-07-15`.
- Controlled parser: `ZZZ_SANDBOX_ONLY_Terpenes_Runtime_NoWrite_Probe`.
- Parser status: inactive; version status `DRAFT`.
- Trigger and assay: unset.
- Selected input: one controlled `Output_redacted_fixture.txt` file.
- Preview executed: yes.
- Sanitized Preview output: `controlled error = UNEXPECTED_PARSE_ERROR`.
- QBench UI behavior: a transient red error notification appeared and then
  disappeared.
- Worksheet service invoked: no.
- Worksheet or File Parser Results destination modified: no.
- Parser activated: no.
- Stage result:
  `failed_safely_runtime_file_collection_compatibility`.

The initial attempt did not produce enough diagnostics to distinguish the
file-collection hypothesis from another unexpected runtime exception. The
corrected retry later observed `file collection kind = array_like` and passed,
confirming the Array-only compatibility problem. The specific browser
collection constructor was intentionally not logged.

## Stage 1 — corrected retry result

- Evidence reference: `stage_1_corrected_preview_sanitized_console_2026-07-15`.
- File collection kind: `array_like`.
- File count: 1.
- Accepted extension: `.txt`.
- Compound Results rows: 24.
- Peak Table rows: 34.
- Reportable channels: 23.
- Dimethylacetamide audit rows: 1.
- Web Crypto available: `true`.
- `QB.success()` reached: yes; it immediately follows the final sanitized log
  in the controlled execution path.
- Controlled error or failed-step output on retry: none.
- Worksheet service invoked: no.
- Worksheet or File Parser Results destination modified: no.
- Parser state after Preview: inactive; version `DRAFT`.
- Trigger and assay after Preview: unset.
- Stage result: `passed`.

The corrected no-write draft accepts either a JavaScript Array or a finite,
nonnegative-integer-length array-like collection. It requires exactly one
entry, uses index `0` and then `item(0)` as a controlled fallback, requires a
nonblank file object, and preserves the exact filename and case-insensitive
`.txt` extension gates. It does not serialize or log the collection and does
not use `Array.from` for collection normalization.

Expected validation failures now carry stable codes:

- `CONTROLLED_FILE_COLLECTION_ERROR`
- `CONTROLLED_FILE_COUNT_ERROR`
- `CONTROLLED_FILE_OBJECT_ERROR`
- `CONTROLLED_FILE_NAME_ERROR`
- `CONTROLLED_FILE_READ_ERROR`

The retry logs only sanitized execution steps, collection kind, file count,
accepted extension, controlled row/channel counts, Dimethylacetamide audit
row count, Web Crypto availability, controlled error code, and failed step.
It does not log raw text, analyte values, sample information, paths, IDs,
runtime objects, cookies, or credentials.

Correction validation: 44 Prompt 4.6 JavaScript tests and 16 Prompt 4.6
Python/static tests passed. The generated distribution and manifest were
byte-identical across repeated builds. Stage 1 is `passed`.

## Later stages

Stages 2A through 7 are `not_run`. Stage 2A has not started and requires its
own exact authorization phrase. No later-stage result is implied by Stage 1.
