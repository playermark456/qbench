# Runtime contract updates

## Merged preflight evidence

- `qbench_runtime_contract_status = insufficient_for_prompt_4_6`
- `qbench_sandbox_probe_status = sufficient_to_begin_controlled_prompt_4_6_probe`

Official QBJS v2.7.0 documentation records two materially different Batch
worksheet behaviors: full worksheet replacement removes the safety boundary
needed here, while the patch method updates only included data and preserves
omitted worksheet data. Only the patch method may be investigated in this
probe. Spreadsheet named ranges, one- and two-dimensional arrays, numeric-cell
typing, noncontiguous blocks, request atomicity, partial writes, and rollback
remain Sandbox questions.

The current tenant evidence records the exact File Parser import URL for
`file_parser.js` 1.1.0. It records `qbjs.js` version 2.7.0 but does not record
the full current-tenant QBJS import URL. Stage 1 therefore imports only the
exact proven File Parser URL and makes no service call. Later patch probes are
locally testable libraries but are runtime-guarded; no QBJS URL is guessed.

Batch context is not yet known. The raw LabSolutions file contains no QBench
Batch ID, and no final parser may require, infer, log, or hardcode one.

## Stage 1 runtime observation

The first authorized no-write Preview selected one controlled fixture and
entered the runtime, but returned `UNEXPECTED_PARSE_ERROR`. No worksheet
service or destination write occurred, and the controlled parser remained
inactive/DRAFT with no trigger or assay.

The initial probe assumed `Array.isArray(QB.files)`. The corrected retry
observed `file collection kind = array_like`, accepted the one controlled file,
completed the controlled parse, reported the exact 24/34/23/1 counts, reported
Web Crypto available, and reached `QB.success()`. This confirms the Array-only
runtime compatibility problem. The specific browser collection constructor
was intentionally not logged. The proven Stage 1 boundary now accepts Arrays
and finite, nonnegative-integer-length array-like objects, requires exactly one
entry, retrieves index `0` or `item(0)`, and emits only a sanitized collection
kind plus stable controlled errors.

Stage 1 passed.

## Stage 2A draft Preview observation

The separately authorized read-only Stage 2A probe was saved as a second
inactive/DRAFT version. The existing console contained two identical completed
output groups after Preview was accidentally invoked. Codex did not rerun it.
Both groups completed the controlled presence/type checks and observed:

- `QB.batch`: absent; type `undefined`;
- `QB.currentBatch`: absent; type `undefined`;
- `QB.context`: absent; type `undefined`;
- `QB.fileParserContext`: absent; type `undefined`;
- `QB.attachment`: absent; type `undefined`.

Therefore `batch_context_status = not_available_in_preview_runtime`. No safe
Batch-context property path or value type was established. This is an observed
draft Preview result, not an official documented runtime contract. The probe
serialized no runtime object and dereferenced no security, authorization, or
session value.

The UI showed one selected controlled file. File metadata was not printed
because the helper maps only true Arrays while this tenant supplies an
array-like `QB.files` collection. That limitation does not affect the completed
Batch-context presence/type checks and does not justify a Stage 2A retry.

No worksheet service, destination write, activation, trigger, or assay was
used. Stage 2B has not started and remains separately authorized.
