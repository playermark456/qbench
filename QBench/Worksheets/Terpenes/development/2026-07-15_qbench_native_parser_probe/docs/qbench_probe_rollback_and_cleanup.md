# Rollback and cleanup plan

Stage 0 created no QBench object and requires no QBench rollback.

For later authorized stages:

1. Never delete evidence objects automatically.
2. Record the exact disposable Sandbox object name and type without committing
   internal IDs.
3. Keep draft parsers inactive unless a stage explicitly authorizes a tightly
   isolated temporary activation.
4. If activation is authorized, deactivate immediately after the controlled
   test and record both transitions.
5. Restore disposable worksheet baseline only with a previously proven narrow
   patch and only when the authorized stage allows it.
6. If failure behavior is partial, unclear, or not safely reversible, stop and
   request method-owner direction.
7. Await method-owner approval before deleting any parser draft, worksheet
   version, Batch, or attachment.

Production cleanup is never applicable because production activity is
permanently prohibited.

## Stage 2B cleanup record

- The temporary parser was deactivated after the single authorized attachment
  event.
- The approved version remains marked active within the disabled parser.
  QBench offered only irreversible obsolescence as the version-status action;
  it was canceled to preserve evidence.
- The exact-filename Batch-attachment trigger remains stored but is inert while
  the parser is inactive.
- `Output_redacted_fixture.txt` remains attached to
  `ZZZ_SANDBOX_ONLY_TERPENES_CONTEXT_PROBE_2026-07-16` as evidence.
- No parser, version, Batch, attachment, or history record was deleted.
- Any deletion or version obsolescence requires separate method-owner
  authorization.
