# Terpenes current-state and gap analysis

Date: 2026-07-14

Scope: repository-only reconnaissance for implementing Terpenes in QBench. No QBench object, active/raw worksheet export, COA source, automation, parser, protocol worksheet, or report configuration was modified.

## Source files used

| Shorthand | Repository file |
|---|---|
| ROOT | `AGENTS.md` |
| TR-AGENTS | `QBench/Worksheets/Terpenes/AGENTS.md` |
| EXPORT-STATUS | `QBench/Docs/qbench_export_status.md` |
| SYSTEM-MAP | `QBench/SYSTEM_MAP.md` |
| ASSAY-MAP | `QBench/ASSAY_ID_MAP.md` |
| NAMED-CELL-INDEX | `QBench/NAMED_CELL_INDEX.md` |
| REPORT-MAP | `QBench/REPORT_RENDERING_MAP.md` |
| AUTOMATION-INDEX | `QBench/AUTOMATION_INDEX.md` |
| PARSER-INDEX | `QBench/FILE_PARSER_INDEX.md` |
| COA-BODY | `COA format/COA Body Source Code.txt` |
| COA-SOURCE-NOTE | `QBench/COA/Source/README.md` |
| T42 | `QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_42__worksheet_export_spreadsheet__active__2026-07-04.json` |
| T43 | `QBench/Rescans/2026-07-04/Worksheets/Terpenes/terpenes__id_43__worksheet_export_spreadsheet__active__2026-07-04.json` |
| T42-0630 | `QBench/Worksheets/Terpenes/terpenes__terpenes_test_ws_id_42__worksheet_export_spreadsheet__active__2026-06-30.json` |
| HM5 | `QBench/Rescans/2026-07-04/Worksheets/Heavy_Metals/heavy_metals__id_5__worksheet_export_spreadsheet__active__2026-07-04.json` |
| HM6 | `QBench/Rescans/2026-07-04/Worksheets/Heavy_Metals/heavy_metals__id_6__worksheet_export_spreadsheet__active__2026-07-04.json` |
| RS11 | `QBench/Rescans/2026-07-04/Worksheets/Residual_Solvents/residual_solvents__id_11__worksheet_export_spreadsheet__active__2026-07-04.json` |
| RS12 | `QBench/Rescans/2026-07-04/Worksheets/Residual_Solvents/residual_solvents__id_12__worksheet_export_spreadsheet__active__2026-07-04.json` |
| PE13 | `QBench/Rescans/2026-07-04/Worksheets/Pesticides/pesticides__id_13__worksheet_export_spreadsheet__active__2026-07-04.json` |
| PE14 | `QBench/Rescans/2026-07-04/Worksheets/Pesticides/pesticides__id_14__worksheet_export_spreadsheet__active__2026-07-04.json` |
| PE15 | `QBench/Rescans/2026-07-04/Worksheets/Pesticides/pesticides__id_15__worksheet_export_spreadsheet__active__2026-07-04.json` |
| PE16 | `QBench/Rescans/2026-07-04/Worksheets/Pesticides/pesticides__id_16__worksheet_export_spreadsheet__active__2026-07-04.json` |
| SOURCE-README | `QBench/Worksheets/Terpenes/source/README.md` |
| BUILD-BRIEF | `QBench/Worksheets/Terpenes/source/terpenes_codex_build_brief_v3.md` |
| WORKSHEET-SPEC | `QBench/Worksheets/Terpenes/source/terpenes_worksheet_spec_v3.json` |
| ANALYTE-MASTER | `QBench/Worksheets/Terpenes/source/terpenes_analyte_master_v3.csv` |
| ASCII-SPEC | `QBench/Worksheets/Terpenes/source/labsolutions_ascii_integration_spec.md` |
| PARSER-SCRIPT | `QBench/Worksheets/Terpenes/source/parse_labsolutions_ascii.py` |
| RAW-FIXTURE | `QBench/Worksheets/Terpenes/source/Output_redacted_fixture.txt` |
| COMPOUND-FIXTURE | `QBench/Worksheets/Terpenes/source/labsolutions_compound_results_fixture.csv` |
| PEAK-FIXTURE | `QBench/Worksheets/Terpenes/source/labsolutions_peak_table_fixture.csv` |
| NORMALIZED-FIXTURE | `QBench/Worksheets/Terpenes/source/labsolutions_normalized_reportable_results_fixture.csv` |
| METRC-PROFILES | `QBench/Worksheets/Terpenes/source/metrc_terpene_export_profiles.json` |
| METRC-MAP | `QBench/Worksheets/Terpenes/source/metrc_terpene_reportable_mapping.csv` |
| SOURCE-MANIFEST | `QBench/Worksheets/Terpenes/source/MANIFEST.sha256` |

## Preflight and source-of-truth notes

