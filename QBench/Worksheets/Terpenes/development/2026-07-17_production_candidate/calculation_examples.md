# Terpenes calculation examples

All values in this document are synthetic design-test values. They are not customer results, validation results, controlled limits, or proposed Key/Value Store constants.

## Direct result conversion and display

Given an actual-sample LabSolutions result of `1234.56789 ug/g` and a matrix-specific LOQ of `50 ug/g`:

```text
internal_ug_g = 1234.56789
internal_mg_g = 1234.56789 / 1000 = 1.23456789
internal_percent = 1234.56789 / 10000 = 0.123456789

display_mg_g = 1.235
display_percent = 0.123
```

The displayed values are rounded only at the final layer. The unrounded `1234.56789 ug/g` remains the value used for LOQ comparison and Total Terpenes.

## LOQ boundary examples

For a synthetic LOQ of `50 ug/g`:

| Unrounded result | COA behavior | Total Terpenes behavior |
| ---: | --- | --- |
| `40 ug/g` | `<LOQ`; no negative or other numeric potency display | Excluded. |
| `50 ug/g` | Numeric display is permitted because the SOP quantifies at or above LOQ. | Excluded because the approved total rule is strictly above LOQ. |
| `60 ug/g` | Numeric mg/g and percent display. | Included as unrounded `60 ug/g`. |
| `-1 ug/g` | `<LOQ`; do not display a negative potency result. | Excluded. |

## Combined Ocimene example

This example starts with two already-authorized, unrounded numeric component values. It does not define how a missing, negative, or below-threshold component is preprocessed.

```text
Ocimene_1_used_ug_g = 600
Ocimene_2_used_ug_g = 400
Ocimene_1_mu_percent = 5
Ocimene_2_mu_percent = 8

Ocimene_ug_g = 600 + 400 = 1000
Ocimene_mg_g = 1000 / 1000 = 1
Ocimene_percent = 1000 / 10000 = 0.1

Ocimene_mu_percent =
  100 * SQRT((600 * 5 / 100)^2 + (400 * 8 / 100)^2) / 1000
  = 4.3863424398922612
```

Display: `1.000 mg/g`, `0.100 %`, and `4.386 % MU`.

The two exact numeric values entering the combined concentration and MU are `600 ug/g` and `400 ug/g`; displayed rounded values are never reused.

## Combined Nerolidol example

This example also begins after component preprocessing:

```text
Nerolidol_1_used_ug_g = 200
Nerolidol_2_used_ug_g = 300
Nerolidol_1_mu_percent = 6
Nerolidol_2_mu_percent = 7

Nerolidol_ug_g = 200 + 300 = 500
Nerolidol_mg_g = 500 / 1000 = 0.5
Nerolidol_percent = 500 / 10000 = 0.05

Nerolidol_mu_percent =
  100 * SQRT((200 * 6 / 100)^2 + (300 * 7 / 100)^2) / 500
  = 4.8373546489791295
```

Display: `0.500 mg/g`, `0.050 %`, and `4.837 % MU`.

The exact numeric component inputs are `200 ug/g` and `300 ug/g`.

## MU guards

- If either required component concentration or component MU is blank, combined MU is blank.
- If the component concentration sum is less than or equal to zero, combined MU is blank.
- A blank combined MU does not authorize a guessed MU or a Total Terpenes MU.

## Total Terpenes example

The normalized synthetic case in [calculation_test_vectors.csv](calculation_test_vectors.csv) evaluates all 21 reportable measurands with a common synthetic LOQ of `50 ug/g`. It includes only the 17 values strictly above LOQ and yields:

```text
Total_Terpenes_ug_g = 1040
Total_Terpenes_mg_g = 1040 / 1000 = 1.04
Total_Terpenes_percent = 1040 / 10000 = 0.104

display_mg_g = 1.040
display_percent = 0.104
```

Ocimene and Nerolidol appear once each as their combined reportable measurands. Component channels, Dimethylacetamide, Peak Table values, untested Metrc analytes, and values at or below LOQ do not contribute.

## Unresolved example boundary

No example assigns a numeric contribution to a missing, negative, or below-threshold Ocimene/Nerolidol component channel. That would invent `TERPENES_COMPONENT_PREPROCESSING_RULE_UNRESOLVED`. Once the laboratory approves that rule, add explicit boundary vectors before implementing worksheet formulas.
