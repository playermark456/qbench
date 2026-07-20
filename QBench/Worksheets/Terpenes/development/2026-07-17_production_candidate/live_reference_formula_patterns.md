# Live non-Terpenes formula-engine patterns

These are software-engine observations only. No equation, constant, dilution factor, LOQ, rounding rule, analyte rollup, unit, MU rule, or Pass/Fail rule was copied from another assay into the Terpenes scientific contract.

## Supported reusable mechanics

- Cross-tab formulas persist through **Export Spreadsheet** as leading-`=` strings in worksheet data.
- Supported function families observed include `IF`, `IFERROR`, `LEN`, `COUNTA`, `COUNTIF`, `AND`, `OR`, `SEARCH`, `FIND`, `XLOOKUP`, `INDEX`, `MATCH`, `TEXT`, and `GET_KVSTORE_VALUE`.
- Blank propagation is commonly implemented by checking source occupancy before calculating and returning `""` when the source is absent.
- Division is commonly guarded by blank/input checks or `IFERROR`; an unguarded scientific equation must not be introduced.
- Qualifier/display separation can use `SEARCH` or `FIND` without changing the underlying quantitative field.
- Formula-heavy technical sections can be read-only and, where appropriate, hidden by column visibility metadata.
- Report-facing formulas generally reference calculation/review tabs rather than repeating raw-input logic.
- Safe non-Terpenes exports confirmed Key/Value value-selector literals including `LOQ`, `MU`, and `MU%`. No internal store identifier is retained in Terpenes tracked evidence.

## Structural counts from safe exports

| Reference | Formula strings | `IFERROR` formulas | Blank-return/input-guard evidence | Reusable conclusion |
| --- | ---: | ---: | --- | --- |
| Cannabinoid Potency Test | 652 | 95 | Extensive across Data, Specifications, Report, and METRC | Guarded calculations, separate report formulas, hidden/read-only technical columns. |
| Heavy Metals Test | 63 | 8 | Present in Specifications and METRC | Compact quantitative review plus separate qualifier/report layers. |
| Quantitative Pesticides Test | 763 | 69 | Extensive in Specifications | Large-table formulas can remain bounded to a compact COA range. |
| Homogeneity Test | 375 | 46 | Extensive across Paste, Data, and COA | Paste, calculation, and report layers can be kept distinct. |
| Residual Solvents Batch | 0 | 0 | None | Legacy sheet is not a formula-engine model. |
| Quantitative Pesticides Batch | 0 | 0 | None | Transfer behavior must not be inferred from worksheet formulas. |

## Terpenes boundary

The future implementation may reuse the guard shape `source absent -> blank`, the separation `input -> calculated review -> report`, and the established `GET_KVSTORE_VALUE` mechanics.

The user-approved Terpenes decision establishes the final unit, dilution ownership, conversions, reportable mapping, component preprocessing, LOQ/MU source dimensions, independent combined-MU equation, Total Terpenes rule, and display rounding. The Phase 3 candidate now implements guarded Terpenes formulas locally from that contract.

Missing, blank, no-peak, zero, and negative component values are converted to zero only in separate formula-owned `used_ug_g` cells; the raw input remains unchanged. Positive values retain full precision. No component LOQ formula exists. Positive contributors require MU; zero contributors do not.

`calculation_contract = passed_authoritative_method_documentation_and_user_approved_reporting_rules`
