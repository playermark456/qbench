from __future__ import annotations

import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "phase4a_sandbox_runtime"


def read_csv(name: str) -> list[dict[str, str]]:
    with (RUNTIME_DIR / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class Phase4A5RuntimeExpectationTests(unittest.TestCase):
    def test_43_field_vector_is_unchanged_and_typed(self) -> None:
        rows = read_csv("phase4a3_runtime_vector.csv")
        self.assertEqual(len(rows), 43)
        self.assertEqual([int(row["sequence"]) for row in rows], list(range(1, 44)))
        self.assertEqual(rows[4]["synthetic_value"], "")
        self.assertEqual(rows[4]["value_type"], "blank")
        self.assertEqual(rows[5]["synthetic_value"], "0")
        self.assertEqual(rows[5]["value_type"], "number")
        self.assertEqual(rows[8]["synthetic_value"], "-1.5")
        self.assertEqual(rows[8]["value_type"], "number")

    def test_direct_analyte_expectations_preserve_blank_zero_and_negative(self) -> None:
        rows = {row["case"]: row for row in read_csv("phase4a3_runtime_expected_vs_actual.csv")}
        self.assertEqual(rows["direct blank behavior"]["expected_display"], "blank")
        self.assertIn("raw remains blank", rows["direct blank behavior"]["expected_full_precision"])
        self.assertEqual(rows["direct zero behavior"]["expected_display"], "<LOQ")
        self.assertIn("remains 0", rows["direct zero behavior"]["expected_full_precision"])
        self.assertEqual(rows["direct negative behavior"]["expected_display"], "<LOQ; no negative potency")
        self.assertIn("remains -1.5", rows["direct negative behavior"]["expected_full_precision"])

    def test_component_preprocessing_contract_remains_distinct(self) -> None:
        rows = {row["case"]: row for row in read_csv("phase4a3_runtime_expected_vs_actual.csv")}
        self.assertEqual(rows["Ocimene preprocessing"]["expected_full_precision"], "3.25 + 9.75")
        self.assertEqual(rows["Nerolidol preprocessing"]["expected_full_precision"], "12.5 + 0")
        self.assertIn("negative component contributes zero", rows["Nerolidol preprocessing"]["note"])


if __name__ == "__main__":
    unittest.main()
