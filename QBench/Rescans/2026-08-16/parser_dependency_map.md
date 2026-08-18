# Parser Dependency Map — 2026-08-16 Production Snapshot

## Current parser paths

| Parser | Trigger / input | Assay and target | Observed write behavior | Downstream automation | Report dependency |
|---|---|---|---|---|---|
| 50 Terpenes Simple Results Parser V2 Controls (active) | Batch attachment ending `.txt` | Terpenes; dynamic Batch `Results` | Code resolves candidate Tests to one Batch, updates `Results`, recalculates, and reads back | 17 watches worksheet 43 and writes 26 Terpenes Test fields | Report 26 renders Terpenes `report_results` |
| 49 attachment-context probe (inactive config) | Exact `Output_redacted_fixture.txt` Batch attachment; no assay | No worksheet target | Captured code performs controlled context inspection and no worksheet-service write | None observed | None |
| 48 runtime no-write probe (inactive) | No configured trigger/file pattern/assay | No target | Draft no-write context probe | None | None |
| 47 Pest Myco Qualitative (active) | Batch attachment containing `.csv`; comma separated | Pesticides; Populate Batch Worksheet; patch enabled | 12 finder names; individual mappings not exposed | Strong inference to automation 8 / worksheet 15 | Report 26 renders Pesticides/Mycotoxins `report_results` |
| 46 Cannabinoid Potency Parser (active) | Batch attachment ending `.csv` | Cannabinoid Potency; dynamic Batch `Results` | Code updates `Results` and recalculates | 11; later status-gated Homogeneity automation 16 | Reports 26 and 44 |
| 45 Gene-up (inactive) | Trigger/assay/file rule not configured | No target exposed | No versions; visible base Code template | None observed | None |
| 41 Heavy Metals DataManager (active) | Batch attachment containing `.txt`; tab separated | Heavy Metals; Populate Batch Worksheet; patch enabled | 48 finder names; mappings not exposed | Strong inference to automation 1 / worksheet 5 | Report 26 renders Heavy Metals `report_results` |
| 25 Cannabis Heavy Metals ICPMS (inactive) | Batch attachment containing `IC`; comma separated | Heavy Metals; Populate Batch Worksheet; patch enabled | 1 finder name; mapping not exposed | Possible automation 1 path if reactivated; unverified | Report 26, if the same Test worksheet is populated |
| 22 Heavy Metals AMM (inactive) | Batch attachment ending `.csv`; comma separated | Heavy Metals; Populate Batch Worksheet; patch enabled | 1 finder name; mapping not exposed | Possible automation 1 path if reactivated; unverified | Report 26, if the same Test worksheet is populated |
| 21 Example (active) | Navigation upload; Test IDs read from a configured cell range; Excel | Populate Multiple Test Worksheets; no assay | 1 finder name; direct Test-worksheet target | No matching automation established | Unknown |

## Destination and relationship classification

| Parser | Direct assay configuration | Worksheet and destination evidence | Field/range evidence | Relationship classification |
|---|---|---|---|---|
| 50 | Terpenes (8) | Assay 8 configures Batch worksheet 43; source selects its dynamic `Results` tab | Source writes parser-owned D:AY cells on matched rows 2–87 and manages audit rows A:AY 91–190 | Direct assay plus source-observed write; automation 17/report 26 are downstream |
| 49 | None | No worksheet-service write | None | Directly observed no-write source; inactive configuration |
| 48 | None | No configured target | None | Directly observed no-write probe source; inactive configuration |
| 47 | Pesticides (4) | Assay 4 configures Batch worksheet 15; parser target is `Populate Batch Worksheet` | Twelve finder names captured; source/destination mappings not exposed | Direct assay, inferred worksheet through assay binding; worksheet 15 is also configured for Mycotoxins (5), so that second-assay path is indirect |
| 46 | Cannabinoid Potency (2) | Assay 2 configures Batch worksheet 7; source selects its dynamic `Results` tab | Source matches Test ID rows and writes only columns whose normalized headers match parsed analyte/DF keys; no fixed A1 destination list | Direct assay plus source-observed dynamic write; automation 11/reports 26 and 44 are downstream |
| 45 | None | No target configured | Base Code template only | No dependency established; inactive configuration |
| 41 | Heavy Metals (3) | Assay 3 configures Batch worksheet 5; parser target is `Populate Batch Worksheet` | Forty-eight finder names captured; source/destination mappings not exposed | Direct assay, inferred worksheet through assay binding; automation 1/report 26 are downstream |
| 25 | Heavy Metals (3) | Same configured Batch target family as parser 41 | One finder name; mapping not exposed | Direct assay; inactive, so downstream path is hypothetical |
| 22 | Heavy Metals (3) | Same configured Batch target family as parser 41 | One finder name; mapping not exposed | Direct assay; inactive, so downstream path is hypothetical |
| 21 | None | `Populate Multiple Test Worksheets`; worksheet IDs not exposed | One finder name; Test-ID cell range exists but its exact address/mapping is not exposed | Active generic parser; no assay, automation, or report edge established |

No parser-to-protocol or parser-to-protocol-step assignment was exposed. “Downstream” above means the parser's assay/worksheet path converges with captured automation or report configuration; it is not a direct parser setting. No-Code source ranges, destination ranges, and mapping rows remain unable to verify because opening Edit was outside the read-only scan boundary.

## Code library and safety observations

- Parsers 50, 46, and 45 import `file_parser.js` 1.1.0 and `qbjs.js` 2.7.0.
- Parser 46 additionally imports SheetJS 0.18.5 and Papa Parse 5.4.1.
- Parsers 48 and 49 import `file_parser.js` 1.1.0.
- Parser 50 enforces a 2,000,000-byte raw-file limit, 200-record limit, 32-section limit, 2,000-row per-section limit, 20,000-character line limit, 128-field limit, and 500-character error-message limit.
- Parser 50 requires exactly one `.txt` file, exactly 24 controlled compound rows, 23 reportable analytes, unique candidate Test IDs, exactly one resolved Batch, an exact 51-column/190-row `Results` contract, and read-after-write verification.
- Parser 50 stores source-file and source-row SHA-256 values in the worksheet/audit design. These are data-lineage hashes, not evidence that QBench provides transactionality or duplicate-job suppression.
- Parser 46 skips unmatched Test rows and can still signal success after warnings. It does not expose parser-job atomicity or rollback.

## Comparison with prior evidence

The July production baseline contained IDs 21, 22, 25, 41, 45, 46, and 47. IDs 48, 49, and 50 are new. Canonical documentation previously omitted production parser 47 from its main table and intentionally omitted the probe ID; the current production list establishes IDs 47 and 49 explicitly.

## Unverified dependencies and operational questions

- No-Code finder names are captured, but source ranges, destination ranges, row-identification logic, and exact worksheet IDs require prohibited Edit actions.
- Parser history, aggregate job counts, attachment IDs, logs, and executed-version correlation were intentionally not opened.
- Duplicate-file handling, multi-file grouping, retry behavior, failed-write formatting, transactionality, rollback, and partial-write behavior remain unverified.
- Parser 50's active production source contains an `SBX_ONLY` comment, while parser IDs 48 and 49 also use `SANDBOX_ONLY` names. Naming does not isolate an object from production execution.
- Current report/named-cell compatibility cannot be certified until current native worksheet exports are available.
