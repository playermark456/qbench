# Test Transfer readiness

The local parser produces Batch Instrument Import landing rows only. It does not write Test Transfer, create tests, or invoke QBench.

- 15 validation-source reportable rows are deliberately `held_unmapped`; the Low/Medium/High labels are not accepted as QBench Test display IDs.
- 19 controls are classified and excluded from Test Transfer.
- A local ignored mapping CSV can resolve selected reportable rows by `labsolutions_sample_name` and/or `labsolutions_sample_id` to `qbench_test_display_id`; the two-record synthetic overlay test passed.
- Parser-produced audit fields, 23 analytes, source traceability, and deterministic keys are ready for the controlled Sandbox landing and subsequent user-authorized transfer workflow.
- Product matrix, QBench Sample ID, final volume, QBench dilution factor, analytical-value confirmation, and staff review remain outside the parser contract.

No Test Transfer row, QBench object, or Pass/Fail result was created during this local validation.
