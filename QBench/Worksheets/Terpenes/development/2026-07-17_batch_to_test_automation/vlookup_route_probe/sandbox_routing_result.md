# Sandbox routing result

Classification: **`per_test_vlookup_error`**

## Result table

| Synthetic QBench Test ID | Lookup value | Observed `route_probe` | Native numeric | Observed ID display | Sentinel | Other field changed |
|---:|---:|---|---|---:|---|---|
| 290 | 101 | blank | Not established | 290 | `UNCHANGED` | No |
| 291 | 202 | blank | Not established | 291 | `UNCHANGED` | No |
| 292 | 303 | blank | Not established | 292 | `UNCHANGED` | No |

The Batch instance contained each Test ID exactly once in `A2:A4`, with 101,
202, and 303 respectively in `B2:B4`. The saved action source was exactly
`=VLOOKUP({{test.id}}, A2:B4, 2)`.

The automation was activated, the Batch worksheet was saved once, one
task-created Automation History entry completed with `Success`, and the
automation was deactivated. Reopening all three Tests showed blank destination
cells, correct Test ID displays, and unchanged formula-owned sentinels.

## Why blank is not a routing failure

The exact post-run Test Worksheet **Export Spreadsheet** retains the three
worksheet labels, `${test.id}`, the `="UNCHANGED"` formula, and read-only
configuration for the ID and sentinel cells. Its `qb_config`, however, contains
only `kvstore_config`; there is no `named_cells` object. Reopening the worksheet
version configuration also showed an empty Named Cells section.

The action therefore referenced a destination system name that was absent from
the saved Test Worksheet version. A successful automation job with no value
written under that condition is a setup error, not evidence for any of the
other three routing classifications.

## Secondary probes

| Probe | Result | Reason |
|---|---|---|
| Zero match | Not run | Allowed only after distinct routing passed |
| Duplicate lookup ID | Not run | Allowed only after distinct routing passed |
| COUNTIF/IF guard | Not run | Allowed only after distinct routing passed |

## Safety

- The automation is inactive.
- The 43-field Terpenes mapping was not configured.
- No Test worksheet value was written.
- No Pass/Fail or compliance artifact was introduced.
- No report was created.
- No live QBench page was accessed.
