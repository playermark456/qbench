# QBench Open Questions

- COA report template ID 26 exposes a Visual Editor but no visible source export/copy/download control. Active version 17 was selected read-only; source HTML was not extractable from the DOM inspection.
- COA assets were visible as QBench attachment download links, including `AIT Watermark.png`, `CoA Signatures.png`, `Header Image.png`, `hexagon-grid-8tile-1336x618.png`, `hexagon-grid.png`, and `Quality Control Verified.png`. Browser download attempts did not create local files, so assets were not saved into the repo.
- Confirm whether active report template ID 44 `Homogeneity` is used for production/sandbox Homogeneity COAs or only retained separately; inspected assays listed Certificate of Analysis Report as default.
- Parser internals for no-code parsers were not fully visible from read-only detail pages, and no parser export/download option was visible.
- File parser code pages did not expose a parser-specific export/download control. A later read-only editor inspection captured parser 46's complete active source and parser 45's visible template without invoking Save, Set Active, Preview, or file selection. Both import `file_parser.js` 1.1.0 and `qbjs.js` 2.7.0 and use the documented `run`/`QB` base model.
- Automation condition rows were not fully exposed in the compact read-only extraction; worksheet-field actions were visible and indexed.
- Moisture Analysis, Stability, and general Microbial Analysis did not show configured assay-level worksheet templates during inspection.

## Prompt 4.6 targeted QBench support request

The first two runtime questions were resolved by current-tenant read-only
inspection. The remaining questions are maintained in the sanitized support
request:

`QBench/Worksheets/Terpenes/development/2026-07-15_qbench_parser_wide_adapter/docs/qbench_prompt_4_6_support_request.md`

Current status:

`qbench_runtime_contract_status = insufficient_for_prompt_4_6`
