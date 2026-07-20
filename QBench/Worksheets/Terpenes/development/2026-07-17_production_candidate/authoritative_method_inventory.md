# Authoritative Terpenes method-document intake inventory

Inventory date: 2026-07-17

## Intake result

The `authoritative_method/` directory was created. It has a narrow local ignore rule that excludes controlled source documents while retaining the `.gitignore` file; sanitized inventory and manifest files outside that directory remain trackable.

The intake is **stopped**. Multiple distinct SOP candidates exist, one filename claims version 1.2 while its visible document control block says version 1.1, and the discovered validation report contains real validation sample/product and internal-system information. The report was not retained in the target directory.

No calculation-contract interpretation, formulas, worksheet JSON, QBench access, API activity, staging, commit, push, or PR action was performed.

## Bounded source locations checked

| Location | Result |
| --- | --- |
| `Downloads/Terpenes Method Documents` | Not present. |
| `Downloads/Terpene Documents` | Three Terpenes method candidates found. |
| `Downloads/Terpene Documents.zip` | Present; extracted unchanged to a temporary local directory and inspected. Three files found. |
| Downloads root, filename filter only | Terpenes SOP candidates and one Analysis Form found. Unrelated matching files were not copied. |
| Repository `QBench/Worksheets/Terpenes` subtree | Implementation materials and worksheet artifacts found; none were treated as controlled scientific method documents or copied. |

## Copied controlled-document candidates

| Target filename | SHA-256 | Source label | Visible classification |
| --- | --- | --- | --- |
| `Terpene Analysis SOP v 1.1__source_downloads.docx` | `b096f9b9668295fcb46756e2963f5b103cae581224ca52ce53776e513a9c9cb0` | Downloads root | Terpene Potency by GC-FID SOP; visible version 1.1; approval field visible; revision date not established. |
| `Terpene Analysis SOP v 1.2.docx` | `b096f9b9668295fcb46756e2963f5b103cae581224ca52ce53776e513a9c9cb0` | Downloads root | Same bytes as the Downloads-root version-1.1 filename, but the visible control block says version 1.1. Revision-label conflict. |
| `Terpene Analysis SOP v 1.1__source_terpene_documents.docx` | `f2ff45d6f3b13eba2c0610fe4cffeb713faf3ef14b0f7f722c1f590f4b398df5` | Downloads/Terpene Documents | Terpene Potency by GC-FID SOP; visible version 1.1; approval field visible; distinct bytes. |
| `Terpene Analysis SOP v 1.1__source_terpene_documents_zip.docx` | `de53223bc129c42cdeb3bf38dede659facbd65bbf0fb4956a211ee57589b2390` | Terpene Documents.zip | Terpene Potency by GC-FID SOP; visible version 1.1; approval field visible; distinct bytes. |
| `Terpenes Analysis Form.docx` | `4aa5f6ed453bb5cbfb933b2eb8bb7f28f6252cb97ecf4a0667e64482661b2302` | Downloads root | Terpenes Potency by GC-FID Form; visible version 1.0; approval field visible; revision date not established. |
| `Terpenes Analysis Protocol.docx` | `a2d34b090823cf5706c091fbdf00b33dd2b6414bcd889f28557d0a05d854278f` | Downloads/Terpene Documents | Validation Protocol for Terpene Potency by GC-FID; visible version 1.0; document text says approval/effective status must precede execution. |

## Duplicate and collision handling

- The protocol and validation-report bytes in the archive exactly match their Downloads/Terpene Documents copies; only the Downloads/Terpene Documents protocol was retained.
- Three different byte streams use the `Terpene Analysis SOP v 1.1.docx` filename. They were preserved with collision-safe source suffixes.
- The Downloads-root filenames `Terpene Analysis SOP v 1.1.docx` and `Terpene Analysis SOP v 1.2.docx` have identical bytes, despite the latter filename's version claim. Both filenames were preserved because the mismatch itself is evidence.

## Excluded candidate

`Validation Report for Terpenes.docx` was found in both the archive and Downloads/Terpene Documents with identical bytes. Visible review showed real validation sample/product and internal-system information. It was not retained in `authoritative_method/`; the locally created copy was immediately removed after hash verification. No source file or archive was changed.

## Required-document coverage

| Category | Status | Intake finding |
| --- | --- | --- |
| A. Current Terpenes SOP | conflicting_candidates | Multiple distinct version-1.1 SOP files; a version-1.2 filename has version-1.1 visible content. |
| B. Current Terpenes Analysis Form | present_but_revision_uncertain | Version-1.0 form candidate is present; currentness cannot be established. |
| C. Current Analysis or Validation Protocol | present_but_revision_uncertain | Version-1.0 protocol candidate is present; execution approval/effective status is not established. |
| D. Current Validation Report | present_but_revision_uncertain | A report candidate exists but was excluded from local method review because it contains real validation sample/product and internal-system data. |
| E. LabSolutions Compound Results source evidence | absent | No standalone LabSolutions method, calibration, or compound-table record was found. |
| F. Exact Conc. unit | absent | No standalone controlled instrument-unit evidence was found. |
| G. Matrix-specific mass/extraction rules | present_candidate | Candidate SOP/form/protocol sources exist, pending controlled-revision resolution. |
| H. Solvent-added versus final-volume convention | present_candidate | Candidate SOP/form/protocol sources exist, pending controlled-revision resolution. |
| I. Dilution-factor definition and application | present_candidate | Candidate SOP/form/protocol sources exist, pending controlled-revision resolution. |
| J. mg/g and percent equations | present_candidate | Candidate SOP/form/protocol sources exist, pending controlled-revision resolution. |
| K. LOQ and below-LOQ behavior | present_candidate | Protocol candidate visibly references LOQ; the applicable reporting policy remains unconfirmed. |
| L. Rounding and significant figures | absent | No clearly controlled source was identified during intake. |
| M. Measurement uncertainty | absent | No dedicated controlled MU source was found. |
| N. Approved COA measurands and units | absent | No approved COA specification was found. |
| O. Ocimene and Nerolidol treatment | absent | No approved reporting convention source was found. |
| P. METRC mapping and units | absent | No approved controlled METRC mapping source was found. |
| Q. Peak Table audit-only treatment | absent | No controlled source identified during intake. |
| R. Dimethylacetamide audit-only treatment | absent | No controlled source identified during intake. |
| S. No Terpenes compliance Pass/Fail | absent | No controlled source identified during intake. |

## Resume gate

The calculation-contract resume prompt cannot proceed. Required resolution is: identify the current approved SOP and Form, resolve the conflicting SOP copies and version label, supply controlled LabSolutions unit evidence, and provide a safely reviewable validation/COA/METRC source set without customer or internal-system data.
