# Document Control configuration — production read-only capture

The expanded Document Control tree exposes 68 unique path/name leaf occurrences in Show All, 66 in Show Approved Only, and 3 in Show Pending Only. Those filter counts are non-additive: `Instrument Maintenance, Calibration, and Qualification SOP` is visible in both Approved and Pending, creating one overlap. Phase 1 recorded a 47-object navigation/list count. Because the scopes differ, the discrepancy is preserved rather than normalized.

Document content was never opened or downloaded. Only the version-state tables for the two relevant Terpenes names were read:

- `04-Testing Methods / Assay Specific SOPs / Terpenes / Terpene Analysis SOP`: draft v1 metadata.
- `04-Testing Methods / Assay Specific SOPs / Terpene Analysis SOP`: approved v1 metadata.
- `04-Testing Methods / Assay Specific SOPs / Terpenes / Terpenes Analysis Form`: approved v1 metadata.

For both Terpenes names: **QBench metadata only — current revision authority supplied by user.** The controlling source remains the user-supplied `Terpene Analysis SOP v 1.4.docx`; its internal 1.3 header is a known typo. Neither attached DOCX was copied into the dated rescan or staged/committed by this scan.

Document Configuration exposes two disabled settings: attaching a document to emails and disabling Team-member acknowledgements. Approval workflows, review intervals, training behavior, template associations, and deeper field definitions were not exposed without entering document content or sensitive workflow surfaces.
