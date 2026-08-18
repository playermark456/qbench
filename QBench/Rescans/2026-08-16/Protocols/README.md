# Protocols and Protocol Steps — 2026-08-16

All 15 protocol detail pages and all 81 protocol-step detail pages were opened serially in read-only mode. The protocols contain 118 assigned step occurrences. Protocols 5 and 9 have zero assigned steps.

## Evidence

- `protocol_inventory.json` — all protocol metadata and ordered assignments.
- `protocol_step_inventory.json` — all 81 step definitions and derived protocol memberships.
- `protocol_step_relationships.csv` — 118 assignments plus one explicit zero-step placeholder row for each empty protocol.
- `../protocol_relationship_map.md` — dependency tables and Cannabinoid Potency reconciliation.

The detail pages did not separately expose active/inactive state, required/optional state, entry/completion conditions, roles, equipment, inventory, resources, or worksheet version-pinning behavior. Those fields are marked `not_exposed` instead of inferred. Native protocol-step worksheet exports remain blocked under the Phase 2 Export Spreadsheet limitation.
