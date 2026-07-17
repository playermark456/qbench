# Saved 43-field destination-contract proof

Date: 2026-07-17

Final classification: **`saved_destination_contract_failed`**.

The saved and reopened isolated Sandbox worksheet definition passed its exact
43-field structural proof. The fresh, reopened synthetic Test did not retain
that definition: QBench instantiated a blank 5-column by 5-row worksheet, and
the supported **Export Spreadsheet to CSV** action returned only those five
blank rows. The publisher therefore remains paused before the first token
request with `destination_contract_proven: false`.

## Isolated Sandbox objects

- Worksheet: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF`
- Saved version: `2 - SBX_ONLY_TERPENES_API_DESTINATION_PROOF_V2 - APPROVED (ACTIVE)`
- Synthetic assay: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF_TEST`
- Synthetic sample: `SBX_ONLY_TERPENES_2026_07_17_API_DESTINATION_PROOF_SAMPLE`
- Synthetic Test state: `NOT STARTED`, reopened after creation and explicitly
  updated to the current active worksheet version

No analytical results were entered and no Pass/Fail artifact was created.

## Definition proof

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

The raw exports are preserved byte-for-byte in the ignored local proof folder.
Tracked evidence is sanitized and contains no Sandbox object identifiers.

## Instantiated Test proof

| Evidence | Result |
|---|---|
| Reopened Test Worksheet tab | Present |
| QBench-supported worksheet export | `2026-07-17_SBX_ONLY_TERPENES_test_294_instantiated_export_spreadsheet.csv` |
| Export SHA-256 | `6470821a32c974f33b2421746c305a52dad7cc3fa2c043e0aa234b9f4ec6d12e` |
| Export shape | Five rows, five empty columns |
| Retained named-cell contract | No; none of the 43 destinations is present in the instantiated export |

Because the runtime instance is blank, all 43 expected destinations are
missing from the instantiated proof even though the saved definition itself
is correct. This is a hard failure under Prompt 5B, not a passing definition-
only proof.

## Publisher gate

- `destination_contract_proven=false`
- `atomicity_classification=api_patch_unresolved`
- `analyte_patch_key_contract=unresolved`
- No OAuth token request occurred.
- No QBench REST API request occurred.
- No PATCH occurred.
- Live QBench was not accessed.

The local proof command now accepts QBench's raw **Export Spreadsheet**
envelope, but a passing provenance file must also assert that a reopened
synthetic Test retained the contract:

```json
{
  "sandbox_hostname": "ait-sandbox.qbench.net",
  "export_action": "Export Spreadsheet",
  "saved": true,
  "reopened": true,
  "synthetic_only": true,
  "export_sha256": "<sha256-of-exact-export-file>",
  "worksheet_display_name": "SBX_ONLY_<task-worksheet-name>",
  "instantiated_test_reopened": true,
  "instantiated_test_contract_proven": true,
  "classification": "saved_destination_contract_passed"
}
```

This run cannot produce that provenance truthfully, so no passing destination
proof lock was written and publisher configuration remains unchanged.
