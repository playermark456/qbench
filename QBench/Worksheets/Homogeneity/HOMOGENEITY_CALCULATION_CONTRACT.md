# Homogeneity Calculation and Data Contract

Date: 2026-07-20
Status: controlling design guidance for future repository and Codex work; QBench candidates still require Sandbox validation.

## Purpose

This document resolves conflicting historical instructions in the repository. Future Homogeneity changes should follow this contract unless a newer dated regulatory decision explicitly supersedes it.

## Inputs

A Homogeneity evaluation uses exactly ten Cannabinoid Potency replicate rows. Preserve row alignment among:

- Sample ID
- Cannabinoid Potency Test ID
- cannabinoid results
- measured mass
- target label claims

The preferred mass source is Test additional field `true_mass_per_unit`, exposed in column AH of the Cannabinoid Potency Batch Worksheet and copied with the potency rows.

## Mass Entry Basis

The worksheet must explicitly distinguish:

### Individual unit/serving mass

Use for individually weighed gummies, chocolates, capsules, pieces, and similar units.

```text
mass_per_unit = entered replicate mass
mg/unit = mg/g x mass_per_unit
```

Do not divide by Servings Per Container.

### Full container mass/volume

Use when each replicate value is the total mass or volume of a complete multi-serving container.

```text
mass_per_unit = entered total container mass or volume / servings per container
mg/unit = mg/g x mass_per_unit
```

Servings Per Container is required only in this mode.

## Variance

Mass and cannabinoid label variance are stored as decimal ratios:

```text
variance = (actual - claim) / claim
```

Apply percentage number formatting for display. Do not multiply the formula by 100 before percentage formatting.

## MN OCM greatest absolute deviation rule

Summary values and final Pass/Fail use the replicate with the greatest absolute deviation, not the highest numerical measured value.

Example:

```text
replicate A = +9.0%
replicate B = -13.5%
selected replicate = B
reported signed deviation = -13.5%
threshold comparison = ABS(-13.5%)
```

For each summary category:

- identify the signed deviation with the greatest absolute magnitude;
- return the mass or mg/unit value from that same replicate row;
- preserve the signed deviation for display;
- compare its absolute magnitude with the allowed tolerance.

Apply this independently to:

- mass variance;
- Target Cannabinoid 1 label variance;
- Target Cannabinoid 2 label variance, when Target 2 is used.

## Cannabinoid target lookup

- Use QBench `product_label_*` sample fields for Product Label Amounts unless a current export proves a different field contract.
- `Total CBG` normalizes internally to `CBG`.
- `Total CBGa` normalizes internally to `CBGa`.
- Preserve the original entered target name for COA-facing text.
- CBG and CBGa are not manual-only targets.
- Manual override cells must be blank by default and visibly identify when active.

## Report display

- Visible terminology: `mg/unit`.
- `mg/unit` is equivalent to mg/serving for the tested unit.
- COA mg/unit values display to two decimal places.
- COA variances display as signed percentages, normally one decimal place.
- Summary labels must say `at Highest Deviation` or `at Highest Absolute Deviation`, not `Highest` when that could imply the largest numerical result.

## Pass/Fail

Final Pass/Fail remains `INCOMPLETE` until required worksheet checks are satisfied. Once ready, fail when any applicable greatest absolute deviation exceeds the allowed variance.

## JSON requirements

Every formula, visible label, style, and number-format change must be synchronized across:

- `config.worksheets[n].data`
- root `data["Paste"]`
- root `data["Data"]`
- root `data["COA"]`

Preserve:

- `report_results = COA!A1:G20`
- `replicate_results = COA!A10:G20`
- COA header row 10
- replicate rows 11 through 20
- formula cells as formulas
- unique named-cell targets

Legacy internal named-cell identifiers containing `mg_container` may remain only for compatibility. Visible labels must use `mg/unit`.

## Validation boundary

Static JSON validation is necessary but not sufficient. Every candidate must undergo:

1. inactive QBench Sandbox import;
2. real-world individual-unit calculation check;
3. full-container calculation check;
4. positive-versus-negative greatest-deviation test;
5. COA preview;
6. Export Spreadsheet and reopen verification;
7. dual-layer JSON comparison.

Do not activate or promote a candidate based only on a local validation report.
