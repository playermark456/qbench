# Authoritative Terpenes method and reporting inventory

Inventory date: 2026-07-20

## Current authority decision

The user explicitly approved the following method set for the production-worksheet design contract:

| Controlled source | Current status | Design authority established |
| --- | --- | --- |
| Terpene Analysis SOP v1.2 | Controlling | Yes, by explicit user approval. |
| Terpenes Analysis Form v1.0 | Current | Yes, by explicit user approval. |
| Terpenes Analysis Protocol v1.0 | Current | Yes, by explicit user approval. |
| Collected Validation Report | Current | Yes, by explicit user approval; raw report remains excluded because it contains real validation and internal-system information. |
| LabSolutions actual-sample `Compound Results(Ch1) > Conc.` | Final `ug/g`; dilution already applied | Yes, by explicit user approval and bounded raw-evidence inspection. |
| Minnesota OCM Metrc Terpenes workbook | Current reporting-field reference | Yes for field names and matrix/unit routing; it is not scientific calculation authority. |

The earlier intake found filename/control-block inconsistencies among preserved SOP candidates. Those facts remain documented in [authoritative_method_file_manifest.csv](authoritative_method_file_manifest.csv), but the user's explicit current-method decision resolves which revision controls this design. Controlled DOCX files remain ignored and uncommitted.

## Source integrity and retention

| Source | SHA-256 | Retention |
| --- | --- | --- |
| `MN OCM Metrc Terpenes.xlsx` | `2238a38be106d64f123de83005f6e4d22ebc7335691e03bc067b081bca7ce8c2` | Raw workbook remains outside the repository and uncommitted. |
| `ASCIIData.txt` | `89d3fa8db21e28d7525ea6261ec6a3932aa226982e6f039a3b35822a54b93974` | Raw LabSolutions evidence remains outside the repository and uncommitted. |

The LabSolutions file was inspected only to confirm that it is block-oriented and contains repeated `Compound Results(Ch1)` sections. No raw sample row, customer information, or instrument value was copied into tracked evidence. The final-unit and dilution decisions come from the user's approved method decision, not from an inferred raw value.

## Minnesota OCM Metrc workbook inspection

The raw workbook contains exactly two worksheets:

| Worksheet | Used range | Reporting route |
| --- | --- | --- |
| `AdditionaL-terpenes (%)` | `A1:F33` | Percentage fields for Raw Plant Material and Concentrate/Extract. |
| `Additional-Terpenes (mg_g)` | `A1:F33` | mg/g fields for Infused Products. |

The tracked derivative [metrc_terpenes_analyte_mapping.csv](metrc_terpenes_analyte_mapping.csv) contains only field labels and approved mapping logic. It contains no workbook identifiers, placeholder identifiers, customer data, or raw analytical values.

### Exact reportable measurands

1. Alpha-Bisabolol
2. Alpha-Humulene
3. Alpha-Pinene
4. Alpha-Terpinene
5. Beta-Caryophyllene
6. Beta-Myrcene
7. Beta-Pinene
8. Camphene
9. Caryophyllene Oxide
10. Delta-3 Carene
11. Eucalyptol
12. Gamma-Terpinene
13. Geraniol
14. Guaiol
15. Isopulegol
16. Limonene
17. Linalool
18. Nerolidol
19. Ocimene
20. P-Isopropyltoluene (P-Cymene)
21. Terpinolene

### Present in the state template but intentionally ignored

- Alpha-Myrcene
- Alpha-Phellandrene
- Beta-Bisabolene
- Cis-Nerolidol
- Cymene
- Farnesene
- Fenchol
- Other Terpenes
- Phytol
- Terpineol
- Valencene

No blank result row is designed for an untested template analyte. `Nerolidol` is used instead of `Cis-Nerolidol`, and `P-Isopropyltoluene (P-Cymene)` is used instead of generic `Cymene`.

## Resolved requirement coverage

| Requirement | Status | Authority/decision |
| --- | --- | --- |
| Final actual-sample `Conc.` unit | resolved | Final `ug/g`, user-approved. |
| Dilution behavior | resolved | LabSolutions already applies dilution; QBench must not reapply it. |
| mg/g conversion | resolved | `ug/g / 1000`. |
| Percent conversion | resolved | `ug/g / 10000`. |
| Reportable mapping | resolved | Exactly 21 reportable measurands from 23 internal channels. |
| Ocimene and Nerolidol rollup | resolved | Missing, blank, no-peak, zero, and negative components contribute zero; positive components retain full precision and each pair sums once. |
| LOQ source | resolved | Matrix-specific QBench Key/Value Store; reportable combined analyte keys. |
| Below-LOQ report qualifier | resolved | Controlling SOP: report `<LOQ`. |
| MU source | resolved | Matrix-specific QBench Key/Value Store `MU%`; component MUs for combined analytes. |
| Combined MU method | resolved | Independent relative-uncertainty propagation with blank/denominator guards. |
| Total Terpenes | resolved | Sum 21 unrounded reportable values strictly above their matrix LOQs; combined analytes once. |
| Rounding | resolved | Full precision internally; three decimals only at display. |
| Metrc routing | resolved | Percent for Raw Plant Material and Concentrate/Extract; mg/g for Infused Product. |
| COA units | resolved | Display both mg/g and percent. |
| Audit-only data | resolved | Dimethylacetamide and Peak Table excluded from reportable results. |
| Terpenes Pass/Fail | resolved | Prohibited; assay is quantitative-only. |
| Missing/negative/below-threshold combined component handling | resolved | Explicit user-approved laboratory reporting rule: nonpositive/absent components contribute zero; every positive numeric component contributes at full precision without component LOQ filtering. |

## Controlling SOP text result and final user decision

Read-only structural inspection found the controlling SOP's reporting rule: a sample analyte below LOQ is reported as `<LOQ`; a sample analyte at or above LOQ is quantified when QC requirements are met. No statement was found that defines the numeric contribution of a missing, negative, or below-threshold Ocimene/Nerolidol component channel.

Visual DOCX rendering could not be completed because LibreOffice is unavailable in the local runtime. The relevant text was therefore checked structurally through the DOCX OOXML; no document was modified or re-exported. The missing numeric preprocessing behavior was subsequently resolved by the user's explicit approved laboratory reporting rule.

## Classification

`calculation_contract = passed_authoritative_method_documentation_and_user_approved_reporting_rules`

The former component-preprocessing marker is retired. See [calculation_contract.md](calculation_contract.md) and [calculation_test_vectors.csv](calculation_test_vectors.csv) for the approved rule and passing boundary cases.
