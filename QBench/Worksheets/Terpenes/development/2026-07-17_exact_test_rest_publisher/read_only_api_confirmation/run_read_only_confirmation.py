#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import ssl
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, ProxyHandler, Request, build_opener


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_ROOT = Path(__file__).resolve().parent
RAW_ROOT = EVIDENCE_ROOT / "raw"
SECRETS_PATH = ROOT / ".env.local.txt"
RUNTIME_EXPORT = (
    ROOT
    / "json_import_rebuild/runtime_instantiation/"
    "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_RUNTIME_TEST_WORKSHEET_export_data.csv"
)
MAPPING_PATH = ROOT / "config/field_mapping_scalar_candidate.csv"

ALLOWED_ORIGIN = "https://ait-sandbox.qbench.net"
HISTORICAL_TOKEN_PATH = "/qbench/api/v1/oauth/token"
TOKEN_PATH = "/qbench/api/v2/auth/token"
TEST_PATH_TEMPLATE = "/qbench/api/v1/test/{test_id}"
WORKSHEET_PATH_TEMPLATE = "/qbench/api/v1/test/{test_id}/worksheet"

EXPECTED_ASSAY = "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_ASSAY"
EXPECTED_SAMPLE = "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_RUNTIME_SAMPLE"
EXPECTED_WORKSHEET = "SBX_ONLY_TERPENES_2026_07_17_JSON_SCALAR_43_FIELD_BASE"
EXPECTED_VERSION = "JSON Scalar 43 Field Base v1"

sys.path.insert(0, str(ROOT))
from src.terpenes_publisher.core import (  # noqa: E402
    HttpResponse,
    QBenchTokenClient,
    load_client_credentials,
)

METADATA_COLUMNS = {
    "ID",
    "sample_id",
    "description",
    "order_id",
    "order_status",
    "due_date",
    "test_id",
    "status",
    "assay",
    "technician",
    "estimated_start_date",
    "estimated_complete_date",
    "start_date",
    "complete_date",
    "results",
}
TRANSIENT_STATUSES = {429, 500, 502, 503, 504}


class ControlledStop(RuntimeError):
    pass


@dataclass(frozen=True)
class LocalIdentity:
    test_id: str
    sample_id: str


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def load_credentials() -> Any:
    entries: dict[str, str] = {}
    duplicates: set[str] = set()
    for raw_line in SECRETS_PATH.read_text(encoding="utf-8").splitlines():
        if not raw_line or raw_line.startswith("#") or "=" not in raw_line:
            continue
        key, value = raw_line.split("=", 1)
        if key in entries:
            duplicates.add(key)
        entries[key] = value
    required = ("QBENCH_BASE_URL", "QBENCH_CLIENT_ID", "QBENCH_CLIENT_SECRET")
    if duplicates.intersection(required):
        raise ControlledStop("duplicate_required_credential_key")
    if any(key not in entries or entries[key] == "" for key in required):
        raise ControlledStop("missing_or_blank_required_credential_key")
    if entries["QBENCH_BASE_URL"] != ALLOWED_ORIGIN:
        raise ControlledStop("origin_preflight_failed")
    return load_client_credentials(SECRETS_PATH)


def load_local_identity() -> LocalIdentity:
    with RUNTIME_EXPORT.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ControlledStop("runtime_export_must_contain_one_row")
    row = rows[0]
    if row.get("assay") != EXPECTED_ASSAY:
        raise ControlledStop("runtime_export_assay_mismatch")
    test_id = row.get("test_id", "")
    sample_id = row.get("sample_id", "")
    if not test_id or not sample_id:
        raise ControlledStop("runtime_export_identity_missing")
    destination_columns = [name for name in row if name not in METADATA_COLUMNS]
    if len(destination_columns) != 43:
        raise ControlledStop("runtime_export_destination_count_mismatch")
    if any(row[name] not in ("", None) for name in destination_columns):
        raise ControlledStop("runtime_export_baseline_not_blank")
    return LocalIdentity(test_id, sample_id)


def load_expected_keys() -> list[str]:
    with MAPPING_PATH.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    keys = [row["destination_named_cell"] for row in rows]
    if len(keys) != 43 or len(set(keys)) != 43:
        raise ControlledStop("expected_mapping_not_exact_43")
    return keys


