# Probe security review

Source and generated JavaScript are statically checked for prohibited
network, dynamic-code, browser-storage, credential, cookie, full-entity-write,
and result-outcome capabilities. The no-write probe contains no worksheet
service reference. Patch probes accept only an injected documented service and
emit narrow `data` objects containing controlled named fields.

The corrected Stage 1 no-write runtime:

- classifies `QB.files` only as `Array`, `array_like`, or `unknown` without
  serializing the runtime object;
- accepts a finite nonnegative integer collection length and requires exactly
  one file;
- retrieves index `0`, with `item(0)` only as a controlled fallback;
- rejects a missing file object, the wrong exact fixture name, or a file read
  failure with stable controlled error codes;
- does not use `Array.from` for file-collection normalization;
- logs only sanitized step names, collection kind, counts, accepted extension,
  Web Crypto availability, controlled error code, and failed step;
- invokes `QB.success()` only after the controlled parse completes;
- contains no `patchWorksheet`, `updateWorksheet`, `QBBatchService`, `fetch`,
  `XMLHttpRequest`, `eval`, Function constructor, `localStorage`, or cookie
  access.

The browser parser:

- accepts text only and strips a UTF-8 BOM;
- normalizes CRLF, CR, and LF;
- enforces file, line, section, field, and row limits;
- validates exactly 24 Compound Results rows and 23 reportable rows;
- retains one Dimethylacetamide audit row and all Peak Table audit rows;
- rejects unknown Compound Results names, ID/name mismatches, duplicates,
  missing rows, and malformed numeric concentration text;
- preserves numerical zero and negative JavaScript Number values;
- never emits raw file text, credentials, QBench IDs, or live analyte values
  to the runtime console;
- performs no worksheet write.

The controlled fixture copy is redacted and hash-locked. No customer or
production information is included. No production parser candidate exists.

The initial Stage 1 Preview failed safely before a successful parse result was
reported. The corrected retry observed only the sanitized collection kind
`array_like`, completed all controlled parse/count checks, reported Web Crypto
available, and reached `QB.success()`. This confirms the Array-only runtime
compatibility problem without logging or claiming a specific collection
constructor. Neither attempt invoked a worksheet service or modified a
worksheet or parser-result destination. The parser remained inactive/DRAFT
with no trigger or assay.

The Stage 2A read-only probe:

- calls only `Object.keys(QB)` plus controlled own-property presence and value
  type checks for five candidate Batch-context keys;
- does not serialize `QB`, inspect nested objects, or dereference any security,
  authorization, session, or identifier value;
- logs no file contents, paths, QBench IDs, credentials, cookies, or storage;
- contains no worksheet service or destination-write capability;
- produced two existing identical sanitized output groups after accidental
  Preview execution; Codex did not rerun Preview;
- observed all five candidate Batch-context paths absent with type `undefined`;
- left the parser inactive/DRAFT with trigger and assay unset.

The UI showed one controlled selected file. File metadata was not emitted
because `QB.files` was array-like rather than a true Array, but the independent
Batch-context presence/type checks completed. The recorded outcome is
`not_available_in_preview_runtime`; no internal Batch ID was exposed, captured,
or committed.

The Stage 2B attachment-context probe:

- uses a fixed allowlist rather than enumerating the runtime object;
- checks only own-property presence and classifies values as `undefined`,
  `null`, `array`, or the JavaScript `typeof` result;
- logs property paths, presence booleans, and value types only;
- never logs a Batch ID, attachment ID, job ID, runtime value, file content,
  customer/sample data, credential, cookie, token, or storage value;
- contains no worksheet service, patch, full replacement, network request,
  dynamic code, browser storage, or destination-write capability;
- was configured only for Batch attachments whose filename exactly equals the
  controlled redacted fixture name;
- ran once against the exact authorized disposable Sandbox Batch;
- produced one persisted `SUCCESS` job-history record;
- was deactivated after the controlled attachment upload.

The persistent QBench history view did not retain the safe `QB.console` lines.
No candidate property presence, absence, path, or type is therefore claimed
from Stage 2B. Browser diagnostics contained no retained matching lines. The
controlled attachment is the only authorized runtime-data change and remains
as evidence. The approved version remains marked active only inside the
disabled parser because the available alternative was irreversible
obsolescence, which was canceled. No internal identifier is committed.
