from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import ssl
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, Request, build_opener


APP_VERSION = "0.1.0"
ALLOWED_BASE_URL = "https://ait-sandbox.qbench.net"
REPORTABLE_ANALYTE_COUNT = 23
COMPOUND_RESULTS_COUNT = 24
PEAK_TABLE_COUNT = 34
PASS_FAIL_PATTERN = re.compile(r"pass[\s_-]*fail", re.IGNORECASE)
BEARER_PATTERN = re.compile(r"(?i)(authorization\s*[:=]\s*bearer\s+|bearer\s+)[^\s,;]+")
URL_PATTERN = re.compile(r"https?://[^\s\]\[(){}<>\"']+", re.IGNORECASE)
CELL_PATTERN = re.compile(r"^(?:(?P<sheet>[^!]+)!)?(?P<start>[A-Z]+\d+)(?::(?P<end>[A-Z]+\d+))?$")
INDEXED_NAME_PATTERN = re.compile(r"^(?P<base>[^\[]+)\[(?P<index>\d+)\]$")


class PublisherError(RuntimeError):
    """Base error whose message is safe for a user-facing log."""


class SecurityError(PublisherError):
    pass


class ConfigurationError(PublisherError):
    pass


class SchemaError(PublisherError):
    pass


class VerificationError(PublisherError):
    pass


class AmbiguousPatchOutcome(PublisherError):
    pass


class ApiError(PublisherError):
    def __init__(self, operation: str, status: int | None = None):
        suffix = f" with HTTP {status}" if status is not None else ""
        super().__init__(f"{operation} failed{suffix}; response details suppressed")
        self.status = status


class Action(str, Enum):
    PUBLISH = "PUBLISH"
    NO_CHANGE = "NO CHANGE"
    BLOCKED = "BLOCKED"
    REAUTHORIZATION_REQUIRED = "REAUTHORIZATION REQUIRED"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def evidence_id(kind: str, value: Any) -> str:
    return f"{kind}_sha256:{sha256_text(canonical_qbench_id(value))[:16]}"


def sanitize_text(value: Any, token: str | None = None) -> str:
    text = str(value)
    if token:
        text = text.replace(token, "[REDACTED_TOKEN]")
    text = BEARER_PATTERN.sub("[REDACTED_AUTHORIZATION]", text)
    text = URL_PATTERN.sub("[REDACTED_URL]", text)
    return text


def canonical_qbench_id(value: Any) -> str:
    if isinstance(value, bool) or value is None:
        raise SchemaError("QBench identifier must be a nonblank string or integer")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str) and value != "":
        return value
    raise SchemaError("QBench identifier must be a nonblank string or integer")


def contains_forbidden_field(name: str) -> bool:
    return bool(PASS_FAIL_PATTERN.search(name)) or name.lower().replace("-", "_") in {
        "passfail",
        "test_result",
        "test_results",
        "compliance_result",
    }


def is_native_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def exact_true(value: Any) -> bool:
    return value is True or value == "TRUE"


def validate_base_url(value: str) -> str:
    candidate = value[:-1] if value.endswith("/") else value
    parsed = urlsplit(candidate)
    if candidate != ALLOWED_BASE_URL:
        raise SecurityError("QBench base URL rejected; only the task Sandbox hostname is allowed")
    if (
        parsed.scheme != "https"
        or parsed.hostname != "ait-sandbox.qbench.net"
        or parsed.port not in (None, 443)
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
    ):
        raise SecurityError("QBench base URL rejected by the exact hostname allowlist")
    return candidate


def load_token(secrets_file: Path | None = None, environ: Mapping[str, str] | None = None) -> str:
    env = os.environ if environ is None else environ
    token = env.get("QBENCH_SANDBOX_TOKEN", "")
    if token:
        return token
    if secrets_file is not None:
        try:
            for raw_line in secrets_file.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, candidate = line.split("=", 1)
                if key == "QBENCH_SANDBOX_TOKEN" and candidate:
                    return candidate
        except OSError as exc:
            raise ConfigurationError("Local secrets file could not be read") from exc
    raise ConfigurationError(
        "Sandbox API credential is unavailable; set QBENCH_SANDBOX_TOKEN or use an ignored local secrets file"
    )


class NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


@dataclass(frozen=True)
class HttpResponse:
    status: int
    body: Any


@dataclass(frozen=True)
class BatchRecord:
    batch_id: str
    display_name: str
    test_ids: tuple[str, ...]
    worksheet_id: str
    worksheet_json: Mapping[str, Any]


@dataclass(frozen=True)
class TestRecord:
    test_id: str
    batch_id: str
    sample_id: str
    assay_id: str
    assay_name: str
    workflow: str
    worksheet_id: str
    worksheet_json: Mapping[str, Any]


def _unwrap_response(payload: Any) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise SchemaError("QBench response must be a JSON object")
    data = payload.get("data")
    if isinstance(data, Mapping) and not any(k in payload for k in ("id", "batch_id", "test_ids")):
        return data
    return payload


def _parse_worksheet_json(value: Any) -> Mapping[str, Any]:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as exc:
            raise SchemaError("worksheet_json is not valid JSON") from exc
    if not isinstance(value, Mapping):
        raise SchemaError("worksheet_json must be a JSON object")
    if not isinstance(value.get("data"), Mapping):
        raise SchemaError("worksheet_json.data must be a sheet mapping")
    qb_config = value.get("qb_config")
    if not isinstance(qb_config, Mapping) or not isinstance(qb_config.get("named_cells"), Mapping):
        raise SchemaError("worksheet_json must contain qb_config.named_cells")
    return value


def _nested_value(payload: Mapping[str, Any], key: str, nested: str) -> Any:
    direct = payload.get(key)
    if direct is not None:
        return direct
    parent_name, child_name = nested.split(".", 1)
    parent = payload.get(parent_name)
    return parent.get(child_name) if isinstance(parent, Mapping) else None


