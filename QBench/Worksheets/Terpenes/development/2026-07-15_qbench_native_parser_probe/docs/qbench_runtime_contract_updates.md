# Runtime contract updates

## Merged preflight evidence

- `qbench_runtime_contract_status = insufficient_for_prompt_4_6`
- `qbench_sandbox_probe_status = sufficient_to_begin_controlled_prompt_4_6_probe`

Official QBJS v2.7.0 documentation records two materially different Batch
worksheet behaviors: full worksheet replacement removes the safety boundary
needed here, while the patch method updates only included data and preserves
omitted worksheet data. Only the patch method may be investigated in this
probe. Spreadsheet named ranges, one- and two-dimensional arrays, numeric-cell
typing, noncontiguous blocks, request atomicity, partial writes, and rollback
remain Sandbox questions.

The current tenant evidence records the exact File Parser import URL for
`file_parser.js` 1.1.0. It records `qbjs.js` version 2.7.0 but does not record
the full current-tenant QBJS import URL. Stage 1 therefore imports only the
exact proven File Parser URL and makes no service call. Later patch probes are
locally testable libraries but are runtime-guarded; no QBJS URL is guessed.

Batch context is not yet known. The raw LabSolutions file contains no QBench
Batch ID, and no final parser may require, infer, log, or hardcode one.
