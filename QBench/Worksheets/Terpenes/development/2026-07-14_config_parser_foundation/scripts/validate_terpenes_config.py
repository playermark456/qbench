#!/usr/bin/env python3
"""Validate the Terpenes parser/config foundation."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from parse_labsolutions_ascii import (  # noqa: E402
    TerpenesConfigError,
    build_alias_map,
    load_json,
    reportable_channels,
    validate_analyte_config,
)


class ConfigValidationError(ValueError):
    """Raised when a Terpenes config violates controlled rules."""


REQUIRED_DISABLED_CONTROL_FLAGS = {
    "sample_pass_fail_enabled",
    "analyte_pass_fail_enabled",
    "coa_pass_fail_enabled",
    "metrc_pass_fail_enabled",
    "kvstore_pass_fail_enabled",
    "label_claim_pass_fail_enabled",
}

FORBIDDEN_RESULT_TOKENS = [
    "pass_fail",
    "Pass",
    "Fail",
    "Not Tested",
    "Claim Met",
    "Claim Not Met",
]


def validation_error(message: str) -> ConfigValidationError:
    return ConfigValidationError(message)


def publish_ready_allowed(
    qc_config: dict[str, Any],
    *,
    batch_qc_disposition: str,
    required_analytical_fields_complete: bool,
    required_audit_fields_complete: bool,
) -> bool:
    logic = qc_config.get("publish_ready_logic", {})
    required_disposition = logic.get("allowed_true_batch_qc_disposition")
    return (
        batch_qc_disposition == required_disposition
        and bool(required_analytical_fields_complete)
        and bool(required_audit_fields_complete)
    )


def _path_text(path: tuple[str, ...]) -> str:
    return ".".join(str(part) for part in path)


def _iter_json_paths(value: Any, path: tuple[str, ...] = ()) -> list[tuple[tuple[str, ...], Any]]:
    items: list[tuple[tuple[str, ...], Any]] = [(path, value)]
    if isinstance(value, dict):
        for key, child in value.items():
            items.extend(_iter_json_paths(child, (*path, str(key))))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            items.extend(_iter_json_paths(child, (*path, str(index))))
    return items


def _contains_forbidden_token(text: str, token: str) -> bool:
    if token == "pass_fail":
        return "pass_fail" in text
    return re.search(rf"\b{re.escape(token)}\b", text) is not None


def validate_no_forbidden_result_artifacts(*configs: dict[str, Any]) -> None:
    for config_index, config in enumerate(configs):
        for path, value in _iter_json_paths(config):
            if not path:
                continue

            key = path[-1]
            if key in REQUIRED_DISABLED_CONTROL_FLAGS:
                if value is not False:
                    raise validation_error(f"{_path_text(path)} must be false.")
                continue

            if isinstance(value, (dict, list)):
                text_values = [key]
            elif isinstance(value, str):
                text_values = [key, value]
            else:
                text_values = [key]

            for text in text_values:
                for token in FORBIDDEN_RESULT_TOKENS:
                    if _contains_forbidden_token(str(text), token):
                        raise validation_error(
                            f"Forbidden Terpenes result/reporting token {token!r} at "
                            f"config[{config_index}].{_path_text(path)}"
                        )


def validate_qc_config(qc_config: dict[str, Any]) -> None:
    if qc_config.get("reporting_mode") != "quantitative_only":
        raise validation_error("QC reporting_mode must be quantitative_only.")

    for flag in REQUIRED_DISABLED_CONTROL_FLAGS:
        if qc_config.get(flag) is not False:
            raise validation_error(f"{flag} must be false.")

    dispositions = qc_config.get("batch_qc_disposition_values")
    if dispositions != ["Accepted", "Hold", "Rejected"]:
        raise validation_error("batch_qc_disposition_values must be Accepted, Hold, Rejected.")

    requires = qc_config.get("publish_ready_requires", [])
    required_rules = {
        "batch_qc_disposition == Accepted",
        "required analytical and audit fields complete",
    }
    if set(requires) != required_rules:
        raise validation_error("publish_ready_requires does not match the controlled rules.")

    for disposition in dispositions:
        allowed = publish_ready_allowed(
            qc_config,
            batch_qc_disposition=disposition,
            required_analytical_fields_complete=True,
            required_audit_fields_complete=True,
        )
        if disposition == "Accepted" and not allowed:
            raise validation_error("Accepted disposition with complete fields must permit publish_ready.")
        if disposition != "Accepted" and allowed:
            raise validation_error("publish_ready must be false unless disposition is Accepted.")

    if publish_ready_allowed(
        qc_config,
        batch_qc_disposition="Accepted",
        required_analytical_fields_complete=False,
        required_audit_fields_complete=True,
    ):
        raise validation_error("publish_ready must require analytical fields.")
    if publish_ready_allowed(
        qc_config,
        batch_qc_disposition="Accepted",
        required_analytical_fields_complete=True,
        required_audit_fields_complete=False,
    ):
        raise validation_error("publish_ready must require audit fields.")


def validate_metrc_config(metrc_config: dict[str, Any], analyte_config: dict[str, Any]) -> None:
    if metrc_config.get("reporting_mode") != "quantitative_only":
        raise validation_error("METRC reporting_mode must be quantitative_only.")
    if metrc_config.get("profile_driven") is not True:
        raise validation_error("METRC mappings must be profile-driven.")
    if metrc_config.get("silent_other_terpenes_mapping_enabled") is not False:
        raise validation_error("Silent mapping to Other Terpenes must be disabled.")

    profile_count = len(metrc_config.get("profiles", {}))
    if profile_count != 9:
        raise validation_error(f"Expected 9 METRC profiles, found {profile_count}.")

    reportable_keys = {row["internal_key"] for row in reportable_channels(analyte_config)}
    mappings = metrc_config.get("metrc_mappings", [])
    mapping_keys = [row.get("internal_key") for row in mappings]
    if len(mappings) != 23:
        raise validation_error(f"Expected 23 METRC mappings, found {len(mappings)}.")
    if set(mapping_keys) != reportable_keys:
        missing = sorted(reportable_keys - set(mapping_keys))
        extra = sorted(set(mapping_keys) - reportable_keys)
        raise validation_error(f"METRC mapping key mismatch: missing={missing}, extra={extra}.")
    if len(mapping_keys) != len(set(mapping_keys)):
        raise validation_error("Duplicate METRC internal keys are not allowed.")

    for row in mappings:
        target = str(row.get("metrc_target_analyte_label", ""))
        if target.casefold() == "other terpenes":
            raise validation_error("No internal analyte may silently map to Other Terpenes.")

    rollup = metrc_config.get("rollups", {}).get("metrc_ocimene", {})
    if rollup.get("components") != ["cisocimene", "transocimene"]:
        raise validation_error("METRC Ocimene rollup must use cisocimene and transocimene.")

    p_cymene = [row for row in mappings if row.get("internal_key") == "pcymene"]
    if not p_cymene or p_cymene[0].get("rule") != "direct_preferred_over_generic":
        raise validation_error("p-Cymene must use the explicit configured target, not a generic fallback.")

    schema_policy = metrc_config.get("schema_outcome_column_policy", {})
    if schema_policy.get("required_by_current_profiles") is not False:
        raise validation_error("Current METRC profiles must not require an outcome column.")
    external_policy = schema_policy.get("if_required_by_external_schema", {})
    neutral_values = external_policy.get("neutral_output_values", [])
    if external_policy.get("output_value") not in neutral_values:
        raise validation_error("External schema outcome column must be blank or neutral.")
    if external_policy.get("include_formula_depends_on_column") is not False:
        raise validation_error("METRC Include calculation must not depend on the outcome column.")


def validate_bundle(base_dir: Path) -> dict[str, Any]:
    config_dir = base_dir / "config"
    analyte_config = load_json(config_dir / "terpenes_analytes.json")
    qc_config = load_json(config_dir / "terpenes_qc.json")
    metrc_config = load_json(config_dir / "metrc_profiles.json")

    try:
        validate_analyte_config(analyte_config)
        build_alias_map(analyte_config)
    except TerpenesConfigError as exc:
        raise validation_error(str(exc)) from exc

    validate_qc_config(qc_config)
    validate_metrc_config(metrc_config, analyte_config)
    validate_no_forbidden_result_artifacts(analyte_config, qc_config, metrc_config)

    reportable_keys = {row["internal_key"] for row in reportable_channels(analyte_config)}
    return {
        "status": "ok",
        "reporting_mode": "quantitative_only",
        "reportable_channel_count": len(reportable_keys),
        "default_coa_measurand_count": analyte_config["default_coa_reporting"]["measurand_count"],
        "metrc_profile_count": len(metrc_config["profiles"]),
        "batch_qc_disposition_values": qc_config["batch_qc_disposition_values"],
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-dir", type=Path, default=BASE_DIR)
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    try:
        summary = validate_bundle(args.base_dir)
    except ConfigValidationError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(1) from exc
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
