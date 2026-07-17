# Prompt 5A official per-Test VLOOKUP routing probe

Date: 2026-07-17

Classification: **`per_test_vlookup_error`**

The isolated old-Sandbox probe was triggered exactly once and then immediately
deactivated. QBench Automation History recorded one successful job, but all
three destination cells remained blank. A post-run **Export Spreadsheet** of
the exact Test Worksheet version then showed that none of the three intended
named cells had persisted in `qb_config`. Because the automation destination
`route_probe` did not exist in the saved worksheet configuration, the no-write
result cannot establish whether `{{test.id}}` was evaluated once per Test.

No retry was performed. The prompt allowed the zero-match, duplicate-match,
and COUNTIF/IF probes only after distinct routing passed, so all three guard
probes remain not run.

## Official mechanism being tested

QBench's official
[Batch Spreadsheet Worksheets & Automations guide](https://junctionconcepts.zendesk.com/hc/en-us/articles/9705726121229-Batch-Spreadsheet-Worksheets-Automations)
documents the action `Set value on all Test Worksheets within the Batch`, the
per-Test `test` variable, and a Batch source expression using
`VLOOKUP({{test.id}}, ...)`. This corrects the original Prompt 5 UI-only
inference that the action necessarily broadcasts the same source value.

The exact old-Sandbox expression saved for the probe was:

```text
=VLOOKUP({{test.id}}, A2:B4, 2)
```

The documented mechanism remains plausible, but this run did not test it
validly because the destination named cell was absent from the saved Test
Worksheet version.

## Controlled observation

| Synthetic QBench Test ID | Batch probe value | `route_probe` before | `route_probe` after reopen | ID display after reopen | Sentinel after reopen |
|---:|---:|---|---|---:|---|
| 290 | 101 | blank | blank | 290 | `UNCHANGED` |
| 291 | 202 | blank | blank | 291 | `UNCHANGED` |
| 292 | 303 | blank | blank | 292 | `UNCHANGED` |

- No native numeric value was written, so numeric-cell behavior was not
  established.
- No other worksheet field changed.
- Exactly one task-created automation-history entry was observed; its status
  was `Success`.
- The automation's final state is inactive.
- No Terpenes Pass/Fail or compliance field was created.

## Name-length deviation

The requested 53-character automation name,
`SBX_ONLY_TERPENES_2026_07_17_VLOOKUP_ROUTE_AUTOMATION`, was rejected by the
old Sandbox with `A field's value is too long.` The accepted 47-character name
is `SBX_ONLY_TERPENES_2026_07_17_VLOOKUP_AUTOMATION`; the full requested name
was retained in its description.

## Evidence boundary

- `source/` contains the exact raw Batch and Test Worksheet **Export
  Spreadsheet** JSON files downloaded after the run.
- `named_cell_mapping.csv` compares intended mappings with the saved export.
- `sanitized_automation_configuration.json` records the exact trigger,
  condition, action, expression, and active window without credentials or
  session data.
- `routing_evidence.json` records the single-trigger observation and the
  classification decision.
- `sandbox_object_inventory.csv` lists every isolated object created.
- `sandbox_routing_result.md` provides the human-readable result record.

The synthetic Test IDs are included because they are the exact lookup keys
required to interpret this probe. No customer identifiers or unrelated
Sandbox IDs are included.

## Design consequence

The original Prompt 5 one-step 43-field automation remains blocked by atomic
preflight, cardinality, authorization, idempotency, and error-handling gaps.
Because per-Test VLOOKUP routing did not pass this validly controlled probe,
the current recommendation remains an exact-Test REST API publisher. A
two-phase native staging-and-commit design should be reconsidered only after a
fresh, separately approved routing probe starts from an exported worksheet
whose named cells are confirmed present before activation.

Live QBench was not accessed. Production was not changed. The 43-field mapping
was not configured.
