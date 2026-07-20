# Terpenes production worksheet design specification

## Scope and current gate

This is a local design specification for future isolated Sandbox candidates. It does not authorize QBench creation, import, activation, API use, automatic QC Review, or automatic publication. Terpenes is quantitative-only; no Pass/Fail artifact is permitted.

Most scientific decisions are resolved. Candidate JSON and formula generation remain blocked only by `TERPENES_COMPONENT_PREPROCESSING_RULE_UNRESOLVED`: the approved numeric treatment of missing, negative, and below-threshold Ocimene/Nerolidol component channels.

`calculation_contract = blocked_missing_authoritative_requirement`

## Test worksheet architecture

Required tab order:

1. `Report`
2. `Data`
3. `Specifications`
4. `Audit`
5. `METRC`

### Data tab

The Test candidate must preserve the proven 43 independent scalar publisher destinations:

| Surface | Exact address contract | Ownership |
| --- | --- | --- |
| 23 LabSolutions concentrations | `Data!D2:Z2` | Writable/importable final actual-sample `ug/g` values in the proven channel order. |
| Seven preparation/compatibility inputs | `Data!B12:B18` | Writable compatibility fields; retained for review and traceability, but must not cause QBench to reapply dilution. |
| Controlled disposition | `Data!B22:B23` | Staff-controlled `batch_qc_disposition` and `publish_ready`; parser and transfer do not populate them. |
| Eleven source/audit fields | `Data!B28:B38` | Writable source traceability; excluded from reportable calculations. |

The 23 input values are the final `Compound Results(Ch1) > Conc.` actual-sample results in `ug/g`. LabSolutions already applies dilution. Existing dilution and preparation fields remain for destination compatibility and audit only; formulas must not multiply or divide the analytical result by them.

All calculated cells must be outside the 43 writable destinations and formula-owned. Use distinct styles for writable inputs, formula-owned calculations, controlled staff fields, and audit-only data.

### Specifications tab

Use one row for each of the 21 reportable measurands plus one Total Terpenes row. Required calculation/review columns:

- reportable analyte;
- source channel or combination group;
- unrounded internal `ug/g`;
- unrounded `mg/g`;
- unrounded percent;
- matrix/product type;
- Key/Value Store LOQ and result unit;
- qualifier;
- Key/Value Store MU percent;
- display `mg/g`, percent, and MU percent;
- Metrc profile field;
- staff note/review context.

For the 19 direct measurands, source one internal channel. For Ocimene, source `Ocimene 1 + Ocimene 2`. For Nerolidol, source `Nerolidol 1 + Nerolidol 2`. The four component channels remain visible for traceability but are not separate COA or Metrc results.

The unresolved component preprocessing rule must be an explicit formula input/guard, never an implicit `MAX(0, value)`, blank-to-zero coercion, or error suppression.

### Key/Value Store binding

The Specifications formulas must follow this semantic lookup contract:

```text
GET_KVSTORE_VALUE(
  terpenes_store_binding,
  assay_key,
  analyte_key,
  matrix_or_product_type_key,
  result_unit_key,
  "LOQ" or "MU%"
)
```

The internal store binding and exact deployed key strings are Sandbox configuration and must not be committed as QBench IDs. Before candidate approval, Sandbox validation must prove one unique nonblank lookup for every required tuple and reject missing/duplicate tuples.

- Direct LOQ key: direct reportable analyte.
- Combined LOQ key: `Ocimene` or `Nerolidol`, never the sum of component LOQs.
- Direct MU key: direct analyte.
- Combined MU keys: the two component-channel names by matrix.

### Calculation ownership

```text
direct_mg_g = direct_ug_g / 1000
direct_percent = direct_ug_g / 10000

combined_ug_g = component_1_used_ug_g + component_2_used_ug_g
combined_mg_g = combined_ug_g / 1000
combined_percent = combined_ug_g / 10000

combined_mu_percent =
  100 * SQRT(
    (component_1_used_ug_g * component_1_mu_percent / 100)^2
    +
    (component_2_used_ug_g * component_2_mu_percent / 100)^2
  ) / (component_1_used_ug_g + component_2_used_ug_g)
```

Combined MU returns blank when a required input/MU is blank or the denominator is nonpositive. The calculation uses unrounded components. No Total Terpenes MU is created.

