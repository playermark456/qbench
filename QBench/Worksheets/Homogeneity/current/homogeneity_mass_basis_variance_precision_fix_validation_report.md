# Homogeneity Mass-Basis, Variance, and Report Precision Validation

## Files
- Base JSON: `/mnt/data/spreadsheet-export-template (30).json`
- Corrected JSON: `/mnt/data/homogeneity_mass_basis_variance_precision_fix__2026-07-20.json`
- Corrected JSON size: `650370` bytes
- Overall result: `PASS`

## Confirmed Root Cause
The prior worksheet always divided entered replicate mass by Servings Per Container. In spreadsheet-4835.xlsx, the entered masses are already individual gummy/unit masses, so the report was exactly tenfold low for a 10-serving package. The cannabinoid variance formula itself was structurally correct, but it was calculated from the tenfold-low mg/unit result.

## Corrected Logic
- `Individual unit/serving mass`: `mg/unit = mg/g x entered individual unit/serving mass`
- `Full container mass/volume`: `mg/unit = mg/g x entered total container mass/volume / servings per container`
- Cannabinoid label variance remains `(actual mg/unit - label mg/unit) / label mg/unit` and is stored as a decimal ratio.
- Data variance cells are formatted as `0.0%`; formulas are not multiplied by 100.
- COA mg/unit remains formatted to two decimal places.

## Formula Evidence
- `Data!D10`: `=PASTE!G5`
- `Data!I12`: `=IF(H12="","",IF(LOWER(TRIM($D$10))="individual unit/serving mass",H12,IF(LOWER(TRIM($D$10))="full container mass/volume",IF(OR($B$43="",VALUE($B$43)<=0),"",H12/VALUE($B$43)),"")))`
- `Data!M12`: `=IF(OR($C12="",I12="",E12=""),"",IFERROR(E12*I12,""))`
- `Data!N12`: `=IF(OR(M12="",L12="",L12=0),"",(M12-L12)/L12)`
- `Data!P12`: `=IF($B$5="","",IF(OR($C12="",I12="",G12=""),"",IFERROR(G12*I12,"")))`
- `Data!Q12`: `=IF($B$5="","",IF(OR(P12="",O12="",O12=0),"",(P12-O12)/O12))`
- `Data!B48`: `=IF(LOWER(TRIM($D$10))="full container mass/volume",IF(B43="","INCOMPLETE",IFERROR(IF(VALUE(B43)>0,"PASS","INCOMPLETE"),"INCOMPLETE")),IF(LOWER(TRIM($D$10))="individual unit/serving mass","NOT REQUIRED","INCOMPLETE"))`
- `Data!B50`: `=IF(OR($D$10="Individual unit/serving mass",$D$10="Full container mass/volume"),"PASS","INCOMPLETE")`
- `COA!B10`: `=IF(DATA!D10="Full container mass/volume","Container Mass/Volume g","Unit/Serving Mass g")`
- `COA!D11`: `=IF(DATA!M12="","",TEXT(DATA!M12,"0.00"))`
- `COA!E11`: `=IF(DATA!N12="","",TEXT(DATA!N12,"0.0%"))`

## Real-World spreadsheet-4835 Results
| Replicate | Corrected Total THC mg/unit | Corrected variance vs 5 mg/unit |
|---:|---:|---:|
| 1 | 5.47081 | 9.4% |
| 2 | 5.24004 | 4.8% |
| 3 | 5.66486 | 13.3% |
| 4 | 5.67502 | 13.5% |
| 5 | 5.65774 | 13.2% |
| 6 | 5.37660 | 7.5% |
| 7 | 5.60546 | 12.1% |
| 8 | 5.40043 | 8.0% |
| 9 | 5.42321 | 8.5% |
| 10 | 5.36110 | 7.2% |

## Validation Checks
| Check | Result | Evidence |
|---|---|---|
| Mass Entry Basis default | `PASS` | `Individual unit/serving mass` |
| Mass Entry Basis named cell | `PASS` | `{'cell': 'Data!D10', 'display_name': 'Mass Entry Basis', 'export': True}` |
| Mass Entry Basis check named cell | `PASS` | `{'cell': 'Data!B50', 'display_name': 'Mass Entry Basis Check', 'export': True}` |
| Individual mass-per-unit formula | `PASS` | `=IF(H12="","",IF(LOWER(TRIM($D$10))="individual unit/serving mass",H12,IF(LOWER(TRIM($D$10))="full container mass/volume",IF(OR($B$43="",VALUE($B$43)<=0),"",H12/VALUE($B$43)),"")))` |
| Target 1 mg/unit uses mass-per-unit helper | `PASS` | `=IF(OR($C12="",I12="",E12=""),"",IFERROR(E12*I12,""))` |
| Target 2 mg/unit uses mass-per-unit helper | `PASS` | `=IF($B$5="","",IF(OR($C12="",I12="",G12=""),"",IFERROR(G12*I12,"")))` |
| Variance remains decimal ratio | `PASS` | `=IF(OR(M12="",L12="",L12=0),"",(M12-L12)/L12)` |
| Data Target 1 variance percent style | `PASS` | `{'readonly': True, 'style': 57, 'type': 'text', 'width': 16}` |
| Data Target 2 variance percent style | `PASS` | `{'readonly': True, 'style': 57, 'type': 'text', 'width': 16}` |
| COA mg/unit two decimals | `PASS` | `=IF(DATA!M12="","",TEXT(DATA!M12,"0.00"))` |
| COA variance one decimal percent | `PASS` | `=IF(DATA!N12="","",TEXT(DATA!N12,"0.0%"))` |
| Servings conditionally required | `PASS` | `=IF(LOWER(TRIM($D$10))="full container mass/volume",IF(B43="","INCOMPLETE",IFERROR(IF(VALUE(B43)>0,"PASS","INCOMPLETE"),"INCOMPLETE")),IF(LOWER(TRIM($D$10))="individual unit/serving mass","NOT REQUIRED","INCOMPLETE"))` |
| Validation includes mass basis | `PASS` | `=IF(AND(B34=10,B36="PASS",B37="PASS",OR(B38="PASS",B38="REVIEWER_CONFIRMED"),B39="PASS",B40="PASS",B41="PASS",OR(B48="PASS",B48="NOT REQUIRED"),B50="PASS"),"READY","INCOMPLETE")` |
| Paste root/config match | `PASS` | `exact match` |
| Data root/config match | `PASS` | `exact match` |
| COA root/config match | `PASS` | `exact match` |
| Real-world replicate 1 mg/unit | `PASS` | `5.47081` |
| Real-world replicate 1 label variance | `PASS` | `0.094162 (9.4%)` |
| No duplicate named-cell targets | `PASS` | `{}` |

## Sandbox Test Required
1. Import the corrected JSON into an inactive QBench Sandbox worksheet.
2. For gummy/piece testing, leave Mass Entry Basis as Individual unit/serving mass.
3. Confirm replicate 1 from spreadsheet-4835 produces 5.47 mg/unit and 9.4% label variance.
4. Confirm the Data tab shows variance as percentages rather than raw decimals.
5. Confirm COA mg/unit values show two decimal places and are not tenfold low.
6. Separately test Full container mass/volume with a multi-serving beverage and confirm division by Servings Per Container occurs exactly once.

Production QBench was not accessed or modified.