class QBenchClient:
    """Minimal documented-endpoint client. GET retries are bounded; PATCH never retries."""

    def __init__(
        self,
        base_url: str,
        token: str,
        *,
        timeout_seconds: float = 20.0,
        get_retries: int = 2,
        opener: Callable[[Request, float], HttpResponse] | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ):
        self.base_url = validate_base_url(base_url)
        if not token:
            raise ConfigurationError("Sandbox token is blank")
        self._token = token
        self.timeout_seconds = timeout_seconds
        self.get_retries = max(0, min(get_retries, 3))
        self._sleep = sleep
        self._opener = opener or self._urlopen

    def _urlopen(self, request: Request, timeout: float) -> HttpResponse:
        context = ssl.create_default_context()
        opener = build_opener(NoRedirectHandler(), HTTPSHandler(context=context))
        with opener.open(request, timeout=timeout) as response:
            raw = response.read()
            try:
                body = json.loads(raw.decode("utf-8")) if raw else {}
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise SchemaError("QBench response body is not valid UTF-8 JSON") from exc
            return HttpResponse(status=response.status, body=body)

    def _request(self, method: str, path: str, payload: Mapping[str, Any] | None, operation: str) -> Any:
        if not path.startswith("/qbench/api/v1/") or "http" in path.lower():
            raise SecurityError("API path rejected")
        url = self.base_url + path
        body = None if payload is None else json.dumps(payload, separators=(",", ":")).encode("utf-8")
        headers = {"Accept": "application/json", "Authorization": f"Bearer {self._token}"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = Request(url, data=body, headers=headers, method=method)
        attempts = self.get_retries + 1 if method == "GET" else 1
        for attempt in range(attempts):
            try:
                response = self._opener(request, self.timeout_seconds)
                if response.status in (429, 500, 502, 503, 504) and method == "GET" and attempt + 1 < attempts:
                    self._sleep(0.05 * (2**attempt))
                    continue
                if not 200 <= response.status < 300:
                    raise ApiError(operation, response.status)
                return response.body
            except HTTPError as exc:
                if method == "GET" and exc.code in (429, 500, 502, 503, 504) and attempt + 1 < attempts:
                    self._sleep(0.05 * (2**attempt))
                    continue
                raise ApiError(operation, exc.code) from None
            except (TimeoutError, URLError, OSError) as exc:
                if method == "GET" and attempt + 1 < attempts:
                    self._sleep(0.05 * (2**attempt))
                    continue
                if method == "PATCH":
                    raise AmbiguousPatchOutcome(
                        "PATCH outcome is unknown after submission; no retry was attempted"
                    ) from None
                raise ApiError(operation) from None
        raise ApiError(operation)

    def get_batch(self, batch_id: Any) -> BatchRecord:
        expected_id = canonical_qbench_id(batch_id)
        payload = _unwrap_response(
            self._request("GET", f"/qbench/api/v1/batch/{quote(expected_id, safe='')}", None, "GET Batch")
        )
        returned_id = canonical_qbench_id(payload.get("id", payload.get("batch_id")))
        if returned_id != expected_id:
            raise SchemaError("GET Batch returned a different Batch ID")
        display_name = payload.get("display_name", payload.get("name"))
        if not isinstance(display_name, str) or display_name == "":
            raise SchemaError("Batch display name is missing")
        test_ids_raw = payload.get("test_ids")
        if not isinstance(test_ids_raw, list):
            raise SchemaError("Batch test_ids must be a JSON array")
        test_ids = tuple(canonical_qbench_id(item) for item in test_ids_raw)
        worksheet_id = canonical_qbench_id(payload.get("worksheet_id"))
        worksheet_json = _parse_worksheet_json(payload.get("worksheet_json"))
        return BatchRecord(returned_id, display_name, test_ids, worksheet_id, worksheet_json)

    def get_test(self, test_id: Any) -> TestRecord:
        expected_id = canonical_qbench_id(test_id)
        payload = _unwrap_response(
            self._request("GET", f"/qbench/api/v1/test/{quote(expected_id, safe='')}", None, "GET Test")
        )
        returned_id = canonical_qbench_id(payload.get("id", payload.get("test_id")))
        if returned_id != expected_id:
            raise SchemaError("GET Test returned a different Test ID")
        batch_id = canonical_qbench_id(_nested_value(payload, "batch_id", "batch.id"))
        sample_id = canonical_qbench_id(_nested_value(payload, "sample_id", "sample.id"))
        assay_id = canonical_qbench_id(_nested_value(payload, "assay_id", "assay.id"))
        assay_name = payload.get("assay_name") or _nested_value(payload, "missing_assay_name", "assay.name")
        workflow = payload.get("workflow", payload.get("workflow_name"))
        if not isinstance(assay_name, str) or assay_name == "":
            raise SchemaError("Test assay name is missing")
        if not isinstance(workflow, str) or workflow == "":
            raise SchemaError("Test workflow is missing")
        worksheet_id = canonical_qbench_id(payload.get("worksheet_id"))
        worksheet_json = _parse_worksheet_json(payload.get("worksheet_json"))
        return TestRecord(
            returned_id,
            batch_id,
            sample_id,
            assay_id,
            assay_name,
            workflow,
            worksheet_id,
            worksheet_json,
        )

    def patch_test_worksheet(self, test_id: Any, data: Mapping[str, Any], reason: str) -> Any:
        exact_id = canonical_qbench_id(test_id)
        if not data:
            raise ConfigurationError("PATCH data must not be empty")
        for name, value in data.items():
            if contains_forbidden_field(name):
                raise SecurityError("PATCH contains a prohibited Pass/Fail or result field")
            if isinstance(value, str) and value.startswith("="):
                raise SecurityError("Formula-like input text is prohibited")
        allowed_reasons = (
            "Reviewed Terpenes Batch publish; source hash ",
            "Prompt 5B controlled rollback; source hash ",
            "Prompt 5B disposable Sandbox API probe",
            "Prompt 5B disposable Sandbox API rollback",
        )
        if not isinstance(reason, str) or not reason.startswith(allowed_reasons):
            raise ConfigurationError("PATCH update reason does not match the controlled contract")
        return self._request(
            "PATCH",
            f"/qbench/api/v1/test/{quote(exact_id, safe='')}/worksheet",
            {"data": dict(data), "qbench_update_reason": reason},
            "PATCH Test Worksheet",
        )


def column_number(letters: str) -> int:
    value = 0
    for letter in letters:
        value = value * 26 + (ord(letter) - ord("A") + 1)
    return value


def column_letters(number: int) -> str:
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(ord("A") + remainder) + result
    return result


def split_address(address: str) -> tuple[str, int]:
    match = re.fullmatch(r"([A-Z]+)(\d+)", address)
    if not match:
        raise SchemaError("Worksheet cell address is invalid")
    return match.group(1), int(match.group(2))


def parse_reference(reference: str) -> tuple[str | None, str, str]:
    match = CELL_PATTERN.fullmatch(reference)
    if not match:
        raise SchemaError("Worksheet reference is invalid")
    return match.group("sheet"), match.group("start"), match.group("end") or match.group("start")


def address_in_range(target: str, start: str, end: str) -> bool:
    tc, tr = split_address(target)
    sc, sr = split_address(start)
    ec, er = split_address(end)
    return column_number(sc) <= column_number(tc) <= column_number(ec) and sr <= tr <= er


class WorksheetDocument:
    def __init__(self, payload: Mapping[str, Any]):
        self.payload = _parse_worksheet_json(payload)
        self.sheets = self.payload["data"]
        self.named_cells = self.payload["qb_config"]["named_cells"]

    def named_reference(self, name: str) -> str:
        entry = self.named_cells.get(name)
        if not isinstance(entry, Mapping) or not isinstance(entry.get("cell"), str):
            raise SchemaError(f"Required named cell is missing: {name}")
        return entry["cell"]

    def get_cell(self, reference: str, default_sheet: str | None = None) -> Any:
        sheet, start, end = parse_reference(reference)
        if start != end:
            raise SchemaError("Expected a scalar worksheet cell")
        sheet = sheet or default_sheet
        if not sheet or sheet not in self.sheets:
            raise SchemaError("Worksheet sheet is missing")
        column, row = split_address(start)
        grid = self.sheets[sheet]
        if not isinstance(grid, list):
            raise SchemaError("Worksheet sheet data must be a row array")
        row_index, column_index = row - 1, column_number(column) - 1
        try:
            return grid[row_index][column_index]
        except (IndexError, TypeError):
            return None

    def set_cell(self, reference: str, value: Any, default_sheet: str | None = None) -> None:
        sheet, start, end = parse_reference(reference)
        if start != end:
            raise SchemaError("Expected a scalar worksheet cell")
        sheet = sheet or default_sheet
        if not sheet or sheet not in self.sheets:
            raise SchemaError("Worksheet sheet is missing")
        column, row = split_address(start)
        grid = self.sheets[sheet]
        row_index, column_index = row - 1, column_number(column) - 1
        while len(grid) <= row_index:
            grid.append([])
        while len(grid[row_index]) <= column_index:
            grid[row_index].append("")
        grid[row_index][column_index] = value

    def named_value_at_row(self, name: str, worksheet_row: int) -> Any:
        reference = self.named_reference(name)
        sheet, start, end = parse_reference(reference)
        start_col, start_row = split_address(start)
        end_col, end_row = split_address(end)
        if start_col != end_col or not start_row <= worksheet_row <= end_row:
            raise SchemaError(f"Named cell does not cover the required row: {name}")
        return self.get_cell(f"{sheet}!{start_col}{worksheet_row}")

    def formula_manifest(self) -> dict[str, str]:
        formulas: dict[str, str] = {}
        for sheet_name, rows in self.sheets.items():
            for row_index, row in enumerate(rows, start=1):
                for column_index, value in enumerate(row, start=1):
                    if isinstance(value, str) and value.startswith("="):
                        formulas[f"{sheet_name}!{column_letters(column_index)}{row_index}"] = value
        return formulas

    def unrelated_digest(self, excluded_references: Iterable[str]) -> str:
        excluded = set(excluded_references)
        retained: list[tuple[str, Any]] = []
        for sheet_name, rows in self.sheets.items():
            for row_index, row in enumerate(rows, start=1):
                for column_index, value in enumerate(row, start=1):
                    ref = f"{sheet_name}!{column_letters(column_index)}{row_index}"
                    if ref not in excluded:
                        retained.append((ref, value))
        return sha256_text(json.dumps(retained, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


@dataclass(frozen=True)
class FieldSpec:
    sequence: int
    source_publish_column: str
    source_publish_cell: str
    source_header: str
    source_named_range: str
    destination_named_cell: str
    destination_cell: str
    transfer_type: str
    required: str
    constraint: str

    @property
    def base_named_cell(self) -> str:
        match = INDEXED_NAME_PATTERN.fullmatch(self.destination_named_cell)
        return match.group("base") if match else self.destination_named_cell


def load_mapping(path: Path) -> tuple[FieldSpec, ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    fields: list[FieldSpec] = []
    for row in rows:
        try:
            fields.append(
                FieldSpec(
                    sequence=int(row["sequence"]),
                    source_publish_column=row["source_publish_column"],
                    source_publish_cell=row["source_publish_cell"],
                    source_header=row["source_header"],
                    source_named_range=row["source_named_range"],
                    destination_named_cell=row["destination_named_cell"],
                    destination_cell=row["destination_cell"],
                    transfer_type=row["transfer_type"],
                    required=row["required"],
                    constraint=row.get("type_or_constraint", row.get("constraint", "")),
                )
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ConfigurationError("Field mapping CSV is malformed") from exc
    if len(fields) != 43 or [item.sequence for item in fields] != list(range(1, 44)):
        raise ConfigurationError("Field mapping must contain exactly 43 ordered entries")
    names = [item.destination_named_cell for item in fields]
    cells = [item.destination_cell for item in fields]
    if len(set(names)) != len(names) or len(set(cells)) != len(cells):
        raise ConfigurationError("Field mapping contains duplicate destinations")
    if any(contains_forbidden_field(item.destination_named_cell) for item in fields):
        raise SecurityError("Field mapping contains a prohibited Pass/Fail or result field")
    if any("dimethylacetamide" in item.destination_named_cell.lower() for item in fields):
        raise SecurityError("Dimethylacetamide must not be a reportable destination")
    return tuple(fields)


class DestinationContract:
    @staticmethod
    def issues(document: WorksheetDocument, fields: Sequence[FieldSpec]) -> list[str]:
        issues: list[str] = []
        exact_named_refs: dict[str, list[str]] = {}
        for name, entry in document.named_cells.items():
            if isinstance(entry, Mapping) and isinstance(entry.get("cell"), str):
                exact_named_refs.setdefault(entry["cell"], []).append(name)
                if contains_forbidden_field(name):
                    issues.append("worksheet_contains_prohibited_pass_fail_named_cell")
        for spec in fields:
            try:
                base_reference = document.named_reference(spec.base_named_cell)
                base_sheet, base_start, base_end = parse_reference(base_reference)
                target_sheet, target_start, target_end = parse_reference(spec.destination_cell)
                if target_start != target_end:
                    issues.append(f"destination_not_scalar:{spec.destination_named_cell}")
                    continue
                if base_sheet != target_sheet or not address_in_range(target_start, base_start, base_end):
                    issues.append(f"destination_named_cell_mismatch:{spec.destination_named_cell}")
                value = document.get_cell(spec.destination_cell)
                if isinstance(value, str) and value.startswith("="):
                    issues.append(f"formula_owned_destination:{spec.destination_named_cell}")
                exact_matches = exact_named_refs.get(spec.destination_cell, [])
                if len(exact_matches) > 1:
                    issues.append(f"ambiguous_destination:{spec.destination_named_cell}")
            except SchemaError:
                issues.append(f"missing_destination_named_cell:{spec.destination_named_cell}")
        return sorted(set(issues))

    @staticmethod
    def values(document: WorksheetDocument, fields: Sequence[FieldSpec]) -> dict[str, Any]:
        return {spec.destination_named_cell: document.get_cell(spec.destination_cell) for spec in fields}


@dataclass(frozen=True)
class SourceRow:
    worksheet_row: int
    test_id: str | None
    sample_id: str | None
    source_hash: str | None
    reviewed_source_hash: str | None
    last_published_source_hash: str | None
    reviewer_id: str | None
    authorized_at: str | None
    proposed: Mapping[str, Any]
    gate_errors: tuple[str, ...]
    reauthorization_errors: tuple[str, ...]


class BatchSourceParser:
    AUTHORIZATION_RANGES = {
        "authorization": "terpenes_batch_publish_authorization",
        "reviewer": "terpenes_batch_publish_authorized_by",
        "authorized_at": "terpenes_batch_publish_authorized_at",
        "reviewed_hash": "terpenes_batch_publish_reviewed_source_row_hash",
        "last_hash": "terpenes_batch_last_published_source_row_hash",
    }

    def __init__(self, document: WorksheetDocument, fields: Sequence[FieldSpec]):
        self.document = document
        self.fields = fields

    def _value(self, sheet: str, column: str, row: int) -> Any:
        return self.document.get_cell(f"{sheet}!{column}{row}")

    def _authorization_values(self, row: int, errors: list[str]) -> dict[str, Any]:
        values: dict[str, Any] = {}
        for key, name in self.AUTHORIZATION_RANGES.items():
            try:
                values[key] = self.document.named_value_at_row(name, row)
            except SchemaError:
                errors.append(f"missing_batch_authorization_contract:{name}")
                values[key] = None
        return values

    def parse(self) -> tuple[SourceRow, ...]:
        try:
            publish_reference = self.document.named_reference("terpenes_batch_publish_table")
            publish_sheet, publish_start, publish_end = parse_reference(publish_reference)
            _, start_row = split_address(publish_start)
            _, end_row = split_address(publish_end)
        except SchemaError as exc:
            raise SchemaError("Batch Publish table contract is missing") from exc
        if publish_sheet != "Publish":
            raise SchemaError("Batch Publish table must be on the Publish sheet")
        rows: list[SourceRow] = []
        for row in range(max(2, start_row + 1), end_row + 1):
            raw_test_id = self._value("Publish", "A", row)
            row_has_content = any(
                self._value("Publish", column_letters(column), row) not in (None, "")
                for column in range(1, column_number("BI") + 1)
            )
            if not row_has_content:
                continue
            errors: list[str] = []
            reauth: list[str] = []
            try:
                test_id = canonical_qbench_id(raw_test_id)
            except SchemaError:
                test_id = None
                errors.append("invalid_test_id")
            sample_raw = self._value("Publish", "B", row)
            try:
                sample_id = canonical_qbench_id(sample_raw)
            except SchemaError:
                sample_id = None
                errors.append("missing_sample_id")
            source_hash_raw = self._value("Publish", "AT", row)
            source_hash = source_hash_raw if isinstance(source_hash_raw, str) and source_hash_raw != "" else None
            if source_hash is None:
                errors.append("missing_source_hash")
            auth = self._authorization_values(row, errors)
            reviewed_hash = auth["reviewed_hash"] if isinstance(auth["reviewed_hash"], str) else None
            last_hash = auth["last_hash"] if isinstance(auth["last_hash"], str) and auth["last_hash"] else None
            if auth["authorization"] != "Authorized":
                errors.append("reviewer_authorization_off")
            reviewer = auth["reviewer"] if isinstance(auth["reviewer"], str) and auth["reviewer"] else None
            if reviewer is None:
                errors.append("reviewer_identifier_missing")
            authorized_at = auth["authorized_at"] if isinstance(auth["authorized_at"], str) and auth["authorized_at"] else None
            if authorized_at is None:
                errors.append("review_timestamp_missing")
            if reviewed_hash is None or source_hash != reviewed_hash:
                reauth.append("row_changed_since_review_authorization")
            proposed = {
                spec.destination_named_cell: self._value(
                    "Publish", spec.source_publish_column, row
                )
                for spec in self.fields
            }
            self._validate_publish_row(row, proposed, errors)
            self._validate_import_row(row, test_id, source_hash, proposed, errors)
            rows.append(
                SourceRow(
                    row,
                    test_id,
                    sample_id,
                    source_hash,
                    reviewed_hash,
                    last_hash,
                    reviewer,
                    authorized_at,
                    proposed,
                    tuple(sorted(set(errors))),
                    tuple(sorted(set(reauth))),
                )
            )
        return tuple(rows)

    def _validate_publish_row(self, row: int, proposed: Mapping[str, Any], errors: list[str]) -> None:
        analytes = [proposed[spec.destination_named_cell] for spec in self.fields[:23]]
        if len(analytes) != REPORTABLE_ANALYTE_COUNT or not all(is_native_number(value) for value in analytes):
            errors.append("reportable_analytes_not_23_native_numeric_values")
        if self._value("Publish", "AX", row) != "Valid":
            errors.append("publish_import_validation_not_valid")
        if self._value("Publish", "AY", row) != "Accepted":
            errors.append("batch_qc_disposition_not_accepted")
        for column, label in (("AV", "counts_not_confirmed"), ("AZ", "source_metadata_incomplete"),
                              ("BA", "preparation_metadata_incomplete"), ("BB", "publish_inputs_incomplete"),
                              ("BC", "publish_ready_not_true")):
            if not exact_true(self._value("Publish", column, row)):
                errors.append(label)
        if self._value("Publish", "AW", row) != "Reviewed":
            errors.append("integration_review_not_reviewed")
        if not is_native_number(self._value("Publish", "AU", row)):
            errors.append("dimethylacetamide_audit_not_numeric")
        required_keys = {spec.destination_named_cell: spec for spec in self.fields}
        for name, value in proposed.items():
            spec = required_keys[name]
            if spec.required == "true" and value in (None, ""):
                errors.append(f"required_publish_value_missing:{name}")
            if isinstance(value, str) and value.startswith("="):
                errors.append(f"formula_like_publish_input:{name}")
        for position in (23, 24):
            if not is_native_number(list(proposed.values())[position]) or list(proposed.values())[position] <= 0:
                errors.append("preparation_value_not_positive_numeric")
        df_value = proposed.get("df")
        mode = proposed.get("df_application_mode")
        if mode not in ("already_applied_by_labsolutions", "apply_in_qbench"):
            errors.append("invalid_df_application_mode")
        if mode == "apply_in_qbench" and (not is_native_number(df_value) or df_value <= 0):
            errors.append("df_not_positive_numeric")
        if proposed.get("labsolutions_conc_unit") != "ug/mL":
            errors.append("labsolutions_conc_unit_not_ug_per_ml")
        if not exact_true(proposed.get("labsolutions_conc_unit_confirmed")):
            errors.append("unit_confirmation_not_true")
        if not exact_true(proposed.get("preparation_values_confirmed")):
            errors.append("preparation_confirmation_not_true")
        if proposed.get("batch_qc_disposition") != "Accepted":
            errors.append("destination_disposition_not_accepted")
        if not exact_true(proposed.get("publish_ready")):
            errors.append("destination_publish_ready_not_true")

    def _validate_import_row(
        self,
        publish_row: int,
        test_id: str | None,
        source_hash: str | None,
        proposed: Mapping[str, Any],
        errors: list[str],
    ) -> None:
        if test_id is None:
            return
        grid = self.document.sheets.get("Instrument Import")
        if not isinstance(grid, list):
            errors.append("instrument_import_sheet_missing")
            return
        matches: list[int] = []
        for import_row in range(2, len(grid) + 1):
            raw = self._value("Instrument Import", "E", import_row)
            try:
                if raw not in (None, "") and canonical_qbench_id(raw) == test_id:
                    matches.append(import_row)
            except SchemaError:
                continue
        if len(matches) != 1:
            errors.append("test_id_not_exactly_once_in_instrument_import")
            return
        row = matches[0]
        if self._value("Instrument Import", "AF", row) != "Valid":
            errors.append("import_af_not_valid")
        if self._value("Instrument Import", "AG", row) != "Import row valid":
            errors.append("import_ag_not_import_row_valid")
        if self._value("Instrument Import", "BE", row) != source_hash:
            errors.append("source_hash_mismatch_between_import_and_publish")
        import_analytes = [self._value("Instrument Import", column_letters(column), row) for column in range(34, 57)]
        publish_analytes = [proposed[spec.destination_named_cell] for spec in self.fields[:23]]
        if not all(is_native_number(value) for value in import_analytes) or import_analytes != publish_analytes:
            errors.append("import_and_publish_analytes_do_not_exactly_match")
        expected_counts = (("X", COMPOUND_RESULTS_COUNT), ("Y", PEAK_TABLE_COUNT), ("Z", REPORTABLE_ANALYTE_COUNT))
        if any(self._value("Instrument Import", column, row) != expected for column, expected in expected_counts):
            errors.append("instrument_import_counts_incorrect")
        if not is_native_number(self._value("Instrument Import", "AA", row)):
            errors.append("import_dimethylacetamide_audit_not_numeric")
        for column in ("H", "I"):
            value = self._value("Instrument Import", column, row)
            if not is_native_number(value) or value <= 0:
                errors.append("import_preparation_values_invalid")
        mode = self._value("Instrument Import", "K", row)
        if mode not in ("already_applied_by_labsolutions", "apply_in_qbench"):
            errors.append("import_df_application_mode_invalid")
        if mode == "apply_in_qbench":
            df_value = self._value("Instrument Import", "J", row)
            if not is_native_number(df_value) or df_value <= 0:
                errors.append("import_df_invalid")
        for column in ("N", "O", "P", "Q", "R", "T", "U", "V", "W", "BE"):
            if self._value("Instrument Import", column, row) in (None, ""):
                errors.append("import_source_metadata_incomplete")
        manual_integration = self._value("Instrument Import", "AC", row)
        if manual_integration not in ("Yes", "No"):
            errors.append("manual_integration_value_invalid")
        if manual_integration == "Yes" and self._value("Instrument Import", "AD", row) in (None, ""):
            errors.append("integration_reason_missing")
        if self._value("Instrument Import", "AE", row) != "Reviewed":
            errors.append("integration_review_not_reviewed")


@dataclass(frozen=True)
class PublisherConfig:
    required_batch_display_name_prefix: str
    expected_assay_ids: tuple[str, ...]
    expected_assay_names: tuple[str, ...]
    expected_workflows: tuple[str, ...]
    destination_contract_proven: bool
    atomicity_classification: str
    analyte_patch_key_contract: str

    @classmethod
    def from_path(cls, path: Path) -> "PublisherConfig":
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ConfigurationError("Publisher configuration could not be loaded") from exc
        return cls(
            str(payload.get("required_batch_display_name_prefix", "SBX_ONLY_")),
            tuple(str(value) for value in payload.get("expected_assay_ids", [])),
            tuple(str(value) for value in payload.get("expected_assay_names", [])),
            tuple(str(value) for value in payload.get("expected_workflows", [])),
            payload.get("destination_contract_proven") is True,
            str(payload.get("atomicity_classification", "api_patch_unresolved")),
            str(payload.get("analyte_patch_key_contract", "unresolved")),
        )

    def runtime_issues(self) -> list[str]:
        issues: list[str] = []
        if not self.required_batch_display_name_prefix:
            issues.append("synthetic_batch_name_prefix_not_configured")
        if not self.expected_assay_ids or not self.expected_assay_names or not self.expected_workflows:
            issues.append("expected_sandbox_assay_or_workflow_not_configured")
        if not self.destination_contract_proven:
            issues.append("saved_destination_contract_not_proven")
        if self.atomicity_classification != "api_patch_atomic":
            issues.append(f"direct_publish_not_allowed:{self.atomicity_classification}")
        if self.analyte_patch_key_contract not in ("indexed_scalar_named_cells", "range_named_cell"):
            issues.append("analyte_patch_key_contract_unresolved")
        return issues


@dataclass(frozen=True)
class GateResult:
    action: Action
    errors: tuple[str, ...]


@dataclass(frozen=True)
class PlanRow:
    worksheet_row: int
    test_id: str | None
    test_evidence_id: str | None
    sample_evidence_id: str | None
    source_hash: str | None
    reviewer_evidence_id: str | None
    action: Action
    errors: tuple[str, ...]
    old_values: Mapping[str, Any]
    proposed_values: Mapping[str, Any]
    formula_manifest: Mapping[str, str]
    unrelated_digest: str | None


@dataclass(frozen=True)
class PreparedPlan:
    timestamp: str
    batch_id: str
    batch_display_name: str
    batch_evidence_id: str
    rows: tuple[PlanRow, ...]

    @property
    def can_publish(self) -> bool:
        return bool(self.rows) and all(row.action in (Action.PUBLISH, Action.NO_CHANGE) for row in self.rows)


class StateStore:
    def __init__(self, path: Path):
        self.path = path

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"schema_version": 1, "tests": {}}
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ConfigurationError("Publisher state ledger could not be read") from exc
        if payload.get("schema_version") != 1 or not isinstance(payload.get("tests"), dict):
            raise ConfigurationError("Publisher state ledger schema is invalid")
        return payload

    def get_hash(self, test_id: str) -> str | None:
        payload = self._load()
        item = payload["tests"].get(evidence_id("test", test_id), {})
        value = item.get("source_hash") if isinstance(item, Mapping) else None
        return value if isinstance(value, str) and value else None

    def record(self, test_id: str, source_hash: str, audit_manifest_sha256: str = "pending") -> None:
        payload = self._load()
        payload["tests"][evidence_id("test", test_id)] = {
            "source_hash": source_hash,
            "published_at": utc_now(),
            "audit_manifest_sha256": audit_manifest_sha256,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(self.path)


class Publisher:
    def __init__(
        self,
        client: QBenchClient,
        fields: Sequence[FieldSpec],
        config: PublisherConfig,
        state: StateStore,
    ):
        self.client = client
        self.fields = tuple(fields)
        self.config = config
        self.state = state

    def prepare(self, batch_id: Any) -> PreparedPlan:
        batch = self.client.get_batch(batch_id)
        if not batch.display_name.startswith(self.config.required_batch_display_name_prefix):
            raise SecurityError("Selected Batch is not explicitly task-synthetic; no worksheet data was processed")
        batch_document = WorksheetDocument(batch.worksheet_json)
        source_rows = BatchSourceParser(batch_document, self.fields).parse()
        publish_counts = Counter(row.test_id for row in source_rows if row.test_id is not None)
        batch_counts = Counter(batch.test_ids)
        fetched: dict[str, TestRecord | PublisherError] = {}
        for row in source_rows:
            if row.test_id is not None and publish_counts[row.test_id] == 1 and batch_counts[row.test_id] == 1:
                try:
                    fetched[row.test_id] = self.client.get_test(row.test_id)
                except PublisherError as exc:
                    fetched[row.test_id] = exc
        plan_rows: list[PlanRow] = []
        global_runtime_issues = self.config.runtime_issues()
        for row in source_rows:
            errors = list(row.gate_errors)
            reauth = list(row.reauthorization_errors)
            old_values: Mapping[str, Any] = {}
            formulas: Mapping[str, str] = {}
            unrelated_digest: str | None = None
            test: TestRecord | None = None
            if row.test_id is None:
                errors.append("missing_test_id")
            else:
                if publish_counts[row.test_id] != 1:
                    errors.append("duplicate_test_id_in_publish_rows")
                if batch_counts[row.test_id] != 1:
                    errors.append("test_id_not_exactly_once_in_selected_batch")
                fetched_value = fetched.get(row.test_id)
                if isinstance(fetched_value, PublisherError):
                    errors.append(f"destination_test_read_failed:{type(fetched_value).__name__}")
                elif isinstance(fetched_value, TestRecord):
                    test = fetched_value
                else:
                    errors.append("destination_test_not_read")
            if test is not None:
                errors.extend(self._test_identity_issues(batch, row, test))
                test_document = WorksheetDocument(test.worksheet_json)
                errors.extend(DestinationContract.issues(test_document, self.fields))
                old_values = DestinationContract.values(test_document, self.fields)
                formulas = test_document.formula_manifest()
                unrelated_digest = test_document.unrelated_digest(spec.destination_cell for spec in self.fields)
                ledger_hash = self.state.get_hash(test.test_id)
                recorded_hash = row.last_published_source_hash or ledger_hash
                values_equal = dict(old_values) == dict(row.proposed)
                if recorded_hash:
                    if recorded_hash != row.source_hash:
                        reauth.append("source_hash_changed_after_prior_publish")
                    elif values_equal:
                        pass
                    else:
                        errors.append("published_hash_matches_but_destination_values_diverged")
                elif any(value not in (None, "") for value in old_values.values()):
                    errors.append("nonblank_destination_has_no_trusted_publish_state")
            errors.extend(global_runtime_issues)
            if reauth:
                action = Action.REAUTHORIZATION_REQUIRED
            elif errors:
                action = Action.BLOCKED
            elif dict(old_values) == dict(row.proposed):
                action = Action.NO_CHANGE
            else:
                action = Action.PUBLISH
            plan_rows.append(
                PlanRow(
                    row.worksheet_row,
                    row.test_id,
                    evidence_id("test", row.test_id) if row.test_id else None,
                    evidence_id("sample", row.sample_id) if row.sample_id else None,
                    row.source_hash,
                    evidence_id("reviewer", row.reviewer_id) if row.reviewer_id else None,
                    action,
                    tuple(sorted(set(errors + reauth))),
                    dict(old_values),
                    dict(row.proposed),
                    dict(formulas),
                    unrelated_digest,
                )
            )
        return PreparedPlan(
            utc_now(),
            batch.batch_id,
            batch.display_name,
            evidence_id("batch", batch.batch_id),
            tuple(plan_rows),
        )

    def _test_identity_issues(self, batch: BatchRecord, row: SourceRow, test: TestRecord) -> list[str]:
        issues: list[str] = []
        if test.test_id != row.test_id:
            issues.append("returned_test_id_mismatch")
        if test.batch_id != batch.batch_id:
            issues.append("returned_test_not_in_selected_batch")
        if row.sample_id is None or test.sample_id != row.sample_id:
            issues.append("sample_identifier_mismatch")
        if test.assay_id not in self.config.expected_assay_ids:
            issues.append("unexpected_assay_id")
        if test.assay_name not in self.config.expected_assay_names:
            issues.append("unexpected_assay_name")
        if test.workflow not in self.config.expected_workflows:
            issues.append("unexpected_workflow")
        return issues

    def publish(
        self,
        plan: PreparedPlan,
        *,
        execute: bool,
        confirmation: str,
    ) -> list[dict[str, Any]]:
        if not execute:
            raise SecurityError("Publish requires the explicit --execute argument")
        expected = f"PUBLISH REVIEWED TERPENES BATCH {plan.batch_display_name}"
        if confirmation != expected:
            raise SecurityError("Typed publish confirmation did not exactly match the required phrase")
        if not plan.can_publish:
            raise VerificationError("Complete Batch publish plan did not pass; no PATCH was sent")
        outcomes: list[dict[str, Any]] = []
        for row in plan.rows:
            if row.action == Action.NO_CHANGE:
                outcomes.append({"test_id": row.test_evidence_id, "result": "no_change", "api_status": "not_sent"})
                continue
            try:
                outcome = self._publish_one(row)
            except PublisherError as exc:
                outcomes.append(
                    {
                        "test_id": row.test_evidence_id,
                        "result": "failed_stop_batch",
                        "error": sanitize_text(exc),
                    }
                )
                break
            outcomes.append(outcome)
        return outcomes

    def _publish_one(self, row: PlanRow) -> dict[str, Any]:
        assert row.test_id and row.source_hash
        current = self.client.get_test(row.test_id)
        current_document = WorksheetDocument(current.worksheet_json)
        current_values = DestinationContract.values(current_document, self.fields)
        if dict(current_values) != dict(row.old_values):
            raise VerificationError("Destination changed after dry-run; PATCH was not sent")
        if current_document.formula_manifest() != dict(row.formula_manifest):
            raise VerificationError("Formula manifest changed after dry-run; PATCH was not sent")
        reason = f"Reviewed Terpenes Batch publish; source hash {row.source_hash[:12]}"
        patch_timed_out = False
        try:
            self.client.patch_test_worksheet(row.test_id, self._patch_payload(row.proposed_values), reason)
        except AmbiguousPatchOutcome:
            patch_timed_out = True
        verification = self.client.get_test(row.test_id)
        verified_document = WorksheetDocument(verification.worksheet_json)
        verification_errors = self._verification_issues(row, verified_document)
        if patch_timed_out:
            verification_errors.append("patch_response_timeout_after_submission")
        if verification_errors:
            rollback = self._rollback(row, verified_document)
            raise VerificationError(
                "Post-write verification failed; rollback " + ("verified" if rollback else "not verified")
            )
        if any(not is_native_number(verified_document.get_cell(spec.destination_cell)) for spec in self.fields[:23]):
            rollback = self._rollback(row, verified_document)
            raise VerificationError(
                "Published analytes were not native numeric cells; rollback " + ("verified" if rollback else "not verified")
            )
        self.state.record(row.test_id, row.source_hash)
        return {
            "test_id": row.test_evidence_id,
            "result": "published_verified",
            "api_status": "success",
            "verification_status": "all_43_values_formulas_and_unrelated_cells_verified",
            "rollback_status": "not_required",
        }

    def _verification_issues(self, row: PlanRow, document: WorksheetDocument) -> list[str]:
        issues = DestinationContract.issues(document, self.fields)
        if DestinationContract.values(document, self.fields) != dict(row.proposed_values):
            issues.append("persisted_values_do_not_match_complete_payload")
        if document.formula_manifest() != dict(row.formula_manifest):
            issues.append("formula_manifest_changed")
        digest = document.unrelated_digest(spec.destination_cell for spec in self.fields)
        if digest != row.unrelated_digest:
            issues.append("unrelated_worksheet_cells_changed")
        return issues

    def _rollback(self, row: PlanRow, current_document: WorksheetDocument) -> bool:
        current_values = DestinationContract.values(current_document, self.fields)
        for name, value in current_values.items():
            if value not in (row.old_values.get(name), row.proposed_values.get(name)):
                return False
        try:
            self.client.patch_test_worksheet(
                row.test_id,
                self._patch_payload(row.old_values),
                f"Prompt 5B controlled rollback; source hash {row.source_hash[:12]}",
            )
            restored = self.client.get_test(row.test_id)
        except PublisherError:
            return False
        restored_document = WorksheetDocument(restored.worksheet_json)
        return (
            DestinationContract.values(restored_document, self.fields) == dict(row.old_values)
            and restored_document.formula_manifest() == dict(row.formula_manifest)
            and restored_document.unrelated_digest(spec.destination_cell for spec in self.fields) == row.unrelated_digest
        )

    def _patch_payload(self, values: Mapping[str, Any]) -> dict[str, Any]:
        if self.config.analyte_patch_key_contract == "indexed_scalar_named_cells":
            return dict(values)
        if self.config.analyte_patch_key_contract == "range_named_cell":
            analytes = [values[spec.destination_named_cell] for spec in self.fields[:23]]
            payload = {"terpenes_instrument_conc": [analytes]}
            payload.update({spec.destination_named_cell: values[spec.destination_named_cell] for spec in self.fields[23:]})
            return payload
        raise ConfigurationError("Analyte PATCH key contract remains unresolved")


class AuditWriter:
    def __init__(self, directory: Path):
        self.directory = directory

    def write(
        self,
        mode: str,
        plan: PreparedPlan | None,
        *,
        sandbox_hostname: str = "ait-sandbox.qbench.net",
        outcomes: Sequence[Mapping[str, Any]] = (),
        final_result: str,
    ) -> Mapping[str, str]:
        self.directory.mkdir(parents=True, exist_ok=True)
        timestamp = utc_now()
        stem = timestamp.replace(":", "").replace("-", "") + f"_{mode}"
        payload = {
            "schema_version": 1,
            "timestamp": timestamp,
            "application_version": APP_VERSION,
            "mode": mode,
            "sandbox_hostname": sandbox_hostname,
            "batch_display_name": plan.batch_display_name if plan else None,
            "batch_id": plan.batch_evidence_id if plan else None,
            "rows": [self._row_payload(row) for row in plan.rows] if plan else [],
            "api_outcomes": list(outcomes),
            "final_result": final_result,
            "authorization_header": "not_recorded",
            "credential": "not_recorded",
        }
        json_path = self.directory / f"{stem}.json"
        md_path = self.directory / f"{stem}.md"
        json_text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
        md_text = self._markdown(payload)
        json_path.write_text(json_text, encoding="utf-8")
        md_path.write_text(md_text, encoding="utf-8")
        manifest = {
            "schema_version": 1,
            "files": {
                json_path.name: hashlib.sha256(json_text.encode("utf-8")).hexdigest(),
                md_path.name: hashlib.sha256(md_text.encode("utf-8")).hexdigest(),
            },
        }
        manifest_path = self.directory / f"{stem}.manifest.json"
        manifest_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        manifest_path.write_text(manifest_text, encoding="utf-8")
        return {
            "json": str(json_path),
            "report": str(md_path),
            "manifest": str(manifest_path),
            "manifest_sha256": hashlib.sha256(manifest_text.encode("utf-8")).hexdigest(),
        }

    @staticmethod
    def _row_payload(row: PlanRow) -> Mapping[str, Any]:
        return {
            "worksheet_row": row.worksheet_row,
            "test_id": row.test_evidence_id,
            "sample_id": row.sample_evidence_id,
            "source_hash": row.source_hash,
            "reviewer_identifier": row.reviewer_evidence_id,
            "validation_state": row.action.value,
            "validation_outcomes": list(row.errors),
            "fields_planned": [
                {
                    "field": name,
                    "old_value": row.old_values.get(name),
                    "proposed_new_value": value,
                    "changed": row.old_values.get(name) != value,
                }
                for name, value in row.proposed_values.items()
            ],
        }

    @staticmethod
    def _markdown(payload: Mapping[str, Any]) -> str:
        lines = [
            f"# Terpenes publisher {payload['mode']} audit",
            "",
            f"- Timestamp: `{payload['timestamp']}`",
            f"- Application version: `{payload['application_version']}`",
            f"- Sandbox hostname: `{payload['sandbox_hostname']}`",
            f"- Batch: `{payload['batch_display_name']}`",
            f"- Final result: `{payload['final_result']}`",
            "",
        ]
        for row in payload["rows"]:
            lines.extend(
                [
                    f"## {row['test_id']}",
                    "",
                    f"- Sample: `{row['sample_id']}`",
                    f"- Source hash: `{row['source_hash']}`",
                    f"- Reviewer: `{row['reviewer_identifier']}`",
                    f"- Action: **{row['validation_state']}**",
                    f"- Validation: `{', '.join(row['validation_outcomes']) or 'passed'}`",
                    "",
                    "| Destination field | Old value | Proposed value | Changed |",
                    "|---|---:|---:|:---:|",
                ]
            )
            for item in row["fields_planned"]:
                old_value = json.dumps(item["old_value"], ensure_ascii=False)
                new_value = json.dumps(item["proposed_new_value"], ensure_ascii=False)
                lines.append(f"| `{item['field']}` | `{old_value}` | `{new_value}` | `{item['changed']}` |")
            lines.append("")
        return "\n".join(lines) + "\n"


def _package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _build_parser() -> argparse.ArgumentParser:
    root = _package_root()
    parser = argparse.ArgumentParser(description="Sandbox-only exact-Test Terpenes publisher")
    parser.add_argument("--base-url", default=os.environ.get("QBENCH_BASE_URL", ALLOWED_BASE_URL))
    parser.add_argument("--secrets-file", type=Path)
    parser.add_argument("--mapping", type=Path, default=root / "config" / "field_mapping.csv")
    parser.add_argument("--config", type=Path, default=root / "config" / "publisher_config.json")
    parser.add_argument("--audit-dir", type=Path, default=root / "audit")
    parser.add_argument("--state-file", type=Path, default=root / "audit" / "publisher_state.json")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("inspect", "dry-run", "publish"):
        sub = subparsers.add_parser(name)
        sub.add_argument("--batch-id", required=True)
        if name == "publish":
            sub.add_argument("--execute", action="store_true")
    return parser


def _print_plan(plan: PreparedPlan) -> None:
    print(f"Batch: {plan.batch_display_name} ({plan.batch_evidence_id})")
    for row in plan.rows:
        print(f"{row.action.value}: {row.test_evidence_id}; fields={len(row.proposed_values)}")
        for error in row.errors:
            print(f"  - {error}")


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    writer = AuditWriter(args.audit_dir)
    try:
        base_url = validate_base_url(args.base_url)
        token = load_token(args.secrets_file)
        fields = load_mapping(args.mapping)
        config = PublisherConfig.from_path(args.config)
        client = QBenchClient(base_url, token)
        publisher = Publisher(client, fields, config, StateStore(args.state_file))
        plan = publisher.prepare(args.batch_id)
        _print_plan(plan)
        if args.command in ("inspect", "dry-run"):
            artifacts = writer.write(args.command, plan, final_result="read_only_complete")
            print(f"Sanitized audit manifest: {artifacts['manifest']}")
            return 0 if args.command == "inspect" or plan.can_publish else 2
        if not args.execute:
            raise SecurityError("Publish requires the explicit --execute argument")
        phrase = f"PUBLISH REVIEWED TERPENES BATCH {plan.batch_display_name}"
        print(f"Type exactly: {phrase}")
        confirmation = input("> ")
        outcomes = publisher.publish(plan, execute=True, confirmation=confirmation)
        final_result = "publish_complete" if len(outcomes) == len(plan.rows) and all(
            item.get("result") in ("published_verified", "no_change") for item in outcomes
        ) else "publish_stopped"
        artifacts = writer.write("publish", plan, outcomes=outcomes, final_result=final_result)
        print(f"Sanitized audit manifest: {artifacts['manifest']}")
        return 0 if final_result == "publish_complete" else 3
    except PublisherError as exc:
        artifacts = writer.write(
            args.command,
            None,
            final_result=f"preflight_blocked:{type(exc).__name__}",
        )
        print(f"ERROR: {sanitize_text(exc)}", file=sys.stderr)
        print(f"Sanitized audit manifest: {artifacts['manifest']}", file=sys.stderr)
        return 2
