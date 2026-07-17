# Batch Publish gate

Status: exact design documented; not implemented because the target-selection
stop condition was reached first.

## Row identity

For candidate Publish row `r`, the controlled source is the single Instrument
Import row whose exact QBench Test ID equals `Publish!A{r}` and whose exact
source-row hash equals `Publish!AT{r}`. Row position alone is never identity.

The validation fields named `AF` and `AG` below are explicitly
`Instrument Import!AF{n}` and `Instrument Import!AG{n}`. They are not the
different Publish-tab confirmation fields at `Publish!AF{r}` and
`Publish!AG{r}`.

## Required gate

A row may enter the transfer set only when all conditions are true before any
destination write:

1. `Instrument Import!AF{n}` is exactly `Valid`.
2. `Instrument Import!AG{n}` is exactly `Import row valid`.
3. `Instrument Import!E{n}` and `Publish!A{r}` contain the same nonblank exact
   QBench Test ID.
4. The Test ID resolves to exactly one Test in the isolated Batch.
5. `Instrument Import!BE{n}` and `Publish!AT{r}` contain the same nonblank
   source-row hash.
6. All 23 Instrument Import analytes in `AH:BD` and all 23 Publish analytes in
   `D:Z` are native numeric values and match in controlled analyte order.
7. `Instrument Import!X{n}` is numeric `24`.
8. `Instrument Import!Y{n}` is numeric `34`.
9. `Instrument Import!Z{n}` is numeric `23`.
10. `Instrument Import!AA{n}` is numeric and retained as audit-only.
11. `Publish!AV{r}` is exact `TRUE`.
12. `Publish!AW{r}` is exact `Reviewed`.
13. `Publish!AX{r}` is exact `Valid`.
14. `Publish!AY{r}` is exact `Accepted`.
15. `Publish!AZ{r}`, `Publish!BA{r}`, and `Publish!BB{r}` are exact `TRUE`.
16. `Publish!BC{r}` is exact `TRUE` after the explicit authorization check.
17. Sample mass and final volume are positive native numeric values. DF is a
    positive native numeric value when `apply_in_qbench` is selected.
18. Unit is exact `ug/mL`; Unit Confirmed and Preparation Values Confirmed are
    exact `TRUE`.
19. Every required source metadata field `AH:AR` is nonblank.
20. The complete destination named-cell contract exists and every destination
    input is writable while every calculated/result cell remains read-only.

Parser-job `SUCCESS` is not part of this gate.

## Explicit reviewer authorization design

The Prompt 4/4.6C Batch Worksheet does not include a dedicated per-row reviewer
publish authorization. A Prompt 5-specific worksheet copy would need these
additional Publish fields, all outside parser-controlled columns:

| Proposed named range | Proposed range | Control |
|---|---|---|
| `terpenes_batch_publish_authorization` | `Publish!BE2:BE87` | Reviewer-controlled enum; default `Not Authorized` |
| `terpenes_batch_publish_authorized_by` | `Publish!BF2:BF87` | Reviewer identity; nonblank only for authorization |
| `terpenes_batch_publish_authorized_at` | `Publish!BG2:BG87` | Review timestamp |
| `terpenes_batch_publish_status` | `Publish!BH2:BH87` | Automation-owned status |
| `terpenes_batch_last_published_source_row_hash` | `Publish!BI2:BI87` | Automation-owned idempotency state |

Allowed authorization values would be:

- `Not Authorized` (default)
- `Authorized`
- `Reauthorization Required`

Normal operation requires a qualified QC reviewer to set `Authorized` only
after reviewing the import validation, analytical batch QC disposition, row
identity, counts, numeric values, and source traceability. The No-Code parser
must never write `BE:BI`.

`Publish!BC{r}` would also need to be revised in the isolated Prompt 5 copy so
it cannot evaluate to `TRUE` unless authorization is `Authorized` and reviewer
identity/time are present.

These proposed fields were not created because the native automation cannot
target exactly one Test or persist row-specific status safely.

## Excluded from transfer

- `Publish!AU{r}` Dimethylacetamide: gate/audit only.
- Peak Table values: gate/audit only.
- Compound/Peak/reportable counts: no corresponding approved Prompt 3 Test
  Worksheet named cells, so gate only.
- Instrument Import or Publish formula cells.
- calculated mg/g, calculated percent, qualifiers, report-display cells,
  specifications, totals, or final outcomes.
- any Terpenes Pass/Fail, label-claim conclusion, METRC outcome, or COA tile.
