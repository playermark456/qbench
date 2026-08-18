# Templates — Production Read-Only Snapshot

This directory contains the non-report template inventory. Report configurations are documented separately under `../Reports/`.

## Family counts

| Family | Visible configurations |
|---|---:|
| Label Templates | 7 |
| Email Templates | 15 |
| Print Templates | 0 |
| Platemap Templates | 1 |
| Invoice Templates | 1 |
| Quotation Templates | 0 |
| Payment Templates | 0 |
| Rich Text Configurations | 0 |
| Internal Reports | 2 |
| Template Macros | 1 |

The directory holds 27 configuration records, 43 saved-version rows, and 26 sanitized source artifacts. `template_source_inventory.csv` provides the path, byte count, SHA-256, active-version relationship, and redaction counts for every captured source.

## Version findings

- Each of the six active label configurations has a newer draft selected by default: ID 24 active v5/draft v6, ID 29 v4/v5, ID 32 v4/v5, ID 33 v2/v3, ID 34 v3/v4, and ID 35 v2/v3. The newer draft source was captured. Selecting the existing active version read-only exposed page setup but did not initialize its Body editor; all six active sources are explicitly marked unavailable rather than reconstructed.
- Inactive label ID 30 has two draft versions and no active version.
- Fourteen system email configurations have one approved active v1 source.
- Email ID 51, `Stability Due`, is an active Alert configuration with no saved version and an empty editor source. This does not establish a functioning alert schedule.
- Platemap ID 39 is active but has no version; the visible design is an empty 8×12 (96-well) grid.
- Invoice ID 40 has approved active v1; Header, Body, Footer, and page setup were captured.
- Internal report IDs 31 and 52 are active and not globally available. Configured user identities were omitted. The configuration page exposed no report query/design source, and neither report was executed.
- Active Code macro ID 27 has no versions, no parameters, and an empty editor source.

## Active email source validation

The first viewport/DOM extraction method was rejected because it duplicated or truncated off-screen CodeMirror text and falsely made 12 sources appear to have unmatched Jinja controls. It is not authoritative evidence of live-source defects.

All 14 approved-active email v1 sources—IDs 1, 2, 5–10, 12, 13, and 15–18—were recaptured from the full CodeMirror editor using read-only Select All. Independent validation found zero Jinja stack/comment defects, zero duplicated control openers, exact JSON/CSV/file hash reconciliation, and zero email, phone, blob, or embedded-image redactions. `template_source_inventory.csv` identifies these artifacts as `full_editor_text_recaptured_via_read_only_select_all`; only this recapture is authoritative.

One real source issue remains: all 14 contain an externally loaded Google Fonts URL and a `qbench.net` anchor using plain `http://`. The XHTML namespace/DOCTYPE URLs and the commented template-attribution URL are inert metadata/comment references and are not classified as runtime transport defects. No credential, token, authorization, or session value was found.

Invoice ID 40 reconciles to approved active v1 and its persisted source, but capture metadata differs on selection provenance: the JSON records `initial_selected`, while `template_versions.csv` records `selected_at_capture=false`. This does not change the version/content association and should be normalized in a future evidence refresh.

## Capture boundary

- No template preview, email preview/send, internal-report run, invoice/record selection, file selection, upload, Save, Save Draft, Save As New Version, Set Active, approval, Clone, Make Public, download, or Delete was used.
- Report assets and report templates are kept under `../Reports/`.
- One opaque blob URL was replaced in the invoice Header source. No literal email or phone values remain in the captured template sources.
- User and uploader identities were omitted.
- Screenshots were omitted because the available full-page scope included account UI.
