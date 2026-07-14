#!/usr/bin/env python3
"""Reference-only Terpenes calculations for Prompt 3 tests."""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any


VALID_DF_APPLICATION_MODES = {"already_applied_by_labsolutions", "apply_in_qbench"}


class CalculationBlocked(ValueError):
    """Raised when controlled calculation prerequisites are not met."""


def to_decimal(value: Any, field_name: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise CalculationBlocked(f"{field_name} must be numeric.") from exc
    return result


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
    batch_qc_disposition: str,
    publish_ready: bool,
    below_loq_reporting_mode: str,
    loq_source_status: str,
    mu_source_status: str,
) -> bool:
    return (
        calculation_is_ready
        and batch_qc_disposition == "Accepted"
        and publish_ready
        and below_loq_reporting_mode != "decision_required"
        and loq_source_status == "confirmed"
        and mu_source_status == "confirmed"
    )


def sum_components(values: dict[str, Any], components: list[str]) -> Decimal:
    total = Decimal("0")
    for component in components:
        total += to_decimal(values[component], component)
    return total


def total_terpenes(values: dict[str, Any], internal_keys: list[str]) -> Decimal:
    return sum_components(values, internal_keys)
