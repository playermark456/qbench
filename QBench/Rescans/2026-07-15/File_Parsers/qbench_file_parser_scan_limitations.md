# QBench File Parser Prompt 4.6A scan limitations

Controlled scan date: 2026-07-15

- `qbench_runtime_contract_status = insufficient_for_prompt_4_6`
- `qbench_sandbox_probe_status = sufficient_to_begin_controlled_prompt_4_6_probe`

## Evidence limits

- No failed result was available in the complete visible 39-job history.
- No numeric-write evidence was visible.
- No parsed-output preview or worksheet-write summary was visible.
- No transaction, atomicity, rollback, or partial-write behavior was proven.
- No underlying parser-result file or destination worksheet was opened or
  downloaded.
- No QBench change occurred.

Result-history success is supporting evidence only. It does not prove an
undocumented JavaScript entry point, signature, named-range payload, write API,
transaction guarantee, or numeric-write behavior.

## Worksheet API limits

Official QBJS v2.7.0 documentation states that `updateWorksheet` completely
replaces Batch worksheet data. It is unsuitable for the proposed Terpenes
writer because it could replace unrelated worksheet data, formulas, tabs, or
metadata.

Official QBJS v2.7.0 documentation states that `patchWorksheet` updates only
fields included in `data` and does not remove omitted data. It is the preferred
candidate for controlled Sandbox investigation, but no claim is made that it
supports Spreadsheet Worksheet named ranges, arrays, noncontiguous ranges,
numeric cell typing, atomicity, rollback, or dry-run behavior.

## Batch-context limit

The raw LabSolutions file will not contain a QBench Batch ID. A future parser
must obtain the current named Batch's internal numeric ID from supported runtime
or attachment context. It must not infer the Batch from customer/sample data,
hardcode an ID, or require the raw file to contain one. The supported runtime
property remains a Sandbox discovery question.

## Scope controls

No parser was created, edited, saved, activated, previewed, or run. No
production action is authorized. Prompt 4.6 and Prompt 5 have not started.
