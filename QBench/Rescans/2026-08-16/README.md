# QBench Production Read-Only Configuration Rescan — 2026-08-16

## Status

Phase 1 began on 2026-08-16, paused at the prompt-defined manual-authentication stop condition, resumed after the user completed the correct QBench login manually, and completed its preflight/navigation checkpoint at `2026-08-16T21:48:12.430Z`. Phase 2 then enumerated every visible worksheet and version. Worksheet metadata is complete, but all native **Export Spreadsheet** targets are blocked by the available authenticated browser tooling. Phase 3 completed the assay, panel, protocol-step, field-definition, and key/value-store inventories at `2026-08-16T23:29:19.441Z`. Phase 4 completed automations, file parsers, reports, and all visible template families at `2026-08-17T01:48:23.745Z` after correcting and validating the Code-parser and email-template source captures. Phase 5 captured controls, control groups, resource groups, inventory, equipment, Document Control metadata, and safe settings structure. Phase 6 completed offline dependency, canonical-index, Cannabinoid Potency protocol, and Terpenes SOP/Form reconciliation without reopening QBench. Phase 7 completed the local secret/privacy, screenshot, structure, manifest, completeness, diff, and public-disclosure reviews.

Sensitive integration configuration was encountered on an authenticated settings page. Details were intentionally omitted. Managed Interfaces remains incomplete pending separate administrative or vendor remediation.

- Scan start: `2026-08-16T21:26:25.149Z`
- Branch: `codex/qbench-production-readonly-rescan-2026-08-16`
- Base: `origin/main` at `ae07feb59e5339932823908841219cc4cb6b5221`
- Repository visibility: public
- Production hostname verified before authentication: `ait.qbench.net`
- Phase 2 production hostname: `ait.qbench.net`
- Original stop page: external sign-in page; authentication URL parameters were never retained
- Original stop reason: manual authentication was required
- Authentication resumed: `2026-08-16T21:41:24.556Z`
- `authentication_completed_manually_by_user = true`
- QBench mutations performed: 0

The original browser stop occurred at the authentication boundary before any configuration object was opened. Google SSO was not completed or authorized. The user later completed the correct QBench login manually, after which read-only configuration navigation resumed. No authentication screenshot was captured because sign-in surfaces can expose account information and are not configuration evidence.

## Phase 1 preflight completed before the stop

- Fetched all remote branch refs and pull-request head refs.
- Read the repository safety instructions.
- Confirmed `origin/main` is the current local base after fetch.
- Confirmed the repository is public through the connected GitHub application.
- Recorded open draft PRs #15 and #16 as unrelated work that must not be overwritten.
- Reconciled the 2026-07-04 worksheet and 2026-07-15 parser evidence as an offline comparison baseline; see `prior_scan_baseline.md`.
- Preserved all pre-existing untracked Terpenes development artifacts.
- Created the required dated scan branch.
- Verified `ait.qbench.net` at the customer portal and employee login routes.

The worktree contained 105 pre-existing untracked files under `QBench/Worksheets/Terpenes/development/` before this scan directory was created. They include local runtime artifacts, controlled/source documents, and a not-ignored `.env.local.txt` path. Their contents were not captured for this scan. They must never be staged by a broad `git add .` or `git add -A`; only explicit rescan and approved canonical documentation paths may be staged.

## Resume verification

- Effective hostname: `ait.qbench.net`
- Safe page URL: `https://ait.qbench.net/`
- Authenticated QBench application visible; no employee-login or customer-portal surface present
- Correct production tenant confirmed by the user and matched to the tenant-specific production hostname
- Branch preserved: `codex/qbench-production-readonly-rescan-2026-08-16`
- Existing ten baseline files preserved and privacy-scanned before further QBench navigation

## Phase 2 worksheet checkpoint

- 148 worksheet objects and 700 visible versions recorded.
- 137 active approved versions identified.
- 17 newer non-active versions above an active version identified on 16 objects.
- 7 latest-draft targets identified on objects without an active version.
- 3 objects have no versions: IDs 41, 68, and 149.
- 161 native **Export Spreadsheet** targets identified across 144 objects.
- 0 of 161 native exports completed because representative invocations of the visible control produced no downloadable file through the available browser tooling.
- **Export to Excel** was not used, and no worksheet JSON was reconstructed.
- Two tightly cropped screenshots for worksheet 8 were manually reviewed and retained as representative configuration-only evidence.
- All 139 worksheet IDs and 623 version IDs from the 2026-07-04 metadata remain present. Nine worksheet objects and 77 version records are new.

