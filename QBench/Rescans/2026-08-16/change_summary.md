# QBench Production Read-Only Rescan — Final Change and Completion Summary

## Result

Phases 1–7 of the 2026-08-16 production read-only configuration rescan are complete to the authorized evidence boundary.

Sensitive integration configuration was encountered on an authenticated settings page. Details were intentionally omitted. Managed Interfaces remains incomplete pending separate administrative or vendor remediation.

The local evidence package and current working tree pass the final secret, privacy, screenshot, structure, and manifest checks described below.

## Environment and closeout fields

| Closeout item | Result |
|---|---|
| Verified production hostname | `ait.qbench.net` |
| Scan start | `2026-08-16T21:26:25.149Z` |
| Scan end | `2026-08-17T14:47:08.151Z` |
| Git branch | `codex/qbench-production-readonly-rescan-2026-08-16` |
| Phase 6 commit | `73468d5` — `docs: reconcile QBench configuration indexes and Terpenes protocol gaps` |
| Draft pull request | Not opened |

```text
codex_model_setting = gpt_5_6_sol_ultra
qbench_environment = production_read_only
qbench_host_verified = ait.qbench.net
qbench_mutations_performed = 0
qbench_parsers_executed = 0
qbench_automations_executed = 0
qbench_reports_generated = 0
qbench_customer_operational_records_saved = 0
credentials_or_secrets_committed = 0
terpenes_authoritative_sop = Terpene Analysis SOP v 1.4.docx
terpenes_sop_version = 1.4
terpenes_header_1_3_classification = known_typographical_error
github_scan_branch = codex/qbench-production-readonly-rescan-2026-08-16
```

The two reference DOCX files were read locally in place. Neither attached source document was copied by this scan, staged, or committed. Visual DOCX rendering was unavailable because LibreOffice was not installed; structural paragraphs, tables, headers, and footers were read with the bundled document runtime.

## Category completion status

| Status | Categories |
|---|---|
| Scanned to the authorized safe evidence layer | Navigation/counts; worksheet and version metadata; assays; panels; protocols and step assignments; KV stores; automations; file parsers; reports; visible template families; controls/control groups; resource groups; inventory list; equipment list/schedules; safe settings structure |
| Partially scanned | Current worksheet definitions; Field Edit-only properties; Document Control workflow/content; inventory/equipment behavioral semantics; Specifications; alerts/stability behavior; active-label source; internal-report design source |
| Blocked | 161 native worksheet export targets through available browser tooling |

Operational customer, sample, Test, Order, Batch, invoice/payment, stock/lot/transaction, staff-identity, parser-history, automation-history, and report-generation objects were omitted for privacy and scope. They were not counted as missing configuration.

## Configuration inventory

| Category | Final count/status | Evidence boundary |
|---|---:|---|
| Worksheets | 148 objects; 700 versions | Metadata complete; 161 required current native **Export Spreadsheet** targets identified, 0 downloaded due browser-tooling blocker |
| Assays | 20 active | Safe detail metadata |
| Panels | 9 active; 88 ordered memberships | Panel-side membership evidence authoritative |
| Protocols | 15; 81 step definitions; 118 assignments | Required/optional/condition/resource semantics not exposed; protocols 5 and 9 empty |
| Fields | 277 definitions across 20 populated object types | Deeper Edit-only attributes excluded |
| Key/value stores | 11 stores; 13,766 ordered scalar rows | API Clients, History, and identities omitted |
| Automations | 16 total; 13 active; 18 conditions; 90 actions | Configuration only; no execution/history |
| File parsers | 10 total; 5 active; 5 Code / 5 No Code | Corrected full-source capture for five Code parsers; no execution/history |
| Reports | 3 configurations | Sanitized source/version metadata; no preview or generation |
| Other template configurations | 27 across visible families | Empty families and source/version limitations preserved |
| Controls / control groups | 4 / 2; 4 memberships | Safe configuration metadata; acceptance/failure semantics not exposed |
| Resource groups | 10; 105 inventory memberships; 137 equipment memberships | Scheduling/availability/required behavior not exposed |
| Inventory | 158 items | No stock, lots, transactions, purchases, supplier accounts, or attachments |
| Equipment | 103 items; 38 active schedule definitions | No history, certificates, service reports, serials, or staff PII |
| Document Control | 68 Show-All leaves; 66 Approved; 3 Pending; 1 overlap | Metadata only; contents and identities omitted |
| Managed Interfaces | `status = blocked_metadata_only`; `objects_counted = 4`; `details_retained = 0`; `secret_values_committed = 0` | `reason = sensitive_integration_configuration_encountered`; `rescan_required = only_after_separate_remediation_and_explicit_authorization` |
| Screenshots | 2 | Both configuration-only worksheet crops manually reviewed; hashes match index |

## Export, screenshot, and comparison counts

| Measure | Count / result |
|---|---:|
| Active-approved worksheet exports downloaded | 0 of 137 |
| Newer-draft worksheet exports downloaded | 0 of 16 |
| Approved non-active worksheet exports downloaded | 0 of 1 |
| Latest-draft/no-active worksheet exports downloaded | 0 of 7 |
| Total export targets / failures | 161 / 161 blocked; the native control produced no downloadable file through available authenticated tooling |
| Screenshots captured and retained | 2 |
| Screenshots sanitized/cropped | 2 |
| Screenshots explicitly omitted/not retained | 2: authentication screenshot never captured; one temporary full-page crop-bounds screenshot deleted |
| Confirmed new objects across comparable prior ID sets | 14: 9 worksheets, assay 21, automation 17, parsers 48–50 |
| Confirmed changed objects across comparable baselines | 24: 23 worksheet active-version transitions (including ID 76 gaining its first active version) plus report 26 active-version change |
| Confirmed missing prior objects/versions | 0 prior worksheet IDs and 0 prior worksheet version IDs; no prior assay, automation, parser, or report ID was found missing |
| Confirmed renamed objects | 1: worksheet ID 76 display name changed |

