# Phase 3 Validation Report — 2026-08-16

## Result

Phase 3 evidence is structurally valid at the current checkpoint. The field inventory is intentionally partial where additional metadata would require prohibited Edit actions. Current native worksheet definitions remain blocked by Phase 2 and are not reconstructed here.

## Deterministic checks

- JSON files parsed: 17 of 17.
- JSON parse failures: 0.
- Assay CSV rows: 20; duplicate assay IDs: 0.
- Panel-assay CSV rows: 88; blank assay IDs: 0; duplicate panel/assay memberships: 0.
- Protocol relationship CSV rows: 120 physical rows, comprising 118 real assignments plus two explicit zero-step placeholders.
- Protocol relationship projection: all 118 real assignment rows have a nonblank step name that reconciles to the JSON inventories.
- Protocol-step definitions: 81; duplicate step IDs: 0.
- Field CSV rows: 277; blank labels/system names: 0.
- KV-store summary rows: 11.
- KV-store scalar rows: 13,766; path-occurrence ordering errors: 0.
- KV-store unique paths: 5,411; maximum occurrence for one path: 146.
- Automated email-address matches: 0.
- JWT-like matches: 0.
- Authorization credential-value matches: 0.
- Cookie assignment matches: 0.
- Authentication/session query-parameter matches: 0.
- Strict CSV/JSON projection mismatches across the 23 scoped Phase 3 artifacts: 0.
- Safe captured URL occurrences: 410; all use HTTPS on `ait.qbench.net`, with no unsafe query parameter.
- QBench mutations performed: 0.

## Reconciliations

- Phase 1 observed 10 KV-store rows on the first page; Phase 3 traversed both pages and established the complete count of 11.
- Protocols 5 and 9 have no steps, explaining the two placeholder rows in the relationship CSV.
- Seventy-five of 81 step definitions have at least one protocol membership. Orphan steps are 20, 21, 53, 74, 75, and 76.
- Cannabinoid worksheet 39 is active/approved at version 7 but its step 21 is not assigned to protocol 4.
- Shared final-review worksheet 41 has no versions while its step 23 is assigned to 12 protocols.
- Protocol 12 sequence 4 assigns step 83 to worksheet 151, which has only draft version 1 and no active version.

## Capture limitations

- No field Edit control was used; field IDs, types, validation, formulas, option/KV sources, and usage relationships remain not exposed.
- Protocol details did not expose active/required state, conditions, role/resource/equipment/inventory assignment, or version behavior.
- KV-store API Clients and History were intentionally omitted. Created-by identities were not retained.
- Phase 2 native Export Spreadsheet blocker prevents a current embedded-`kvstore_config` comparison.
