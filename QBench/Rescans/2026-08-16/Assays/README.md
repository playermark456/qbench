# Assays — 2026-08-16

The production assay list and all 20 detail pages were opened serially in read-only mode. All 20 displayed assays were active. No customer, sample, test, order, batch, technician, or team values were retained.

## Evidence

- `assay_inventory.json` — complete safe detail-page metadata.
- `assay_inventory.csv` — flat assay/worksheet/protocol summary.
- `QBench/ASSAY_ID_MAP.md` — canonical current ID map.

## Findings

- Assay ID 21, **Pesticides Quantitative Flower**, is present and was absent from the earlier 19-row canonical map.
- General Microbial Analysis ID 6 currently exposes test worksheet 44 and batch worksheet 45; the prior canonical note that no assay-level worksheets were visible is no longer current.
- Moisture Analysis ID 10 and Stability ID 13 expose no test or batch worksheet.
- Terpenes ID 8 exposes test worksheet 42 and batch worksheet 43 but no protocol assignment.
- Assay detail pages did not expose reverse panel membership. The empty assay-side panel arrays are therefore not authoritative; the 88 current memberships are captured from the panel detail pages in `../Panels/panel_inventory.json` and `../Panels/panel_assay_relationships.csv`.
- Default-report controls did not yield reliable report IDs during this pass; report relationships are deferred to Phase 4.

Fields containing personal technician/team choices were deliberately omitted. Assay active state, displayed codes, methods, worksheets, protocols, resource-group references, sample types, and safe page URLs are retained where exposed.
