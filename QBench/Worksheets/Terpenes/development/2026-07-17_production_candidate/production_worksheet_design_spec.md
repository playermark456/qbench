# Terpenes production worksheet design specification

## Scope and safety boundary

This is a documentation-only architecture proposal for two future Sandbox candidates. It does not authorize candidate JSON generation. The June 30 source exports and technical proof worksheets remain unchanged references. The design is quantitative-only: no Terpenes Pass/Fail named cell, formula, report field, tile, or automation value is permitted.

Formula implementation is intentionally deferred until the authoritative calculation contract is supplied and confirmed.

## Test worksheet

Recommended tab order:

1. `Report`
2. `Data`
3. `Specifications`
4. `Audit`

An optional `METRC` tab is deferred until the authoritative METRC reporting policy is resolved. It must not be inferred from another assay.

### Data tab sections

| Section | Content | Ownership |
| --- | --- | --- |
| Sample identity | Test/sample identity expressions and staff review context. | QBench/Test context; not a publisher destination. |
| Raw instrument values | The exact 23 scalar concentration inputs at D2:Z2 in the proven channel order. | Editable/importable destinations only; no formula. |
| Sample preparation and calculation inputs | B12:B18: sample mass, final volume, dilution fields, instrument-unit confirmation, and preparation confirmation. | Exact scalar contract; no formula. |
| Controlled disposition | B22:B23: batch QC disposition and publish readiness. | Controlled values only; neither parser nor transfer may populate them. |
| Source and audit metadata | B28:B38: source file and instrumentation traceability. | Exact scalar contract; no calculation/report result. |
| Calculated-result review | Per-channel mg/g, percent, LOQ/qualifier, and staff-review cells outside the 43 inputs. | Formula-owned only after calculation approval. |

The `Audit` tab should present source filename/hash, parser state, import status, transfer state, and non-reportable diagnostic context without exposing those values on the COA. Staff-editable inputs, formula-owned cells, and audit-only cells must have distinct styles and read-only behavior.

Input cells, formula cells, and audit-only cells will use clearly different shading, borders, wrapped headers, number formats, widths, and row heights. No calculated value may be written directly into a 43-input destination.

### Specifications tab

The review table will have one row per reportable channel and include display analyte, instrument concentration, mg/g, percent, LOQ, measurement uncertainty when authorized, qualifier, METRC display name/profile context, and staff note. It is for quantitative review, not compliance classification.

### Report tab

The Report tab will be a compact formula-driven COA table. It will show only approved reportable analytes, result units, and authorized qualifier/LOQ information. It must exclude raw concentrations, preparation details, audit data, Dimethylacetamide, Peak Table data, internal system names, and Pass/Fail.

`report_results` will be defined only after the approved COA measurand policy determines the exact complete table. It will include its header row and intended reportable rows only, with no empty trailing space. Its documentation-only shape is `Report!A1:F{approved_row_count_plus_header}`; no exact row count may be chosen while `TERPENES_REPORT_MEASURANDS_UNRESOLVED` remains open.

## Batch worksheet

Recommended tab order:

1. `Run Setup`
2. `Raw Import`
3. `Normalized Import`
4. `Batch Review`
5. `Test Transfer`
6. `Audit`

| Tab | Purpose | Required boundary |
| --- | --- | --- |
| Run Setup | Polished sequence surface for standards, blank, system suitability, QC rows, and sample rows. | No customer-result Pass/Fail. |
| Raw Import | Byte/order-preserving parser landing surface with no scientific interpretation. | Parser-owned cells only; no report or Test destinations. |
| Normalized Import | The normalized 57-column no-code input surface, including source metadata and audit data. | Parser writes only A:AE and AH:BE; AF/AG are formula-owned. |
| Batch Review | Readable row-level view of sequence, identifiers, channels, import/duplicate status, QC/audit notes, and shortened source reference. | Dimethylacetamide and Peak Table data remain audit-only; no automatic QC Review. |
| Test Transfer | Deterministic one-row-per-Test manual copy/paste surface in the exact Test input order, with six staff instructions. | Never transfer B22/B23 or values that require manual preparation authority. No automatic Publish. |
| Audit | Source hashes, duplicate checks, parser state, and transfer history. | Audit-only; excluded from report and scientific calculations. |

Live reference worksheets show that Batch-to-Test activity is commonly separated into a `Data Modified` Batch automation, but the exact automation body and scientific mapping were not adopted. The Terpenes proposal retains a manual, reviewable transfer gate until an authorized transfer contract exists.

## Data classifications

| Classification | Candidate representation |
| --- | --- |
| Raw instrument values | 23 `Compound Results(Ch1) > Conc.` values only. Peak Table, area, height, and retention time are not quantitation sources. |
| Sample preparation inputs | Exact Test scalar fields; authority and units pending the calculation contract. |
| Calculated mg/g and percent | Formula-owned cells outside the destination contract; not implemented until authoritative confirmation. |
| LOQ and MU | Review/report fields only after their scientific source and handling are confirmed. |
| Audit-only data | Source metadata, Dimethylacetamide, and Peak Table context; excluded from Report and METRC-facing results. |
| Staff-review fields | Quantitative review notes, controlled batch disposition, and manual transfer checks; never sample Pass/Fail. |
| Batch-to-Test transfer fields | Deterministic scalar block matching the 23 instrument channels plus only Batch-authoritative scalar inputs. |
| COA-facing values | Compact formula-driven approved measurand table inside `report_results`. |
| METRC-facing values | Profile-specific quantitative values, with required Ocimene/Nerolidol handling, after approved profile and qualifier rules are confirmed. |

## Open design gates

The candidate cannot be generated, imported, or approved until the calculation contract establishes instrument concentration units, authoritative preparation inputs, dilution-factor behavior, rounding/significant figures, below-LOQ treatment, permitted qualifiers, and the approved COA measurand policy.

Documentation markers retained for that gate:

- `TERPENES_CONC_UNIT_UNRESOLVED`
- `TERPENES_MG_G_FORMULA_UNRESOLVED`
- `TERPENES_PERCENT_FORMULA_UNRESOLVED`
- `TERPENES_LOQ_POLICY_UNRESOLVED`
- `TERPENES_ROUNDING_POLICY_UNRESOLVED`
- `TERPENES_MU_POLICY_UNRESOLVED`
- `TERPENES_REPORT_MEASURANDS_UNRESOLVED`
- `TERPENES_OCIMENE_POLICY_UNRESOLVED`
- `TERPENES_NEROLIDOL_POLICY_UNRESOLVED`

These are documentation-only markers and must not be placed in QBench.

## Future Sandbox validation sequence

1. Resolve and approve the authoritative calculation contract.
2. Generate fresh-UUID Test and Batch candidates from preserved old-renderer envelopes.
3. Validate JSON structure, styles, dual data representations, formula ownership, and named-cell uniqueness locally.
4. Import only into isolated Sandbox definitions.
5. Save through the normal version workflow and prove the visible Draft row.
6. Reopen from the Worksheets list and export the saved definition with **Export Spreadsheet**.
7. Compare formula text, styles, dimensions, named cells, report range, and UUID regeneration semantically.
8. Instantiate one synthetic Test and Batch without customer data.
9. Verify parser landing, review, manual transfer, calculation, blank/error behavior, and COA preview against approved test vectors.
10. Promote only after independent scientific review and Sandbox evidence pass.
