# Phase 4A.4 validation report

## Outcome

The definition-owned binding defect is corrected locally and all renderer, calculation, and runtime-configuration contracts pass. Sandbox execution is blocked one gate later because the authenticated visual browser cannot load the exact candidate into QBench's spreadsheet renderer.

## Proven configuration

- Key/Value binding: visible association UUID, not the store title
- Assay key: `Terpenes`
- Matrix source: `Data!C2 = ${test.sample.product_matrix}`
- Matrix mode: dynamic per Test
- Result unit: `ug/g`
- Synthetic runtime matrix normalization: identity mapping only

## Local result

- Candidate SHA-256: `b68f0e1589ba4e2f5c3c85196c648ed5238a1700b02d8feca3e20850ede19014`
- Renderer contract: passed
- Calculation contract: passed
- Runtime configuration contract: passed
- V2/V3 formula count: 309/309
- Destinations: 43/43 exact
- Named definitions: 44/44 exact
- Unresolved operational markers: 0
- Tests: 26/26 passed

## Sandbox result

- Exact V3 collision: none
- Inactive V3 shell: created
- Exact candidate pre-save render: blocked; default `Sheet1` remained
- Saved versions: none
- Round trip: not run
- Runtime objects: not created
- Report preview: not run

No unsafe workaround was used. No local or Sandbox V2 content was changed, no placeholder Key/Value entry was created, and U2/U4 were not made runtime-editable.

Final classification: `test_v3_runtime_blocked_sandbox_candidate_load_not_applied`
