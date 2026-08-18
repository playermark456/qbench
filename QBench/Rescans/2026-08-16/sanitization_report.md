# Sanitization Report — 2026-08-16

## Current baseline

- Screenshots reviewed: 2
- Screenshots retained for checkpoint commit: 2
- Screenshots omitted: 1 authentication surface category
- Downloaded QBench native worksheet artifacts reviewed: 0; native export capture is blocked
- Credentials or secrets committed: 0

The action log retains only safe QBench URLs without session material and a hostname-only Google sign-in URL. OAuth query parameters and state values were omitted.

## Resume-check baseline audit

Before authenticated configuration navigation resumed, all ten existing baseline files were scanned. Results:

- Login-page or account-chooser screenshots: 0
- Email addresses: 0
- Authentication URLs containing query or fragment parameters: 0
- JWT-like values: 0
- Cookie, token, CSRF, authorization-header, password, or autofill values: 0
- Generic security terms and the hostname-only original stop reference were manually reviewed and contain no secret or session material

## Phase 2 worksheet evidence review

- Worksheet/version text artifacts reviewed: 6 before the validation report was added
- Email-address matches: 0
- JWT-like matches: 0
- Bearer-credential matches: 0
- Credential/token assignment matches: 0
- Authentication URL parameters: 0
- Source DOCX files under the dated scan directory: 0
- Native worksheet exports: 0; none were produced by the visible **Export Spreadsheet** control
- Screenshot files: 2, both tightly cropped and manually reviewed
- Retained screenshot content: active version selector/status and native export-menu labels only
- Excluded from retained screenshots: account name, password-expiry notice, staff data, credentials, session material, and operational records

A temporary full-page screenshot used only to calculate safe crop bounds displayed account and password-expiry UI. It was deleted immediately after the two crops were created and reviewed; it is not present in the repository or scan directory.

## Phase 3 configuration evidence review

- Assay JSON/CSV: 20 objects; technician and team values omitted.
- Panel JSON/CSV: 9 objects and 88 membership rows; configuration only.
- Protocol JSON/CSV: 15 protocols, 81 step definitions, and 118 assignments; no operational records.
- Field JSON/CSV: 277 definitions only; no Customer, Contact, User, Sample, Test, Order, Batch, Inventory, or Equipment record values.
- KV-store evidence: 11 stores and 13,766 ordered scalar rows; created-by identities omitted; API Clients and History not opened.
- Phase 3 screenshots captured: 0.
- Automated in-memory checks across Phase 3 evidence found 0 email addresses, 0 JWT-like values, 0 authorization credential values, 0 cookie assignments, and 0 authentication/session query parameters.
- Secret-like KV values requiring redaction: 0. The extractor would have replaced any detected value with `[REDACTED_SECRET]` without preserving its length or hash.
- Attached SOP/form DOCX files copied by this scan, staged, or committed: 0.

## Phase 4 source and interaction sanitization

- Automation evidence: 16 objects, 18 condition blocks, and 90 actions; no history or operational records.
- Parser evidence: 10 objects and five corrected full-editor Code sources. The initial overlapping viewport extraction was rejected; exact persisted hashes and `node --check` PASS results bind to the read-only select-all recapture. Source checks found 0 email addresses, 0 phone numbers, and 0 hard-coded operational record IDs.
- Report source artifacts: 9 sanitized HTML files. Replacements total 3 email values, 1 phone value, 11 opaque blob URLs, and 4 embedded image payloads.
- Non-report template source artifacts: 26 sanitized HTML files. The 14 active email sources were recaptured through the corrected full-editor method and independently passed Jinja stack/comment validation. Replacements total 1 opaque blob URL and 0 email, phone, or embedded-image values.
- Signature-image contents downloaded or committed: 0.
- Report-password values inspected or committed: 0.
- Phase 4 screenshots captured or retained: 0; safe element-only capture was unavailable.
- Phase 4 read-only browser log rows: 336.
- Phase 4 log URLs with a hostname other than `ait.qbench.net`: 0.
- Phase 4 log URLs with query parameters other than a safe object `id`: 0.
- Phase 4 mutation flags: 0.
- Parsers executed: 0; automations executed: 0; reports generated: 0; emails sent: 0; internal reports run: 0.

## Phase 5 metadata sanitization

- Controls: 4 configuration objects and 4 group memberships; no results or operational records.
- Control groups: 2; no execution/failure records.
- Resource groups: 10, with 105 safe item-membership rows and 137 safe equipment-membership rows.
- Inventory items: 158 unique IDs. Retained values are ID, name, category, source page, explicit resource-group IDs, and units/size exposed by safe membership rows; separate supplier/manufacturer/catalog fields and operational values were omitted.
- Equipment: 103 unique IDs and 38 schedule definitions. Serial, certificate, service, exact-location, staff, and operational values were omitted.
- Document Control: 68 expanded-tree leaf occurrences; no document content, attachments, notes, training records, or identity-bearing workflow data.
- Settings: safe labels and Boolean states only; Customer Portal values omitted.
- Locations: aggregate count only.
- Phase 5 screenshots captured or retained: 0.
- Phase 5 read-only interaction log rows: 96; every row has the 13 required columns and a `No mutation = Yes` flag.
- Sensitive integration configuration was encountered on an authenticated settings page. Details were intentionally omitted. Managed Interfaces remains incomplete pending separate administrative or vendor remediation.
- Phase 5 action-log mutation flags: 0.
- QBench mutations, parsers executed, automations executed, reports generated, emails sent, and operational records saved remain 0.

## Phase 6 and Phase 7 final review

- Phase 6 and Phase 7 QBench interactions: 0; all work used existing sanitized evidence and the local reference documents.
- Dated scan files: 156 including `MANIFEST.sha256`; 155 files are covered by the manifest.
- JSON parse: 39/39 pass. CSV parse: 39/39 pass.
- Screenshots: 2/2 opened, manually reviewed, and hash-matched; both are configuration-only worksheet crops.
- DOCX files in dated scan: 0. Neither attached source document was copied by this scan, staged, or committed.
- Managed Interfaces: `status = blocked_metadata_only`; `objects_counted = 4`; `details_retained = 0`; `secret_values_committed = 0`; `reason = sensitive_integration_configuration_encountered`; `rescan_required = only_after_separate_remediation_and_explicit_authorization`.
- Final secret and privacy review passed.
- Public disclosure review of the sanitized tree passed.
- QBench mutations, parsers executed, automations executed, reports generated, customer operational records saved, and credentials/secrets committed: 0.
