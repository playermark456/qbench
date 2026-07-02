# QBench Sandbox System Map

Catalog date: 2026-06-30

## Scope

This catalog covers the visible Sandbox assays, worksheet templates, worksheet named cells, report templates, file parsers, and automations. QBench was treated as read-only. Worksheet files in this repository are QBench Export Spreadsheet JSON downloads.

## Assays/modules found

- Cannabinoid Potency (QBench assay ID 2, code CP)
- Homogeneity (QBench assay ID 11, code HOM)
- Terpenes (QBench assay ID 8, code TR)
- Heavy Metals (QBench assay ID 3, code HM)
- Mycotoxins (QBench assay ID 5, code MY)
- Pesticides (QBench assay ID 4, code PE)
- Residual Solvents (QBench assay ID 7, code RS)
- Foreign Material (QBench assay ID 12, code FM)
- Water Activity (QBench assay ID 9, code WA)
- Moisture Analysis (QBench assay ID 10, code MO)
- Stability (QBench assay ID 13, code STAB)
- Microbial Analysis (QBench assay ID 6, code MICRO)
- Aspergillus spp. (QBench assay ID 14, code MI-ASP)
- Total Aerobic Microbial Count (QBench assay ID 18, code MI-AE)
- Total Yeast and Mold (QBench assay ID 19, code MI-YM)
- Enterobacteriaceae (QBench assay ID 20, code MI-EB)
- Salmonella species (QBench assay ID 15, code MI-SLM)
- STEC (QBench assay ID 16, code MI-STEC)
- Listeria monocytogenes (QBench assay ID 17, code MI-LIS)

## Worksheet layer

- 34 worksheet JSON files are present under QBench/Worksheets.
- 32 are active/approved exports for configured or related worksheet templates.
- 2 are draft/default captures for Pesticides worksheet 14 and Residual Solvents worksheet 12, because those pages opened a draft by default. Active versions were also exported for both.
- Moisture Analysis, Stability, and the general Microbial Analysis assay did not show a configured assay-level worksheet in the inspected assay pages.

## Parser layer

Six file parsers were visible: Cannabinoid Potency Parser, Gene-up, Heavy Metals DataManager, Cannabis Heavy Metals ICPMS File Parser, Heavy Metals File Parser - AMM, and Example [File Parser]. No parser-specific export/download option was visible in read-only inspection.

## Automation layer

Fifteen automations were visible: twelve active and three inactive. Active automations mainly propagate batch worksheet calculated values into individual test worksheet named cells.

## COA/report layer

The active Certificate of Analysis Report template (ID 26) is the default report listed on inspected assays. It is a Sample Report using the Visual Editor. QBench opened draft report version 18 by default; active version 17 was selected read-only for inspection. A separate active Homogeneity report template (ID 44) is also visible.

COA rendering appears to work by reading worksheet named cells/ranges, especially eport_results, eport_header, eport_content, pass_fail, and METRC-specific cells. Report source HTML/code was not available through a visible export/copy/download control in the read-only UI.

## Incomplete areas

See Docs/qbench_open_questions.md for items that could not be determined without changing QBench or using unsupported download paths.
