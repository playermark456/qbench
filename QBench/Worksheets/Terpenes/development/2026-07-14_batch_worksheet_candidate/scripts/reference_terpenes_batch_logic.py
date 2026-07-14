#!/usr/bin/env python3
"""Reference-only Terpenes batch worksheet logic for tests and Sandbox comparison.

These functions do not execute inside QBench. They mirror the intended static
worksheet behavior so unit tests can exercise boundary cases and gate order.
"""
from __future__ import annotations

from collections import Counter
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable


SAMPLE_TYPES = {
    "Calibration Standard",
    "Initial CCV",
    "Continuing CCV",
    "Blank",
    "LOQ Check",
    "Matrix Spike",
    "Duplicate",
    "Unknown",
    "Dilution",
    "Other QC",
}
PUBLISH_SAMPLE_TYPES = {"Unknown", "Dilution"}
DF_APPLICATION_MODES = {"already_applied_by_labsolutions", "apply_in_qbench"}
BATCH_QC_DISPOSITIONS = {"Accepted", "Hold", "Rejected"}
MANUAL_INTEGRATION_VALUES = {"No", "Yes"}
INTEGRATION_REVIEW_VALUES = {"Not Reviewed", "Reviewed", "Review Required"}
IMPORT_STATUS_VALUES = {"Valid", "Review Required", "Rejected"}
INTERNAL_QC_EVALUATION_VALUES = {
    "within_criteria",
    "outside_criteria",
    "decision_required",
    "not_evaluated",
    "not_applicable",
    "review_required",
}

SOURCE_FIELDS = [
    "source_batch_id",
    "source_instrument_file",
    "source_file_hash",
    "source_data_file",
    "source_method_file",
    "source_sequence_file",
    "parser_version",
    "imported_at",
    "instrument_name",
    "detector_id",
    "detector_name",
    "source_injection_id",
    "source_row_hash",
]


def is_strict_number(value: Any) -> bool:
    """Return true only for real numeric values, not numeric-looking text."""
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float, Decimal)):
        return True
    return False


def as_decimal(value: Any) -> Decimal:
    if not is_strict_number(value):
        raise ValueError(f"Not a strict numeric value: {value!r}")
    try:
        return Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"Not a decimal value: {value!r}") from exc


def positive_number(value: Any) -> bool:
    return is_strict_number(value) and as_decimal(value) > 0


def all_strict_numbers(values: Iterable[Any], expected_count: int) -> bool:
    values = list(values)
    return len(values) == expected_count and all(is_strict_number(value) for value in values)


def duplicate_test_ids(test_ids: Iterable[str]) -> set[str]:
    normalized = [test_id for test_id in test_ids if test_id]
    counts = Counter(normalized)
    return {test_id for test_id, count in counts.items() if count > 1}


def import_row_message(row: dict[str, Any]) -> str:
    if not row.get("import_row_id"):
        return ""
    sample_type = row.get("sample_type", "")
    analytes = row.get("analyte_values", [])
    if sample_type not in SAMPLE_TYPES:
        return "Sample type required"
    if sample_type in PUBLISH_SAMPLE_TYPES and not row.get("qbench_test_id"):
        return "QBench Test ID required"
    if row.get("sample_mass_g") not in ("", None) and not positive_number(row.get("sample_mass_g")):
        return "Sample mass required"
    if row.get("final_volume_ml") not in ("", None) and not positive_number(row.get("final_volume_ml")):
        return "Final volume required"
    if row.get("df_application_mode") not in ("", None) and row.get("df_application_mode") not in DF_APPLICATION_MODES:
        return "Dilution mode required"
    if row.get("df_application_mode") == "apply_in_qbench" and not positive_number(row.get("qbench_df")):
        return "Dilution factor required"
    if row.get("compound_result_row_count") != 24:
        return "Compound Results row count required"
    if row.get("reportable_compound_row_count") != 23:
        return "Reportable analyte count required"
    if sample_type in PUBLISH_SAMPLE_TYPES and not all_strict_numbers(analytes, 23):
        return "Analytical values incomplete"
    if not is_strict_number(row.get("dimethylacetamide_conc")):
        return "Dimethylacetamide audit value required"
    if row.get("manual_integration") not in MANUAL_INTEGRATION_VALUES:
        return "Manual integration value required"
    if row.get("manual_integration") == "Yes" and not row.get("integration_reason"):
        return "Integration reason required"
    if row.get("integration_review_status") not in INTEGRATION_REVIEW_VALUES:
        return "Integration review required"
    if (
        row.get("manual_integration") == "Yes" or (row.get("unknown_peak_count") or 0) > 0
    ) and row.get("integration_review_status") != "Reviewed":
        return "Integration review required"
    for field in [
        "source_instrument_file",
        "source_file_hash",
        "source_data_file",
        "source_method_file",
        "source_sequence_file",
        "instrument_name",
        "detector_id",
        "detector_name",
        "parser_version",
        "source_row_hash",
    ]:
        if not row.get(field):
            return "Source traceability incomplete"
    return "Import row valid"


