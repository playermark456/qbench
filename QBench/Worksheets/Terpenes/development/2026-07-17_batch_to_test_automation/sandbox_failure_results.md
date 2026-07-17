# Sandbox failure-test results

Prompt 5A qualification: the official `VLOOKUP({{test.id}}, ...)` pattern means
the original UI-only inspection did not settle per-Test source routing. The
separate one-field probe is classified `per_test_vlookup_error` because its
destination named cell did not persist. The eleven full-publisher failure cases
below remain unexecuted.

The automation was stopped before activation because the original UI-only
inspection did not prove selection of exactly one Test. The eleven requested
runtime cases were not executed; running a 43-field design without proven
cardinality and atomicity would itself violate the test contract.

| Case | Required safe result | Prompt 5 result |
|---:|---|---|
| 1. AF rejected | No Test write; rejected status | Not run |
| 2. AG `Analytical values incomplete` | No Test write; clear status | Not run |
| 3. AG `Peak Table row count required` | No Test write; clear status | Not run |
| 4. Publish authorization off | No Test write; `Not Authorized` | Not run |
| 5. Missing matching Test | No Test write; `Missing matching Test` | Not run; native action has no match check |
| 6. Multiple matching Tests | No Test write; `Multiple matching Tests` | Not run; native action has no cardinality check |
| 7. Nonnumeric analyte | No Test write; numeric validation status | Not run |
| 8. Missing source-row hash | No Test write; traceability status | Not run |
| 9. Duplicate execution, unchanged hash | No write; `Already Published - No Change` | Not run |
| 10. Changed hash after publish | No overwrite; reauthorization required | Not run |
| 11. Missing/renamed destination field | No partial write; destination-contract error | Not run |

## Capability failure that was tested

The task-created inactive automation's action editor was inspected. The only
relevant action was `Set value on all Test Worksheets within the Batch`.
Selecting copy mode exposed destination field, `Copy Value`, `From Worksheet`,
and source field controls, but no exact-Test-ID selector or cardinality guard.

Outcome: activation blocked; zero Test Worksheet writes.

## Partial-write boundary

The UI configures worksheet fields as separate action cases and exposed no
full-destination preflight or atomic multi-field transaction. Partial-write
behavior was not risked in the Sandbox. Because atomicity cannot be established
before writing, this independently satisfies a Prompt 5 stop condition.