| Finding | Source |
|---|---|
| The required Terpenes Prompt 0 package files are present in the repository: Terpenes AGENTS, preflight validation, source README, build brief, worksheet spec, and analyte master. | TR-AGENTS; `QBench/Worksheets/Terpenes/docs/source_package_preflight_validation.md`; SOURCE-README; BUILD-BRIEF; WORKSHEET-SPEC; ANALYTE-MASTER |
| The source package is an implementation input, not an approved QBench production template. | SOURCE-README |
| Terpenes worksheet IDs 42 and 43 must be treated as immutable source exports. | TR-AGENTS |
| The latest active Terpenes rescan files are the 2026-07-04 active exports for worksheet IDs 42 and 43; EXPORT-STATUS records both as changed from 2026-06-30, with unchanged tabs, named-cell counts, formula counts, and processed data. | EXPORT-STATUS; T42; T43 |
| Terpenes is QBench assay ID 8, code TR, with worksheet 42 as the Terpenes test worksheet and worksheet 43 as the Terpenes batch worksheet. | ASSAY-MAP; COA-BODY |

## Terpenes source-package inventory

All files under `QBench/Worksheets/Terpenes/source/` were inspected. The source directory contains 13 files: 12 package files plus `MANIFEST.sha256`; all 12 manifest-covered files verify `PASS`. Sources: SOURCE-README; SOURCE-MANIFEST.

| File | Current evidence | Source |
|---|---|---|
| `README.md` | Identifies the source package as implementation inputs, not approved production templates; lists expected parser summary counts. | SOURCE-README |
| `MANIFEST.sha256` | Lists 12 SHA-256-covered source files, excluding the manifest itself; current repository bytes verify 12/12. | SOURCE-MANIFEST |
| `terpenes_codex_build_brief_v3.md` | Defines METRC template conclusions, profile coverage warnings, and implementation acceptance criteria for both `%` and `mg/g` outputs, Ocimene rollup, Nerolidol mapping, p-Cymene specificity, and profile validation. | BUILD-BRIEF |
| `terpenes_worksheet_spec_v3.json` | Defines units, conversion formulas, QC rule inputs, LabSolutions import rules, METRC profile metadata, and unresolved decisions. | WORKSHEET-SPEC |
| `terpenes_analyte_master_v3.csv` | Contains 23 rows with worksheet labels, LabSolutions compound names, QBench keys, METRC targets, mapping rules, and unit notes. | ANALYTE-MASTER |
| `labsolutions_ascii_integration_spec.md` | Defines required LabSolutions ASCII sections and parser behavior; requires Compound Results for quantitation and Peak Table for integration review/QC. | ASCII-SPEC |
| `parse_labsolutions_ascii.py` | Repository-friendly parser that reads bracketed sections, parses Peak Table and Compound Results, aliases names, excludes Dimethylacetamide from reportable normalized rows, and writes JSON/CSV outputs. | PARSER-SCRIPT |
| `Output_redacted_fixture.txt` | Redacted LabSolutions ASCII fixture with `[Header]`, `[File Information]`, `[Sample Information]`, `[Original Files]`, `[File Description]`, `[Configuration]`, `[Peak Table(Ch1)]`, and `[Compound Results(Ch1)]`; contains 34 Peak Table rows and 24 Compound Results rows. | RAW-FIXTURE |
| `labsolutions_compound_results_fixture.csv` | Contains 24 Compound Results fixture rows; first row is Dimethylacetamide with `reportable=False`. | COMPOUND-FIXTURE |
| `labsolutions_peak_table_fixture.csv` | Contains 34 Peak Table fixture rows; first row is Dimethylacetamide with `reportable=False`. | PEAK-FIXTURE |
| `labsolutions_normalized_reportable_results_fixture.csv` | Contains 23 normalized reportable rows; first row is alpha-Pinene mapped to `α-Pinene`, with `labsolutions_conc`, sample amount, and dilution factor fields. | NORMALIZED-FIXTURE |
| `metrc_terpene_export_profiles.json` | Defines 9 METRC export profiles and 8 issues requiring confirmation. | METRC-PROFILES |
| `metrc_terpene_reportable_mapping.csv` | Contains 23 worksheet-to-METRC mapping rows, including Ocimene rollup components, p-Cymene preferred explicit mapping, and trans-Nerolidol to generic Nerolidol. | METRC-MAP |

## Current Terpenes worksheet state

### Worksheet 42: Terpenes Test Worksheet

| Item | Current state | Source |
|---|---|---|
| Tabs | Exact tabs are `Report`, `Data`, and `Specifications`. | T42 |
| Formula count | 0 formulas. | T42; EXPORT-STATUS |
| Named-cell count | 47 named cells. | T42; NAMED-CELL-INDEX |
| Current report range | `qb_config.report_export_range` is empty, `qb_config.portal_export_range` is empty, the `Report` tab has no non-empty grid values, and there is no `report_results` named cell. | T42; REPORT-MAP |
| Current kvstore configuration | `qb_config.kvstore_config` is `{}` in the latest active 2026-07-04 export. | T42 |
| Current visible Data tab content | Row 1 stores sample metadata headers and 23 terpene analyte headers; row 2 uses QBench placeholders for test display ID, sample product matrix, and assay title; row 3 says `Result (mg/g or %?)`. | T42 |
| Current visible Specifications tab content | Rows 1-2 hold Customer, Program, and Matrix placeholders; row 4 has `Analyte`, `Measurement Uncertainty (%)`, `LOQ (mg/g)`, `Result (%)`, and `Result (mg/g)`; rows 5-27 list the 23 current analytes. | T42 |

