# Phase 4A.3 isolated Key/Value fixture

## Fixture identity

- Name: `SBX_ONLY_TERPENES_RUNTIME_KV_V2`
- Environment: QBench Sandbox only
- Purpose: synthetic formula-resolution testing; it does not establish approved production LOQ or MU values
- Collision check: no existing exact-name fixture was found before creation
- Association: only the exact V2 Test Worksheet was associated
- Shared or operational stores modified: none

## Synthetic dimensions and values

The fixture uses the documented dimensions: assay, reportable analyte or component channel, matrix/product type, result unit, and selector (`LOQ` or `MU%`).

- Assay: `Terpenes`
- Matrix/product type: `SBX_ONLY_RUNTIME_MATRIX_V2`
- Result unit: `ug/g`
- Reportable analytes with LOQ selectors: 21
- Reportable analytes with MU% selectors: 21
- Component MU% selectors: Ocimene 1, Ocimene 2, Nerolidol 1, and Nerolidol 2
- Synthetic LOQ: 10 for each reportable analyte
- Synthetic direct MU% values: Alpha-Pinene 5, Camphene 6, Beta-Myrcene 7, Beta-Pinene 8, and 9 for the remaining direct reportable analytes
- Synthetic component MU% values: Ocimene 1 = 4, Ocimene 2 = 8, Nerolidol 1 = 7, Nerolidol 2 = 11

The saved fixture was reloaded and its expanded selector tree showed 21 LOQ selectors, 25 MU% selectors, the synthetic matrix, and all four internal component MU keys.

## Binding result

Association alone did not make the saved worksheet executable. `Specifications!U2` (store binding) and `Specifications!U4` (matrix/product type) remained read-only cells containing `SANDBOX_CONFIGURATION_REQUIRED`. The saved LOQ and MU formulas intentionally return blank while either sentinel remains.

No formula was hardcoded or bypassed. Runtime fixture creation stopped at this controlled binding failure.
