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
reported. It invoked no worksheet service and modified no worksheet or parser
result destination. The parser remained inactive/DRAFT. The FileList cause is
not treated as proven until the corrected retry diagnostics run.
