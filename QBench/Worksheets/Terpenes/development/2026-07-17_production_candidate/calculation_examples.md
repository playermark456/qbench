# Terpenes calculation examples

All values are synthetic design-test values. They are not customer results, validation results, controlled limits, or proposed Key/Value Store constants.

## Direct conversion and display

```text
input_ug_g = 1234.56789
internal_mg_g = 1234.56789 / 1000 = 1.23456789
internal_percent = 1234.56789 / 10000 = 0.123456789

display_mg_g = 1.235
display_percent = 0.123
```

The unrounded `ug/g` value remains the LOQ-comparison and Total Terpenes input.

## Component preprocessing

| Raw component value | Used component value | Reason |
| --- | ---: | --- |
| missing or blank | `0` | Approved missing-value rule. |
| no integrated peak | `0` | Approved no-peak rule. |
| `0` | `0` | Nonpositive values do not contribute. |
| `-12.5 ug/g` | `0` | Negative values do not contribute and are never displayed. |
| `0.00456789 ug/g` | `0.00456789 ug/g` | Every positive component is retained at full precision; no component LOQ applies. |

The imported raw cell is preserved unchanged. The normalized used value is a separate formula-owned value.

## Combined Ocimene: both positive

```text
Ocimene_1_used_ug_g = 600
Ocimene_2_used_ug_g = 400
Ocimene_1_mu_percent = 5
Ocimene_2_mu_percent = 8

Ocimene_ug_g = 600 + 400 = 1000
Ocimene_mg_g = 1
Ocimene_percent = 0.1

Ocimene_mu_percent =
  100 * SQRT((600 * 5 / 100)^2 + (400 * 8 / 100)^2) / 1000
  = 4.3863424398922612
```

Display: `1.000 mg/g`, `0.100 %`, and `4.386 % MU`.

## Combined Nerolidol: one positive and one zero

```text
Nerolidol_1_raw_ug_g = -10
Nerolidol_2_raw_ug_g = 250

Nerolidol_1_used_ug_g = 0
Nerolidol_2_used_ug_g = 250
Nerolidol_2_mu_percent = 7

Nerolidol_ug_g = 250
Nerolidol_mg_g = 0.25
Nerolidol_percent = 0.025
Nerolidol_mu_percent = 7
```

No MU lookup is required for Nerolidol 1 because its used concentration is zero.

## Combined MU guards

- Both used components positive: propagate both positive-component MUs independently.
- Only one used component positive: combined MU equals that positive component's MU.
- Both used components zero: combined MU is blank.
- Positive component missing its required MU: MU status is unresolved and numeric MU remains blank.
- A zero used component never requires MU.

## Combined LOQ boundaries

For a synthetic combined-analyte LOQ of `100 ug/g`:

| Combined result | COA behavior | Total behavior |
| ---: | --- | --- |
| `50 ug/g` | `<LOQ` | Excluded. |
| `100 ug/g` | Numeric result | Excluded; total requires strictly above LOQ. |
| `101 ug/g` | Numeric result | Included as unrounded `101 ug/g`. |

Components are never compared individually to the combined-analyte LOQ.

## Total Terpenes

The normalized synthetic case in [calculation_test_vectors.csv](calculation_test_vectors.csv) evaluates all 21 reportable measurands and yields:

```text
Total_Terpenes_ug_g = 1040
Total_Terpenes_mg_g = 1.04
Total_Terpenes_percent = 0.104

display_mg_g = 1.040
display_percent = 0.104
```

Ocimene and Nerolidol appear once each as combined reportable measurands. Component channels, Dimethylacetamide, Peak Table values, untested Metrc analytes, and values at or below LOQ do not contribute.
