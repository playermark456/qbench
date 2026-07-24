# QBench coded-parser write contract

Status: `passed_authoritative_operational_live_parser`

The upload artifact is a self-contained browser JavaScript source. It uses the
operational QBench wrapper imports, `QB.files`, `QB.console`,
`QB.progressBar`, `QB.success`, `QB.error`, and `QBBatchService`.

Before any update it validates one TXT or CSV source, complete record sections,
the controlled 24-ID / 23-channel contract, capacity, resolved Test linkage,
one-Batch selection, and the exact 57-column `Instrument Import` header.

It deterministically replaces parser-owned cells only in rows 2:201:

- `A:AE`
- `AH:BE`

Columns `AF:AG`, formulas, images, dollar references, the header, and all
other worksheets are retained from the fetched dynamic worksheet maps. After
all checks pass, it makes one `QBBatchService.update` call with worksheet
recalculation enabled. A failure calls `QB.error` without a retry write.

Reportable Samples use their LabSolutions Sample ID only when that visible Test
identifier resolves to the one selected Batch. Controls and unresolved Samples
remain unlinked. Logs contain counts only.
