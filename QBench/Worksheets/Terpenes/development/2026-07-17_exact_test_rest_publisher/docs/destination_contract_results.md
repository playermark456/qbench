# Saved 43-field destination-contract proof

Date: 2026-07-17

Current controlled-stop classification:
**`normal_assay_test_instantiation_failed_blank_default`**.

The saved and reopened isolated Sandbox Worksheet definition passed its exact
43-field structural proof. That result is preserved independently from two
runtime-instantiation failures. The earlier direct Test retained a blank 5x5
default worksheet, and a second, brand-new Test created normally from a
preconfigured isolated Assay also retained the blank 5x5 default after
navigating away and reopening it.

| Evidence layer | Classification |
|---|---|
| Saved/reopened Worksheet definition | `passed_43_of_43` |
| Direct existing-Test instantiation | `failed_blank_default_5x5` |
| Normal Assay-created Test instantiation | `normal_assay_test_instantiation_failed_blank_default` |
| Publisher destination gate | `destination_contract_proven=false` |

## Isolated Sandbox objects

- Worksheet: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF`
- Saved version: `2 - SBX_ONLY_TERPENES_API_DESTINATION_PROOF_V2 - APPROVED (ACTIVE)`
- Retained direct-path Assay: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF_TEST`
- Retained direct-path Sample: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF_SAMPLE`
- Normal-path Assay: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_ASSAY`
- Normal-path Sample: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_ASSAY_SAMPLE`

Internal Sandbox identifiers are omitted from tracked evidence. The new
normal-path Test identifier is recorded only in an ignored local evidence
file. The complete sanitized inventory is in
`sandbox_destination_proof/sanitized_object_inventory.json`.

No analytical results were entered and no Pass/Fail artifact was created.

## Saved Worksheet definition proof

| Evidence | Result |
|---|---|
| Saved/reopened raw Export Spreadsheet | `2026-07-17_SBX_ONLY_TERPENES_API_DESTINATION_PROOF_v2_approved_active_saved_reopened_export_spreadsheet.json` |
| Raw export SHA-256 | `2dfa8e9b94a6806be81b5b4ab58395e3fbefe3ebd0a56a4e7e53e6803d968bef` |
| Logical destinations | 43/43 present and exact |
| Writable targets | 43/43 |
| Missing / renamed / duplicated / formula-owned | None |
| Named-cell systems | 91, with zero duplicate references |
| Surrounding formulas | 265 intact; manifest SHA-256 `f149f36e2892eda5c72dddc9cf281e749df5c5313fceb58b140dae639581e910` |
| Pass/Fail destinations | Zero |
| Dimethylacetamide reportable destination | No |
| Peak Table reportable destination | No |

The raw definition export is preserved byte-for-byte in the ignored local
proof folder. The tracked copy is sanitized and contains no internal Sandbox
object identifiers.

## Normal Assay association proof

Before the new Sample was created, the isolated normal-path Assay was saved
with these settings:

- Active: yes.
- Show in Customer Portal: no.
- Test Worksheet: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF`.
- Batch Worksheet: none.
- Associated Worksheet active version: Version 2,
  `SBX_ONLY_TERPENES_API_DESTINATION_PROOF_V2`, APPROVED and ACTIVE.

The Assay page was left and reopened from the Assays list. The Test Worksheet
association persisted, and the Worksheet Versions view independently
confirmed Version 2 was the approved active version before Sample creation.

## Runtime Test evidence

### Direct existing-Test path

The earlier direct-path Test remains unchanged. After reopening, its Worksheet
tab contained only a blank 5-column by 5-row grid. QBench's supported
**Export Spreadsheet to CSV** action produced
`2026-07-17_SBX_ONLY_TERPENES_test_294_instantiated_export_spreadsheet.csv`
with SHA-256
`6470821a32c974f33b2421746c305a52dad7cc3fa2c043e0aa234b9f4ec6d12e`.
The export had five blank rows and none of the 43 destination cells.

### Normal Assay-created Test path

A fresh synthetic Sample was created after the Assay association was saved.
Assigning only the new isolated Assay created a brand-new Test through the
normal workflow. The Test:

- identified the expected isolated Assay;
- remained `NOT STARTED`;
- received no analytical results or Pass/Fail values;
- showed only the blank 5-column by 5-row default worksheet initially;
- was left for the Tests list, reopened from that list, and again showed only
  the blank 5x5 default worksheet.

Because the reopened UI state already proved the normal instance did not
retain the Worksheet definition, no runtime CSV export was needed and no
attempt was made to treat CSV as named-cell-contract evidence.

## Publisher gate

- `destination_contract_proven=false`
- `atomicity_classification=api_patch_unresolved`
- `analyte_patch_key_contract=unresolved`
- No OAuth token request occurred.
- No QBench REST API request occurred.
- No PATCH occurred.
- Live QBench was not accessed.

The saved Worksheet definition is therefore proven, but the publisher remains
blocked until a normally instantiated Test retains that definition and a
later explicitly authorized read-only API confirmation resolves the Test
worksheet representation. This run cannot truthfully produce a passing
destination-proof lock, so publisher configuration remains unchanged.
