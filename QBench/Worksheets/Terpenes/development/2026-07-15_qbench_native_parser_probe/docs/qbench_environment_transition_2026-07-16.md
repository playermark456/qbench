# Prompt 4.6 environment transition record

Date: 2026-07-16

## Environment policy

- `https://ait.qbench.net/` is the live QBench instance and is now
  read-only/reference-only for this work.
- All future writable QBench implementation and validation work moves to
  `https://ait-sandbox.qbench.net/`.
- No cleanup, deletion, obsolescence, deactivation, upload, attachment,
  Preview, activation, save, or other live QBench action is authorized by this
  transition record.
- The older Sandbox may not match the live tenant. No existing Sandbox object
  is an authoritative implementation source.
- GitHub-controlled worksheet candidates, parser code, mappings, and
  specifications remain the source of truth.

## Prompt 4.6 closure

Prompt 4.6 live probing is closed after Stage 2B with:

`batch_context_status = unresolved_console_output_not_persisted`

The Stage 3 scalar patch and every later write probe were not run against the
live tenant. No generated worksheet candidate was imported, no worksheet
version was saved or activated, no worksheet was attached to the disposable
Batch, no Preview was run for Stage 3, no worksheet service was invoked, and
no scalar or range cell value was written.

Before the freeze, pre-patch preparation created one inactive, unversioned
worksheet shell named
`ZZZ_SANDBOX_ONLY_Prompt_4_6_Runtime_Probe_2026-07-16`. The generated Probe
worksheet JSON was not uploaded into it, and its default blank configuration
was not saved as a version. This inert shell is retained in live QBench for
separate evidence review and cleanup; it is not an implementation source and
must not be modified during this task.

## Retained live evidence

- The Stage 1/2A parser remains inactive.
- The Stage 2B parser remains disabled.
- The approved Stage 2B version label remains preserved because the available
  obsolescence action was irreversible.
- The exact-filename trigger is inert because its parser is disabled.
- The controlled redacted attachment remains in the disposable live Batch.
- The inactive, unversioned Stage 3 preparation shell remains blank and inert.
- No worksheet configuration, version, Batch association, cell, worksheet
  service, or File Parser Results destination write occurred.

## Next task

The next task is **Prompt 4.6B: Full QBench Sandbox implementation and
validation** at `https://ait-sandbox.qbench.net/`, under its own authorization
and with repository-controlled artifacts as the implementation baseline.
Prompt 5 has not started and is not authorized by this transition.
