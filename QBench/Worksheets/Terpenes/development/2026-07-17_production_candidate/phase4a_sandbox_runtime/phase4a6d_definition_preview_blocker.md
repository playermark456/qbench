# Phase 4A.6D definition-preview controlled stop

Date: 2026-07-21

The exact existing Dynamic Spreadsheet object was opened through the Sandbox Worksheets list. Visual verification established:

- object type: Dynamic Spreadsheet;
- object state: Active;
- Version 1 remains present and approved/active;
- user-created Version 2 remains present with actual status Draft;
- no Version 3 exists;
- Report, Data, and Specifications render;
- the V4 Key/Value Store association remains present.

Version 2 was selected and previewed read-only using the prior controlled Test only as the preview entity. The Specifications sheet rendered, but all displayed LOQ and MU result cells remained blank after an additional wait. In particular, the required Alpha-Pinene LOQ and MU cells were blank rather than 10 and 5.

Therefore:

- `version_2_binding_definition = blocked_preview_lookup_values_blank`
- `key_value_definition_preview = failed_blank_loq_mu`
- Version 2 was not approved or activated.
- No new Assay, Sample, or Test was created.
- The 43-field runtime vector was not entered.

Historical controlled-stop classification at that time: `test_v4_binding_fix_runtime_blocked_version_2_definition_preview_blank_loq_mu`

## Subsequent lifecycle correction

Later evidence established that the preview used a Test instantiated while Version 2 was still Draft. That prior Test correctly remained on Version 1 after Version 2 approval. A fresh user-created Test instantiated after approval resolved the direct LOQ and MU lookups.

- `prior_blank_lookup_conclusion = superseded_old_test_instantiated_before_version_2_approval`
- `definition_preview_as_runtime_gate = invalid_for_dynamic_key_value_resolution`
- `former_final_classification = superseded_by_fresh_version_2_runtime_evidence`

The historical observation remains preserved, but it is not the current runtime classification.
