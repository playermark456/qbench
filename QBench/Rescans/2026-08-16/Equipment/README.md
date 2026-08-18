# Equipment configuration — production read-only capture

The complete list reconciles to 103 unique equipment IDs: 97 In Service, 3 Retired, 2 Backup Equipment Only, and 1 Out of Service. Safe retained fields are ID, internal code, equipment type, literal status, an explicit In-Service status interpretation, site-level location, visible schedule names, and resource-group IDs. A separate active-state field was not exposed and is recorded as `not_exposed`.

Equipment Configurations exposes 38 active schedule definitions: 24 daily, 5 as needed, 3 annually, 3 monthly, 1 every two years, 1 bi-weekly, and 1 weekly. Four schedules require a record attachment.

Equipment 107 displayed the undelimited schedule text `No Maintenance Required Cold Storage Temperature | -70C`. It appears to combine a sentinel and a defined schedule, but the read-only evidence cannot prove the split. The raw display is preserved and this equipment-to-schedule linkage remains unresolved rather than being normalized by inference.

The Phase 3 field inventory exposes 19 Equipment field definitions, including calibration and maintenance structure. It also contains duplicate-seeming hidden fields `Date Disposed` and `Disposal Date`; behavior was not tested. Required-assignment and availability semantics were not exposed.

Records, issues, usage, comments, attachments, certificates, service reports, serials, model/manufacturer details, suppliers, detailed locations, dates, tags, and staff identities were omitted. No equipment detail tab other than Details was opened.
