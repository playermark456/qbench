#!/usr/bin/env python3
"""Build sanitized local Phase 3 Terpenes Test and Batch worksheet candidates."""

from __future__ import annotations

import copy
import csv
import importlib.util
import json
import re
import uuid
from pathlib import Path
from typing import Any


PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[4]
OUTPUT_DIR = PACKAGE_DIR / "production_candidates"

TEST_TARGET = "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_TEST_WS"
TEST_VERSION = "Terpenes Production Test Worksheet v1"
BATCH_TARGET = "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS"
BATCH_VERSION = "Terpenes Production Batch Worksheet v1"

TEST_OUTPUT = OUTPUT_DIR / f"{TEST_TARGET}__v1.json"
BATCH_OUTPUT = OUTPUT_DIR / f"{BATCH_TARGET}__v1.json"

TEST_BUILDER_PATH = (
    REPO_ROOT
    / "QBench/Worksheets/Terpenes/development/2026-07-14_test_worksheet_candidate/scripts/build_terpenes_test_worksheet.py"
)
BATCH_BUILDER_PATH = (
    REPO_ROOT
    / "QBench/Worksheets/Terpenes/development/2026-07-14_batch_worksheet_candidate/scripts/build_terpenes_batch_worksheet.py"
)
SCALAR_NAMED_CELL_SOURCE = (
    REPO_ROOT
    / "QBench/Worksheets/Terpenes/development/2026-07-17_exact_test_rest_publisher/json_import_rebuild/"
    "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE.json"
)
METRC_MAPPING_PATH = PACKAGE_DIR / "metrc_terpenes_analyte_mapping.csv"

UUID_RE = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}"
)

INTERNAL_CHANNELS = [
    "alpha-Pinene",
    "Camphene",
    "beta-Myrcene",
    "(-)-beta-Pinene",
    "delta-3-Carene",
    "alpha-Terpinene",
    "Ocimene 1",
    "D-Limonene",
    "p-Cymene",
    "Ocimene 2",
    "Eucalyptol",
    "Gamma terpinene",
    "Terpinolene",
    "Linalool",
    "(-)-Isopulegol",
    "Geraniol",
    "beta-Caryophyllene",
    "alpha-Humulene",
    "Nerolidol 1",
    "Nerolidol 2",
    "(-)-Guaiol",
    "Caryophyllene oxide",
    "(-)-alpha-Bisabolol",
]

REPORTABLE_ORDER = [
    "Alpha-Bisabolol",
    "Alpha-Humulene",
    "Alpha-Pinene",
    "Alpha-Terpinene",
    "Beta-Caryophyllene",
    "Beta-Myrcene",
    "Beta-Pinene",
    "Camphene",
    "Caryophyllene Oxide",
    "Delta-3 Carene",
    "Eucalyptol",
    "Gamma-Terpinene",
    "Geraniol",
    "Guaiol",
    "Isopulegol",
    "Limonene",
    "Linalool",
    "Nerolidol",
    "Ocimene",
    "P-Isopropyltoluene (P-Cymene)",
    "Terpinolene",
]


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load builder: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def col_letter(index: int) -> str:
    label = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        label = chr(65 + remainder) + label
    return label


def cell_ref(row: int, col: int) -> str:
    return f"{col_letter(col)}{row}"


def blank_grid(rows: int, cols: int) -> list[list[Any]]:
    return [["" for _ in range(cols)] for _ in range(rows)]


