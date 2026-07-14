# Terpenes Codex Build Brief v3 - METRC CSV Template Integration

## Source files
- METRC CSV upload template workbook: `6867a117-96f8-4aa6-87ba-7fe7fdc49931.xlsx`
- Prior LabSolutions ASCII import fixture and parser remain part of the build.
- Prior QBench worksheet JSON shells remain the template-generation targets.

## New METRC conclusions

1. Generate METRC export rows by profile. The template uses `%` for raw plant material and concentrate/extract terpene rows, and `mg/g` for infused product additional/sub-contract terpene rows.
2. Keep both `%` and `mg/g` results in QBench for every analyte. The export profile decides which unit is populated in the METRC CSV/template row.
3. Do not use generic `Cymene` for the p-Cymene method analyte. Use `P-Isopropyltoluene (P-Cymene)` or `P. Isopropyltoluene` rows.
4. METRC does not provide separate cis/trans Ocimene rows in this template. Export `Ocimene = cis-Ocimene + trans-Ocimene`.
5. METRC provides `Cis-Nerolidol` and generic `Nerolidol`, but no `Trans-Nerolidol`. Export `trans-Nerolidol`/LabSolutions `Nerolidol 2` to generic `Nerolidol` unless the lab approves a total Nerolidol rule.
6. Treat R&D Terpenes `Alpha-Humulene (ppm)` and Full Panel Finished Products mixed units as configuration warnings that must be explicitly accepted before automatic export.

## Terpene-related template sheets found

- `Additional-Terpenes (%)`: 26 terpene-related rows
- `Additional-Terpenes (mg_g)`: 26 terpene-related rows
- `Full Panel (FinPrd) Tribal Only`: 26 terpene-related rows
- `R&D Terpenes`: 26 terpene-related rows
- `Full Panel (Conc.) Tribal Only`: 25 terpene-related rows
- `Full Panel (Flower) Tribal Only`: 25 terpene-related rows
- `Sub-Contract - Terpenes (ConEx)`: 13 terpene-related rows
- `Sub-Contact - Terpenes(Infused)`: 13 terpene-related rows
- `Sub-Contract - Terpenes (RawPM)`: 13 terpene-related rows

## Codex implementation task

```text
Add METRC CSV/template export-profile support to the Terpenes worksheet generator. Read config/metrc_export_profiles.yml and config/terpenes_analytes.yml. For each selected profile, generate export rows using the exact METRC analyte label and unit from the profile. Preserve LabSolutions/QBench cis/trans rows, but roll up Ocimene into one METRC Ocimene field. Map trans-Nerolidol/Nerolidol 2 to generic Nerolidol and cis-Nerolidol to Cis-Nerolidol. Use P-Isopropyltoluene (P-Cymene) for p-Cymene, never generic Cymene. Generate Total Terpenes from final export values. Leave Other Terpenes blank/zero unless explicitly configured. Add validation warnings for R&D Alpha-Humulene ppm and Full Panel Finished Products mixed units.

Acceptance criteria:
1. The generator outputs both % and mg/g result cells for every reportable terpene analyte.
2. METRC export profiles select units without changing underlying LabSolutions import calculations.
3. Ocimene export equals cis-Ocimene + trans-Ocimene for both % and mg/g profiles.
4. No trans-Ocimene field is required or generated for METRC unless a future template adds one.
5. cis-Nerolidol and generic Nerolidol are exported separately according to config.
6. p-Cymene maps to P-Isopropyltoluene (P-Cymene) / P. Isopropyltoluene and not to generic Cymene.
7. Validation fails if a configured analyte cannot be found in the selected METRC profile and no approved fallback exists.
8. Validation warns on Full Panel Finished Products mixed terpene units and R&D Alpha-Humulene ppm.
9. The extracted METRC template row fixture is covered by tests so future template changes are detected.
```

## Reportable mapping snapshot

