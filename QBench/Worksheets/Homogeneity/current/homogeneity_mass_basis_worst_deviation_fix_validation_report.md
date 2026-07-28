# Homogeneity Mass-Basis + Highest Absolute Deviation Validation Report

- Source JSON: `homogeneity_mass_basis_variance_precision_fix__2026-07-20.json`
- Corrected JSON: `homogeneity_mass_basis_worst_deviation_fix__2026-07-20.json`
- File size: `651340` bytes
- Overall result: `PASS`

## Regulatory clarification implemented

The summary boxes no longer select the highest numerical mass or cannabinoid result. They select the replicate with the greatest absolute deviation from the applicable claim/basis, while preserving the signed deviation for display.

Example: when one replicate is `+9.0%` and another is `-13.5%`, the selected summary replicate is the `-13.5%` replicate.

## Corrected summary logic

- `Data!B26`, `Data!B28`, and `Data!B30` select the signed deviation with the greatest absolute magnitude.
- `Data!B25`, `Data!B27`, and `Data!B29` return the mass or mg/unit value from the same replicate row.
- `Data!B31` applies the allowed variance threshold to the absolute magnitude of these selected worst deviations.
- COA summary labels now say `at Highest Deviation` rather than implying the highest numerical result.

## Validation checks

| Check | Result | Evidence |
|---|---|---|
| Paste root/config data layers match | `PASS` | `exact equality` |
| Data root/config data layers match | `PASS` | `exact equality` |
| COA root/config data layers match | `PASS` | `exact equality` |
| Data!B25 formula updated | `PASS` | `=IF(B26="","",INDEX(H12:H21,MATCH(B26,K12:K21,0)))` |
| Data!B26 formula updated | `PASS` | `=IF(COUNT(K12:K21)=0,"",IF(MAX(K12:K21)>=ABS(MIN(K12:K21)),MAX(K12:K21),MIN(K12:K21)))` |
| Data!B27 formula updated | `PASS` | `=IF(B28="","",INDEX(M12:M21,MATCH(B28,N12:N21,0)))` |
| Data!B28 formula updated | `PASS` | `=IF(COUNT(N12:N21)=0,"",IF(MAX(N12:N21)>=ABS(MIN(N12:N21)),MAX(N12:N21),MIN(N12:N21)))` |
| Data!B29 formula updated | `PASS` | `=IF($B$5="","",IF(B30="","",INDEX(P12:P21,MATCH(B30,Q12:Q21,0))))` |
| Data!B30 formula updated | `PASS` | `=IF($B$5="","",IF(COUNT(Q12:Q21)=0,"",IF(MAX(Q12:Q21)>=ABS(MIN(Q12:Q21)),MAX(Q12:Q21),MIN(Q12:Q21))))` |
| Data!B31 formula updated | `PASS` | `=IF(B42<>"READY","INCOMPLETE",IF(OR(AND(B26<>"",ABS(B26)>$B$9),AND(B28<>"",ABS(B28)>$B$9),AND($B$5<>"",B30<>"",ABS(B30)>$B$9)),"FAIL","PASS"))` |
| Worst-deviation selection preserves sign | `PASS` | `-0.135` |
| Worst-deviation pass/fail uses absolute magnitude | `PASS` | `abs(-0.135)=0.135 <= 0.15` |
| Worst-deviation fail example | `PASS` | `abs(-0.155)=0.155 > 0.15` |
| Summary values no longer select highest numerical values | `PASS` | Summary values use `INDEX/MATCH` against selected worst signed deviation. |
| Mass-basis formula retained M12 | `PASS` | `=IF(OR($C12="",I12="",E12=""),"",IFERROR(E12*I12,""))` |
| Variance remains decimal ratio N12 | `PASS` | `=IF(OR(M12="",L12="",L12=0),"",(M12-L12)/L12)` |
| COA variance remains percent formatted | `PASS` | `TEXT(...,"0.0%")` retained. |

## Sandbox test checklist

1. Import the corrected JSON into an inactive QBench Sandbox worksheet.
2. Confirm the mass-entry-basis behavior still works for individual-unit and full-container cases.
3. Enter two controlled deviations such as `+9.0%` and `-13.5%` and confirm the summary box uses the replicate associated with `-13.5%`.
4. Test a failing case such as `+9.0%` and `-15.5%` with a 15% tolerance; the overall result must be `FAIL`.
5. Confirm the COA summary displays the actual mass/mg-unit value from the selected worst-deviation replicate and displays the signed deviation.
6. Do not promote or activate until the COA preview and both JSON data layers are confirmed in Sandbox.