These comparison counts are limited to categories with authoritative prior ID-level inventories. They are not extrapolated to categories whose earlier evidence was list-only or absent.

## Phase 6 reconciliation

- Added `dependency_map.md` and `dependency_graph.json`, joining assays, worksheets, protocols, parser/automation paths, reports, KV stores, controls, resource groups, inventory, and equipment without inventing name-only edges.
- Reconciled the canonical assay and protocol indexes, including the new Pesticides Quantitative Flower assay and the complete Cannabinoid Potency worksheet 32–40 / step-assignment gaps.
- Confirmed Cannabinoid Potency protocol 4 is the strongest visible structural reference for a future Terpenes protocol but is not a complete gold standard: worksheet 39/step 21 is unassigned, worksheet 41 has no versions, steps 20 and 74–76 are unassigned, and conditionality was not exposed.
- Completed the controlling SOP v1.4 and Form-to-QBench crosswalk. Terpenes is **Partially represented**: the active parser 50 → worksheet 43 → automation 17 → worksheet 42 → report 26 result path exists, but protocol 9 is empty/unassigned and the method, preparation, QC, resource, current worksheet, and report-range controls are missing or unverified.
- Preserved document discrepancies without invention: the user-confirmed Version 1.3 header typo, the Form’s internal-standard volume conflict with the controlling SOP, stale footer metadata, page-indicator inconsistencies, and Form criteria that are less complete than the SOP.

## Material findings

1. Active automation 1 swaps Lead and Mercury relative to the last verified active worksheets.
2. Active automation 6 returns 17 Residual Solvents columns into a 19-cell destination, omitting Total Xylenes and Trichloroethene.
3. Active automation 11 swaps Unknown Peaks 2 and 3 in actions 21–22.
4. Automation 10 has a likely destination-name mismatch relative to the last verified worksheet 16 export; a current native export is required before classifying it as a confirmed current defect.
5. Report 44 conflicts with the canonical Homogeneity contract by preferring `homogeneity_metrc`, reconstructing Potency cells instead of rendering `report_results`, and converting missing numeric lookups to literal `0.0`.
6. Report 26 v24 renders Terpenes `report_results` and reads generic `pass_fail`, while the last verified Terpenes worksheet export contains neither. Current compatibility is unable to be verified because v14 was not exported.
7. Current KV-store data differs materially from historical embedded worksheet snapshots. Current assignment edges remain unverified until native worksheet exports or explicit read-only assignment surfaces are available.
8. Sensitive integration configuration was encountered on an authenticated settings page. Details were intentionally omitted. Managed Interfaces remains incomplete pending separate administrative or vendor remediation.

## Stability, timezone, and rendering findings

- Stability evidence is limited to active assay 13, three Sample field definitions, and active Stability Due email template 51. Template 51 has no saved version and an empty visible source. Multiple pull dates, 3/6/12-month interval representation, scheduling, reminder timing, recipient roles, and record-versus-field-versus-step modeling remain unable to be verified read-only.
- Tenant timezone was not exposed on the safe General Settings surface. Current report sources call `local_time` without embedding a timezone identifier, so rendering timezone remains unverified.
- Reports 26 and 44 contain fixed elements approximately 8.48–8.5 inches wide despite one-inch Letter margins; report 20 instead contains a 100.311%-wide table. No PDF/report preview was generated, so fit, clipping, page breaks, and counter placement remain unverified.
- Report 44 also has automatic-page-number/CSS-counter duplication risk, an unused page-break class, and no exposed attachment for its requested watermark.

## Final validation

- All dated JSON files parse.
- All dated CSV files parse.
- Dependency graph node/relationship counts reconcile to the source inventories.
- The only two screenshots were opened and manually reviewed. They contain worksheet version/export configuration only, and their SHA-256 values match `Screenshots/index.csv`.
- No DOCX, HAR, MHTML, or unsafe browser artifact is present in the dated scan.
- Final secret and privacy review passed.
- `MANIFEST.sha256` covers every regular file in the dated scan except itself using exact staged Git blob bytes; path-set and content verification pass after final generation.
- Unrelated untracked Terpenes development paths remain excluded. Exact-path staging was used; no attached reference DOCX was staged.

## Completeness and omissions

The rescan is complete under the amended scope. It does not claim that current native worksheet definitions, field Edit-only properties, operational histories, report previews, parser/automation runtime behavior, customer operational data, or identity-bearing records were captured. Each omission is recorded in `completeness_matrix.md`, `privacy_omissions.md`, and the category README files.

Open questions remain active and are consolidated in `open_questions.md` and `QBench/Docs/qbench_open_questions.md`. None authorizes a production change; the confirmed automation defects, likely automation-10 mismatch, protocol gaps, Terpenes/Form reconciliation, current export blocker, Stability model, and report-rendering questions require separate controlled follow-up.

## Public-repository disclosure gate

**Gate status: passed for the sanitized candidate.**

Sensitive integration configuration was encountered on an authenticated settings page. Details were intentionally omitted. Managed Interfaces remains incomplete pending separate administrative or vendor remediation.

Publication requires the sanitized tree and publication branch to pass the final disclosure and validation gates.

No push, draft pull request, merge, or force-push was performed.