| Worksheet analyte | METRC target | Rule | Notes |
|---|---|---|---|
| α-Pinene | Alpha-Pinene | direct | Greek alpha normalized to Alpha. |
| Camphene | Camphene | direct |  |
| β-Myrcene | Beta-Myrcene | direct | Greek beta normalized to Beta. |
| (-)-β-pinene | Beta-Pinene | direct | METRC label omits (-)- stereochemical prefix. |
| Delta-3-carene | Delta-3 Carene | direct | METRC uses a space before Carene. |
| α-Terpinene | Alpha-Terpinene | direct |  |
| cis-Ocimene | Ocimene | rollup_component | METRC template has no cis/trans Ocimene split. Sum cis-Ocimene + trans-Ocimene for the Ocimene export field. |
| d-Limonene | Limonene | direct | METRC label omits d- prefix. |
| p-Cymene | P-Isopropyltoluene (P-Cymene) | direct_preferred_over_generic | Use the explicit p-Cymene/P-Isopropyltoluene row; do not use generic Cymene unless method expands to generic cymene. |
| trans-Ocimene | Ocimene | rollup_component | METRC template has no trans-Ocimene row. Sum cis-Ocimene + trans-Ocimene for the Ocimene export field. |
| Eucalyptol | Eucalyptol | direct | SOP synonym 1,8-Cineole maps to Eucalyptol in METRC. |
| γ-Terpinene | Gamma-Terpinene | direct | Greek gamma normalized to Gamma. |
| Terpinolene | Terpinolene | direct |  |
| Linalool | Linalool | direct |  |
| (-)-Isopulegol | Isopulegol | direct | METRC label omits (-)- stereochemical prefix. |
| Geraniol | Geraniol | direct |  |
| β-Caryophyllene | Beta-Caryophyllene | direct |  |
| α-Humulene | Alpha-Humulene | direct | R&D Terpenes tab has Alpha-Humulene as ppm; all other terpene panels use % or mg/g. Treat as a template issue until confirmed. |
| cis-Nerolidol | Cis-Nerolidol | direct | METRC has an explicit Cis-Nerolidol row. |
| trans-Nerolidol | Nerolidol | direct_assumed_trans | METRC template has generic Nerolidol but no Trans-Nerolidol. Map LabSolutions Nerolidol 2/trans-Nerolidol to generic Nerolidol unless method owner requires total Nerolidol. |
| (-)-Guaiol | Guaiol | direct | METRC label omits (-)- stereochemical prefix. |
| Caryophyllene Oxide | Caryophyllene Oxide | direct |  |
| (-)-α-Bisabolol | Alpha-Bisabolol | direct | METRC label omits (-)- and uses Alpha. |

## Profile coverage warnings

The METRC template is not uniformly complete across all terpene-related profiles. Codex should validate profile coverage before export and fail or warn when a selected profile lacks a reportable analyte row.

- `additional_raw_concentrate` missing: none
- `additional_infused` missing: none
- `full_panel_concentrates_tribal_only` missing: (-)-Guaiol
- `full_panel_flower_tribal_only` missing: p-Cymene
- `full_panel_finished_products_tribal_only` missing: none
- `rd_terpenes` missing: none
- `subcontract_concentrate_extract` missing: Camphene, Delta-3-carene, cis-Ocimene, p-Cymene, trans-Ocimene, γ-Terpinene, Terpinolene, (-)-Isopulegol, Geraniol, cis-Nerolidol, (-)-Guaiol
- `subcontract_infused` missing: Camphene, Delta-3-carene, cis-Ocimene, p-Cymene, trans-Ocimene, γ-Terpinene, Terpinolene, (-)-Isopulegol, Geraniol, cis-Nerolidol, (-)-Guaiol
- `subcontract_raw_pm` missing: Camphene, Delta-3-carene, cis-Ocimene, p-Cymene, trans-Ocimene, γ-Terpinene, Terpinolene, (-)-Isopulegol, Geraniol, cis-Nerolidol, (-)-Guaiol