### Worksheet 42 current named cells

All current named cells are exportable in T42. Cell addresses are stored without tab names in the JSON; based on the visible worksheet layout, these addresses correspond to the `Specifications` grid, but the worksheet-internal tab binding is not explicit in the named-cell object. That tab binding is therefore unknown from the JSON field alone. Source: T42.

| Named cell | Cell | Display name | Source |
|---|---:|---|---|
| `apinene_metrc` | D5 | A Pinene METRC | T42 |
| `apinene_metrc_mgg` | E5 | A Pinene METRC mg/g | T42 |
| `camphene_metrc` | D6 | Camphene METRC | T42 |
| `camphene_metrc_mgg` | E6 | Camphene METRC mg/g | T42 |
| `bmyrcene_metrc` | D7 | B Myrcene METRC | T42 |
| `bmyrcene_metrc_mgg` | E7 | B Myrcene METRC mg/g | T42 |
| `bpinene_metrc` | D8 | B Pinene METRC | T42 |
| `bpinene_metrc_mgg` | E8 | B Pinene METRC mg/g | T42 |
| `delta3carene_metrc` | D9 | Delta 3 Carene METRC | T42 |
| `delta3carene_metrc_mgg` | E9 | Delta 3 Carene METRC mg/g | T42 |
| `aterpinene_metrc` | D10 | A Terpinene METRC | T42 |
| `aterpinene_metrc_mgg` | E10 | A Terpinene METRC mg/g | T42 |
| `cisocimene_metrc` | D11 | Cis Ocimene METRC | T42 |
| `cisocimene_metrc_mgg` | E11 | Cis Ocimene METRC mg/g | T42 |
| `dlimonene_metrc` | D12 | D Limonene METRC | T42 |
| `dlimonene_metrc_mgg` | E12 | D Limonene METRC mg/g | T42 |
| `pcymene_metrc` | D13 | P Cymene METRC | T42 |
| `pcymene_metrc_mgg` | E13 | P Cymene METRC mg/g | T42 |
| `transocimene_metrc` | D14 | Trans Ocimene METRC | T42 |
| `transocimene_metrc_mgg` | E14 | Trans Ocimene METRC mg/g | T42 |
| `eucalyptol_metrc` | D15 | Eucalyptol METRC | T42 |
| `eucalyptol_metrc_mgg` | E15 | Eucalyptol METRC mg/g | T42 |
| `gterpinene_metrc` | D16 | G Terpinene METRC | T42 |
| `gterpinene_metrc_mgg` | E16 | G Terpinene METRC mg/g | T42 |
| `terpinolene_metrc` | D17 | Terpinolene METRC | T42 |
| `terpinolene_metrc_mgg` | E17 | Terpinolene METRC mg/g | T42 |
| `linalool_metrc` | D18 | Linalool METRC | T42 |
| `linalool_metrc_mgg` | E18 | Linalool METRC mg/g | T42 |
| `isopulegol_metrc` | D19 | Isopulegol METRC | T42 |
| `isopulegol_metrc_mgg` | E19 | Isopulegol METRC mg/g | T42 |
| `geraniol_metrc` | D20 | Geraniol METRC | T42 |
| `geraniol_metrc_mgg` | E20 | Geraniol METRC mg/g | T42 |
| `bcaryophyllene_metrc` | D21 | B Caryophyllene METRC | T42 |
| `bcaryophyllene_metrc_mgg` | E21 | B Caryophyllene METRC mg/g | T42 |
| `ahumulene_metrc` | D22 | A Humulene METRC | T42 |
| `ahumulene_metrc_mgg` | E22 | A Humulene METRC mg/g | T42 |
| `cisnerolidol_metrc` | D23 | Cis Nerolidol METRC | T42 |
| `cisnerolidol_metrc_mgg` | E23 | Cis Nerolidol METRC mg/g | T42 |
| `transnerolidol_metrc` | D24 | Trans Nerolidol METRC | T42 |
| `transnerolidol_metrc_mgg` | E24 | Trans Nerolidol METRC mg/g | T42 |
| `guaiol_metrc` | D25 | Guaiol METRC | T42 |
| `guaiol_metrc_mgg` | E25 | Guaiol METRC mg/g | T42 |
| `caryophylleneoxide_metrc` | D26 | Caryophyllene Oxide METRC | T42 |
| `caryophylleneoxide_metrc_mgg` | E26 | Caryophyllene Oxide METRC mg/g | T42 |
| `bisabolol_metrc` | D27 | Bisabolol METRC | T42 |
| `bisabolol_metrc_mgg` | E27 | Bisabolol METRC mg/g | T42 |
| `testterpenes` | E4 | Test Terpenes | T42 |