def import_validation_status(row: dict[str, Any]) -> str:
    message = import_row_message(row)
    if not message:
        return ""
    rejected_messages = {
        "Sample type required",
        "QBench Test ID required",
        "Compound Results row count required",
        "Reportable analyte count required",
        "Analytical values incomplete",
        "Dimethylacetamide audit value required",
    }
    if message in rejected_messages:
        return "Rejected"
    if message == "Import row valid":
        return "Valid"
    return "Review Required"


def source_audit_complete(row: dict[str, Any]) -> bool:
    return (
        all(row.get(field) not in ("", None) for field in SOURCE_FIELDS)
        and is_strict_number(row.get("dimethylacetamide_conc"))
        and row.get("compound_results_complete") is True
        and row.get("integration_review_status") == "Reviewed"
        and row.get("import_validation_status") == "Valid"
    )


def analytical_values_complete(values: Iterable[Any]) -> bool:
    return all_strict_numbers(values, 23)


def publish_row_message(row: dict[str, Any], duplicate_ids: set[str]) -> str:
    if not row.get("qbench_test_id"):
        return ""
    if row["qbench_test_id"] in duplicate_ids:
        return "Duplicate Test ID"
    if not analytical_values_complete(row.get("analyte_values", [])):
        return "Analytical values incomplete"
    if not positive_number(row.get("sample_mass_g")):
        return "Sample mass required"
    if not positive_number(row.get("final_volume_ml")):
        return "Final volume required"
    mode = row.get("df_application_mode")
    if mode not in DF_APPLICATION_MODES:
        return "Dilution mode required"
    if mode == "apply_in_qbench" and not positive_number(row.get("df")):
        return "Dilution factor required"
    if row.get("labsolutions_conc_unit") != "ug/mL" or row.get("unit_confirmed") is not True:
        return "Unit confirmation required"
    if row.get("preparation_values_confirmed") is not True:
        return "Preparation confirmation required"
    if not source_audit_complete(row):
        if not is_strict_number(row.get("dimethylacetamide_conc")):
            return "Dimethylacetamide audit value required"
        if row.get("compound_results_complete") is not True:
            return "Compound Results validation required"
        if row.get("integration_review_status") != "Reviewed":
            return "Integration review required"
        if row.get("import_validation_status") != "Valid":
            return "Import validation required"
        return "Source traceability incomplete"
    if row.get("batch_qc_disposition") != "Accepted":
        return "Batch QC on hold"
    if row_prerequisites_complete(row, duplicate_ids):
        return "Ready for transfer"
    return "Batch release review required"


def row_prerequisites_complete(row: dict[str, Any], duplicate_ids: set[str]) -> bool:
    if not row.get("qbench_test_id") or row["qbench_test_id"] in duplicate_ids:
        return False
    mode = row.get("df_application_mode")
    df_ok = mode == "already_applied_by_labsolutions" or (
        mode == "apply_in_qbench" and positive_number(row.get("df"))
    )
    return (
        analytical_values_complete(row.get("analyte_values", []))
        and positive_number(row.get("sample_mass_g"))
        and positive_number(row.get("final_volume_ml"))
        and df_ok
        and row.get("labsolutions_conc_unit") == "ug/mL"
        and row.get("unit_confirmed") is True
        and row.get("preparation_values_confirmed") is True
        and source_audit_complete(row)
        and row.get("batch_qc_disposition") == "Accepted"
    )


