# Live non-Terpenes Report and COA patterns

## Safe worksheet-definition evidence

| Reference | Report-facing tab | `report_results` | Headers included | Backing/report separation |
| --- | --- | --- | --- | --- |
| Cannabinoid Potency Test | `Report` | `Report!A1:F21` | Yes | Data, Purity Data, Specifications, Report, METRC. |
| Heavy Metals Test | `Report` | `Report!A1:F6` | Yes | Data, Specifications, Report, METRC. |
| Quantitative Pesticides Test | `Report` | `Report!A1:L40` | Yes | A large Specifications table feeds a smaller bounded report surface. |
| Homogeneity Test | `COA` | `COA!A1:G20` | Yes | Paste, Data, and COA are distinct. |

## Reusable patterns

- The named report range includes the header row.
- The COA-facing range is compact and explicitly bounded; it does not automatically cover the full technical worksheet.
- Report tabs reference calculated/review tabs rather than raw import data directly.
- Blank-return formulas are common in Report and COA surfaces, allowing unused rows to remain visually empty.
- The exact empty-row suppression behavior of the live report-template renderer was not extracted. It must be verified in Sandbox preview rather than assumed.
- Page-width constraints are managed by a deliberately narrow report range: six or seven columns in compact assays, with a larger bounded range for a large analyte panel.
- LOQ, qualifier, result, and MU presentation vary by assay and are not transferable scientific policy.

The active Certificate of Analysis template definition shell was inspected read-only. The source editor did not expose safe text through the visible page representation, so no live Jinja body was copied. Existing repository COA source remains a separate local reference; this review does not claim a newly verified live rendering call.

## Terpenes proposal

- Use a dedicated `Report` tab.
- Define `report_results` as `Report!A1:E23`.
- Include the header row, exactly 21 approved reportable measurands, and Total Terpenes.
- Use columns Analyte, Result (mg/g), Result (%), LOQ, and MU (%).
- Display below-LOQ reportable analytes as `<LOQ` according to the controlling SOP; verify the fixed-row qualifier rendering in Sandbox COA preview.
- Exclude raw concentrations, preparation inputs, source/audit fields, Peak Table data, Dimethylacetamide, internal identifiers, and Pass/Fail.
- Keep the range narrow enough for a single COA table and verify blank-range and page-width behavior in Sandbox.
