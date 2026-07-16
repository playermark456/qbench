# QBench Sandbox change log

| Stage | Authorization | QBench objects changed | Result |
|---|---|---|---|
| 0 | Initial Prompt 4.6 submission | None | Repository preparation only |
| 1 | `AUTHORIZE STAGE 1 — NO-WRITE QBENCH RUNTIME PREVIEW` | One controlled File Parser configuration exists; parser inactive, version `DRAFT` | Initial Preview failed safely with `UNEXPECTED_PARSE_ERROR`; corrected Preview observed `array_like`, completed 24/34/23/1 counts, reached `QB.success()`, and passed; no worksheet service or destination write |
| 2A | `AUTHORIZE STAGE 2A — READ-ONLY BATCH-CONTEXT PREVIEW` | Added Version 2 of the same controlled parser; inactive, `DRAFT` | Existing console contained two identical completed outputs; all five candidate Batch-context paths absent/`undefined`; `not_available_in_preview_runtime`; no Codex rerun, service call, or destination write |
| 2B | `AUTHORIZE STAGE 2B — TEMPORARY SANDBOX ATTACHMENT TRIGGER — BATCH: ZZZ_SANDBOX_ONLY_TERPENES_CONTEXT_PROBE_2026-07-16` | Added one dedicated Sandbox-only File Parser, exact Batch-attachment filename trigger, one approved/active-marked version, one controlled Batch attachment, and one File Parser History record; parser inactive after run | One matching attachment-trigger job recorded `SUCCESS`, but job history did not persist the safe console payload; Batch context remains unresolved; no worksheet service or worksheet/results destination write |
| 3 | Not received | None | Not run |
| 4 | Not received | None | Not run |
| 5 | Not received | None | Not run |
| 6 | Not received | None | Not run |
| 7 | Not received | None | Not run |

Stage 1 changed only the explicitly authorized inactive/DRAFT parser
configuration. It added no trigger or assay, activated nothing, imported no
worksheet, invoked no worksheet service, and modified no Batch, attachment,
File Parser Results destination, automation, key/value-store value, or
production object.

The initial failure is recorded as
`failed_safely_runtime_file_collection_compatibility`. The corrected
sanitized diagnostics confirmed an `array_like` runtime collection and the
corrected Preview passed. The specific collection constructor was not logged.
No cleanup action was authorized or performed in Stage 1.

Stage 2A added only a second inactive/DRAFT version of the existing controlled
parser. The existing Preview console was inspected without rerunning it. One
controlled file was selected; no trigger, assay, filename rule, activation,
worksheet import, service call, attachment upload, destination write, Batch
change, or production change occurred. The parser remained inactive and both
versions remained `DRAFT` at the end of Stage 2A.

Stage 2B created a separate parser named
`ZZZ_SANDBOX_ONLY_Terpenes_Attachment_Context_Probe_2026-07-16`, configured it
for Batch attachments whose filename exactly equals
`Output_redacted_fixture.txt`, submitted and approved its no-write version, set
that isolated version active, and temporarily activated the parser. One
controlled fixture was added to
`ZZZ_SANDBOX_ONLY_TERPENES_CONTEXT_PROBE_2026-07-16`. The matching history job
recorded `SUCCESS` and the attachment remains as evidence. The parser was then
deactivated. QBench offered only irreversible obsolescence for the version,
so that action was canceled; the approved version remains marked active within
the disabled parser. The stored trigger is inert while the parser is inactive.

No worksheet was imported, no assay or automation was changed, no worksheet
service was invoked, no worksheet or File Parser Results destination was
modified, and production was neither accessed nor changed. Internal parser,
Batch, attachment, and job identifiers are intentionally omitted. Stage 3 was
not started.
