# Settings and additional configuration — partial production read-only capture

Safe General Settings labels and Boolean states, Customer Portal structure, one inactive Log Type, and an aggregate count of 1,097 Locations were recorded. Display sequence, section label, and same-label occurrence distinguish repeated controls without asserting stable setting IDs. Customer Portal text values, operational log counts, and all location detail were omitted.

Not opened because values could expose secrets or personal/configuration data:

- Email Settings
- Developer Settings
- Parameter Store

The Specification Module is enabled in General Settings, but no standalone Specifications/spec-group route was exposed in visible navigation. Specifications therefore remain `module_enabled_but_no_visible_route / unable_to_verify_read_only`.

Stability is limited to cross-phase anchors: active assay 13 with no worksheet/protocol, three Sample fields, and active email template 51 with no version and empty source. Multiple pull dates, 3/6/12-month interval representation, schedules, reminder timing, recipient roles, and record-vs-field-vs-step behavior remain unable to verify.

## Managed Interfaces

Sensitive integration configuration was encountered on an authenticated settings page. Details were intentionally omitted. Managed Interfaces remains incomplete pending separate administrative or vendor remediation.

```text
status = blocked_metadata_only
objects_counted = 4
details_retained = 0
secret_values_committed = 0
reason = sensitive_integration_configuration_encountered
rescan_required = only_after_separate_remediation_and_explicit_authorization
```
