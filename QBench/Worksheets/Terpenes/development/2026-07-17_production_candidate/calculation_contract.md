# Terpenes calculation contract - passed

## Controlling classification

`calculation_contract = passed_authoritative_method_documentation_and_user_approved_reporting_rules`

The controlling method set and explicit user-approved laboratory reporting rules resolve every calculation-critical requirement for local production-candidate design. The final prior blocker, component-channel preprocessing for combined Ocimene and Nerolidol, was resolved by explicit user decision on 2026-07-20.

## Authoritative decisions

- Controlling method: Terpene Analysis SOP v1.2.
- Current supporting records: Terpenes Analysis Form v1.0, Terpenes Analysis Protocol v1.0, and the collected Validation Report.
- Actual-sample quantitation source: `Compound Results(Ch1) > Conc.`.
- Final sample concentration unit: micrograms per gram (`ug/g`).
- LabSolutions has already applied dilution. QBench must never apply dilution again.
- Internal calculations retain full precision.
- `result_mg_g = result_ug_g / 1000`.
- `result_percent = result_ug_g / 10000`.
- Final analytical results and MU display to three decimal places only at the report/display layer.
- Terpenes is quantitative-only. No Pass/Fail artifact is permitted.

## Component preprocessing

Apply independently to `Ocimene 1`, `Ocimene 2`, `Nerolidol 1`, and `Nerolidol 2` while preserving the imported raw value unchanged:

```text
component_used_ug_g =
  IF(component_raw_ug_g is missing or blank or has no integrated peak, 0,
    IF(component_raw_ug_g <= 0, 0, component_raw_ug_g))
```

- Missing, blank, no integrated peak, zero, and negative values contribute `0`.
- A positive numeric component contributes its full-precision value.
- No component-channel reporting LOQ is retrieved or applied.
- A positive component is retained even if it would be below a hypothetical component-channel LOQ.

## Reportable mapping and combined results

The 23 internal chromatographic channels produce exactly 21 reportable measurands. Dimethylacetamide and Peak Table data remain audit-only. The exact mapping is in [metrc_terpenes_analyte_mapping.csv](metrc_terpenes_analyte_mapping.csv).

```text
Ocimene_ug_g = Ocimene_1_used_ug_g + Ocimene_2_used_ug_g
Nerolidol_ug_g = Nerolidol_1_used_ug_g + Nerolidol_2_used_ug_g

combined_mg_g = combined_ug_g / 1000
combined_percent = combined_ug_g / 10000
```

Never sum displayed rounded values.

## Key/Value Store contract

Operational thresholds and MU values are environment configuration, not hardcoded worksheet constants:

```text
GET_KVSTORE_VALUE(
  terpenes_store_binding,
  scope_or_program_key,
  matrix_or_product_type_key,
  analyte_key,
  field
)
```

- The first-level scope/program key is `Terpenes`.
- The second-level key is the selected runtime matrix.
- LOQ uses the 21 reportable analyte keys. Combined keys are `Ocimene` and `Nerolidol`; component LOQs are not retrieved or summed.
- Direct MU uses each directly reported analyte key.
- Combined MU uses `Ocimene 1`, `Ocimene 2`, `Nerolidol 1`, and `Nerolidol 2` only for positive contributing components.
- The terminal `field` is `LOQ` or `MU`.
- Stored LOQ values are numeric `ug/g`; stored MU values are numeric relative percent.
- The worksheet owns display-unit conversion. Result unit is informational and is not a Key/Value hierarchy level or lookup argument.
- The store identifier and matrix key remain sanitized Sandbox configuration bindings; no internal QBench ID is committed.

## Qualifier and Total Terpenes behavior

Compare each unrounded reportable result, including combined Ocimene/Nerolidol, only after calculation against its matrix-specific reportable-analyte LOQ:

- `result_ug_g < LOQ_ug_g`: display `<LOQ`; exclude from Total Terpenes.
- `result_ug_g = LOQ_ug_g`: display numerically; exclude from Total Terpenes because inclusion is strictly above LOQ.
- `result_ug_g > LOQ_ug_g`: display numerically; include the unrounded `ug/g` value in Total Terpenes.
- Never display a negative potency value.

```text
Total_Terpenes_ug_g =
  SUM(each of the 21 unrounded reportable measurands where result_ug_g > matrix_LOQ_ug_g)

Total_Terpenes_mg_g = Total_Terpenes_ug_g / 1000
Total_Terpenes_percent = Total_Terpenes_ug_g / 10000
```

Ocimene and Nerolidol each contribute once. Do not calculate Total Terpenes MU.

## Combined measurement uncertainty

Only positive used components participate. A zero used component contributes zero concentration and zero absolute uncertainty and does not require an MU lookup.

When both components are positive:

```text
combined_mu_percent =
  100 * SQRT(
    (component_1_used_ug_g * component_1_mu_percent / 100)^2
    +
    (component_2_used_ug_g * component_2_mu_percent / 100)^2
  )
  / (component_1_used_ug_g + component_2_used_ug_g)
```

When only one component is positive, combined MU percent equals that component's MU percent. When both are zero, combined MU is blank. If a positive contributing component lacks its required MU, flag MU as unresolved and do not fabricate a value.

## Phase 3 authorization boundary

Local Test and Batch production-candidate JSON generation is authorized after the calculation vectors pass. This authorization does not permit QBench access, import, activation, approval, API use, automatic publication, automatic QC Review, or PR merge. Sandbox saved-definition and runtime validation remain a separate next phase.