Notable omissions: T42 has no `report_results`, no `report_header`, no `report_content`, no `pass_fail`, no `df`, no batch-to-test results range such as `terpenes_results`, and no explicit `metrc_analyte_name_*`, `metrc_quantity_*`, `metrc_pass_fail_*`, `metrc_notes_*`, or `metrc_to_include_*` named cells. Sources: T42; NAMED-CELL-INDEX; REPORT-MAP.

### Worksheet 42 current formulas

There are no current formulas in worksheet 42. Source: T42; EXPORT-STATUS.

### Worksheet 43: Terpenes Batch Worksheet

| Item | Current state | Source |
|---|---|---|
| Tabs | Exact tab is `Sheet1`. | T43 |
| Formula count | 0 formulas. | T43; EXPORT-STATUS |
| Named-cell count | 0 named cells. | T43; EXPORT-STATUS |
| Current report range | `qb_config.report_export_range` is empty, `qb_config.portal_export_range` is empty, and there is no `report_results` named cell. | T43 |
| Current kvstore configuration | `qb_config.kvstore_config` is `{}`. | T43 |
| Current batch layout | Row 1 has `Sample ID`; rows 2-6 list `STD 1` through `STD 5`; row 7 lists `Blank`; rows 8-10 list `System Suitability 1` through `System Suitability 3`; rows 11-96 contain `${tests[n].get_display_id()}` in column A and `${tests[n].sample.product_matrix}` in column B for test indexes 0-85. | T43 |

### Worksheet 43 current formulas

There are no current formulas in worksheet 43. Source: T43; EXPORT-STATUS.

## Current kvstore state and discrepancy

| Finding | Source |
|---|---|
| The latest active Terpenes test worksheet export, T42, has an empty `qb_config.kvstore_config`. | T42 |
| The latest active Terpenes batch worksheet export, T43, has an empty `qb_config.kvstore_config`. | T43 |
| The preserved 2026-06-30 active Terpenes test export contains a `kvstore_config` UUID `ff2cde0c-abba-4522-991c-2473042479bc` with METRC/profile-style mappings including `Additional-Terpenes (%)`, `Additional-Terpenes (mg_g)`, `Full Panel (Conc.) Tribal Only`, `Full Panel (FinPrd) Tribal Only`, `Full Panel (Flower) Tribal Only`, and `R&D Terpenes`. | T42-0630 |
| The Pesticides qualitative test worksheet also contains `ff2cde0c-abba-4522-991c-2473042479bc`, indicating this UUID is a shared METRC/profile-style mapping pattern rather than a Terpenes-only scientific limits table. | PE14 |
| Unknown QBench internal: the repository does not explain why the July 4 Terpenes rescan has empty kvstore config while the June 30 preserved active export has the shared METRC/profile-style kvstore mapping. | T42; T42-0630; EXPORT-STATUS |

## Existing COA dependencies

| Dependency | Current state | Source |
|---|---|---|
| Assay ID | The COA body source maps `TERPENES` to assay ID `8`. | COA-BODY |
| Test map | The COA body source includes a Terpenes entry in `test_map` and later sets `TERPENES_TEST = test_map[ASSAY_ID_MAP['TERPENES']]['test']`. | COA-BODY |
| Rendering call | The COA body source renders Terpenes with `QBTestService().render_worksheet(TERPENES_TEST, named_cell="report_results", ignore_empty_rows=true)`. | COA-BODY |
| Ancillary COA text | The Terpenes section displays assay title, test method, total primary sample weight, equations, METRC source package ID, and METRC lab test ID when values exist. | COA-BODY |
| Protocol placeholder | `PROTOCOL_STEP_ID_MAP['TERPENES_PREPARATION']` is `-1`, and the source comment says not all protocol steps were created yet. | COA-BODY |
| Active report-source certainty | `QBench/COA/Source/README.md` says no QBench report source file was downloaded from the active Visual Editor report template during inspection, so whether `COA format/COA Body Source Code.txt` exactly matches the current active QBench template is unknown from repository evidence alone. | COA-SOURCE-NOTE; COA-BODY |
| Primary COA gap | The available COA body source expects `report_results`, but the latest Terpenes test worksheet does not define `report_results`. | COA-BODY; T42; REPORT-MAP |

## Existing automation and parser dependencies

| Area | Current state | Source |
|---|---|---|
| Terpenes automation | No active or inactive Terpenes automation is listed in `AUTOMATION_INDEX.md`. | AUTOMATION-INDEX |
| Similar batch-to-test automations | Heavy Metals automation ID 1 updates arsenic, cadmium, lead, mercury, and `df`; Residual Solvents automation ID 6 updates `residual_solvents_results` and `df`; Pesticides automation ID 8 updates `pesticides_results`, `mycotoxin_results`, and `df`; Pesticide quantitative automation ID 10 updates `pest_quantitative_results`. | AUTOMATION-INDEX |
| Terpenes parser | No Terpenes QBench file parser is listed in `FILE_PARSER_INDEX.md`. | PARSER-INDEX |
| Parser visibility | Parser internals for no-code parsers and parser exports/downloads were not visible from read-only inspection; unknown QBench internals may exist outside repository evidence. | PARSER-INDEX; SYSTEM-MAP |
| Source-package parser | The Terpenes source package contains `parse_labsolutions_ascii.py` and fixtures for a repository-friendly LabSolutions ASCII parser; SOURCE-README identifies these as implementation inputs, not approved QBench production parser configuration. | SOURCE-README; ASCII-SPEC |
| Required import source | The Terpenes implementation input requires quantitation from `Compound Results(Ch1) > Conc.`, with `Peak Table(Ch1)` retained for integration review/QC and Dimethylacetamide excluded from reportable terpene results. | TR-AGENTS; ASCII-SPEC; WORKSHEET-SPEC |

