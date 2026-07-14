#!/usr/bin/env python3
"""Reference-only Terpenes calculations for Prompt 3 tests."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any


VALID_DF_APPLICATION_MODES = {"already_applied_by_labsolutions", "apply_in_qbench"}
CONTROLLED_BELOW_LOQ_REPORTING_MODES = {
    "decision_required",
    "display_less_than_loq",
    "display_numeric_result",
}
REPORT_RELEASE_BELOW_LOQ_MODES = {"display_less_than_loq", "display_numeric_result"}


class CalculationBlocked(ValueError):
    """Raised when controlled calculation prerequisites are not met."""


def to_decimal(value: Any, field_name: str) -> Decimal:
    if value in ("", None):
        raise CalculationBlocked(f"{field_name} must be numeric.")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise CalculationBlocked(f"{field_name} must be numeric.") from exc
    return result


def is_numeric(value: Any) -> bool:
    try:
        to_decimal(value, "value")
    except CalculationBlocked:
        return False
    return True


def positive_decimal(value: Any, field_name: str) -> Decimal:
    result = to_decimal(value, field_name)
    if result <= 0:
        raise CalculationBlocked(f"{field_name} must be greater than zero.")
    return result


def calculation_ready(
    *,
    labsolutions_conc_unit: str,
    labsolutions_conc_unit_confirmed: bool,
    preparation_values_confirmed: bool,
    sample_mass_g: Any,
    final_volume_ml: Any,
    df_application_mode: str,
    df: Any = None,
) -> bool:
    if not labsolutions_conc_unit_confirmed:
        return False
    if labsolutions_conc_unit != "ug/mL":
        return False
    if not preparation_values_confirmed:
        return False
    try:
        positive_decimal(sample_mass_g, "sample_mass_g")
        positive_decimal(final_volume_ml, "final_volume_ml")
    except CalculationBlocked:
        return False
    if df_application_mode not in VALID_DF_APPLICATION_MODES:
        return False
    if df_application_mode == "apply_in_qbench":
        try:
            positive_decimal(df, "df")
        except CalculationBlocked:
            return False
    return True


def dilution_multiplier(df_application_mode: str, df: Any = None) -> Decimal:
    if df_application_mode == "already_applied_by_labsolutions":
        return Decimal("1")
    if df_application_mode == "apply_in_qbench":
        return positive_decimal(df, "df")
    raise CalculationBlocked("df_application_mode is unresolved or invalid.")


def calculate_result(
    *,
    conc_ug_ml: Any,
    final_volume_ml: Any,
    sample_mass_g: Any,
    df_application_mode: str,
    df: Any = None,
) -> dict[str, Decimal]:
    concentration = to_decimal(conc_ug_ml, "conc_ug_ml")
    final_volume = positive_decimal(final_volume_ml, "final_volume_ml")
    sample_mass = positive_decimal(sample_mass_g, "sample_mass_g")
    multiplier = dilution_multiplier(df_application_mode, df)
    effective_concentration = concentration * multiplier
    result_mg_g = effective_concentration * final_volume / sample_mass / Decimal("1000")
    result_percent = result_mg_g / Decimal("10")
    return {
        "effective_concentration_ug_ml": effective_concentration,
        "result_mg_g": result_mg_g,
        "result_percent": result_percent,
    }


def reporting_ready(
    *,
    calculation_is_ready: bool,
    analytical_results_are_complete: bool,
    batch_qc_disposition: str,
    publish_ready: bool,
    below_loq_reporting_mode: str,
    loq_source_status: str,
    mu_source_status: str,
) -> bool:
    return (
        calculation_is_ready
        and analytical_results_are_complete
        and batch_qc_disposition == "Accepted"
        and publish_ready
        and below_loq_reporting_mode in REPORT_RELEASE_BELOW_LOQ_MODES
        and loq_source_status == "confirmed"
        and mu_source_status == "confirmed"
    )


def analytical_results_complete(instrument_inputs: list[Any], calculated_mg_g_results: list[Any]) -> bool:
    return (
        len(instrument_inputs) == 23
        and len(calculated_mg_g_results) == 23
        and all(is_numeric(value) for value in instrument_inputs)
        and all(is_numeric(value) for value in calculated_mg_g_results)
    )


def report_display_value(
    *,
    reporting_is_ready: bool,
    qualifier: str,
    below_loq_reporting_mode: str,
    numerical_result: Any,
) -> Any:
    if not reporting_is_ready:
        return ""
    if qualifier == "<LOQ":
        if below_loq_reporting_mode == "display_less_than_loq":
            return "<LOQ"
        if below_loq_reporting_mode == "display_numeric_result":
            return to_decimal(numerical_result, "numerical_result")
        return ""
    if qualifier == "Reported":
        return to_decimal(numerical_result, "numerical_result")
    return ""


def sum_components(values: dict[str, Any], components: list[str]) -> Decimal:
    total = Decimal("0")
    for component in components:
        total += to_decimal(values[component], component)
    return total


def total_terpenes(values: dict[str, Any], internal_keys: list[str]) -> Decimal:
    return sum_components(values, internal_keys)


def complete_sum_components(values: dict[str, Any], components: list[str]) -> Decimal | None:
    if any(component not in values or not is_numeric(values[component]) for component in components):
        return None
    return sum_components(values, components)


def complete_total_terpenes(values: dict[str, Any], internal_keys: list[str]) -> Decimal | None:
    if len(internal_keys) != 23:
        return None
    if any(key not in values or not is_numeric(values[key]) for key in internal_keys):
        return None
    return total_terpenes(values, internal_keys)
