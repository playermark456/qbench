#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = Path(__file__).resolve().parent

REQUIRED = {
    "README.md",
    "preflight_plan.md",
    "oauth_result_sanitized.md",
    "object_identity_results.md",
    "worksheet_get_results.md",
    "worksheet_contract_results.md",
    "field_key_comparison.csv",
    "request_ledger_sanitized.json",
    "raw_response_sha256.txt",
    "sanitized_object_inventory.json",
    "next_patch_phase_gate.md",
    "run_summary_sanitized.json",
    "run_read_only_confirmation.py",
}


def main() -> int:
    failures: list[str] = []
    for name in sorted(REQUIRED):
        if not (EVIDENCE / name).is_file():
            failures.append(f"missing evidence file: {name}")

    with (ROOT / "config/field_mapping_scalar_candidate.csv").open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        expected = [row["destination_named_cell"] for row in csv.DictReader(handle)]
    with (EVIDENCE / "field_key_comparison.csv").open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        comparison = list(csv.DictReader(handle))
    if len(expected) != 43 or len(comparison) != 43:
        failures.append("field comparison must contain exactly 43 expected keys")
    if [row.get("expected_key") for row in comparison] != expected:
        failures.append("field comparison keys do not match the ordered candidate mapping")
    allowed_classifications = {
        "observed_exact",
        "missing",
        "renamed",
        "duplicated",
        "present_but_unreadable",
        "not_exposed_by_get_contract",
    }
    if any(row.get("classification") not in allowed_classifications for row in comparison):
        failures.append("field comparison contains an unsupported classification")
    if any(row.get("classification") != "not_exposed_by_get_contract" for row in comparison):
        failures.append("OAuth-stop comparison must classify all 43 keys as not exposed")
    prohibited = ("pass_fail", "pass-fail", "dimethylacetamide", "peak_table", "peak table", "sdf")
    if any(any(term in key.lower() for term in prohibited) for key in expected):
        failures.append("expected mapping contains a prohibited destination")

    ledger = json.loads(
        (EVIDENCE / "request_ledger_sanitized.json").read_text(encoding="utf-8")
    )
    requests = ledger.get("requests", [])
    if ledger.get("allowed_origin") != "https://ait-sandbox.qbench.net":
        failures.append("ledger allowed origin is not exact")
    if len(requests) != 1:
        failures.append("controlled-stop ledger must contain exactly one request")
    else:
        request = requests[0]
        expected_request = {
            "sequence": 1,
            "method": "POST",
            "endpoint_template": "/qbench/api/v1/oauth/token",
            "http_status": 404,
            "content_type": "application/json",
            "allowed_origin": True,
            "redirect_escaped_allowed_origin": False,
        }
        if request != expected_request:
            failures.append("sanitized token-request ledger entry is incorrect")
    if any(request.get("method") in {"GET", "PATCH", "PUT", "DELETE"} for request in requests):
        failures.append("ledger contains a prohibited or post-OAuth request")
    if any(
        request.get("method") == "POST"
        and request.get("endpoint_template") != "/qbench/api/v1/oauth/token"
        for request in requests
    ):
        failures.append("ledger contains a non-token POST")
    for key in (
        "authorization_headers_recorded",
        "credentials_or_tokens_recorded",
        "internal_object_ids_recorded",
    ):
        if ledger.get(key) is not False:
            failures.append(f"ledger safety flag must be false: {key}")

    summary = json.loads(
        (EVIDENCE / "run_summary_sanitized.json").read_text(encoding="utf-8")
    )
    if summary.get("origin_preflight") != "passed_exact_sandbox_origin":
        failures.append("summary origin preflight is incorrect")
    if summary.get("result") != "controlled_stop" or summary.get("stop_reason") != "http_status_404":
        failures.append("summary OAuth controlled stop is incorrect")
    oauth = summary.get("oauth", {})
    for key, expected_value in {
        "result": "failed",
        "http_status": 404,
        "content_type": "application/json",
        "token_type": "not_available",
        "approximate_expiration_seconds": "not_available",
        "origin": "https://ait-sandbox.qbench.net",
        "credentials_or_token_exposed": False,
        "token_persisted": False,
        "token_request_attempts": 1,
        "client_assertion_persisted_or_displayed": False,
    }.items():
        if oauth.get(key) != expected_value:
            failures.append(f"summary OAuth field is incorrect: {key}")
    if summary.get("identity", {}).get("classification") != "not_run":
        failures.append("identity must not be claimed after OAuth failure")
    if summary.get("worksheet_get", {}).get("result") != "not_run":
        failures.append("worksheet GET must not be claimed after OAuth failure")

    inventory = json.loads(
        (EVIDENCE / "sanitized_object_inventory.json").read_text(encoding="utf-8")
    )
    for key, expected_value in {
        "classification": "oauth_token_endpoint_404_controlled_stop",
        "token_post_requests": 1,
        "get_requests": 0,
        "patch_requests": 0,
        "put_requests": 0,
        "delete_requests": 0,
        "non_token_post_requests": 0,
        "objects_created": 0,
        "objects_changed": 0,
        "analytical_results_changed": False,
        "publish_or_qc_review_performed": False,
        "pass_fail_artifact_introduced": False,
        "live_qbench_accessed": False,
        "internal_object_ids_recorded": False,
        "credentials_or_tokens_recorded": False,
        "authorization_headers_recorded": False,
    }.items():
        if inventory.get(key) != expected_value:
            failures.append(f"sanitized inventory field is incorrect: {key}")

    evidence_names = REQUIRED - {"run_read_only_confirmation.py"}
    evidence_text = "\n".join(
        (EVIDENCE / name).read_text(encoding="utf-8", errors="replace")
        for name in sorted(evidence_names)
    )
    if re.search(r"(?i)authorization\s*:\s*bearer\s+\S+", evidence_text):
        failures.append("tracked evidence contains an Authorization bearer header")
    if re.search(r"(?i)bearer\s+[A-Za-z0-9._~+/-]{16,}", evidence_text):
        failures.append("tracked evidence contains a bearer-token-like value")
    if re.search(r'(?i)"(?:test|sample|assay|worksheet|version|user)_id"\s*:\s*"?\d+', evidence_text):
        failures.append("tracked evidence contains an internal QBench ID")

    credentials: dict[str, str] = {}
    for line in (ROOT / ".env.local.txt").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            key, value = line.split("=", 1)
            credentials[key] = value
    for key in ("QBENCH_CLIENT_ID", "QBENCH_CLIENT_SECRET"):
        value = credentials.get(key, "")
        if value and value in evidence_text:
            failures.append(f"tracked evidence contains local credential value: {key}")

    runner = (EVIDENCE / "run_read_only_confirmation.py").read_text(encoding="utf-8")
    for required_text in (
        'ALLOWED_ORIGIN = "https://ait-sandbox.qbench.net"',
        'TOKEN_PATH = "/qbench/api/v1/oauth/token"',
        'ProxyHandler({})',
        'ssl.create_default_context()',
        'class RejectRedirects(HTTPRedirectHandler)',
        'raise ControlledStop("prohibited_method_rejected_before_dispatch")',
    ):
        if required_text not in runner:
            failures.append(f"read-only runner guard missing: {required_text}")
    if "https://ait.qbench.net" in runner:
        failures.append("live QBench origin appears in read-only runner")

    if failures:
        print("Read-only API evidence validation FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("Read-only API evidence validation PASSED")
    print("- exact Sandbox origin preflight passed")
    print("- one token POST returned sanitized HTTP 404; zero GET requests")
    print("- 43 expected keys recorded as not exposed because GET was not reached")
    print("- zero PATCH, PUT, DELETE, non-token POST, object changes, or result changes")
    print("- no credential, token, Authorization header, or internal ID in tracked evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
