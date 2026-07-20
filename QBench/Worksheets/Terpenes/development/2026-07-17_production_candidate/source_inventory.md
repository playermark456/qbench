# Terpenes production-candidate source inventory

## Preserved source exports

| Source role | Local raw-evidence location | SHA-256 |
| --- | --- | --- |
| Test worksheet visual shell | `source_exports/` (ignored raw evidence) | `2ebae7a36e95038777f116a7d8ce821009841e39f6a9f338e552eba90c096138` |
| Batch worksheet visual shell | `source_exports/` (ignored raw evidence) | `44431ec52954228b111a5ed698a6bafd6464a5a2f7669b966bdb447a005c0cf1` |

Both files were copied byte-for-byte into this package. They remain immutable visual and structural references, not candidate files.

## Test worksheet source

The source contains three tabs, in the correct candidate tab order: `Report`, `Data`, and `Specifications`. Each has a 652-by-350 configured canvas; the populated exported grids are respectively 8-by-8, 5-by-31, and 41-by-25.

| Tab | Visible staff-facing content | Formatting and layout | Defects / incomplete content |
| --- | --- | --- | --- |
| Report | No visible content. | 8 rows at 27 px and eight 100 px text columns; no merges or conditional formatting. | Entirely blank, has no formulas, no named report range, and cannot support a COA rendering. |
| Data | Sample identity headers at A1:C1; the 23 analyte headings at D1:Z1; template identity expressions in A2:C2; a placeholder result-unit label. | Five configured 27 px rows, 31 columns, and cell-level styles across A1:AE4. The first three columns are 170/159/160 px; analyte columns start at 100 px. No merges, filters, freezes, or conditional formatting. | Zero formulas. It has no preparation inputs, no calculated-result review, no audit/source section, and the `Result (mg/g or %?)` text is an unresolved placeholder. |
| Specifications | Customer/program/matrix header, then a 23-analyte quantitative review table with columns for measurement uncertainty, LOQ, percent, and mg/g. | 41 configured 27 px rows, 25 columns, and cell-level header/body styles for the visible table. No merges, filters, freezes, or conditional formatting. | Zero formulas and blank MU, LOQ, percent, and mg/g result cells. It is a useful visual review shell but not a functioning specification workflow. |

The source has 47 named cells: 46 legacy individual percent/mg/g METRC cells across the 23 channels and one legacy Terpenes cell. None is the proven 43-input destination contract. These legacy result destinations must not be confused with parser or publisher write targets.

## Batch worksheet source

The source has one tab, `Sheet1`, on a 652-by-350 configured canvas with a 96-by-28 populated grid. It is a sequence-oriented staff-facing shell:

- A1 is `Sample ID`.
- Rows 2:6 are standards; row 7 is a blank; rows 8:10 are system-suitability rows.
- Rows 11:96 reserve sample and product-matrix expressions for batch Tests.

It has 96 configured 27 px rows and 28 columns. The first two columns are 194 px and 221 px; the remaining configured columns begin at 100 px. It has cell-level styling for the sequence and headers, but no merges, filters, freezes, conditional formatting, named cells, or formulas.

The sequence, standards, blank, system-suitability rows, sample-row surface, and staff-facing width/style pattern are appropriate references for the candidate's `Run Setup` tab. The source does not provide an instrument import surface, analyte results, audit data, transfer surface, no-code parser mapping, or QC workflow.

## Reusable versus non-reusable source elements

| Reuse in candidate | Do not retain unchanged |
| --- | --- |
| Test tab order, identity header pattern, analyte display order, quantitative Specifications table layout, and basic staff-facing styles. | Blank Report tab, placeholder result-unit text, and all formula-free/blank result cells. |
| Batch sequence structure: standards, blank, system suitability, sample rows, widths, and header styling. | The single `Sheet1` tab name, absence of import/transfer/audit sections, and absence of formula ownership. |
| Exact 23-channel display order in the Test Data header. | Legacy result named-cell scheme as a substitute for the proven 43 scalar input contract. |

## Supporting contracts inspected

- The proven scalar mapping defines exactly 43 independent Test inputs: 23 instrument concentrations at `Data!D2:Z2`, seven preparation fields at `Data!B12:B18`, two controlled fields at `Data!B22:B23`, and eleven audit/source fields at `Data!B28:B38`.
- The no-code fallback proves two non-overlapping Batch import routes: `A2:AE2` to `Instrument Import!A2` and `AH2:BE2` to `Instrument Import!AH2`. Columns AF and AG are worksheet-owned formulas and must never be parser-write targets.
- The runtime-instantiation evidence proves the 43 scalar destinations persisted in an instantiated Test; it does not establish an approved scientific calculation contract for a staff-facing production worksheet.
- The user-approved method decision establishes that the 23 actual-sample values are final `ug/g` and already include dilution. Preparation/dilution fields remain compatibility and audit inputs; they must not be reapplied to the analytical result.
- The Minnesota OCM Metrc workbook SHA-256 is `2238a38be106d64f123de83005f6e4d22ebc7335691e03bc067b081bca7ce8c2`. Its two sheets provide percentage fields for Raw Plant Material and Concentrate/Extract and mg/g fields for Infused Products. The raw workbook remains outside the repository; only the sanitized field mapping is tracked.

## Calculation-contract and candidate status

The user approved Terpene Analysis SOP v1.2 as controlling, the version-1.0 Form and Protocol as current, the collected Validation Report as current, and actual-sample LabSolutions `Compound Results(Ch1) > Conc.` as final `ug/g` with dilution already applied. The conversions, 21-measurand mapping, Key/Value LOQ/MU dimensions, independent combined-MU method, strict-above Total Terpenes rule, three-decimal display rounding, dual-unit COA, matrix-specific Metrc route, and quantitative-only model are now documented.

The user explicitly approved the final component preprocessing rule: missing, blank, no-peak, zero, and negative component results contribute zero; positive numeric results contribute at full precision; and no component-channel LOQ is applied. Only the combined reportable Ocimene or Nerolidol result is compared with its matrix-specific reportable LOQ.

`calculation_contract = passed_authoritative_method_documentation_and_user_approved_reporting_rules`

The local Test and Batch candidates were generated under `production_candidates/` and passed the dedicated Phase 3 validator. They have not been imported into QBench. Isolated Sandbox saved-definition and runtime validation remain the next controlled phase.
