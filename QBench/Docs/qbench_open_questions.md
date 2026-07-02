# QBench Open Questions

- COA report template ID 26 exposes a Visual Editor but no visible source export/copy/download control. Active version 17 was selected read-only; source HTML was not extractable from the DOM inspection.
- COA assets were visible as QBench attachment download links, including `AIT Watermark.png`, `CoA Signatures.png`, `Header Image.png`, `hexagon-grid-8tile-1336x618.png`, `hexagon-grid.png`, and `Quality Control Verified.png`. Browser download attempts did not create local files, so assets were not saved into the repo.
- Confirm whether active report template ID 44 `Homogeneity` is used for production/sandbox Homogeneity COAs or only retained separately; inspected assays listed Certificate of Analysis Report as default.
- Parser internals for no-code parsers were not fully visible from read-only detail pages, and no parser export/download option was visible.
- File parser code pages did not expose a parser-specific export/copy control. Parser 46 showed only `importScripts('https://d30nr38ylt5b32.cloudfront.net/v1.1.0/file_parser.js');`; parser 45 showed only `// Prod template` in the visible editor summary.
- Automation condition rows were not fully exposed in the compact read-only extraction; worksheet-field actions were visible and indexed.
- Moisture Analysis, Stability, and general Microbial Analysis did not show configured assay-level worksheet templates during inspection.