def validate_path(method: str, path: str, template: str) -> None:
    if method == "POST":
        if path != TOKEN_PATH or template != TOKEN_PATH:
            raise ControlledStop("non_token_post_rejected_before_dispatch")
        return
    if method != "GET":
        raise ControlledStop("prohibited_method_rejected_before_dispatch")
    allowed_templates = {TEST_PATH_TEMPLATE, WORKSHEET_PATH_TEMPLATE}
    if template not in allowed_templates:
        raise ControlledStop("undocumented_get_rejected_before_dispatch")
    if not path.startswith("/qbench/api/v1/test/") or "http" in path.lower():
        raise ControlledStop("unsafe_get_path_rejected_before_dispatch")


def validate_url(url: str) -> None:
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "ait-sandbox.qbench.net"
        or parsed.port not in (None, 443)
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or f"{parsed.scheme}://{parsed.netloc}" != ALLOWED_ORIGIN
    ):
        raise ControlledStop("request_origin_rejected_before_dispatch")


class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        return None


class GuardedTransport:
    def __init__(self) -> None:
        self.ledger: list[dict[str, Any]] = []
        self._sequence = 0
        self.token_http_metadata: dict[str, Any] = {}
        self._opener = build_opener(
            ProxyHandler({}),
            HTTPSHandler(context=ssl.create_default_context()),
            RejectRedirects(),
        )

    def _record(
        self,
        method: str,
        template: str,
        status: int,
        content_type: str,
        redirect_escaped: bool = False,
    ) -> None:
        self._sequence += 1
        self.ledger.append(
            {
                "sequence": self._sequence,
                "method": method,
                "endpoint_template": template,
                "http_status": status,
                "content_type": content_type,
                "allowed_origin": True,
                "redirect_escaped_allowed_origin": redirect_escaped,
            }
        )

    def dispatch(
        self,
        method: str,
        path: str,
        template: str,
        *,
        data: bytes | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float = 20.0,
    ) -> tuple[int, str, bytes]:
        validate_path(method, path, template)
        url = ALLOWED_ORIGIN + path
        validate_url(url)
        request = Request(url, data=data, headers=dict(headers or {}), method=method)
        try:
            with self._opener.open(request, timeout=timeout) as response:
                body = response.read()
                content_type = response.headers.get_content_type()
                self._record(method, template, response.status, content_type)
                return response.status, content_type, body
        except HTTPError as exc:
            content_type = exc.headers.get_content_type() if exc.headers else "unknown"
            location = exc.headers.get("Location") if exc.headers else None
            redirect_escaped = False
            if location:
                redirect = urlsplit(location)
                redirect_escaped = bool(redirect.scheme or redirect.netloc) and (
                    f"{redirect.scheme}://{redirect.netloc}" != ALLOWED_ORIGIN
                )
            self._record(method, template, exc.code, content_type, redirect_escaped)
            raise ControlledStop(f"http_status_{exc.code}") from None
        except (TimeoutError, URLError, OSError):
            self._record(method, template, 0, "unavailable")
            raise ControlledStop("transport_failure") from None

    def token_opener(self, request: Request, timeout: float) -> HttpResponse:
        parsed = urlsplit(request.full_url)
        path = parsed.path
        content_type_header = request.get_header("Content-type") or ""
        if not content_type_header.startswith("multipart/form-data; boundary="):
            raise ControlledStop("oauth_content_type_contract_violation")
        status, content_type, raw = self.dispatch(
            request.get_method(),
            path,
            TOKEN_PATH,
            data=request.data,
            headers={
                "Accept": "application/json",
                "Content-Type": content_type_header,
            },
            timeout=timeout,
        )
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ControlledStop("oauth_response_not_json") from None
        self.token_http_metadata = {
            "http_status": status,
            "content_type": content_type,
        }
        return HttpResponse(status, payload)

    def get_json(self, path: str, template: str, token: str) -> tuple[bytes, Any, int, str]:
        last_error: ControlledStop | None = None
        for attempt in range(2):
            try:
                status, content_type, raw = self.dispatch(
                    "GET",
                    path,
                    template,
                    headers={"Accept": "application/json", "Authorization": f"Bearer {token}"},
                )
                try:
                    payload = json.loads(raw.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError):
                    raise ControlledStop("get_response_not_json") from None
                return raw, payload, status, content_type
            except ControlledStop as exc:
                last_error = exc
                status = self.ledger[-1]["http_status"] if self.ledger else 0
                if attempt == 0 and (status in TRANSIENT_STATUSES or status == 0):
                    time.sleep(0.1)
                    continue
                raise
        raise last_error or ControlledStop("get_failed")


def unwrap_data(payload: Any) -> Any:
    if isinstance(payload, Mapping) and isinstance(payload.get("data"), Mapping):
        return payload["data"]
    return payload