## Comparison worksheet inventory

| Worksheet | Active export state inspected | Source |
|---|---|---|
| Heavy Metals batch worksheet ID 5 | One tab, `Sheet1`; 0 formulas; 0 named cells; 1 top-level kvstore config entry. | HM5 |
| Heavy Metals test worksheet ID 6 | Tabs are `Data`, `Specifications`, and `Report`; 43 formulas; 26 named cells; 1 top-level kvstore config entry. | HM6 |
| Residual Solvents batch worksheet ID 11 | One tab, `Sheet1`; 0 formulas; 0 named cells; empty kvstore config. | RS11 |
| Residual Solvents test worksheet ID 12 | Tabs are `Data`, `Specifications`, and `Report`; 323 formulas; 43 named cells; 1 top-level kvstore config entry. | RS12 |
| Pesticides quantitative batch worksheet ID 13 | One tab, `Sheet1`; 0 formulas; 0 named cells; empty kvstore config. | PE13 |
| Pesticides qualitative test worksheet ID 14 | Tabs are `Data`, `Specifications`, and `Report`; 982 formulas; 58 named cells; 2 top-level kvstore config entries. | PE14 |
| Pesticide/Mycotoxin qualitative batch worksheet ID 15 | One tab, `Sheet1`; 0 formulas; 0 named cells; empty kvstore config. | PE15 |
| Pesticides quantitative test worksheet ID 16 | Tabs are `Data`, `Specifications`, and `Report`; 763 formulas; 72 named cells; 1 top-level kvstore config entry. | PE16 |

## Patterns worth copying

| Pattern | Why it is useful for Terpenes | Source |
|---|---|---|
| Data/Specifications/Report tab structure | Heavy Metals, Residual Solvents, and Pesticides active test worksheets use `Data`, `Specifications`, and `Report` tabs, while Terpenes already has those tabs but lacks formulas and a populated report range. | HM6; RS12; PE14; PE16; T42 |
| Batch-to-test named result range | Residual Solvents exposes `residual_solvents_results` at `Data!E2:W2`; Pesticides exposes `pesticides_results` at `Data!E2:BG2` or `Data!E2:BU2`; Heavy Metals uses individual named cells plus `df`. Terpenes needs an equivalent automation target for 23 channel results and dilution/config metadata if batch import remains the source. | RS12; PE14; PE16; HM6; AUTOMATION-INDEX |
| Dedicated dilution factor named cell | Heavy Metals, Residual Solvents, and Pesticides use `df` named cells; Terpenes source rules say never apply dilution unless `df_application_mode` explicitly requires it, so Terpenes should capture dilution separately before any application decision. | HM6; RS12; PE14; PE16; TR-AGENTS; WORKSHEET-SPEC |
| Kvstore-driven matrix/program specifications | Heavy Metals, Residual Solvents, and Pesticides use `GET_KVSTORE_VALUE(uuid,$B$2,$C$2,analyte,field)` to retrieve LOQ, MU, and pass/fail limits by customer/program/matrix/analyte. Terpenes needs a comparable configuration only after reportable limits, units, and profile behavior are approved. | HM6; RS12; PE14 |
| Kvstore key gating | Residual Solvents and Pesticides pull available keys with `CONCAT(GET_KVSTORE_VALUE(...,"keys"))` and conditionally include analytes only when present; this is useful for Terpenes METRC profile coverage because some profiles omit Guaiol, p-Cymene, or many subcontract analytes. | RS12; PE14; METRC-PROFILES; METRC-MAP |
| LOQ display pattern | Existing methods display `<LOQ` when the numeric result is below the configured LOQ, then carry that display value into the report. Terpenes needs an approved below-LOQ reporting/METRC rule before copying this pattern. | HM6; RS12; PE14; WORKSHEET-SPEC |
| Pass/fail rollup pattern | Existing methods compute `pass_fail` from row statuses, usually returning `Not Tested`, `Fail`, or `Pass`; Terpenes instructions explicitly forbid creating a general Terpenes pass/fail rule without approval. | HM6; RS12; PE14; TR-AGENTS |
| Compact report range | Heavy Metals uses `Report!A1:F6`, Residual Solvents uses `Report!A1:F31`, Pesticides qualitative uses `Report!A1:R25`, and Pesticides quantitative uses `Report!A1:L40`. Terpenes needs a compact `report_results` range sized for the approved default COA measurand list. | HM6; RS12; PE14; PE16; COA-BODY |
| Unit conversion row | Pesticides qualitative converts row 2 values with row 3 formulas like `=E2/1000`; Terpenes similarly needs stable calculated cells for both `%` and `mg/g`, but must use the approved LabSolutions `Conc.` conversion rather than normalized `Conc. %` or `Norm Conc.`. | PE14; ASCII-SPEC; WORKSHEET-SPEC; TR-AGENTS |
| Shared METRC/profile mapping UUID | The `ff2cde0c-abba-4522-991c-2473042479bc` kvstore mapping appears in the preserved Terpenes June 30 export and in Pesticides; it includes terpene-related METRC/profile labels that can guide later profile configuration, but the latest Terpenes July 4 export does not currently carry it. | T42-0630; PE14; T42 |

