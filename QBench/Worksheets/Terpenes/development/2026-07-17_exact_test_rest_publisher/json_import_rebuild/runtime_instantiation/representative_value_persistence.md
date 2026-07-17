# Representative value persistence

Status: **`runtime_representative_value_persistence=passed`**.

The five temporary values were entered and saved:

- D2 = numeric `1.01`
- O2 = numeric `12.12`
- Z2 = numeric `23.23`
- B12 = numeric `0.5`
- B30 = exact text `json_scalar_runtime_probe`

After leaving and reopening the Test from the Tests list, all five values
persisted exactly. B22 and B23 remained blank, and the other 38 destinations
remained blank.

Only the five temporary values were then cleared. After save, leave, and
reopen, all 43 destinations were blank again and the 40x26 grid and anchors
remained intact.
