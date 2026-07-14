# LabSolutions ASCII Export Integration Spec for Terpenes

Source example: `Output_redacted_fixture.txt`, a sanitized LabSolutions ASCII/text report fixture. The fixture preserves the section layout, analyte names, and representative numerical data needed for parser tests while replacing internal usernames, instrument identifiers, and local file paths.

## Sections present in the export

- `[Header]`
- `[File Information]`
- `[Sample Information]`
- `[Original Files]`
- `[Configuration]`
- `[Peak Table(Ch1)]`
- `[Compound Results(Ch1)]`

## Critical interpretation

Use **`Compound Results(Ch1)` as the quantitation source**. It contains 24 compound IDs: 23 reportable terpene worksheet analytes plus **Dimethylacetamide**, which should be retained as method/internal-standard information but excluded from terpene reporting.

Use **`Peak Table(Ch1)` for integration review and chromatographic QC**. The peak table contains 34 peaks because several compound IDs have multiple peak-table rows that are aggregated into one Compound Results row. Examples in this export include Geraniol, beta-Caryophyllene, alpha-Humulene, Nerolidol 1, Nerolidol 2, Guaiol, Caryophyllene oxide, and alpha-Bisabolol.

Do **not** use `Conc. %` or `Norm Conc.` as sample potency percentage. In this export, the Compound Results `Conc. %` values sum to approximately 100%, which means they are normalized composition fields for the report, not the cannabis/hemp sample potency result. Use the `Conc.` field as the concentration input only after confirming its unit from the LabSolutions method.

## Required parser behavior

1. Read bracketed sections and tab-delimited rows.
2. Pull sample metadata from `[Sample Information]`: Sample Name, Sample ID, Sample Amount, Dilution Factor, Vial#, Injection Volume, Injection Count, and Acquired.
3. Pull source traceability from `[Original Files]`: Data File, Method File, Batch File, and Report Format File.
4. Pull instrument metadata from `[Configuration]`: Instrument Name, Detector ID, and Detector Name.
5. Parse `[Compound Results(Ch1)]` into one normalized row per reportable analyte.
6. Parse `[Peak Table(Ch1)]` into raw integration rows for review/QC only.
7. Exclude `Dimethylacetamide` from reportable terpene analytes.
8. Normalize LabSolutions names into worksheet labels using the alias table below.
9. Store `Sample Amount` and `Dilution Factor`, but do not double-apply them unless validation confirms how LabSolutions calculated `Conc.`.
10. Validate that all configured analytes appear exactly once in Compound Results, except any explicitly disabled analytes.

## Alias mapping from this export

| LabSolutions name | Worksheet label | Reportable |
|---|---|---|
| Dimethylacetamide | Dimethylacetamide | No |
| alpha-Pinene | α-Pinene | Yes |
| Camphene | Camphene | Yes |
| beta-Myrcene | β-Myrcene | Yes |
| (-)-beta-Pinene | (-)-β-pinene | Yes |
| delta-3-Carene | Delta-3-carene | Yes |
| alpha-Terpinene | α-Terpinene | Yes |
| Ocimene 1 | cis-Ocimene | Yes |
| D-Limonene | d-Limonene | Yes |
| p-Cymene | p-Cymene | Yes |
| Ocimene 2 | trans-Ocimene | Yes |
| Eucalyptol | Eucalyptol | Yes |
| Gamma terpinene | γ-Terpinene | Yes |
| Terpinolene | Terpinolene | Yes |
| Linalool | Linalool | Yes |
| (-)-Isopulegol | (-)-Isopulegol | Yes |
| Geraniol | Geraniol | Yes |
| beta-Caryophyllene | β-Caryophyllene | Yes |
| alpha-Humulene | α-Humulene | Yes |
| Nerolidol 1 | cis-Nerolidol | Yes |
| Nerolidol 2 | trans-Nerolidol | Yes |
| (-)-Guaiol | (-)-Guaiol | Yes |
| Caryophyllene oxide | Caryophyllene Oxide | Yes |
| (-)-alpha-Bisabolol | (-)-α-Bisabolol | Yes |

## Recommended normalized result columns

| Column | Source |
|---|---|
| sample_name | `[Sample Information] > Sample Name` |
| sample_id | `[Sample Information] > Sample ID` |
| acquired_at | `[Sample Information] > Acquired` |
| vial_number | `[Sample Information] > Vial#` |
| injection_volume_uL | `[Sample Information] > Injection Volume` |
| source_id | `[Compound Results(Ch1)] > ID#` |
| source_name | `[Compound Results(Ch1)] > Name` |
| worksheet_label | alias-mapped compound name |
| r_time_min | `[Compound Results(Ch1)] > R.Time` |
| area | `[Compound Results(Ch1)] > Area` |
| height | `[Compound Results(Ch1)] > Height` |
| labsolutions_conc | `[Compound Results(Ch1)] > Conc.` |
| curve | `[Compound Results(Ch1)] > Curve` |
| area_ratio | `[Compound Results(Ch1)] > Area Ratio` |
| height_ratio | `[Compound Results(Ch1)] > Height Ratio` |
| normalized_conc_percent_not_potency | `[Compound Results(Ch1)] > Conc. %` |
| sample_amount_export | `[Sample Information] > Sample Amount` |
| dilution_factor_export | `[Sample Information] > Dilution Factor` |

## Formula impact

The worksheet should treat `labsolutions_conc` as the instrument concentration input. The current draft conversion remains valid if `labsolutions_conc` is confirmed as extract concentration in `ug/mL`:

```text
Result mg/g = labsolutions_conc * final_volume_mL / sample_mass_g / 1000
Result %    = Result mg/g / 10
```

`Dilution Factor` should be captured separately. A config flag can decide whether to apply it:

```text
corrected_conc = IF(apply_export_dilution_factor, labsolutions_conc * dilution_factor_export, labsolutions_conc)
```

Default recommendation: **do not apply the export Dilution Factor a second time** until the LabSolutions method is verified.

## Codex acceptance tests to add

- Parser returns 8 sections from the provided `Output_redacted_fixture.txt` fixture.
- Parser returns 24 Compound Results rows, 23 reportable rows, and 34 Peak Table rows.
- Parser excludes Dimethylacetamide from reportable result output.
- Parser maps `Ocimene 1` to `cis-Ocimene` and `Ocimene 2` to `trans-Ocimene`.
- Parser maps `Nerolidol 1` to `cis-Nerolidol` and `Nerolidol 2` to `trans-Nerolidol`.
- Parser fails or warns if `Conc. %` or `Norm Conc.` is referenced by a potency formula.
- Parser preserves sample metadata, original data file, method file, batch file, instrument, and detector for audit trail.
- Compound Results should drive final results; Peak Table should not be used as the primary quantitation table.