def recursive_values_for_keys(value: Any, keys: set[str]) -> list[Any]:
    found: list[Any] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key in keys:
                found.append(child)
            found.extend(recursive_values_for_keys(child, keys))
    elif isinstance(value, list):
        for child in value:
            found.extend(recursive_values_for_keys(child, keys))
    return found


def recursive_strings(value: Any) -> set[str]:
    result: set[str] = set()
    if isinstance(value, str):
        result.add(value)
    elif isinstance(value, Mapping):
        for child in value.values():
            result.update(recursive_strings(child))
    elif isinstance(value, list):
        for child in value:
            result.update(recursive_strings(child))
    return result


def classify_identity(payload: Any, local: LocalIdentity) -> dict[str, Any]:
    body = unwrap_data(payload)
    strings = recursive_strings(body)
    test_ids = recursive_values_for_keys(body, {"id", "test_id"})
    sample_ids = recursive_values_for_keys(body, {"sample_id"})
    assay_titles = recursive_values_for_keys(body, {"assay_name"})
    if isinstance(body, Mapping) and isinstance(body.get("assay"), Mapping):
        assay_titles.extend(recursive_values_for_keys(body["assay"], {"name", "title"}))
    result = {
        "requested_test_id_matched": any(str(value) == local.test_id for value in test_ids),
        "runtime_sample_id_matched": any(str(value) == local.sample_id for value in sample_ids),
        "expected_assay_title_matched": EXPECTED_ASSAY in strings
        or any(value == EXPECTED_ASSAY for value in assay_titles),
        "expected_sample_title_exposed": EXPECTED_SAMPLE in strings,
        "expected_worksheet_title_exposed": EXPECTED_WORKSHEET in strings,
        "expected_version_title_exposed": EXPECTED_VERSION in strings,
    }
    result["classification"] = (
        "passed_exact_runtime_test"
        if result["requested_test_id_matched"]
        and result["runtime_sample_id_matched"]
        and result["expected_assay_title_matched"]
        else "insufficient_documented_api_surface"
    )
    return result


def mapping_candidates(value: Any) -> list[Mapping[str, Any]]:
    result: list[Mapping[str, Any]] = []
    if isinstance(value, Mapping):
        result.append(value)
        for child in value.values():
            result.extend(mapping_candidates(child))
    elif isinstance(value, list):
        for child in value:
            result.extend(mapping_candidates(child))
    return result


def extract_field_mapping(payload: Any, expected_keys: list[str]) -> Mapping[str, Any] | None:
    expected = set(expected_keys)
    candidates = mapping_candidates(payload)
    if not candidates:
        return None
    best = max(candidates, key=lambda item: len(expected.intersection(item.keys())))
    return best if expected.intersection(best.keys()) else None


def contains_prohibited(name: str) -> bool:
    normalized = name.lower().replace("-", "_").replace(" ", "_")
    return any(
        value in normalized
        for value in ("pass_fail", "dimethylacetamide", "peak_table", "sdf")
    )


def classify_fields(field_map: Mapping[str, Any] | None, expected_keys: list[str]) -> tuple[list[dict[str, str]], dict[str, Any]]:
    rows: list[dict[str, str]] = []
    if field_map is None:
        for key in expected_keys:
            rows.append({"expected_key": key, "classification": "not_exposed_by_get_contract"})
        return rows, {
            "exact_system_name_keys_exposed": False,
            "all_43_values_blank": False,
            "prohibited_keys_observed": [],
        }
    keys = list(field_map.keys())
    lower = {key.lower(): key for key in keys if isinstance(key, str)}
    for expected in expected_keys:
        if expected in field_map:
            classification = "observed_exact"
        elif expected.lower() in lower:
            classification = "renamed"
        else:
            classification = "missing"
        rows.append({"expected_key": expected, "classification": classification})
    exact_values = [field_map[key] for key in expected_keys if key in field_map]
    blank = len(exact_values) == 43 and all(value in (None, "") for value in exact_values)
    prohibited = sorted(str(key) for key in keys if isinstance(key, str) and contains_prohibited(key))
    return rows, {
        "exact_system_name_keys_exposed": all(row["classification"] == "observed_exact" for row in rows),
        "all_43_values_blank": blank,
        "prohibited_keys_observed": prohibited,
    }


