# Phase 3 QBench Sandbox Import And Test Checklist

Release folder:
`QBench/Releases/Homogeneity/2026-07-01/`

Worksheet JSON:
`homogeneity_phase1_production_candidate__2026-07-01.json`

Important safety rules:

- Use QBench Sandbox only.
- Do not use production QBench.
- Do not build or enable automation for this phase.
- Do not modify COA source during worksheet import testing unless separately approved.

## Import And Setup

| Step | Status | Notes |
|---|---|---|
| Import worksheet JSON into QBench Sandbox | Not started | Use the Phase 1 production-candidate JSON from this release folder. |
| Attach worksheet to Homogeneity assay/test | Not started | Homogeneity assay ID should be `11`. |
| Confirm named cells are visible | Not started | Confirm at least `pass_fail`, `report_results`, `replicate_count`, `unique_cp_test_id_count`, `duplicate_cp_test_id_check`, `parent_sample_match_check`, and `validation_status`. |
| Confirm worksheet opens without formula errors | Not started | Check Paste, Data, and COA tabs. |
| Confirm label-source named cells are visible | Not started | Confirm `label_cannabinoid_1_source_status`, `label_cannabinoid_2_source_status`, manual override cells, and `qbench_sample_label_amount_lookup`. |
| Confirm label source table remains raw | Not started | `Paste!P25:P36` should contain raw QBench sample label amount placeholders/values, not lookup formulas. |

## Test Data Setup

| Step | Status | Notes |
|---|---|---|
| Create one sample/order with Homogeneity and 10 Cannabinoid Potency Test IDs | Not started | All 10 CP Test IDs should represent replicate units under the same parent sample. |
| Open the Cannabinoid Potency batch worksheet/results source | Not started | Use Sandbox data only. |
| Paste 10 potency result rows into Homogeneity | Not started | Paste into `Paste!A10:AG19`. |
| Confirm pasted cannabinoid result units | Not started | Pasted cannabinoid values are expected to be `ug/g`, not `mg/g`. |
| Enter actual unit mass for all 10 units | Not started | Enter values in `Paste!AH10:AH19`. |
| Confirm Target Cannabinoid 1 default | Not started | `Paste!B4` should default to `Total THC`. |
| Enter Target Cannabinoid 1 | Not started | Keep `Total THC` for the primary Sandbox test; then test another supported target if needed. |
| Optionally enter Target Cannabinoid 2 | Not started | Leave blank if not used. |
| Confirm label cannabinoid claim auto-pull | Not started | Target 1 label claim should pull from the matching QBench sample `Product Label Amount` field when populated. |
| Confirm label source/status | Not started | `Paste!Q4` and `Paste!U4` should show which QBench sample field was used, or whether manual override was used. |
| Enter manual label override only if needed | Not started | Use the manual override cells only when the QBench sample label field is blank or not populated in Sandbox. |
| Enter label unit mass if available | Not started | If blank, worksheet should use average actual unit mass as the mass variance basis. |

## Unit Conversion Checks

| Check | Expected Result | Actual Result |
|---|---|---|
| `Paste!AI10` Total THC helper | `(D9-THC ug/g + THCa ug/g * 0.877) / 1000` |  |
| `Paste!AJ10` Total CBD helper | `(CBD ug/g + CBDa ug/g * 0.877) / 1000` |  |
| D9-THC `4058.954 ug/g` with blank/zero THCa | Total THC should be `4.058954 mg/g` |  |
| Total THC `4.058954 mg/g` with `5 g` unit mass | Total THC should be about `20.29477 mg/container` |  |
| CBG `4105.178 ug/g` | CBG should be `4.105178 mg/g` |  |
| CBG `4.105178 mg/g` with `5 g` unit mass | CBG should be about `20.52589 mg/container` |  |
| Label Total THC `20 mg/container` with about `20 mg/container` actual | Variance should be a few percent, not a massive ug/g-based variance |  |

## Worksheet Validation Checks

