# Live QBench implementation-reference inventory

Inspection date: 2026-07-17

Origin: `https://ait.qbench.net`

Mode: authenticated browser, configuration definitions only, strictly read-only

## Scope correction

Live QBench is not expected to contain an operational Terpenes implementation. It was used only as an implementation-reference library for established non-Terpenes assays. No live worksheet or formula is scientific authority for Terpenes.

## Reclassification of interrupted work

| Interrupted observation | Classification | Disposition |
| --- | --- | --- |
| A live definition artifact labeled for Terpenes was opened and exported. | `invalid_terpenes_assumption` if interpreted as an operational workflow | Raw export and SHA-256 preserved locally because the bytes are safe definition evidence. No operational, authoritative, or scientific claim is retained. |
| The artifact contained familiar Report/Data/Specifications/METRC structures. | `duplicate` | Those generic structures are now supported by safer non-Terpenes references. The Terpenes artifact is not used to design science. |
| The artifact contained formulas and named cells. | `invalid_terpenes_assumption` if used to resolve the Terpenes contract | Formula details are excluded from sanitized Terpenes guidance. |
| Broad landing-page output transiently exposed staff/interface identifiers. | `customer_data_risk_remove` | Not copied into any evidence file. No customer record was opened. |
| Runtime behavior of the definition artifact. | `unresolved` | Not inspected; the user clarified there is no operational Terpenes workflow. |

Preserved interrupted raw-export hash: `da29850580e8b1909a59d7df3c32fc0a954727c8bf06fc33cbfc6ec5ccbc169e`. The raw file remains ignored and uncommitted.

## Non-Terpenes definitions inspected

| Assay category | Definition object | Visible version state used | Safe structural result | Raw export SHA-256 |
| --- | --- | --- | --- | --- |
| Cannabinoid Potency | Test Worksheet | latest visible Draft | Five tabs: Data, Purity Data, Specifications, Report, METRC; 35 qualified named cells; compact `report_results`; formula and read-only sections. | `12660bcf72bc52702e363c506e5993abc172190e73f512938e7de224631cfe98` |
| Residual Solvents | Batch Worksheet | Approved/Active | One formula-free `Sheet1`; no named cells. Useful as a legacy counterexample, not as the target architecture. | `78d98effb4f281a930708443070fd5f2e7b1e50a53fb3f3414adfc7b070c28ae` |
| Heavy Metals | Test Worksheet | latest visible Draft | Data, Specifications, Report, METRC; 46 qualified named cells; compact `report_results`; guarded calculation and qualifier mechanics. | `425b698d7caebb6171a2ccca88d29b28227d7ef3fcafbd256753f4119604535e` |
| Pesticides, quantitative | Test Worksheet | Approved/Active | Data, Specifications, Report; large analyte table; 72 qualified named cells; bounded `report_results`. | `641a8ea9dc8318e69ac112a313400bd9d5e7374e74f97f53218005073e7371ab` |
| Pesticides, quantitative | Batch Worksheet | Approved/Active | One wide formula-free sheet with extensive read-only metadata; no named cells. | `a93295f7b97e0c3e14a651c1a03ad3536472d6fbf25b292f47057c83b60f95ec` |
| Homogeneity | Test Worksheet | Approved/Active | Paste, Data, COA; 38 qualified named cells; explicit `report_results`; strong paste/calculation/report separation. | `9f6403c2874b1c36623b6786b666f80688cd0ba5d345b9ae832049f1f04fa4fb` |

## Other definition categories inspected

- File Parser list and safe definition shells: an active code-based Cannabinoid Potency parser and active/inactive no-code Heavy Metals parsers were visible. Parser bodies or mappings were not copied.
- Automation list: active `Data Modified` Batch-to-Test automations were visible for several established assay categories; Homogeneity used a Test-level `Data Modified` automation. Automation bodies were not copied.
- Report Template list and active Certificate of Analysis definition shell: template source text was not extracted from the editor.

## Access result

- Completed customer records opened: **no**.
- Configuration exports: **yes**, six non-Terpenes definition exports during the correction run plus one previously preserved definition artifact.
- Live object modifications: **none**.
- Live API requests: **none**.
- Unsaved-change state entered: **no**.