def write_field_comparison(rows: list[dict[str, str]]) -> None:
    with (EVIDENCE_ROOT / "field_key_comparison.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=("expected_key", "classification"), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_historical_requests() -> list[dict[str, Any]]:
    path = EVIDENCE_ROOT / "request_ledger_sanitized.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ControlledStop("historical_oauth_404_ledger_missing_or_invalid") from exc
    requests = payload.get("requests")
    if not isinstance(requests, list) or len(requests) != 1:
        raise ControlledStop("oauth_retry_already_consumed_or_history_not_exact")
    request = requests[0]
    expected = {
        "sequence": 1,
        "method": "POST",
        "endpoint_template": HISTORICAL_TOKEN_PATH,
        "http_status": 404,
        "content_type": "application/json",
        "allowed_origin": True,
        "redirect_escaped_allowed_origin": False,
    }
    if request != expected:
        raise ControlledStop("historical_oauth_404_ledger_not_exact")
    return [{**request, "phase": "historical_incorrect_endpoint"}]


def save_ledger(transport: GuardedTransport, historical_requests: list[dict[str, Any]]) -> None:
    current = [
        {**request, "phase": "authoritative_retry_and_read_only_confirmation"}
        for request in transport.ledger
    ]
    requests = historical_requests + current
    for sequence, request in enumerate(requests, start=1):
        request["sequence"] = sequence
    write_json(
        EVIDENCE_ROOT / "request_ledger_sanitized.json",
        {
            "schema_version": 2,
            "allowed_origin": ALLOWED_ORIGIN,
            "requests": requests,
            "method_counts": dict(Counter(request["method"] for request in requests)),
            "authorization_headers_recorded": False,
            "credentials_or_tokens_recorded": False,
            "internal_object_ids_recorded": False,
        },
    )


def main() -> int:
    transport = GuardedTransport()
    historical_requests: list[dict[str, Any]] = []
    summary: dict[str, Any] = {
        "schema_version": 1,
        "origin_preflight": "not_run",
        "oauth": {"result": "not_run"},
        "identity": {"classification": "not_run"},
        "worksheet_get": {"result": "not_run"},
        "worksheet_contract": {"classification": "not_run"},
        "safety": {
            "patch_requests": 0,
            "put_requests": 0,
            "delete_requests": 0,
            "non_token_post_requests": 0,
            "live_qbench_requests": 0,
            "qbench_objects_changed": False,
            "analytical_results_changed": False,
            "publish_or_qc_review_performed": False,
            "pass_fail_artifact_introduced": False,
        },
    }
    try:
        historical_requests = load_historical_requests()
        credentials = load_credentials()
        local = load_local_identity()
        expected_keys = load_expected_keys()
        summary["origin_preflight"] = "passed_exact_sandbox_origin"
        access_token = QBenchTokenClient(
            credentials,
            TOKEN_PATH,
            opener=transport.token_opener,
            timeout_seconds=20.0,
        ).exchange()
        summary["oauth"] = {
            "result": "succeeded",
            **transport.token_http_metadata,
            "token_type": "Bearer",
            "approximate_expiration_seconds": max(
                1, int(access_token.expires_at_epoch - time.time())
            ),
            "origin": ALLOWED_ORIGIN,
            "credentials_or_token_exposed": False,
            "token_persisted": False,
            "token_request_attempts": 1,
            "client_assertion_persisted_or_displayed_by_runner": False,
            "request_contract": {
                "method": "POST",
                "endpoint_template": TOKEN_PATH,
                "content_type": "multipart/form-data",
                "fields": ["assertion", "grant_type"],
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            },
        }

        test_path = TEST_PATH_TEMPLATE.format(test_id=local.test_id)
        test_raw, test_payload, test_status, test_content_type = transport.get_json(
            test_path, TEST_PATH_TEMPLATE, access_token.value
        )
        RAW_ROOT.mkdir(parents=True, exist_ok=True)
        (RAW_ROOT / "test_response.json").write_bytes(test_raw)
        identity = classify_identity(test_payload, local)
        summary["identity"] = identity
        summary["test_get"] = {
            "result": "succeeded",
            "http_status": test_status,
            "content_type": test_content_type,
            "endpoint_template": TEST_PATH_TEMPLATE,
            "raw_sha256": sha256_bytes(test_raw),
        }
        if identity["classification"] != "passed_exact_runtime_test":
            raise ControlledStop("read_only_api_identity_insufficient")

        worksheet_path = WORKSHEET_PATH_TEMPLATE.format(test_id=local.test_id)
        worksheet_raw, worksheet_payload, worksheet_status, worksheet_content_type = transport.get_json(
            worksheet_path, WORKSHEET_PATH_TEMPLATE, access_token.value
        )
        (RAW_ROOT / "worksheet_response.json").write_bytes(worksheet_raw)
        field_map = extract_field_mapping(worksheet_payload, expected_keys)
        rows, contract_details = classify_fields(field_map, expected_keys)
        counts = dict(Counter(row["classification"] for row in rows))

        sanitized_payload = {
            "schema_version": 1,
            "method": "GET",
            "endpoint_template": WORKSHEET_PATH_TEMPLATE,
            "worksheet_fields": dict(field_map) if field_map is not None else {},
        }
        sanitized_path = EVIDENCE_ROOT / "worksheet_response_sanitized.json"
        write_json(sanitized_path, sanitized_payload)
        write_field_comparison(rows)
        sanitized_hash = sha256_bytes(sanitized_path.read_bytes())
        raw_hash = sha256_bytes(worksheet_raw)
        (EVIDENCE_ROOT / "raw_response_sha256.txt").write_text(
            raw_hash + "\n", encoding="ascii", newline="\n"
        )

        if contract_details["exact_system_name_keys_exposed"] and contract_details["all_43_values_blank"]:
            classification = "passed_43_of_43"
            destination_state = "runtime_instantiation_and_read_only_api_confirmation_passed"
            patch_key_state = "read_only_get_confirmed_exact_system_names_pending_patch_proof"
        elif field_map is None:
            classification = "partial_values_only"
            destination_state = "runtime_instantiation_passed_read_only_get_keys_not_exposed"
            patch_key_state = "unresolved_get_does_not_expose_exact_keys"
        else:
            classification = "failed_exact_key_or_blank_contract"
            destination_state = "runtime_instantiation_passed_read_only_api_confirmation_failed"
            patch_key_state = "unresolved_read_only_get_contract_failed"

        summary["worksheet_get"] = {
            "result": "succeeded",
            "method": "GET",
            "endpoint_template": WORKSHEET_PATH_TEMPLATE,
            "http_status": worksheet_status,
            "content_type": worksheet_content_type,
            "raw_response_sha256": raw_hash,
            "sanitized_derivative_filename": "worksheet_response_sanitized.json",
            "sanitized_derivative_sha256": sanitized_hash,
        }
        summary["worksheet_contract"] = {
            "classification": classification,
            "classification_counts": {
                name: counts.get(name, 0)
                for name in (
                    "observed_exact",
                    "missing",
                    "renamed",
                    "duplicated",
                    "present_but_unreadable",
                    "not_exposed_by_get_contract",
                )
            },
            **contract_details,
            "destination_contract_proven": destination_state,
            "analyte_patch_key_contract": patch_key_state,
            "atomicity_classification": "api_patch_unresolved",
        }
        summary["result"] = "completed"
    except ControlledStop as exc:
        if (
            summary["oauth"].get("result") == "not_run"
            and transport.ledger
            and transport.ledger[0]["method"] == "POST"
            and transport.ledger[0]["endpoint_template"] == TOKEN_PATH
        ):
            summary["oauth"] = {
                "result": "failed",
                "http_status": transport.ledger[0]["http_status"],
                "content_type": transport.ledger[0]["content_type"],
                "token_type": "not_available",
                "approximate_expiration_seconds": "not_available",
                "origin": ALLOWED_ORIGIN,
                "credentials_or_token_exposed": False,
                "token_persisted": False,
                "token_request_attempts": 1,
                "client_assertion_persisted_or_displayed_by_runner": False,
                "request_contract": {
                    "method": "POST",
                    "endpoint_template": TOKEN_PATH,
                    "content_type": "multipart/form-data",
                    "fields": ["assertion", "grant_type"],
                    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                },
            }
        summary["result"] = "controlled_stop"
        summary["stop_reason"] = str(exc)
    except Exception:
        summary["result"] = "controlled_stop"
        summary["stop_reason"] = "sanitized_unexpected_error"
    finally:
        if transport.ledger:
            save_ledger(transport, historical_requests)
        write_json(EVIDENCE_ROOT / "run_summary_sanitized.json", summary)

    result = summary.get("result")
    print(f"read_only_api_confirmation={result}")
    print(f"origin_preflight={summary.get('origin_preflight')}")
    print(f"oauth_result={summary.get('oauth', {}).get('result')}")
    print(f"identity_classification={summary.get('identity', {}).get('classification')}")
    print(f"worksheet_contract={summary.get('worksheet_contract', {}).get('classification')}")
    print(f"request_count={len(transport.ledger)}")
    return 0 if result == "completed" else 2


if __name__ == "__main__":
    raise SystemExit(main())
