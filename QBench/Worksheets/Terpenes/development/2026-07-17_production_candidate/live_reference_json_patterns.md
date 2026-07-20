# Live non-Terpenes worksheet JSON patterns

## Observed envelope conventions

- Top-level objects include `config`, `qb_config`, and `data`.
- `config.worksheets` carries worksheet definitions.
- Every inspected worksheet had a UUID-shaped `worksheetId`.
- Old-renderer metadata was present: `rows`, `columns`, `minDimensions`, `tableHeight`, `tableWidth`, worksheet `style`, and `mergeCells`.
- In the inspected exports, top-level `config.style` was an array and worksheet-level `style` was an object. These types must be preserved from the chosen structural base.
- Formula cells were serialized as leading-`=` strings in worksheet data, not as a separate `formula` property.
- The inspected multi-tab Test definitions used sheet-qualified named-cell addresses.
- The inspected single-tab Batch definitions had no named cells, so they do not overturn the proven old-Sandbox one-tab requirement for unqualified imported named-cell addresses.
- No merge ranges were populated in the safe reference set; `mergeCells` still existed as renderer metadata.

## Dual data representation

The worksheet-level data and top-level `data[worksheetName]` representations were not always byte-for-byte identical in live exports. A validator must compare their rendered/semantic cell content after normalizing the export representation. Literal equality remains appropriate only when a controlled candidate contract explicitly requires it.

## Named-cell conventions

- Use unique, stable system names.
- Use one named scalar per independent input when API or parser destinations require scalar writes.
- Use an explicit bounded range for COA embedding, such as `report_results`.
- Multi-tab references should be sheet-qualified in logical documentation and in live multi-tab definitions.
- For the proven old-Sandbox single-tab import path, keep the QBench JSON `cell` representation unqualified while retaining a sheet-qualified logical address in mapping documentation.
- Never infer address format solely from another renderer/version; round-trip the exact saved Draft.

## Generation and round-trip rules

1. Start from a raw export known to render in the target QBench generation.
2. Preserve config/style types, row/column metadata, cell metadata, dimensions, and top-level data representation.
3. Generate fresh worksheet UUIDs; do not preserve source-specific IDs.
4. Preserve style indexes and their referenced style table; do not renumber opportunistically.
5. Treat property ordering, UUID replacement, and representation normalization as harmless only after semantic validation.
6. Reject missing tabs, dimension changes, style-type changes, formula text changes, named-cell changes, or address changes.
7. Save, reopen from the Worksheets list, and use **Export Spreadsheet** for the round-trip proof.