## Source-package implementation requirements and gaps

| Requirement or input | Current repository evidence | Gap for implementation | Source |
|---|---|---|---|
| Internal channels | The analyte master defines 23 internal chromatographic channels. | T42 has 23 analyte rows but no formulas, no parser-driven values, and no batch/test automation target for all 23 channels. | ANALYTE-MASTER; T42; T43 |
| Default COA reporting | Terpenes instructions say the default COA uses the approved 21-measurand list. | T42 currently has no `report_results` range and no 21-measurand COA layout. | TR-AGENTS; T42; COA-BODY |
| Quantitation source | Quantitation must use `Compound Results(Ch1) > Conc.` and never `Conc. %` or `Norm Conc.` as sample potency. | T42 has no formulas to convert LabSolutions `Conc.` into `%` and `mg/g`. | TR-AGENTS; ASCII-SPEC; WORKSHEET-SPEC; T42 |
| Audit/QC retention | Dimethylacetamide and Peak Table data must be retained for audit/QC while Dimethylacetamide is excluded from reportable terpene results. | T43 has no visible columns or named ranges for Compound Results, Peak Table rows, Dimethylacetamide retention, or audit metadata. | TR-AGENTS; ASCII-SPEC; T43 |
| Dual result units | Both `%` and `mg/g` must be stored for every reportable terpene analyte. | T42 has named cells for current `%` and `mg/g` result positions, but the cells have no formulas and no upstream data values. | TR-AGENTS; WORKSHEET-SPEC; T42 |
| Ocimene METRC behavior | METRC does not provide separate cis/trans Ocimene rows; export should roll cis-Ocimene + trans-Ocimene into Ocimene. | T42 currently has separate `cisocimene_*` and `transocimene_*` named cells and no total Ocimene output cell. | BUILD-BRIEF; METRC-MAP; T42 |
| Nerolidol METRC behavior | METRC provides `Cis-Nerolidol` and generic `Nerolidol`; source package maps trans-Nerolidol/Nerolidol 2 to generic Nerolidol unless total Nerolidol is approved. | T42 has separate cis/trans named cells but no profile-specific generic Nerolidol export logic. | BUILD-BRIEF; METRC-MAP; T42 |
| p-Cymene METRC behavior | p-Cymene should map to `P-Isopropyltoluene (P-Cymene)` or `P. Isopropyltoluene`, not generic `Cymene`. | T42 has `pcymene_*` cells but no profile validation or fallback handling. | TR-AGENTS; BUILD-BRIEF; METRC-MAP; T42 |
| Other Terpenes | Other Terpenes should not be silently populated and should remain blank/zero unless explicitly configured. | T42 has no Other Terpenes cells or policy implementation. | TR-AGENTS; WORKSHEET-SPEC; METRC-PROFILES; T42 |
| Pass/fail | A general Terpenes pass/fail rule must not be created without approval. | T42 has no `pass_fail` named cell, which is consistent with the no-unapproved-pass/fail rule but leaves the first-page COA tile behavior unknown if Terpenes contributes to overall pass/fail. | TR-AGENTS; T42; COA-BODY |

## Current active behavior vs proposed Terpenes behavior