| Check | Expected Result | Actual Result |
|---|---|---|
| `replicate_count` | `10` |  |
| `unique_cp_test_id_count` | `10` |  |
| `duplicate_cp_test_id_check` | `PASS` |  |
| `parent_sample_match_check` | `PASS` or `REVIEWER_CONFIRMED` |  |
| `required_unit_mass_check` | `PASS` |  |
| `required_target_fields_check` | `PASS` |  |
| `optional_target_2_label_claim_check` | `PASS` |  |
| `validation_status` | `READY` |  |
| `pass_fail` | `PASS` or `FAIL` after validation is ready; COA should display `Pass` or `Fail` |  |
| `label_cannabinoid_1_source_status` | Shows pulled QBench sample field or manual override |  |
| `label_cannabinoid_2_source_status` | Shows pulled QBench sample field, manual override, or Target 2 not used |  |
| `Paste!AH10:AH19` | All 10 Actual Unit Mass g values filled before `validation_status` can become `READY` |  |

## Parent Sample Confirmation Fallback

If pasted Cannabinoid Potency batch rows do not contain enough information to prove parent sample matching:

1. Do not fake the validation.
2. Reviewer must confirm that all 10 CP Test IDs belong to the same parent sample.
3. Enter `YES` in `Paste!D6`.
4. Confirm `parent_sample_match_check` becomes `REVIEWER_CONFIRMED`.
5. Confirm `validation_status` becomes `READY` only after all other checks pass.

## Negative Tests

| Test | Expected Result | Actual Result |
|---|---|---|
| Fewer than 10 CP Test IDs | `validation_status` remains incomplete |  |
| Duplicate CP Test ID | `duplicate_cp_test_id_check = FAIL` |  |
| 11th CP Test ID pasted below input range | `extra_pasted_rows_check = FAIL` |  |
| Missing unit mass | `required_unit_mass_check = INCOMPLETE` |  |
| Missing Target 1 | `required_target_fields_check = INCOMPLETE` |  |
| Missing Target 1 label claim | `required_target_fields_check = INCOMPLETE` |  |
| Target 2 entered without label claim | `optional_target_2_label_claim_check = INCOMPLETE` |  |
| Mismatched Sample IDs in pasted rows | `parent_sample_match_check = FAIL` |  |
| QBench sample label field blank, no manual override | Related label claim check remains `INCOMPLETE` |  |
| QBench sample label field equals `None` | Treated as blank; related label claim check remains `INCOMPLETE` unless manual override is entered |  |
| QBench sample label field remains unresolved like `${...}` | Treated as blank; related label claim check remains `INCOMPLETE` unless manual override is entered |  |

## COA Preview Checks

| Step | Expected Result | Actual Result |
|---|---|---|
| Generate COA preview | Preview completes without error |  |
| Confirm Homogeneity tile displays correctly | Tile displays `Pass`, `Fail`, or `Not Tested` according to COA logic |  |
| Confirm Homogeneity detail page renders `report_results` | Detail table appears from `COA!A1:G20` |  |
| Confirm table fits on one page | No clipped columns or unreadable wrapping |  |
| Confirm COA does not calculate Homogeneity | COA displays worksheet-calculated output only |  |

## Manual Calculation Checks

For at least one passing and one failing case, manually verify:

- Total THC conversion from pasted `ug/g` to `mg/g`.
- Total CBD conversion from pasted `ug/g` to `mg/g`, if used.
- Individual cannabinoid target conversion from pasted `ug/g` to `mg/g`.
- mg/container for Target Cannabinoid 1.
- mg/container for optional Target Cannabinoid 2, if used.
- cannabinoid variance from label claim.
- unit mass variance from label mass when label mass is provided.
- unit mass variance from average actual unit mass when label mass is blank.
- highest reported unit mass and variance.
- highest reported cannabinoid mg/container and variance.
- final Homogeneity Pass/Fail.

## Acceptance Criteria

Sandbox testing passes only when:

- The worksheet imports cleanly.
- All required named cells are visible.
- The validation fields behave as expected.
- `validation_status` reaches `READY` only for valid 10-replicate data.
- `pass_fail` produces a final `PASS`/`FAIL` only when validation is ready.
- The COA Homogeneity tile displays correctly.
- The COA Homogeneity detail page renders `report_results`.
- Manual calculations match worksheet output.