See `Worksheets/README.md`, `worksheet_version_inventory.csv`, and `worksheet_comparison_summary.md` for the evidence and comparison boundary.

## Phase 3 configuration checkpoint

- 20 active assays captured from all detail pages; assay ID 21, Pesticides Quantitative Flower, was added to the canonical assay map.
- 9 active panels and 88 ordered panel-to-assay memberships captured.
- 15 protocols, 81 protocol-step definitions, and 118 ordered assignments captured.
- Protocols 5 (Microbials) and 9 (Terpenes) have zero assigned steps. Terpenes assay 8 exposes no protocol assignment.
- Cannabinoid Potency protocol 4 has 24 steps and is the broadest current structural model, but worksheet 39 is unassigned and assigned final-review worksheet 41 has no version.
- 277 field definitions captured across 20 populated object types; two default-test panes were empty. Deeper field properties requiring an Edit action were not opened.
- 11 key/value stores and 13,766 ordered scalar rows captured from the complete two-page list. API Clients, History, and created-by identities were omitted.
- The Phase 3 end hostname guard verified `ait.qbench.net`; QBench mutations remain 0.

See `Assays/`, `Panels/`, `Protocols/`, `Fields/`, `Key_Value_Stores/`, `protocol_relationship_map.md`, and `kvstore_dependency_analysis.md`.

## Phase 4 automation, parser, report, and template checkpoint

- 16 automations captured: 13 active, 3 inactive, 18 condition blocks, and 90 ordered actions. New active ID 17 propagates 26 Terpenes fields from worksheet 43 to Test worksheets.
- 10 file parsers captured: 5 active/5 inactive and 5 Code/5 No Code. Full source for Code IDs 45, 46, 48, 49, and 50 was recaptured through the read-only full-editor interface after rejecting a viewport-derived extraction; all five corrected artifacts passed `node --check`. Sixty-three No-Code finder names were recorded without entering Edit.
- Active parser 50 and automation 17 form a visible Terpenes parser-to-Batch-to-Test path. Parser 50's source contains an `SBX_ONLY` marker even though its production configuration is active.
- 3 report configurations and complete version lists captured. Report 26 advanced from active v20 to v24, and sanitized Header/Body/Footer source is now attributable to the active version.
- 27 non-report template configurations captured across labels, email, platemap, invoice, internal-report, and macro families. Four template families were verified empty.
- Stability Due email ID 51, platemap ID 39, and macro ID 27 are active but have no saved version; the visible editors/designs are empty.
- Six active label configurations each have a newer draft. Draft source was captured; active source did not initialize after read-only version selection and was not reconstructed.
- Fourteen approved-active email v1 sources were recaptured after rejecting the same viewport method; independent Jinja stack/comment validation passed 14/14. All 14 retain runtime plain-HTTP Google Fonts and `qbench.net` references.
- Cross-export validation confirmed active automation defects in IDs 1 (Lead/Mercury swapped), 6 (17-column return into a 19-cell Residual Solvents result range), and 11 (Unknown Peak 2/3 swapped). ID 10 has a likely broken destination name relative to the last active worksheet export and requires a current native export before correction.
- Report 44 conflicts with the canonical Homogeneity contract by preferring `homogeneity_metrc` over `pass_fail` and reconstructing a table instead of rendering `report_results`; current named-cell compatibility remains export-blocked.
- Tenant timezone was not exposed on the read-only General Settings surface. All current reports use `local_time` without embedding a timezone identifier.
- Reports generated, parsers executed, automations executed, emails sent, internal reports run, and QBench mutations: 0.

See `Automations/`, `File_Parsers/`, `Reports/`, `Templates/`, `automation_cascade_analysis.md`, `parser_dependency_map.md`, and `report_dependency_map.md`.

## Phase 5 partial controls, resources, equipment, and settings checkpoint

