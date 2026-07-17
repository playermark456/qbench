# Sandbox cleanup plan

No cleanup was performed during the proof. Retain the isolated native objects
until Draft PR #13 review accepts the evidence and no further QBench support or
compatibility comparison is needed.

When cleanup is explicitly authorized, use the normal Sandbox UI and verify
each exact task-created name before changing anything:

1. Confirm the retained Test is `NOT STARTED`, has blank B2/B3, and has no
   analytical results or Pass/Fail artifact.
2. Remove only the fresh Test created from
   `SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_ASSAY`.
3. Remove only `SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_SAMPLE`.
4. Remove only `SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_ASSAY`.
5. Retire and then remove only the versions belonging to
   `SBX_ONLY_TERPENES_2026_07_17_NATIVE_TEST_WS_PROBE`, followed by the
   worksheet itself if QBench permits.
6. Do not modify or delete any pre-existing worksheet or any earlier Prompt 5B
   destination-proof object.
7. Preserve the raw local exports and tracked sanitized evidence after Sandbox
   object cleanup.

Stop if any displayed name, relationship, or state differs from this plan.