def collect_uuids(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            found.update(UUID_RE.findall(str(key)))
            found.update(collect_uuids(item))
    elif isinstance(value, list):
        for item in value:
            found.update(collect_uuids(item))
    elif isinstance(value, str):
        found.update(UUID_RE.findall(value))
    return {item.lower() for item in found}


def freshen_uuids(value: Any, target: str) -> Any:
    namespace = uuid.uuid5(uuid.NAMESPACE_URL, f"qbench-local-phase3:{target}")
    mapping: dict[str, str] = {}

    def replacement(match: re.Match[str]) -> str:
        old = match.group(0).lower()
        if old not in mapping:
            mapping[old] = str(uuid.uuid5(namespace, old))
        return mapping[old]

    def walk(item: Any) -> Any:
        if isinstance(item, dict):
            return {UUID_RE.sub(replacement, str(key)): walk(value) for key, value in item.items()}
        if isinstance(item, list):
            return [walk(value) for value in item]
        if isinstance(item, str):
            return UUID_RE.sub(replacement, item)
        return item

    return walk(value)


def build_cells(
    helper: Any,
    data: list[list[Any]],
    widths: list[int],
    *,
    editable: set[str] | None = None,
    reserve: set[str] | None = None,
) -> dict[str, dict[str, Any]]:
    editable = editable or set()
    reserve = reserve or set()
    cells: dict[str, dict[str, Any]] = {}
    for row in range(1, len(data) + 1):
        for col in range(1, len(widths) + 1):
            ref = cell_ref(row, col)
            value = data[row - 1][col - 1]
            if value in ("", None) and ref not in editable and ref not in reserve:
                continue
            helper.set_cell_metadata(cells, row, col, readonly=ref not in editable, widths=widths)
    return cells


def style_range(helper: Any, style: dict[str, int], row: int, start: int, end: int, style_id: int) -> None:
    helper.style_range(style, row, start, end, style_id)


def load_reportable_mapping() -> dict[str, list[dict[str, str]]]:
    with METRC_MAPPING_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    result: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if row["internal_status"] == "audit_only":
            continue
        result.setdefault(row["reportable_measurand"], []).append(row)
    if sorted(result) != sorted(REPORTABLE_ORDER):
        raise AssertionError("Metrc mapping does not contain the exact 21 reportable measurands")
    return result


def test_data_tab(
    helper: Any,
    *,
    target_name: str = TEST_TARGET,
    version_name: str = TEST_VERSION,
) -> tuple[list[list[Any]], list[int], dict[str, int], dict[str, dict[str, Any]]]:
    rows, cols = 40, 26
    widths = [195, 180, 250] + [120] * 23
    data = blank_grid(rows, cols)
    data[0][0:3] = [version_name, target_name, "Final sample Conc.: ug/g; dilution already applied"]
    data[0][3:26] = INTERNAL_CHANNELS
    data[1][0:3] = [
        "${test.get_display_id()}",
        "${test.sample.get_display_id()}",
        "${test.sample.product_matrix}",
    ]
    data[2][0:3] = [
        "Raw Compound Results(Ch1) > Conc.",
        "Preserved unchanged",
        "Calculated results are formula-owned on Specifications",
    ]

    data[9][0:3] = ["Preparation and compatibility inputs", "Value", "Audit/compatibility only; not applied to result"]
    prep = [
        (12, "Sample Mass (g)", "Compatibility destination; not used in ug/g conversion"),
        (13, "Final Volume (mL)", "Compatibility destination; not used in ug/g conversion"),
        (14, "DF", "Audit-only value; QBench does not apply dilution"),
        (15, "DF Application Mode", "Must document already_applied_by_labsolutions"),
        (16, "LabSolutions Conc. Unit", "Must be ug/g"),
        (17, "Unit Confirmed", "Controlled confirmation"),
        (18, "Preparation Values Confirmed", "Controlled confirmation"),
    ]
    for row, label, note in prep:
        data[row - 1][0] = label
        data[row - 1][2] = note

    data[20][0:3] = ["Controlled disposition", "Value", "Staff-controlled quantitative workflow only"]
    data[21][0:3] = ["Batch QC Disposition", "", "Accepted / Hold / Rejected"]
    data[22][0:3] = ["Publish Ready", "", "Manual authorization gate; no automatic publication"]

    data[26][0:3] = ["Source and audit metadata", "Value", "Excluded from reportable results"]
    audit_labels = [
        "Source Batch ID",
        "Source Instrument File",
        "Source File Hash",
        "Source Data File",
        "Source Method File",
        "Source Sequence File",
        "Parser Version",
        "Imported At",
        "Instrument Name",
        "Detector ID",
        "Detector Name",
    ]
    for row, label in enumerate(audit_labels, start=28):
        data[row - 1][0] = label
    data[39][0] = "End of worksheet"

    destination_refs = {f"{col_letter(col)}2" for col in range(4, 27)}
    destination_refs.update({f"B{row}" for row in range(12, 19)})
    destination_refs.update({"B22", "B23"})
    destination_refs.update({f"B{row}" for row in range(28, 39)})

    style: dict[str, int] = {}
    style_range(helper, style, 1, 1, 3, 23)
    style_range(helper, style, 1, 4, 26, 7)
    style_range(helper, style, 2, 1, 3, 4)
    style_range(helper, style, 2, 4, 26, 9)
    style_range(helper, style, 3, 1, 3, 4)
    for row in (10, 21, 27, 40):
        style_range(helper, style, row, 1, 3, 7)
    for row in list(range(12, 19)) + [22, 23] + list(range(28, 39)):
        style[cell_ref(row, 1)] = 2
        style[cell_ref(row, 2)] = 9
        style[cell_ref(row, 3)] = 1

    cells = build_cells(helper, data, widths, editable=destination_refs, reserve=destination_refs)
    return data, widths, style, cells


def kv_formula(row: int, selector: str, analyte_expression: str) -> str:
    gate = 'OR($U$2="SANDBOX_CONFIGURATION_REQUIRED",$U$4="SANDBOX_CONFIGURATION_REQUIRED")'
    return (
        f'=IF({gate},"",GET_KVSTORE_VALUE($U$2,$U$3,{analyte_expression},$U$4,$U$5,"{selector}"))'
    )


def test_specifications_tab(
    helper: Any,
    mapping: dict[str, list[dict[str, str]]],
) -> tuple[list[list[Any]], list[int], dict[str, int], dict[str, dict[str, Any]]]:
    rows, cols = 23, 21
    widths = [190, 220, 110, 105, 105, 105, 105, 125, 110, 105, 105, 105, 115, 115, 105, 105, 260, 245, 25, 210, 220]
    data = blank_grid(rows, cols)
    data[0][0:18] = [
        "Analyte",
        "Instrument source",
        "Result (ug/g)",
        "Result (mg/g)",
        "Result (%)",
        "LOQ (ug/g)",
        "MU (%)",
        "Qualifier / status",
        "Display mg/g",
        "Display %",
        "Display LOQ mg/g",
        "Display MU %",
        "Component 1 used ug/g",
        "Component 2 used ug/g",
        "Component 1 MU %",
        "Component 2 MU %",
        "Metrc percent field",
        "Metrc mg/g field",
    ]
    data[0][19:21] = ["Sandbox Key/Value binding", "Configured value"]
    data[1][19:21] = ["Store binding", "SANDBOX_CONFIGURATION_REQUIRED"]
    data[2][19:21] = ["Assay key", "Terpenes"]
    data[3][19:21] = ["Matrix/product type", "SANDBOX_CONFIGURATION_REQUIRED"]
    data[4][19:21] = ["Result unit", "ug/g"]
    data[5][19:21] = ["Selectors", "LOQ / MU%"]

    source_col = {name: col_letter(4 + index) for index, name in enumerate(INTERNAL_CHANNELS)}

    for offset, analyte in enumerate(REPORTABLE_ORDER, start=2):
        row = offset
        entries = mapping[analyte]
        data[row - 1][0] = analyte
        data[row - 1][16] = entries[0]["metrc_percent_field"]
        data[row - 1][17] = entries[0]["metrc_mg_g_field"]

        if len(entries) == 1:
            instrument = entries[0]["instrument_channel"]
            col = source_col[instrument]
            data[row - 1][1] = instrument
            data[row - 1][2] = f'=IF(DATA!{col}2="","",IF(ISNUMBER(DATA!{col}2)<>TRUE,"",DATA!{col}2))'
            data[row - 1][6] = kv_formula(row, "MU%", f"A{row}")
        else:
            instruments = [entry["instrument_channel"] for entry in entries]
            instruments.sort(key=lambda value: int(value.rsplit(" ", 1)[1]))
            first, second = instruments
            first_col, second_col = source_col[first], source_col[second]
            data[row - 1][1] = f"{first} + {second}"
            data[row - 1][12] = (
                f'=IF(OR(DATA!{first_col}2="",ISNUMBER(DATA!{first_col}2)<>TRUE,DATA!{first_col}2<=0),0,DATA!{first_col}2)'
            )
            data[row - 1][13] = (
                f'=IF(OR(DATA!{second_col}2="",ISNUMBER(DATA!{second_col}2)<>TRUE,DATA!{second_col}2<=0),0,DATA!{second_col}2)'
            )
            data[row - 1][2] = f"=M{row}+N{row}"
            data[row - 1][14] = f'=IF(M{row}=0,"",{kv_formula(row, "MU%", json.dumps(first))[1:]})'
            data[row - 1][15] = f'=IF(N{row}=0,"",{kv_formula(row, "MU%", json.dumps(second))[1:]})'
            data[row - 1][6] = (
                f'=IF(C{row}<=0,"",IF(AND(M{row}>0,N{row}=0),'
                f'IF(ISNUMBER(O{row}),O{row},"MU UNRESOLVED"),'
                f'IF(AND(M{row}=0,N{row}>0),IF(ISNUMBER(P{row}),P{row},"MU UNRESOLVED"),'
                f'IF(OR(ISNUMBER(O{row})<>TRUE,ISNUMBER(P{row})<>TRUE),"MU UNRESOLVED",'
                f'100*SQRT((M{row}*O{row}/100)^2+(N{row}*P{row}/100)^2)/C{row}))))'
            )

        data[row - 1][3] = f'=IF(ISNUMBER(C{row}),C{row}/1000,"")'
        data[row - 1][4] = f'=IF(ISNUMBER(C{row}),C{row}/10000,"")'
        data[row - 1][5] = kv_formula(row, "LOQ", f"A{row}")
        data[row - 1][7] = (
            f'=IF(C{row}="","",IF(C{row}<0,"<LOQ",IF(ISNUMBER(F{row})<>TRUE,"LOQ UNRESOLVED",'
            f'IF(C{row}<F{row},"<LOQ",""))))'
        )
        data[row - 1][8] = (
            f'=IF(H{row}="<LOQ","<LOQ",IF(H{row}<>"","",IF(ISNUMBER(D{row}),ROUND(D{row},3),"")))'
        )
        data[row - 1][9] = (
            f'=IF(H{row}="<LOQ","<LOQ",IF(H{row}<>"","",IF(ISNUMBER(E{row}),ROUND(E{row},3),"")))'
        )
        data[row - 1][10] = f'=IF(ISNUMBER(F{row}),ROUND(F{row}/1000,3),"")'
        data[row - 1][11] = f'=IF(OR(H{row}<>"",ISNUMBER(G{row})<>TRUE),"",ROUND(G{row},3))'

    total_row = 23
    data[total_row - 1][0] = "Total Terpenes"
    data[total_row - 1][1] = "21 reportable measurands strictly above matrix LOQ"
    contributions = [
        f'IF(AND(ISNUMBER(C{row}),ISNUMBER(F{row}),C{row}>F{row}),C{row},0)'
        for row in range(2, 23)
    ]
    data[total_row - 1][2] = f'=SUM({",".join(contributions)})'
    data[total_row - 1][3] = f"=C{total_row}/1000"
    data[total_row - 1][4] = f"=C{total_row}/10000"
    data[total_row - 1][8] = f"=ROUND(D{total_row},3)"
    data[total_row - 1][9] = f"=ROUND(E{total_row},3)"
    data[total_row - 1][16] = "Total Terpenes (%) Additional (Raw Plant Material & Concentrate/Extract)"
    data[total_row - 1][17] = "Total Terpenes (mg/g) Additional (Infused Products)"

    style: dict[str, int] = {}
    style_range(helper, style, 1, 1, 18, 7)
    style_range(helper, style, 1, 20, 21, 7)
    for row in range(2, 24):
        style[cell_ref(row, 1)] = 17 if row == 23 else 2
        for col in range(2, 19):
            style[cell_ref(row, col)] = 4 if row == 23 else 1
    for row in range(2, 7):
        style[cell_ref(row, 20)] = 2
        style[cell_ref(row, 21)] = 4

    cells = build_cells(helper, data, widths)
    return data, widths, style, cells


def test_report_tab(
    helper: Any,
    *,
    preserve_historical_cell_extent: bool = False,
) -> tuple[list[list[Any]], list[int], dict[str, int], dict[str, dict[str, Any]]]:
    widths = [210, 120, 120, 110, 105]
    data = blank_grid(23, 5)
    data[0] = ["Analyte", "Result (mg/g)", "Result (%)", "LOQ", "MU (%)"]
    for row, analyte in enumerate(REPORTABLE_ORDER, start=2):
        data[row - 1][0] = analyte
        data[row - 1][1] = f"=SPECIFICATIONS!I{row}"
        data[row - 1][2] = f"=SPECIFICATIONS!J{row}"
        data[row - 1][3] = f"=SPECIFICATIONS!K{row}"
        data[row - 1][4] = f"=SPECIFICATIONS!L{row}"
    data[22][0] = "Total Terpenes"
    data[22][1] = "=SPECIFICATIONS!I23"
    data[22][2] = "=SPECIFICATIONS!J23"

    style: dict[str, int] = {}
    style_range(helper, style, 1, 1, 5, 23)
    for row in range(2, 24):
        for col in range(1, 6):
            style[cell_ref(row, col)] = 17 if row == 23 else 5
    reserve = (
        {cell_ref(row, col) for row in range(1, 24) for col in range(1, 6)}
        if preserve_historical_cell_extent
        else None
    )
    cells = build_cells(helper, data, widths, reserve=reserve)
    return data, widths, style, cells


def exact_test_named_cells() -> dict[str, Any]:
    source = load_json(SCALAR_NAMED_CELL_SOURCE)["qb_config"]["named_cells"]
    if len(source) != 43:
        raise AssertionError("Expected exactly 43 proven scalar named cells")
    result: dict[str, Any] = {}
    for name, definition in source.items():
        item = copy.deepcopy(definition)
        if "!" not in item["cell"]:
            item["cell"] = f'Data!{item["cell"]}'
        result[name] = item
    result["report_results"] = {"cell": "Report!A1:E23", "display_name": "", "export": True}
    return result


def build_test_candidate(
    test_builder: Any,
    *,
    target_name: str = TEST_TARGET,
    version_name: str = TEST_VERSION,
    preserve_historical_identity: bool = False,
) -> dict[str, Any]:
    candidate = test_builder.build_candidate()
    mapping = load_reportable_mapping()
    data_args = test_data_tab(
        test_builder,
        target_name=target_name,
        version_name=version_name,
    )
    spec_args = test_specifications_tab(test_builder, mapping)
    report_args = test_report_tab(
        test_builder,
        preserve_historical_cell_extent=preserve_historical_identity,
    )

    for name, args in [("Report", report_args), ("Data", data_args), ("Specifications", spec_args)]:
        data, widths, style, cells = args
        test_builder.update_worksheet(
            candidate,
            name,
            data,
            widths,
            style,
            cells,
            table_width=sum(widths),
            table_height=len(data) * 27,
        )

    candidate["qb_config"]["named_cells"] = exact_test_named_cells()
    candidate["qb_config"]["kvstore_config"] = {}
    candidate["qb_config"]["portal_export_range"] = ""
    candidate["qb_config"]["report_export_range"] = ""
    candidate["data"] = {
        worksheet["worksheetName"]: copy.deepcopy(worksheet["data"])
        for worksheet in candidate["config"]["worksheets"]
    }
    if not preserve_historical_identity:
        for worksheet in candidate["config"]["worksheets"]:
            worksheet["csvFileName"] = f'{target_name}__{worksheet["worksheetName"]}.csv'

    source_uuids = collect_uuids(candidate)
    if preserve_historical_identity:
        if collect_uuids(candidate) != source_uuids:
            raise AssertionError("Test candidate changed the proven historical UUID set")
    else:
        candidate = freshen_uuids(candidate, target_name)
        if source_uuids & collect_uuids(candidate):
            raise AssertionError("Test candidate retained source UUIDs")
    return candidate


def replace_strings(value: Any, replacements: list[tuple[str, str]]) -> Any:
    if isinstance(value, dict):
        return {key: replace_strings(item, replacements) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_strings(item, replacements) for item in value]
    if isinstance(value, str):
        for old, new in replacements:
            value = value.replace(old, new)
        return value
    return value


def worksheet_by_name(candidate: dict[str, Any], name: str) -> dict[str, Any]:
    return next(item for item in candidate["config"]["worksheets"] if item["worksheetName"] == name)


def patch_batch_dilution_contract(candidate: dict[str, Any]) -> dict[str, Any]:
    instrument = worksheet_by_name(candidate, "Instrument Import")
    transfer = worksheet_by_name(candidate, "Test Transfer")

    for row in range(2, 202):
        message = instrument["data"][row - 1][32]
        message = message.replace(
            f'AND(K{row}<>"",K{row}<>"already_applied_by_labsolutions",K{row}<>"apply_in_qbench")',
            f'AND(OR(D{row}="Unknown",D{row}="Dilution"),K{row}<>"already_applied_by_labsolutions")',
        )
        message = message.replace(f'AND(K{row}="apply_in_qbench",ISNUMBER(J{row})<>TRUE)', "FALSE")
        message = message.replace(f'AND(K{row}="apply_in_qbench",ISNUMBER(J{row}),J{row}<=0)', "FALSE")
        instrument["data"][row - 1][32] = message

    for row in range(2, 88):
        prereq = transfer["data"][row - 1][53]
        prereq = prereq.replace(
            f'OR(AD{row}="already_applied_by_labsolutions",AND(AD{row}="apply_in_qbench",ISNUMBER(AC{row}),AC{row}>0))',
            f'AD{row}="already_applied_by_labsolutions"',
        )
        transfer["data"][row - 1][53] = prereq

        message = transfer["data"][row - 1][55]
        message = message.replace(
            f'AND(AD{row}<>"already_applied_by_labsolutions",AD{row}<>"apply_in_qbench")',
            f'AD{row}<>"already_applied_by_labsolutions"',
        )
        message = message.replace(
            f'AND(AD{row}="apply_in_qbench",OR(ISNUMBER(AC{row})<>TRUE,AC{row}<=0))',
            "FALSE",
        )
        transfer["data"][row - 1][55] = message

    candidate = replace_strings(candidate, [("apply_in_qbench", "already_applied_by_labsolutions")])
    # replace_strings returns a new object; mutate the caller's object in place.
    original_keys = list(candidate.keys())
    if not original_keys:
        raise AssertionError("Unexpected empty Batch candidate")
    return candidate


def build_batch_candidate(
    batch_builder: Any,
    *,
    target_name: str = BATCH_TARGET,
    version_name: str = BATCH_VERSION,
    preserve_historical_identity: bool = False,
) -> dict[str, Any]:
    candidate = batch_builder.build_candidate()
    source_uuids = collect_uuids(candidate)

    candidate = replace_strings(
        candidate,
        [
            ("'QC Review'!", "'Batch Review'!"),
            ("QC Review!", "Batch Review!"),
            ("'Publish'!", "'Test Transfer'!"),
            ("Publish!", "Test Transfer!"),
            ("ug/mL", "ug/g"),
        ],
    )
    for worksheet in candidate["config"]["worksheets"]:
        if worksheet["worksheetName"] == "QC Review":
            worksheet["worksheetName"] = "Batch Review"
        elif worksheet["worksheetName"] == "Publish":
            worksheet["worksheetName"] = "Test Transfer"

    candidate["data"] = {
        ("Batch Review" if name == "QC Review" else "Test Transfer" if name == "Publish" else name): data
        for name, data in candidate["data"].items()
    }
    candidate = patch_batch_dilution_contract(candidate)
    candidate = replace_strings(candidate, [("apply_in_qbench", "already_applied_by_labsolutions")])

    review = worksheet_by_name(candidate, "Batch Review")
    review["data"][1][1] = "2026-07-20-phase3"
    review["data"][1][2] = "Phase 3 local candidate; quantitative-only"
    run_setup = worksheet_by_name(candidate, "Run Setup")
    run_setup["data"][18][0:3] = [
        "candidate_version",
        version_name,
        "Local candidate; Sandbox runtime validation pending",
    ]

    if not preserve_historical_identity:
        for worksheet in candidate["config"]["worksheets"]:
            worksheet["csvFileName"] = f'{target_name}__{worksheet["worksheetName"]}.csv'
    candidate["data"] = {
        worksheet["worksheetName"]: copy.deepcopy(worksheet["data"])
        for worksheet in candidate["config"]["worksheets"]
    }

    if "apply_in_qbench" in json.dumps(candidate, ensure_ascii=False):
        raise AssertionError("Batch candidate still permits QBench dilution application")
    if preserve_historical_identity:
        if collect_uuids(candidate) != source_uuids:
            raise AssertionError("Batch candidate changed the proven historical UUID set")
    else:
        candidate = freshen_uuids(candidate, target_name)
        if source_uuids & collect_uuids(candidate):
            raise AssertionError("Batch candidate retained source UUIDs")
    return candidate


def main() -> None:
    test_builder = load_module("phase3_test_builder_base", TEST_BUILDER_PATH)
    batch_builder = load_module("phase3_batch_builder_base", BATCH_BUILDER_PATH)
    test_candidate = build_test_candidate(test_builder)
    batch_candidate = build_batch_candidate(batch_builder)
    dump_json(TEST_OUTPUT, test_candidate)
    dump_json(BATCH_OUTPUT, batch_candidate)
    print(f"built_test={TEST_OUTPUT.relative_to(REPO_ROOT).as_posix()}")
    print(f"built_batch={BATCH_OUTPUT.relative_to(REPO_ROOT).as_posix()}")


if __name__ == "__main__":
    main()