| Area | Current active behavior | Proposed or required behavior for later implementation | Source |
|---|---|---|---|
| Worksheet calculations | Current active T42 and T43 have 0 formulas, and T42 has placeholder text `Result (mg/g or %?)`. | Later implementation should calculate and store both `%` and `mg/g` from LabSolutions `Compound Results(Ch1) > Conc.` after unit/sample-prep decisions are approved. | T42; T43; TR-AGENTS; WORKSHEET-SPEC; ASCII-SPEC |
| COA rendering | Current available COA body source tries to render Terpenes `named_cell="report_results"`, but current active T42 has no `report_results` and an empty Report tab. | Later implementation should add a compact `report_results` named cell/range that matches the approved default COA measurand list before any COA/report upload or activation. | COA-BODY; T42; REPORT-MAP; TR-AGENTS |
| METRC cells | Current active T42 exposes individual `%` and `mg/g` named cells for 23 analytes, including separate cis/trans Ocimene and cis/trans Nerolidol cells. | Later implementation should preserve internal channels but export profile-specific METRC values, including total Ocimene rollup, approved Nerolidol mapping, and p-Cymene-specific mapping. | T42; BUILD-BRIEF; METRC-PROFILES; METRC-MAP; TR-AGENTS |
| Batch worksheet | Current active T43 only lays out standards, blank/system suitability rows, and test display ID/matrix rows; it has no result import surface, named cells, or formulas. | Later implementation should define parser/import storage for Compound Results, Peak Table audit rows, Dimethylacetamide retention, sample metadata, dilution factor, and per-test result transfer. | T43; ASCII-SPEC; PARSER-SCRIPT; COMPOUND-FIXTURE; PEAK-FIXTURE |
| Automation | Current repository indexes do not list any Terpenes automation. | Later implementation should add any batch-to-test automation only after batch/test named ranges are stable and approved. | AUTOMATION-INDEX; T42; T43 |
| Parser | Current QBench parser index does not list a Terpenes QBench parser. | Later implementation can use the source-package parser and fixtures as repository inputs, but QBench parser configuration remains future work and not production-approved. | PARSER-INDEX; SOURCE-README; PARSER-SCRIPT |
| Pass/fail | Current active T42 has no `pass_fail`; Terpenes instructions prohibit creating a general Terpenes pass/fail rule without approval. | Later implementation should only add pass/fail behavior if a scientific/reporting requirement is explicitly approved. | T42; TR-AGENTS |

## Unresolved scientific and reporting decisions

Every item below remains unresolved or requires explicit approval before later implementation.

| Decision | Current evidence | Source |
|---|---|---|
| Confirm the LabSolutions `Conc.` unit and whether it is extract concentration in `ug/mL`. | The worksheet spec assumes `mg/g = extract_conc_ug_mL * final_volume_mL / sample_mass_g / 1000`, but also says to confirm the instrument export unit and columns. | WORKSHEET-SPEC; ASCII-SPEC |
| Confirm final volume and sample mass sources for the `%` and `mg/g` conversion. | The source package says to store Sample Amount but use QBench/sample-prep mass unless the export amount is confirmed authoritative. | WORKSHEET-SPEC; ASCII-SPEC |
| Confirm dilution factor application mode. | Terpenes instructions say never apply dilution unless `df_application_mode` explicitly requires it; the source spec recommends not double-applying export Dilution Factor until the LabSolutions method is verified. | TR-AGENTS; WORKSHEET-SPEC; ASCII-SPEC |
| Decide the default COA 21-measurand row list, labels, ordering, and whether the Report tab should show `%`, `mg/g`, or both. | Terpenes instructions say default COA uses the approved 21-measurand list, while T42 currently lists 23 analytes and has no report range. | TR-AGENTS; T42 |
| Decide whether the COA should show total Ocimene, separate cis/trans Ocimene, or both. | The source package requires rolling resolved Ocimene channels into total Ocimene for default COA and METRC, while T42 currently exposes cis/trans cells separately. | TR-AGENTS; BUILD-BRIEF; METRC-MAP; T42 |
| Decide COA and METRC treatment for Nerolidol. | The source package says to roll resolved Nerolidol channels according to approved COA and METRC configurations and asks whether generic METRC Nerolidol should receive trans-Nerolidol or total cis+trans Nerolidol. | TR-AGENTS; WORKSHEET-SPEC; BUILD-BRIEF; METRC-MAP |
| Decide below-LOQ report and METRC behavior. | The worksheet spec asks whether below-LOQ METRC quantity should be `0` with `<LOQ` note or excluded. | WORKSHEET-SPEC |
| Decide whether to create any Terpenes pass/fail output. | Terpenes instructions prohibit a general Terpenes pass/fail rule without approval; COA tile behavior for Terpenes therefore remains unknown. | TR-AGENTS; COA-BODY |
| Decide whether Measurement Uncertainty and LOQ should be profile/matrix/program kvstore values, static worksheet values, or blank for Terpenes. | T42 has MU and LOQ columns but no formulas; comparison methods use kvstore values. | T42; HM6; RS12; PE14 |
| Decide controlling bracketing CCV criterion. | The worksheet spec states SOP text says 10 percent while Analysis Form says 15 percent. | WORKSHEET-SPEC |
| Decide how chromatographic QC and Peak Table audit data appear in QBench. | The source package requires retaining Peak Table data for review/QC, but current T43 has no Peak Table storage layout. | ASCII-SPEC; T43 |
| Confirm Full Panel Finished Products mixed-unit behavior. | METRC profiles say individual terpene rows are `%` but Total Terpenes is `mg/g` for `Full Panel (FinPrd) Tribal Only`. | METRC-PROFILES; WORKSHEET-SPEC |
| Confirm R&D Terpenes Alpha-Humulene unit. | METRC profiles identify Alpha-Humulene as `ppm` on `R&D Terpenes` while most terpene rows are `%` or `mg/g`. | METRC-PROFILES; BUILD-BRIEF; WORKSHEET-SPEC |
| Confirm Full Panel Flower p-Cymene fallback. | METRC profiles say explicit p-Cymene is absent from `Full Panel (Flower) Tribal Only`; p-Cymene should not silently map to generic Cymene. | METRC-PROFILES; BUILD-BRIEF; TR-AGENTS |
| Confirm Guaiol handling for Full Panel Concentrates. | METRC profiles say Guaiol is absent from `Full Panel (Conc.) Tribal Only`. | METRC-PROFILES; BUILD-BRIEF |
| Confirm sub-contract profile behavior for missing analytes. | METRC profiles show subcontract terpene sheets include limited analyte sets and omit many internal channels. | METRC-PROFILES; BUILD-BRIEF |
| Confirm profile selection source in QBench. | The source package defines export profiles, but repository evidence does not show the QBench UI/config field that selects a Terpenes METRC export profile. Unknown QBench internal. | METRC-PROFILES; T42; PARSER-INDEX |
| Confirm active COA source parity. | `COA format/COA Body Source Code.txt` contains a Terpenes render call, but `QBench/COA/Source/README.md` says active Visual Editor source was not downloadable during inspection. Unknown QBench internal. | COA-BODY; COA-SOURCE-NOTE |

