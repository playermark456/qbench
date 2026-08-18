# QBench Template Index

Last verified read-only in the production tenant at `ait.qbench.net` on 2026-08-16/17 UTC. Current dated evidence is under `QBench/Rescans/2026-08-16/Reports/` and `QBench/Rescans/2026-08-16/Templates/`.

## Family inventory

| Family | Current visible count | Status / capture |
|---|---:|---|
| Report Templates | 3 | All version lists and sanitized active source captured |
| Label Templates | 7 | All version lists; selected newer-draft sources captured |
| Email Templates | 15 | 14 active v1 sources; Stability Due has no version |
| Print Templates | 0 | Empty list verified |
| Platemap Templates | 1 | Active, no versions, empty 96-well grid |
| Invoice Templates | 1 | Active v1 source captured |
| Quotation Templates | 0 | Empty list verified |
| Payment Templates | 0 | Empty list verified |
| Rich Text Configurations | 0 | Empty list verified |
| Internal Reports | 2 | Active configuration metadata; source not exposed; not run |
| Template Macros | 1 | Active configuration, no versions or parameters, empty source |

## Report templates

| ID | Name | Configuration status | Active version | Notes |
|---:|---|---|---|---|
| 26 | Certificate of Analysis Report | Active | 24 — Terpenes final | 24 versions; sanitized Header/Body/Footer and six safe attachment names captured |
| 44 | Homogeneity | Active | 2 — 3.0 | Standalone Homogeneity source; operational selection remains unverified |
| 20 | 1Certificate of Analysis Report | Inactive | 1 | Legacy configuration; v1 still displays approved active |

## Labels

| ID | Name | Level | Configuration | Active version | Newer draft |
|---:|---|---|---|---:|---:|
| 24 | Inventory Label | Inventory | Active | 5 | 6 |
| 29 | Equipment Label (Barcode) | Equipment | Active | 4 | 5 |
| 30 | Equipment Calibration | Equipment | Inactive | — | 2 |
| 32 | Sample Intake Sample Label | Sample | Active | 4 | 5 |
| 33 | Sample Assay Labels | Test | Active | 2 | 3 |
| 34 | Location Label | Location | Active | 3 | 4 |
| 35 | Batch Label (Barcode) | Batch | Active | 2 | 3 |

The six active-label draft sources were captured because the UI selected those drafts by default. The existing active-version editor source did not initialize after read-only version selection and was not reconstructed. Therefore IDs 24, 29, 32, 33, 34, and 35 all have an active-source evidence gap; the captured drafts must not be represented as their active content.

## Email, platemap, invoice, internal-report, and macro gaps

- Email IDs 1, 2, 5–10, 12, 13, and 15–18 each have approved active v1 source.
- The initial viewport/DOM capture was rejected because off-screen CodeMirror text was duplicated/truncated and produced a false preliminary “12 malformed sources” result. All 14 sources were authoritatively recaptured through full-editor read-only Select All; independent stack/comment validation found zero Jinja defects or duplicate openers, and JSON/CSV/file hashes reconcile exactly.
- All 14 recaptured sources contain runtime `http://` references for Google Fonts and a `qbench.net` anchor. XHTML declaration/namespace URLs and a commented attribution URL are not runtime resource findings. No credential, token, authorization, or session value was found; HTTPS migration and compatibility validation remain open.
- Email ID 51, `Stability Due`, is an active Alert configuration with no version and empty source. Alert scheduling, recipients, timepoint logic, and reminder timing remain unverified.
- Platemap ID 39, `Total Aerobic Microbial`, is active but has no version.
- Invoice ID 40 has approved active v1. Its content/version association reconciles, but JSON capture metadata says `initial_selected` while `template_versions.csv` says `selected_at_capture=false`; selection provenance should be normalized on the next evidence refresh.
- Internal report IDs 31 (`Test`) and 52 (`# Tests`) are active, restricted configurations; configured identities were omitted and source was not exposed.
- Macro ID 27, `gdxg`, is active but has no version, parameters, or source content.

## Safety and evidence limits

No report, preview, email, internal report, label, invoice, or operational record was generated or selected. Signature-image content and staff identities were omitted. Persisted report/template sources contain no literal email, phone, credential, token, authorization, or session values; field names and sanitized marker metadata are not evidence of exposed values. Tenant timezone is not exposed on the inspected General Settings surface. Current report-to-worksheet range compatibility remains unverified because current native worksheet exports are blocked.
