# Prompt 4.6C duplicate upload results

The same exact canonical file was uploaded a second time to
`SBX_ONLY_TERPENES_2026_07_16_NO_CODE_IMPORT_01`.

Observed behavior:

- QBench kept one attachment record and advanced it from version 1 to version 2;
- the version-2 attachment triggered a second parser job;
- File Parser History reported `SUCCESS` for the second Batch Worksheet job;
- Instrument Import row 2 remained the canonical deterministic row;
- AF2 remained `Valid` and AG2 remained `Import row valid`;
- the audit counts remained numeric `24`, `34`, `23`, and `100`;
- the 23 AH:BD analyte cells remained numeric and BE2 retained the exact
  source-row hash;
- row 3 remained blank, so the duplicate did not append another import row;
- Publish remained blank and the Batch still had no tests.

The duplicate is therefore versioned at the attachment layer and idempotent at
the configured fixed worksheet targets. This is observed old-Sandbox behavior,
not a production guarantee.