## Proposed dependency order for later implementation

1. Approve scientific/reporting decisions first: LabSolutions `Conc.` unit, sample mass/final volume source, dilution mode, below-LOQ behavior, default 21-measurand COA list, Ocimene/Nerolidol rollups, pass/fail policy, and METRC profile fallback rules. Sources: TR-AGENTS; WORKSHEET-SPEC; BUILD-BRIEF; METRC-PROFILES; METRC-MAP.
2. Freeze the Terpenes worksheet schema: preserve compatibility named cells that are still required, add `report_results`, define a batch-to-test results range, define audit/QC storage, and keep worksheet IDs 42/43 raw exports immutable. Sources: ROOT; TR-AGENTS; T42; T43; COA-BODY.
3. Build and test the LabSolutions parser flow against the source fixtures: parse Compound Results and Peak Table, exclude Dimethylacetamide from reportable output, retain audit data, and normalize aliases. Sources: SOURCE-README; ASCII-SPEC; ANALYTE-MASTER.
4. Design the batch worksheet import/storage surface before automation: include standards, blank/system suitability, sample rows, 23 reportable channels, Dimethylacetamide/audit fields, sample metadata, dilution factor, and Peak Table retention. Sources: T43; ASCII-SPEC; ANALYTE-MASTER.
5. Implement test worksheet calculations: convert LabSolutions `Conc.` to `mg/g` and `%`, store both units, avoid double dilution, apply approved Ocimene/Nerolidol rollups, and avoid unapproved pass/fail logic. Sources: WORKSHEET-SPEC; TR-AGENTS; T42.
6. Implement kvstore/profile configuration after schema and calculations: use existing `GET_KVSTORE_VALUE` and key-gating patterns where appropriate, but keep profile gaps as validation warnings or failures rather than silent mappings. Sources: HM6; RS12; PE14; T42-0630; METRC-PROFILES.
7. Add batch-to-test automation only after batch/test named ranges are stable: copy the Residual Solvents/Pesticides pattern of batch data updates into a test worksheet named result range plus `df`/metadata as approved. Sources: AUTOMATION-INDEX; RS12; PE14; PE16.
8. Satisfy COA dependencies: create a compact `report_results` named cell and confirm the available COA body source or active report template renders it correctly before any report upload/change. Sources: COA-BODY; REPORT-MAP; T42.
9. Validate in repository before QBench Sandbox import: parse JSON, confirm unique tabs and named cells, confirm formulas, confirm report range non-empty, confirm source exports are preserved, and add fixture-based parser/METRC tests. Sources: ROOT; TR-AGENTS; SOURCE-README.

## Implementation risk summary

| Risk | Why it matters | Source |
|---|---|---|
| COA rendering will fail or render blank for Terpenes until `report_results` exists. | The COA body source calls `render_worksheet(... named_cell="report_results" ...)`, but T42 has no such named cell and an empty Report tab. | COA-BODY; T42 |
| Current Terpenes worksheet cells look like placeholders, not a working calculation template. | T42 has 0 formulas, row 3 asks `Result (mg/g or %?)`, and T43 has no result columns beyond sample IDs/matrices. | T42; T43 |
| METRC export cannot be safely implemented by direct one-to-one named cells only. | Source package requires profile-specific units, Ocimene rollup, Nerolidol mapping, p-Cymene specificity, and warnings/failures for missing profile coverage. | BUILD-BRIEF; METRC-PROFILES; METRC-MAP |
| Parser and automation are not currently configured in QBench for Terpenes based on repository indexes. | No Terpenes parser or automation appears in the current indexes; QBench internals not captured in the repository are unknown. | PARSER-INDEX; AUTOMATION-INDEX |
| The July 4 kvstore state does not preserve the June 30 Terpenes METRC/profile mapping in the latest Terpenes export. | T42 has empty kvstore config; T42-0630 has `ff2cde0c-abba-4522-991c-2473042479bc`. | T42; T42-0630 |
