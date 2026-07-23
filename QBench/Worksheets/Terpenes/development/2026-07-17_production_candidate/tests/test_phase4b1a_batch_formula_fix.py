#!/usr/bin/env python3
"""Focused, deterministic checks for the Batch v2 formula reconciliation."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import build_phase3_candidates as phase3  # noqa: E402
import build_phase3_candidates_v2 as phase3_v2  # noqa: E402


SOURCE_PATH = ROOT / "production_candidates" / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v2.json"
CORRECTED_PATH = (
    ROOT
    / "production_candidates"
    / "SBX_ONLY_TERPENES_PRODUCTION_CANDIDATE_BATCH_WS__v2_formula_fix.json"
)
SOURCE_SHA256 = "a4b92be3590e57f3456e12c65219cb6a5cb340248c6f3e50c6d3f36f56777837"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def worksheet(candidate: dict[str, Any], name: str) -> dict[str, Any]:
    return next(item for item in candidate["config"]["worksheets"] if item["worksheetName"] == name)


def cell_name(row: int, col: int) -> str:
    result = ""
    while col:
        col, remainder = divmod(col - 1, 26)
        result = chr(65 + remainder) + result
    return f"{result}{row}"


def all_formulas(value: Any) -> Iterator[str]:
    if isinstance(value, dict):
        for item in value.values():
            yield from all_formulas(item)
    elif isinstance(value, list):
        for item in value:
            yield from all_formulas(item)
    elif isinstance(value, str) and value.startswith("="):
        yield value


def approved_bd_formula(source_formula: str) -> str:
    old = "IF('Batch Review'!$B$18<>TRUE,\"Batch release review required\",\"Ready for transfer\")"
    new = (
        "IF(AND('Run Setup'!$B$24=TRUE,'Batch Review'!$B$9=TRUE,"
        "'Batch Review'!$B$11=TRUE,'Batch Review'!$B$12=TRUE,"
        "'Batch Review'!$B$14>0,'Batch Review'!$B$15=\"Accepted\"),"
        "\"Ready for transfer\",\"Batch release review required\")"
    )
    if old not in source_formula:
        raise AssertionError("Approved Batch Review B18 dependency was not found")
    return source_formula.replace(old, new)


def has_cycle(graph: dict[str, set[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        result = any(visit(child) for child in graph.get(node, set()))
        visiting.remove(node)
        visited.add(node)
        return result

    return any(visit(node) for node in graph)


class BatchFormulaFixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source_hash_before = sha256(SOURCE_PATH)
        if cls.source_hash_before != SOURCE_SHA256:
            raise AssertionError("Authoritative historical Batch v2 candidate hash differs")
        cls.source = load_json(SOURCE_PATH)
        _, cls.corrected = phase3_v2.build_candidates()

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temporary:
            cls.temporary_path = Path(temporary.name)
        phase3.dump_json(cls.temporary_path, cls.corrected)
        cls.corrected_from_json = load_json(cls.temporary_path)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary_path.unlink(missing_ok=True)

    def expected_changed_cells(self) -> set[tuple[str, str]]:
        return {
            *( ("Batch Review", f"B{row}") for row in range(12, 15) ),
            *( ("Test Transfer", f"BD{row}") for row in range(2, 88) ),
        }

    def changed_cells(self, container: str) -> list[tuple[str, str, Any, Any]]:
        changes: list[tuple[str, str, Any, Any]] = []
        for source_sheet in self.source["config"]["worksheets"]:
            name = source_sheet["worksheetName"]
            source_data = source_sheet["data"] if container == "embedded" else self.source["data"][name]
            candidate_sheet = worksheet(self.corrected, name)
            corrected_data = candidate_sheet["data"] if container == "embedded" else self.corrected["data"][name]
            self.assertEqual(len(source_data), len(corrected_data), name)
            for row, (source_row, corrected_row) in enumerate(zip(source_data, corrected_data), start=1):
                self.assertEqual(len(source_row), len(corrected_row), f"{name}!{row}")
                for col, (before, after) in enumerate(zip(source_row, corrected_row), start=1):
                    if before != after:
                        changes.append((name, cell_name(row, col), before, after))
        return changes

    def test_01_json_and_strict_changed_cell_validation(self) -> None:
        self.assertEqual(self.source_hash_before, SOURCE_SHA256)
        self.assertEqual(sha256(SOURCE_PATH), SOURCE_SHA256)
        self.assertEqual(self.corrected, self.corrected_from_json)
        self.assertTrue(CORRECTED_PATH.exists())
        self.assertEqual(load_json(CORRECTED_PATH), self.corrected)

        expected = self.expected_changed_cells()
        embedded = self.changed_cells("embedded")
        mirrored = self.changed_cells("mirrored")
        self.assertEqual({(name, cell) for name, cell, _, _ in embedded}, expected)
        self.assertEqual({(name, cell) for name, cell, _, _ in mirrored}, expected)
        self.assertTrue(all(isinstance(before, str) and before.startswith("=") for _, _, before, _ in embedded))
        self.assertTrue(all(isinstance(after, str) and after.startswith("=") for _, _, _, after in embedded))
        self.assertEqual(len(embedded), len(mirrored))

        for item in self.corrected["config"]["worksheets"]:
            self.assertEqual(item["data"], self.corrected["data"][item["worksheetName"]])

        review = worksheet(self.corrected, "Batch Review")["data"]
        self.assertEqual(review[11][1], "=IF(AND($B$14>0,COUNTIF('Test Transfer'!BB2:BB87,FALSE)=0),TRUE,FALSE)")
        self.assertEqual(review[12][1], "=COUNTIF('Test Transfer'!BD2:BD87,\"Duplicate Test ID\")")
        self.assertEqual(review[13][1], "=COUNTIF('Test Transfer'!A2:A87,\"<>\")")
        transfer = worksheet(self.corrected, "Test Transfer")["data"]
        source_transfer = worksheet(self.source, "Test Transfer")["data"]
        for row in range(2, 88):
            self.assertEqual(transfer[row - 1][55], approved_bd_formula(source_transfer[row - 1][55]))

    def test_02_cross_sheet_reference_validation(self) -> None:
        self.assertEqual(
            [item["worksheetName"] for item in self.corrected["config"]["worksheets"]],
            ["Run Setup", "Instrument Import", "Batch Review", "Test Transfer"],
        )
        self.assertEqual(
            {item["worksheetName"]: (len(item["data"]), len(item["data"][0])) for item in self.corrected["config"]["worksheets"]},
            {
                "Run Setup": (25, 3),
                "Instrument Import": (201, 57),
                "Batch Review": (45, 24),
                "Test Transfer": (87, 56),
            },
        )
        names = {item["worksheetName"] for item in self.corrected["config"]["worksheets"]}
        formulas = list(all_formulas(self.corrected))
        self.assertFalse(any("TESTTRANSFER!" in formula for formula in formulas))
        self.assertFalse(any(re.search(r"(?<!')Test Transfer!", formula) for formula in formulas))
        self.assertTrue(
            any("'Test Transfer'!" in formula for row in worksheet(self.corrected, "Batch Review")["data"][11:14] for formula in row)
        )
        for formula in formulas:
            for match in re.finditer(r"(?:'([^']+)'|([A-Za-z_][A-Za-z0-9_ ]*))!", formula):
                self.assertIn((match.group(1) or match.group(2)).strip(), names, formula)

    def test_03_af_ag_and_parser_range_preservation(self) -> None:
        source_import = worksheet(self.source, "Instrument Import")
        corrected_import = worksheet(self.corrected, "Instrument Import")
        self.assertEqual(
            [row[31:33] for row in source_import["data"]],
            [row[31:33] for row in corrected_import["data"]],
        )
        self.assertEqual(source_import["cells"], corrected_import["cells"])
        for row in range(2, 202):
            self.assertTrue(corrected_import["cells"][f"AF{row}"]["readonly"])
            self.assertTrue(corrected_import["cells"][f"AG{row}"]["readonly"])
            self.assertTrue(str(corrected_import["data"][row - 1][31]).startswith("="))
            self.assertTrue(str(corrected_import["data"][row - 1][32]).startswith("="))
            for column in list(range(1, 32)) + list(range(34, 58)):
                self.assertFalse(corrected_import["cells"][cell_name(row, column)]["readonly"])

    def test_04_dependency_graph_is_acyclic(self) -> None:
        review = worksheet(self.corrected, "Batch Review")["data"]
        transfer = worksheet(self.corrected, "Test Transfer")["data"]
        self.assertIn("'Test Transfer'!BD2:BD87", review[12][1])
        self.assertIn('"Duplicate Test ID"', transfer[1][55])
        self.assertNotIn("'Batch Review'!$B$18", transfer[1][55])
        self.assertIn("$B$13=0", review[17][1])
        self.assertIn("Duplicate Test ID", review[18][1])

        graph = {
            "B12": {"B14", "BB"},
            "B13": {"BD"},
            "B14": {"A"},
            "B18": {"B12", "B13", "B14", "B9", "B11", "B15", "RunSetupB24"},
            "B19": {"B12", "B13", "B14", "B9", "B11", "B15", "RunSetupB24"},
            "BB": {"A"},
            "BC": {"BB", "B18"},
            "BD": {"A", "B9", "B11", "B12", "B14", "B15", "RunSetupB24"},
        }
        self.assertNotIn("B18", graph["BD"])
        self.assertFalse(has_cycle(graph))

    def test_05_pre_and_post_transfer_local_evaluation(self) -> None:
        def evaluate(rows: list[dict[str, Any]]) -> dict[str, Any]:
            duplicate_count = sum(
                1 for row in rows if sum(other["test_id"] == row["test_id"] for other in rows) > 1
            )
            az = [len(row["analytical_values"]) == 23 for row in rows]
            ba = [row["source_traceability_complete"] for row in rows]
            bb = [
                all(
                    (
                        az[index],
                        row["sample_mass_present"],
                        row["final_volume_present"],
                        row["preparation_complete"],
                        row["audit_complete"],
                        ba[index],
                        row["batch_qc"] == "Accepted",
                    )
                )
                for index, row in enumerate(rows)
            ]
            b14 = len(rows)
            b12 = b14 > 0 and not any(value is False for value in bb)
            run_setup_complete = False
            b18 = run_setup_complete and b12 and duplicate_count == 0 and b14 > 0
            b19 = "Run setup incomplete" if not run_setup_complete else "Ready for transfer"
            bd = [
                "Analytical values incomplete"
                if not az[index]
                else "Batch release review required"
                if not b18
                else "Ready for transfer"
                for index, _ in enumerate(rows)
            ]
            return {
                "az": az,
                "ba": ba,
                "bb": bb,
                "b12": b12,
                "b13": duplicate_count,
                "b14": b14,
                "b18": b18,
                "b19": b19,
                "bc": ["TRUE" if ready and b18 else "FALSE" for ready in bb],
                "bd": bd,
                "formula_error_count": 0,
            }

        pre_transfer_rows = [
            {
                "test_id": "SANITIZED-001",
                "analytical_values": [],
                "sample_mass_present": False,
                "final_volume_present": False,
                "preparation_complete": False,
                "audit_complete": False,
                "source_traceability_complete": False,
                "batch_qc": "Hold",
            },
            {
                "test_id": "SANITIZED-002",
                "analytical_values": [],
                "sample_mass_present": False,
                "final_volume_present": False,
                "preparation_complete": False,
                "audit_complete": False,
                "source_traceability_complete": False,
                "batch_qc": "Hold",
            },
        ]
        pre_transfer = evaluate(pre_transfer_rows)
        self.assertEqual((pre_transfer["az"], pre_transfer["ba"], pre_transfer["bb"]), ([False, False], [False, False], [False, False]))
        self.assertEqual((pre_transfer["b12"], pre_transfer["b13"], pre_transfer["b14"]), (False, 0, 2))
        self.assertEqual((pre_transfer["b18"], pre_transfer["b19"]), (False, "Run setup incomplete"))
        self.assertEqual(pre_transfer["bc"], ["FALSE", "FALSE"])
        self.assertEqual(pre_transfer["bd"], ["Analytical values incomplete", "Analytical values incomplete"])
        self.assertEqual(pre_transfer["formula_error_count"], 0)

        post_transfer_rows = [
            {
                "test_id": "SANITIZED-001",
                "analytical_values": list(range(1, 24)),
                "sample_mass_present": True,
                "final_volume_present": True,
                "preparation_complete": True,
                "audit_complete": True,
                "source_traceability_complete": True,
                "batch_qc": "Accepted",
            },
            {
                "test_id": "SANITIZED-002",
                "analytical_values": list(range(101, 124)),
                "sample_mass_present": True,
                "final_volume_present": True,
                "preparation_complete": True,
                "audit_complete": True,
                "source_traceability_complete": True,
                "batch_qc": "Accepted",
            },
        ]
        post_transfer = evaluate(post_transfer_rows)
        self.assertEqual((post_transfer["az"], post_transfer["ba"], post_transfer["bb"]), ([True, True], [True, True], [True, True]))
        self.assertEqual((post_transfer["b12"], post_transfer["b13"], post_transfer["b14"]), (True, 0, 2))
        self.assertEqual((post_transfer["b18"], post_transfer["b19"]), (False, "Run setup incomplete"))
        self.assertEqual(post_transfer["bc"], ["FALSE", "FALSE"])
        self.assertEqual(post_transfer["bd"], ["Batch release review required", "Batch release review required"])
        self.assertEqual(post_transfer["formula_error_count"], 0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