def evaluate_minimum(value: Any, minimum: Decimal) -> str:
    if value in ("", None):
        return "not_evaluated"
    if not is_strict_number(value):
        return "review_required"
    return "within_criteria" if as_decimal(value) >= minimum else "outside_criteria"


def evaluate_maximum(value: Any, maximum: Decimal) -> str:
    if value in ("", None):
        return "not_evaluated"
    if not is_strict_number(value):
        return "review_required"
    return "within_criteria" if as_decimal(value) <= maximum else "outside_criteria"


def evaluate_range(value: Any, minimum: Decimal, maximum: Decimal) -> str:
    if value in ("", None):
        return "not_evaluated"
    if not is_strict_number(value):
        return "review_required"
    numeric = as_decimal(value)
    return "within_criteria" if minimum <= numeric <= maximum else "outside_criteria"


def bracketing_ccv_evaluation(value: Any, criterion_status: str, accuracy_window: Any) -> str:
    if criterion_status == "decision_required":
        return "decision_required"
    if criterion_status == "not_applicable":
        return "not_applicable"
    if not is_strict_number(accuracy_window):
        return "decision_required"
    window = as_decimal(accuracy_window)
    return evaluate_range(value, Decimal("100") - window, Decimal("100") + window)


def overall_analyte_qc_evaluation(evaluations: Iterable[str]) -> str:
    values = list(evaluations)
    for value in values:
        if value not in INTERNAL_QC_EVALUATION_VALUES:
            return "review_required"
    if "outside_criteria" in values:
        return "outside_criteria"
    if "decision_required" in values:
        return "decision_required"
    if "review_required" in values:
        return "review_required"
    if "not_evaluated" in values:
        return "not_evaluated"
    return "within_criteria"


def qc_configuration_complete(
    *,
    bracketing_ccv_criterion_status: str,
    bracketing_ccv_accuracy_percent_window: Any = "",
    lcs_criterion_status: str | None = None,
) -> bool:
    if bracketing_ccv_criterion_status == "decision_required":
        return False
    if bracketing_ccv_criterion_status != "not_applicable" and not is_strict_number(
        bracketing_ccv_accuracy_percent_window
    ):
        return False
    if lcs_criterion_status == "decision_required":
        return False
    return True


def batch_publish_ready(
    *,
    qc_configuration_is_complete: bool,
    integration_review_is_complete: bool,
    qc_data_is_complete: bool,
    qc_review_is_complete: bool,
    all_publish_rows_are_valid: bool,
    duplicate_test_id_count: int,
    batch_qc_disposition: str,
    batch_qc_reviewer: str,
    batch_qc_reviewed_at: str,
) -> bool:
    return (
        qc_configuration_is_complete
        and integration_review_is_complete
        and qc_data_is_complete
        and qc_review_is_complete
        and all_publish_rows_are_valid
        and duplicate_test_id_count == 0
        and batch_qc_disposition == "Accepted"
        and bool(batch_qc_reviewer)
        and bool(batch_qc_reviewed_at)
    )


def batch_publish_message(
    *,
    qc_configuration_is_complete: bool,
    integration_review_is_complete: bool,
    qc_data_is_complete: bool,
    qc_review_is_complete: bool,
    all_publish_rows_are_valid: bool,
    duplicate_test_id_count: int,
    batch_qc_disposition: str,
    batch_qc_reviewer: str,
    batch_qc_reviewed_at: str,
) -> str:
    if not qc_configuration_is_complete:
        return "QC configuration incomplete"
    if not integration_review_is_complete:
        return "Integration review incomplete"
    if not qc_data_is_complete:
        return "QC data incomplete"
    if not qc_review_is_complete:
        return "QC review incomplete"
    if not all_publish_rows_are_valid:
        return "Publish rows incomplete"
    if duplicate_test_id_count > 0:
        return "Duplicate Test ID"
    if batch_qc_disposition != "Accepted":
        return "Batch QC on hold"
    if not batch_qc_reviewer or not batch_qc_reviewed_at:
        return "Batch release review required"
    return "Ready for transfer"


def publish_ready(row_prerequisites_are_complete: bool, batch_is_publish_ready: bool) -> str:
    if row_prerequisites_are_complete and batch_is_publish_ready:
        return "TRUE"
    return "FALSE"
