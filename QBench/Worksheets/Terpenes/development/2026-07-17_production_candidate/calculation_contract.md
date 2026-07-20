# Terpenes calculation contract - one authoritative rule remains unresolved

## Controlling classification

`calculation_contract = blocked_missing_authoritative_requirement`

The user-approved method and reporting decision resolves the controlling method set, final LabSolutions sample-result unit, dilution ownership, output conversions, reportable measurands, Key/Value Store dimensions, measurement-uncertainty method, Total Terpenes rule, display rounding, matrix-specific Metrc routing, and quantitative-only reporting model.

The contract does not pass yet because the controlling SOP does not state what numeric value enters a combined Ocimene or Nerolidol result when an individual component channel is missing, negative, or below its applicable channel threshold. The implementation must not silently replace such a channel with zero, retain it, omit it, or block the combined result without an approved rule.

## Authoritative decisions

- Controlling method: Terpene Analysis SOP v1.2, by explicit user approval.
- Current supporting records: Terpenes Analysis Form v1.0, Terpenes Analysis Protocol v1.0, and the collected Validation Report, by explicit user approval.
- Quantitation source for actual samples: `Compound Results(Ch1) > Conc.`.
- Final sample concentration unit: micrograms per gram (`ug/g`).
- LabSolutions has already applied the dilution factor. QBench must not apply dilution again.
- Internal calculations retain full precision.
- `result_mg_g = result_ug_g / 1000`.
- `result_percent = result_ug_g / 10000`.
- Final analytical results and MU are displayed to three decimal places only at the report/display layer.
- Terpenes is quantitative-only. No Pass/Fail named cell, formula, report field, tile, Metrc field, or automation value is permitted.

## Reportable contract

The 23 internal chromatographic channels produce exactly 21 reportable measurands. Ocimene 1 and Ocimene 2 remain internal and produce one combined Ocimene result. Nerolidol 1 and Nerolidol 2 remain internal and produce one combined Nerolidol result. Dimethylacetamide and Peak Table data are audit-only.

The exact channel-to-report and Metrc mapping is in [metrc_terpenes_analyte_mapping.csv](metrc_terpenes_analyte_mapping.csv).

## Combined results

After the unresolved component preprocessing rule has produced two authorized numeric component values:

```text
Ocimene_ug_g = Ocimene_1_used_ug_g + Ocimene_2_used_ug_g
Nerolidol_ug_g = Nerolidol_1_used_ug_g + Nerolidol_2_used_ug_g
```

The `_used_ug_g` suffix is deliberate. It means the unrounded numeric component after the approved missing/negative/below-threshold rule. It must not be implemented as an undocumented normalization.

```text
combined_mg_g = combined_ug_g / 1000
combined_percent = combined_ug_g / 10000
```

## Key/Value Store contract

Terpenes thresholds and MU values must be environment configuration, not hardcoded worksheet constants. The established QBench implementation pattern is represented semantically as:

```text
GET_KVSTORE_VALUE(
  terpenes_store_binding,
  assay_key,
  analyte_key,
  matrix_or_product_type_key,
  result_unit_key,
  value_selector
)
```

Required key dimensions:

- `assay_key`: Terpenes assay key configured in Sandbox.
- `analyte_key`: the reportable measurand for LOQ; the direct analyte or component-channel name for MU.
- `matrix_or_product_type_key`: the QBench matrix/product type used by the validated Terpenes store.
- `result_unit_key`: the configured result unit when the store contract distinguishes units.
- `value_selector`: `LOQ` or `MU%`.

The store identifier is a Sandbox-bound configuration value and must not be committed as an internal QBench ID. Store entries and exact key strings must be created and proven in Sandbox before runtime use.

For LOQ, use reportable combined keys `Ocimene` and `Nerolidol`; never sum component-channel LOQs. For MU, use `Ocimene 1`, `Ocimene 2`, `Nerolidol 1`, and `Nerolidol 2` component keys.

## Qualifier and total behavior

The controlling SOP states that a result below LOQ is reported as `<LOQ`; it quantifies a sample result at or above LOQ. The worksheet must compare the unrounded reportable result against its matrix-specific Key/Value Store LOQ.

- Below LOQ: show `<LOQ`; suppress negative or other numeric potency display; exclude from Total Terpenes.
- Equal to LOQ: numeric report display is permitted by the SOP, but the user-approved Total Terpenes rule is strictly above LOQ, so equality is excluded from the total.
- Above LOQ: show numeric mg/g and percent; include the unrounded `ug/g` value in Total Terpenes.

```text
Total_Terpenes_ug_g =
  SUM(each of the 21 unrounded reportable measurands where result_ug_g > matrix_LOQ_ug_g)

Total_Terpenes_mg_g = Total_Terpenes_ug_g / 1000
Total_Terpenes_percent = Total_Terpenes_ug_g / 10000
```

Ocimene and Nerolidol each contribute once as combined measurands. Total Terpenes excludes their four component channels, Dimethylacetamide, Peak Table values, untested Metrc analytes, non-sample sequence records, blanks, zero/negative report values, and below-LOQ values. No Total Terpenes MU is calculated.

## Measurement uncertainty

For each of the 19 directly reported analytes, retrieve matrix-specific relative MU percent using the direct reportable analyte key. For Ocimene and Nerolidol, retrieve the two component-channel MU percentages and propagate independent relative uncertainties from the same unrounded component values used in the combined result:

```text
combined_mu_percent =
  100 * SQRT(
    (component_1_used_ug_g * component_1_mu_percent / 100)^2
    +
    (component_2_used_ug_g * component_2_mu_percent / 100)^2
  )
  / (component_1_used_ug_g + component_2_used_ug_g)
```

Return blank if either required input or MU is blank, or if the denominator is less than or equal to zero. Display a calculated MU to three decimal places without rounding its intermediates.

## Remaining authoritative requirement

Only this rule remains unresolved:

`TERPENES_COMPONENT_PREPROCESSING_RULE_UNRESOLVED`

For each of `Ocimene 1`, `Ocimene 2`, `Nerolidol 1`, and `Nerolidol 2`, specify what numeric value (if any) becomes `component_used_ug_g` when the source channel is:

1. missing/no peak;
2. negative; or
3. below its applicable channel threshold.

The rule must also identify whether a component-channel threshold exists, where it comes from, and whether a missing component blocks the combined measurand. The current SOP supplies the reportable-analyte `<LOQ` qualifier but not this component preprocessing rule.

## Resume gate

Until that single rule is approved:

- the synthetic vectors may validate only direct-result behavior and combined calculations whose already-preprocessed numeric components are supplied;
- no formula may encode a component normalization assumption;
- no production-candidate worksheet JSON may be generated; and
- the classification remains `blocked_missing_authoritative_requirement`.
