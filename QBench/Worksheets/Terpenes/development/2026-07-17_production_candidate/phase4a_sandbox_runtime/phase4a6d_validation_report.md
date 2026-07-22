# Phase 4A.6D validation report

Date: 2026-07-21

## Passed local gates

- Exact user export filename and SHA-256: passed
- Exported workbook contract: passed
- Correct Sandbox V4 store binding and embedded hierarchy: passed
- Semantic Version 2 round trip: `passed_with_expected_qbench_normalization`
- Deterministic binding-fix delta: `passed_exact_store_binding_only`
- Original V4 candidate unchanged: passed
- Formula / lookup counts: 309 / 44
- Writable destination / named-definition counts: 43 / 44
- `report_results`: `Report!A1:E23`
- Pass/Fail exclusion: passed

## Failed approval gate

- `key_value_definition_preview = failed_blank_loq_mu`
- Alpha-Pinene LOQ expected 10, actual blank
- Alpha-Pinene MU expected 5, actual blank

The prompt requires resolved LOQ and MU values before Version 2 approval. The run stopped without approval, activation, runtime-object creation, or analytical entry.

## Local validation

- Deterministic binding-fix validator: passed
- Version 2 semantic comparator: passed
- Production-candidate tests: 43/43 passed
- Phase 3 v2 scientific-logic, worksheet-schema, and historical-renderer package validator: passed
- Candidate SHA-256 preservation: passed
- JSON and CSV parse validation: passed
- Sanitized tracked-evidence security scans: passed
- Git whitespace checks: passed

Final classification: `test_v4_binding_fix_runtime_blocked_version_2_definition_preview_blank_loq_mu`
