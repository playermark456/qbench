# Probe security review

Stage 0 source and generated JavaScript are statically checked for prohibited
network, dynamic-code, browser-storage, credential, cookie, full-entity-write,
and result-outcome capabilities. The no-write probe contains no worksheet
service reference. Patch probes accept only an injected documented service and
emit narrow `data` objects containing controlled named fields.

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