- 4 active controls and 2 control groups captured; the four reverse memberships reconcile exactly.
- 10 resource groups captured with 105 item-membership rows and 137 equipment-membership rows.
- 158 unique inventory items captured across all eight pages using safe ID/name/category/page metadata, explicit resource-group IDs, and units/size exposed by safe membership rows; IDs 292 and 273 have blank categories, and all 105 group-membership rows have blank default quantities. Stock, lots, quantities, separate supplier/manufacturer/catalog fields and account data, transactions, purchases, and attachments were excluded.
- 103 unique equipment records captured using safe ID/code/type/status/site/schedule metadata only: 97 In Service, 3 Retired, 2 Backup Equipment Only, and 1 Out of Service. Equipment 107 has an undelimited schedule display that could not be safely resolved.
- 38 active equipment schedule definitions captured.
- Document Control expanded-tree views expose 68 Show-All leaves, 66 Approved leaves, and 3 Pending leaves. Approved and Pending are non-additive because one leaf appears in both. The earlier 47-object navigation count is retained as a different view scope.
- Terpenes document entries were read at metadata level only and are labeled `QBench metadata only — current revision authority supplied by user`.
- General Settings Boolean structure, Customer Portal labels, 1 inactive Log Type, and an aggregate 1,097-Location count were captured without operational records or sensitive values.
- The Specification Module is enabled, but no standalone Specifications/spec-group route was exposed in visible navigation.
- Stability evidence remains limited to assay 13, three Sample fields, and empty/unversioned email template 51.
- `status = blocked_metadata_only`; `objects_counted = 4`; `details_retained = 0`; `secret_values_committed = 0`; `reason = sensitive_integration_configuration_encountered`; `rescan_required = only_after_separate_remediation_and_explicit_authorization`.

See `Controls/`, `Control_Groups/`, `Resource_Groups/`, `Inventory/`, `Equipment/`, `Document_Control/`, and `Settings/`.

`MANIFEST.sha256` is the Phase 7 final local integrity manifest for every regular dated-scan file except itself. It is generated and verified against exact staged Git blob bytes; line-ending-converting checkouts must use Git blob bytes for verification.

## Phase 6 offline reconciliation

- Built the end-to-end dependency map and machine-readable dependency graph from the sanitized Phase 1–5 evidence.
- Reconciled the assay, protocol, worksheet, field, KV-store, parser, automation, report, control, resource, inventory, and equipment indexes.
- Reconciled Cannabinoid Potency protocol 4 as a useful but incomplete structural reference: worksheet 39 remains unassigned, worksheet 41 has no versions, orphan/patch step definitions remain outside the protocol, and conditionality was not exposed.
- Confirmed both reference DOCX files were locally available and read them in place. The controlling SOP is Version 1.4; its internal Version 1.3 header is the user-confirmed typo. Neither attached source document was copied by this scan, staged, or committed.
- Completed `Terpenes/terpenes_sop_v1_4_qbench_protocol_crosswalk.md`, including the Form record-structure reconciliation and preserved source-document discrepancies.
- Reconciled the active parser 50 → worksheet 43 → automation 17 → worksheet 42 → report 26 chain. That chain transfers results but does not establish the full controlled SOP method because protocol 9 is empty/unassigned and method, QC, resource, current worksheet, and report-range layers remain missing or unverified.
- QBench was not reopened for Phase 6; QBench mutations remain 0.

## Remaining limitations before final publication

- Native current worksheet definitions and structural worksheet comparison, blocked as described above

## Phase 7 final local validation

- Parsed all 39 JSON and 39 CSV artifacts.
- Opened and manually reviewed both retained screenshots; both are safe worksheet-configuration crops and their hashes match `Screenshots/index.csv`.
- Reconciled the dependency graph and category counts to the authoritative inventories.
- Final secret and privacy review passed.
- Generated and verified the 155-entry final manifest from staged Git blob bytes.
- Confirmed 0 DOCX files in the dated rescan and exact-path staging only.
- Completed `change_summary.md` with counts, findings, omissions, closeout fields, and validation status.

## Phase 1 navigation inventory

The authenticated navigation inventory and list-page counts are recorded in `navigation_inventory.csv`. Notable changes from the prior repository baseline include 148 worksheets, 16 automations, and 10 file parsers. Resource Groups, Key/Value Stores, and several template/configuration pages display an incorrect `0 - 0 of 0` range despite visible configuration rows; these counts were therefore based on unique detail IDs or visible data rows and are explicitly labeled.

Operational routes for Customers, Contacts, Orders, Samples, Tests, Batches, invoices, payments, quotations, parser-result history, report-generation history, and email history were intentionally not opened.

## Attachment availability

Both reference documents are available locally. `Terpene Analysis SOP v 1.4.docx` is the controlling Version 1.4 document; an internal Version 1.3 header is a known typographical error. `Terpenes Analysis Form.docx` is the recording-structure reference. Neither attached source DOCX was copied into the dated rescan or staged/committed by this scan.
