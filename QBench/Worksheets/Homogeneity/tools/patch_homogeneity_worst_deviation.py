#!/usr/bin/env python3
"""Patch a mass-basis-corrected Homogeneity JSON so summary and pass/fail use greatest absolute deviation."""
import copy, json, re, sys

def col_index(col):
    n = 0
    for ch in col:
        n = n * 26 + ord(ch) - 64
    return n - 1

def set_cell(data, address, value):
    m = re.fullmatch(r"([A-Z]+)(\d+)", address)
    r, c = int(m.group(2)) - 1, col_index(m.group(1))
    while len(data) <= r:
        data.append([])
    while len(data[r]) <= c:
        data[r].append(None)
    data[r][c] = value

def patch(doc):
    doc = copy.deepcopy(doc)
    updates = {
        "Data": {
            "A25": '=IF($D$10="Full container mass/volume","Container Mass/Volume at Highest Absolute Deviation g","Unit/Serving Mass at Highest Absolute Deviation g")',
            "B25": '=IF(B26="","",INDEX(H12:H21,MATCH(B26,K12:K21,0)))',
            "A26": "Mass Variance at Highest Absolute Deviation",
            "B26": '=IF(COUNT(K12:K21)=0,"",IF(MAX(K12:K21)>=ABS(MIN(K12:K21)),MAX(K12:K21),MIN(K12:K21)))',
            "A27": '=IF($B$3="","Cannabinoid 1 mg/unit at Highest Absolute Deviation",$B$3&" mg/unit at Highest Absolute Deviation")',
            "B27": '=IF(B28="","",INDEX(M12:M21,MATCH(B28,N12:N21,0)))',
            "A28": '=IF($B$3="","Cannabinoid 1 Variance at Highest Absolute Deviation",$B$3&" Variance at Highest Absolute Deviation")',
            "B28": '=IF(COUNT(N12:N21)=0,"",IF(MAX(N12:N21)>=ABS(MIN(N12:N21)),MAX(N12:N21),MIN(N12:N21)))',
            "A29": '=IF($B$5="","Cannabinoid 2 mg/unit at Highest Absolute Deviation",$B$5&" mg/unit at Highest Absolute Deviation")',
            "B29": '=IF($B$5="","",IF(B30="","",INDEX(P12:P21,MATCH(B30,Q12:Q21,0))))',
            "A30": '=IF($B$5="","Cannabinoid 2 Variance at Highest Absolute Deviation",$B$5&" Variance at Highest Absolute Deviation")',
            "B30": '=IF($B$5="","",IF(COUNT(Q12:Q21)=0,"",IF(MAX(Q12:Q21)>=ABS(MIN(Q12:Q21)),MAX(Q12:Q21),MIN(Q12:Q21))))',
            "B31": '=IF(B42<>"READY","INCOMPLETE",IF(OR(AND(B26<>"",ABS(B26)>$B$9),AND(B28<>"",ABS(B28)>$B$9),AND($B$5<>"",B30<>"",ABS(B30)>$B$9)),"FAIL","PASS"))',
            "C42": "pass_fail remains INCOMPLETE until all required checks pass. Final PASS/FAIL is based on the greatest absolute signed deviation for mass and each selected cannabinoid.",
        },
        "COA": {
            "A6": '=IF(DATA!D10="Full container mass/volume","Container Mass/Volume at Highest Deviation g","Unit/Serving Mass at Highest Deviation g")',
            "C6": "Mass Variance at Highest Deviation",
            "A7": '=IF(DATA!B3="","",DATA!B3&" mg/unit at Highest Deviation")',
            "C7": '=IF(DATA!B3="","",DATA!B3&" Variance at Highest Deviation")',
            "A8": '=IF(DATA!B5="","",DATA!B5&" mg/unit at Highest Deviation")',
            "C8": '=IF(DATA!B5="","",DATA!B5&" Variance at Highest Deviation")',
        },
    }
    for sheet, cells in updates.items():
        for addr, value in cells.items():
            set_cell(doc["data"][sheet], addr, value)
        ws = next(w for w in doc["config"]["worksheets"] if w["worksheetName"] == sheet)
        for addr, value in cells.items():
            set_cell(ws["data"], addr, value)
    labels = {
        "highest_reported_unit_mass_g": "Entered Mass at Highest Absolute Deviation g",
        "highest_mass_label_variance": "Mass Variance at Highest Absolute Deviation",
        "highest_reported_cannabinoid_1_mg_container": "Cannabinoid 1 mg/unit at Highest Absolute Deviation",
        "highest_cannabinoid_1_label_variance": "Cannabinoid 1 Variance at Highest Absolute Deviation",
        "highest_reported_cannabinoid_2_mg_container": "Cannabinoid 2 mg/unit at Highest Absolute Deviation",
        "highest_cannabinoid_2_label_variance": "Cannabinoid 2 Variance at Highest Absolute Deviation",
    }
    named = doc.get("qb_config", {}).get("named_cells", {})
    for key, label in labels.items():
        if key in named:
            named[key]["display_name"] = label
    return doc

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: patch_homogeneity_worst_deviation.py input.json output.json")
    source = json.load(open(sys.argv[1], encoding="utf-8"))
    json.dump(patch(source), open(sys.argv[2], "w", encoding="utf-8"), indent=2, ensure_ascii=False)
