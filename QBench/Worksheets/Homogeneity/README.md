# Homogeneity

- QBench assay ID: 11
- Assay code: HOM
- Worksheet/template status: Homogeneity Test Worksheet; Cannabinoid Potency Batch Worksheet is the primary copy/paste source.
- Report named cells: see `../../NAMED_CELL_INDEX.md` and `../../REPORT_RENDERING_MAP.md`.
- Parser status: see `../../FILE_PARSER_INDEX.md`.
- Automation status: see `../../AUTOMATION_INDEX.md`.
- COA/report dependency: worksheet named cells feed the Certificate of Analysis report.

## Controlling calculation contract

Report-facing cannabinoid content is `mg/unit`, equivalent to `mg/serving` for the tested unit.

The worksheet must distinguish the basis of the entered replicate mass:

- **Individual unit/serving mass:** `mg/unit = mg/g x entered individual unit/serving mass`.
- **Full container mass/volume:** `mg/unit = mg/g x entered total container mass/volume / servings per container`.

Do not divide an individual gummy, piece, capsule, or serving mass by Servings Per Container. Servings Per Container is required only when the entered mass represents the complete multi-serving container.

Cannabinoid label variance remains:

`(actual mg/unit - label mg/unit) / label mg/unit`

The stored value is a decimal ratio and is displayed with percentage number formatting. Do not multiply the formula by 100 before applying percent formatting.

## MN OCM highest-deviation rule

Summary boxes and final Pass/Fail must use the replicate with the **greatest absolute deviation** from the applicable label claim or mass basis, not the highest numerical mass or cannabinoid result.

Example: between `+9.0%` and `-13.5%`, select the replicate associated with `-13.5%`, preserve the negative sign for display, and compare `ABS(-13.5%)` with the allowed tolerance.

## Cannabinoid target and label lookup

- Product Label Amount values use QBench `product_label_*` sample fields unless verified otherwise by a current export.
- `Total CBG` normalizes internally to `CBG`; `Total CBGa` normalizes internally to `CBGa`.
- The original entered target name remains the COA-facing label.
- CBG and CBGa are not manual-only targets.
- Manual override cells must be blank by default and must clearly identify when an override is active.

## True Mass per Unit source

The preferred workflow is to record Test additional field `true_mass_per_unit` on each Cannabinoid Potency Test, expose it as the final column of the Cannabinoid Potency Batch Worksheet, and copy/paste it with the potency results into the Homogeneity Paste tab.

The field is optional at the potency-batch level: a missing Test value should remain blank and must not break the batch worksheet. Homogeneity may still require all ten masses before producing a final result.

See `../Cannabinoids/development/2026-07-20_true_mass_optional/` for the batch-column design, patcher, evidence, and Sandbox checklist.

## JSON integrity requirements

When editing a Homogeneity worksheet export:

- Update both `config.worksheets[n].data` and root `data["Paste"]`, `data["Data"]`, and `data["COA"]`.
- Preserve `report_results = COA!A1:G20` and `replicate_results = COA!A10:G20` unless a separately approved report-layout change is being made.
- Preserve formulas as formulas; do not flatten evaluated values.
- Avoid duplicate named-cell targets.
- Retain legacy internal named-cell system names containing `mg_container` only when required for compatibility; visible labels must say `mg/unit`.

## Promotion boundary

Every candidate requires inactive QBench Sandbox import, real-row calculation checks, COA preview, export/reopen verification, and confirmation that both JSON data layers remain synchronized before activation or production promotion.