For each reportable measurand, compare the unrounded result to the Key/Value Store LOQ. Below LOQ displays `<LOQ` and no negative potency value. Equality may display numerically, but the Total Terpenes inclusion test is strictly `result_ug_g > LOQ_ug_g`.

```text
Total_Terpenes_ug_g =
  SUM(the 21 unrounded reportable results strictly above their matrix LOQs)

Total_Terpenes_mg_g = Total_Terpenes_ug_g / 1000
Total_Terpenes_percent = Total_Terpenes_ug_g / 10000
```

### Report tab

The compact COA table has exactly five columns:

1. Analyte
2. Result (mg/g)
3. Result (%)
4. LOQ
5. MU (%)

It contains the 21 tested/reportable measurands plus Total Terpenes. The bounded named range is:

`report_results = Report!A1:E23`

The range includes one header row and 22 result rows. Report cells reference Specifications calculations, not raw import cells. Final numeric result and MU cells use three-decimal display formats; internal cells retain full precision.

Below-LOQ analytes remain in the fixed 21-row report table and show `<LOQ` according to the controlling SOP. Sandbox COA preview must verify how the report renderer handles the qualifier across the result columns.

Exclude raw `ug/g`, four component channels, preparation/dilution fields, Peak Table, Dimethylacetamide, QC calculations, parser metadata, audit hashes, and all Pass/Fail content.

### METRC tab

Use [metrc_terpenes_analyte_mapping.csv](metrc_terpenes_analyte_mapping.csv) as the field-name contract. Route exactly one matrix-appropriate unit field per reportable measurand unless a future validated upload contract explicitly requires otherwise:

- Raw Plant Material -> percentage field.
- Concentrate/Extract -> percentage field.
- Infused Product -> mg/g field.

Do not populate unused template analytes, `Cis-Nerolidol`, generic `Cymene`, `Other Terpenes`, or both unit fields for the same result. Ocimene and Nerolidol each map once as combined results. COA display remains dual-unit regardless of the single-unit Metrc route.

### Audit tab

Present source filename/hash, parser state, import and transfer state, original 23-channel values, Dimethylacetamide, and Peak Table context. Audit data must remain reviewable/exportable but cannot enter `report_results`, Metrc values, or Total Terpenes.

## Batch worksheet architecture

Required tab order:

1. `Run Setup`
2. `Raw Import`
3. `Normalized Import`
4. `Batch Review`
5. `Test Transfer`
6. `Audit`

| Tab | Purpose | Required boundary |
| --- | --- | --- |
| Run Setup | Staff sequence surface for standards, blank, system suitability, QC, and sample records. | No customer-result Pass/Fail. |
| Raw Import | Byte/order-preserving parser landing surface. | Parser-owned; no scientific calculation. |
| Normalized Import | Existing 57-column no-code surface. | Parser writes only `A:AE` and `AH:BE`; `AF/AG` remain worksheet-owned formulas. |
| Batch Review | Review 23 final `ug/g` channels, record type, import status, QC/audit notes, Dimethylacetamide, and Peak Table context. | No automatic QC Review or result publication. |
| Test Transfer | Deterministic one-row-per-Test manual transfer in exact 43-field-compatible order. | Do not transfer staff-controlled `B22:B23`; no automatic Publish. |
| Audit | Source hashes, duplicate checks, parser state, and transfer history. | Excluded from scientific report values. |

The parser preserves all 23 internal channels and audit-only evidence. Scientific combination, LOQ, MU, unit conversion, Total Terpenes, report, and Metrc formulas belong to the Test worksheet after the remaining component rule is approved.

## Local validation requirements

Before any future candidate JSON is generated:

1. approve and document the component preprocessing rule;
2. extend [calculation_test_vectors.csv](calculation_test_vectors.csv) with missing, negative, and below-threshold component boundary cases;
3. validate 23 unique internal channels and exactly 21 unique reportable measurands;
4. validate all workbook-derived Metrc field labels and ignored fields;
5. validate every Key/Value tuple and blank/error guard;
6. validate conversions, combined results, independent MU propagation, strict-above Total Terpenes, and display rounding;
7. prove the exact 43 writable destinations remain blank/non-formula and every calculated output is formula-owned;
8. prove no Pass/Fail string, named cell, formula, report field, or automation value exists; and
9. run existing no-code parser and AF/AG formula-ownership tests.

Sandbox creation, saved-version round trip, instantiated runtime proof, COA preview, and Metrc export verification are separate later gates. No live/production QBench action is authorized.
