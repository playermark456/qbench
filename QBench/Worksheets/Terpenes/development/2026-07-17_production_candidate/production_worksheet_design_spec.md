# Terpenes production worksheet design specification

## Scope and current gate

This specification describes the two local Phase 3 production candidates. It does not authorize QBench access, import, approval, activation, API use, automatic QC Review, or automatic publication. Terpenes remains quantitative-only and has no Pass/Fail artifact.

`calculation_contract = passed_authoritative_method_documentation_and_user_approved_reporting_rules`

The final component-channel preprocessing rule was supplied and approved explicitly by the user. Local candidate generation is complete; saved-definition and runtime validation in an isolated Sandbox are separate future gates.

## Approved component preprocessing

Apply the following independently to Ocimene 1, Ocimene 2, Nerolidol 1, and Nerolidol 2:

- missing, blank, no integrated peak, zero, or negative raw result -> `used_ug_g = 0`;
- positive numeric raw result -> retain the full-precision positive value as `used_ug_g`;
- preserve the raw result separately for audit; and
- do not request or apply a component-channel LOQ.

Ocimene and Nerolidol each sum their two `used_ug_g` values at full precision. Only the combined reportable result is compared with its matrix-specific reportable-analyte LOQ. Display `<LOQ` when combined `ug/g < LOQ`; display a numeric result at or above LOQ. Include a reportable measurand in Total Terpenes only when its unrounded result is strictly above LOQ.

Only positive components participate in combined MU. One positive component uses that component's MU; two positive components use independent relative propagation; two zero components return blank. A zero component does not require an MU lookup. A positive contributor without MU makes the combined MU unresolved; no value is fabricated.

## Test worksheet candidate

- Target: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS`
- Version: `Terpenes Production Test Worksheet v1`
- File: `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS__v1.json`

Required tab order and populated grid dimensions:

| Tab | Rows x columns | Purpose |
| --- | ---: | --- |
| Report | 23 x 5 | Compact COA result range. |
| Data | 40 x 26 | Exact 43 writable inputs plus visible audit/ownership context. |
| Specifications | 23 x 21 | Formula-owned calculation, LOQ, MU, qualifier, total, and display layer. |

### Exact writable destination contract

| Surface | Exact address contract | Ownership |
| --- | --- | --- |
| 23 LabSolutions concentrations | `Data!D2:Z2` | Writable final actual-sample `ug/g` channels. |
| Seven preparation/compatibility inputs | `Data!B12:B18` | Writable audit/compatibility inputs; never reapplied to the analytical result. |
| Controlled disposition | `Data!B22:B23` | Staff-controlled; no automatic publication or QC disposition. |
| Eleven source/audit fields | `Data!B28:B38` | Writable traceability fields, excluded from reportable calculations. |

These 43 cells remain blank, unique, writable, exportable, and non-formula. All calculated cells are outside the destination contract, visibly distinct, protected, and formula-owned. Dimethylacetamide and Peak Table data remain audit-only.

### Calculation and Key/Value binding

The Test worksheet retains all 23 internal channels and produces exactly 21 reportable measurands. Nineteen map directly; Ocimene and Nerolidol each combine two channels under the approved preprocessing rule. LabSolutions values are already final `ug/g`, including dilution. QBench does not reapply dilution.

Matrix-specific reportable LOQ and MU values use documented `GET_KVSTORE_VALUE` placeholders. The tracked candidate contains `SANDBOX_CONFIGURATION_REQUIRED` instead of internal store identifiers. Combined analytes use the reportable `Ocimene` or `Nerolidol` LOQ, while their positive component channels use component MU keys only. Component LOQ lookup is prohibited.

Internal calculations retain full precision:

```text
mg/g = ug/g / 1000
percent = ug/g / 10000

combined_ug_g = component_1_used_ug_g + component_2_used_ug_g

combined_mu_percent =
  100 * SQRT(
    (component_1_used_ug_g * component_1_mu_percent / 100)^2 +
    (component_2_used_ug_g * component_2_mu_percent / 100)^2
  ) / combined_ug_g
```

The combined-MU formula is guarded for zero components and missing MU values. Display-only values and MU are rounded to the thousandth. Total Terpenes sums the 21 unrounded reportable results for which `result_ug_g > LOQ_ug_g`; combined analytes are counted once and Total Terpenes has no MU.

### Report contract

`report_results = Report!A1:E23`

The five exact headers are `Analyte`, `Result (mg/g)`, `Result (%)`, `LOQ`, and `MU (%)`. The range contains one header, 21 reportable analytes, and Total Terpenes. It excludes all four component-channel labels, raw `ug/g`, preparation inputs, Peak Table, Dimethylacetamide, parser/audit fields, and Pass/Fail content.

## Batch worksheet candidate

- Target: `SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS`
- Version: `Terpenes Production Batch Worksheet v1`
- File: `production_candidates/SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v1.json`

Required tab order and populated grid dimensions:

| Tab | Rows x columns | Purpose |
| --- | ---: | --- |
| Run Setup | 25 x 3 | Staff sequence and readiness surface. |
| Instrument Import | 201 x 57 | No-code parser landing surface. |
| Batch Review | 45 x 24 | Review of final `ug/g`, record type, audit evidence, and disposition context. |
| Test Transfer | 87 x 56 | Manual, reviewable Test-transfer surface. |

The no-code parser contract is unchanged:

- source `A2:AE2` -> `Instrument Import!A2`;
- source `AH2:BE2` -> `Instrument Import!AH2`;
- columns AF and AG are worksheet-owned formulas for every data row and are never parser write targets.

The Batch worksheet preserves 23 numeric terpene channels, Dimethylacetamide, Peak Table audit data, and sequence-record classification. Null, Blank, Standard, CCV, LOQ, and QC records are excluded from Test transfer. Batch Review and Test Transfer remain separate. Any ready/status fields are advisory formula output only; no automatic QBench publication or QC Review action exists.

## Local validation gate

The dedicated validator proves JSON syntax, tab order, dimensions, synchronized worksheet data, fresh UUIDs, the exact 43 destination contract, 23 channels, 21 reportables, component preprocessing, combined MU, reportable LOQ behavior, strict-above Total Terpenes, display rounding, report range dimensions, AF/AG ownership, and absence of Pass/Fail, credentials, signed URLs, customer data, and internal production QBench IDs.

The next controlled phase is isolated Sandbox import, saved/reopened round trip, instantiated runtime proof, Key/Value binding validation, COA preview, and transfer verification. No production action is authorized.
