from __future__ import annotations

import copy
import hashlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from pathlib import Path
from urllib.error import URLError
from unittest.mock import patch

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "src"))

from terpenes_publisher import (  # noqa: E402
    ALLOWED_BASE_URL,
    ClientCredentials,
    Action,
    AmbiguousPatchOutcome,
    ApiError,
    AuditWriter,
    BatchRecord,
    ConfigurationError,
    DestinationContract,
    HttpResponse,
    Publisher,
    PublisherConfig,
    QBenchClient,
    QBenchTokenClient,
    SchemaError,
    SecurityError,
    StateStore,
    TestRecord,
    VerificationError,
    WorksheetDocument,
    contains_forbidden_field,
    credential_key_status,
    load_client_credentials,
    load_mapping,
    main,
    prove_destination_contract,
    sanitize_text,
    validate_base_url,
)
from terpenes_publisher.core import column_letters, column_number  # noqa: E402


MAPPING_PATH = PACKAGE_ROOT / "config" / "field_mapping.csv"
FIELDS = load_mapping(MAPPING_PATH)


def grid(rows: int, columns: int) -> list[list[object]]:
    return [["" for _ in range(columns)] for _ in range(rows)]


def set_cell(payload: dict, reference: str, value: object) -> None:
    sheet, address = reference.split("!", 1)
    letters = "".join(character for character in address if character.isalpha())
    row = int("".join(character for character in address if character.isdigit()))
    payload["data"][sheet][row - 1][column_number(letters) - 1] = value


def make_batch_worksheet(row_count: int = 1) -> dict:
    payload = {
        "config": {},
        "qb_config": {
            "named_cells": {
                "terpenes_batch_import_table": {"cell": "Instrument Import!A1:BE20"},
                "terpenes_batch_publish_table": {"cell": "Publish!A1:BI20"},
                "terpenes_batch_publish_authorization": {"cell": "Publish!BE2:BE20"},
                "terpenes_batch_publish_authorized_by": {"cell": "Publish!BF2:BF20"},
                "terpenes_batch_publish_authorized_at": {"cell": "Publish!BG2:BG20"},
                "terpenes_batch_publish_reviewed_source_row_hash": {"cell": "Publish!BH2:BH20"},
                "terpenes_batch_last_published_source_row_hash": {"cell": "Publish!BI2:BI20"},
            }
        },
        "data": {
            "Instrument Import": grid(20, column_number("BE")),
            "Publish": grid(20, column_number("BI")),
        },
    }
    for offset in range(row_count):
        worksheet_row = offset + 2
        test_id = f"SBX-T-{offset + 1:03d}"
        sample_id = f"SBX-S-{offset + 1:03d}"
        source_hash = hashlib.sha256(f"row-{offset + 1}".encode()).hexdigest()
        analytes = [round(offset + (index + 1) / 100, 4) for index in range(23)]
        set_cell(payload, f"Instrument Import!E{worksheet_row}", test_id)
        set_cell(payload, f"Instrument Import!H{worksheet_row}", 1.0 + offset)
        set_cell(payload, f"Instrument Import!I{worksheet_row}", 10.0)
        set_cell(payload, f"Instrument Import!J{worksheet_row}", 1.0)
        set_cell(payload, f"Instrument Import!K{worksheet_row}", "already_applied_by_labsolutions")
        for column in ("N", "O", "P", "Q", "R", "T", "U", "V", "W"):
            set_cell(payload, f"Instrument Import!{column}{worksheet_row}", f"synthetic_{column.lower()}")
        set_cell(payload, f"Instrument Import!X{worksheet_row}", 24)
        set_cell(payload, f"Instrument Import!Y{worksheet_row}", 34)
        set_cell(payload, f"Instrument Import!Z{worksheet_row}", 23)
        set_cell(payload, f"Instrument Import!AA{worksheet_row}", 0.25 + offset)
        set_cell(payload, f"Instrument Import!AC{worksheet_row}", "No")
        set_cell(payload, f"Instrument Import!AE{worksheet_row}", "Reviewed")
        set_cell(payload, f"Instrument Import!AF{worksheet_row}", "Valid")
        set_cell(payload, f"Instrument Import!AG{worksheet_row}", "Import row valid")
        for column_index, value in zip(range(column_number("AH"), column_number("BD") + 1), analytes):
            set_cell(payload, f"Instrument Import!{column_letters(column_index)}{worksheet_row}", value)
        set_cell(payload, f"Instrument Import!BE{worksheet_row}", source_hash)

        set_cell(payload, f"Publish!A{worksheet_row}", test_id)
        set_cell(payload, f"Publish!B{worksheet_row}", sample_id)
        set_cell(payload, f"Publish!C{worksheet_row}", "Synthetic Matrix")
        for column_index, value in zip(range(column_number("D"), column_number("Z") + 1), analytes):
            set_cell(payload, f"Publish!{column_letters(column_index)}{worksheet_row}", value)
        publish_values = {
            "AA": 1.0 + offset,
            "AB": 10.0,
            "AC": 1.0,
            "AD": "already_applied_by_labsolutions",
            "AE": "ug/mL",
            "AF": True,
            "AG": True,
            "AH": f"SBX-BATCH-SOURCE-{offset + 1}",
            "AI": f"synthetic_instrument_{offset + 1}.txt",
            "AJ": hashlib.sha256(f"source-file-{offset + 1}".encode()).hexdigest(),
            "AK": f"synthetic_data_{offset + 1}.lcd",
            "AL": "synthetic_method.mth",
            "AM": "synthetic_sequence.lcb",
            "AN": "synthetic-parser/1.0",
            "AO": "2026-07-17T00:00:00Z",
            "AP": "SBX_SYNTHETIC_GC",
            "AQ": "SBX_FID_01",
            "AR": "Synthetic FID",
            "AT": source_hash,
            "AU": 0.25 + offset,
            "AV": True,
            "AW": "Reviewed",
            "AX": "Valid",
            "AY": "Accepted",
            "AZ": True,
            "BA": True,
            "BB": True,
            "BC": True,
            "BE": "Authorized",
            "BF": "synthetic-reviewer",
            "BG": "2026-07-17T00:01:00Z",
            "BH": source_hash,
            "BI": "",
        }
        for column, value in publish_values.items():
            set_cell(payload, f"Publish!{column}{worksheet_row}", value)
    return payload


def make_test_worksheet() -> dict:
    named_cells = {"terpenes_instrument_conc": {"cell": "Data!D2:Z2"}}
    for spec in FIELDS[23:]:
        named_cells[spec.destination_named_cell] = {"cell": spec.destination_cell}
    writable_cells = {
        spec.destination_cell.split("!", 1)[1]: {"readonly": False, "type": "text"}
        for spec in FIELDS
    }
    payload = {
        "config": {"worksheets": [{"worksheetName": "Data", "cells": writable_cells}]},
        "qb_config": {"named_cells": named_cells},
        "data": {"Data": grid(45, 26)},
    }
    for column in range(column_number("D"), column_number("Z") + 1):
        set_cell(payload, f"Data!{column_letters(column)}3", "=1+1")
    set_cell(payload, "Data!B24", "=COUNT(D2:Z2)=23")
    set_cell(payload, "Data!A40", "UNCHANGED")
    return payload


def make_records(row_count: int = 1) -> tuple[BatchRecord, list[TestRecord]]:
    batch_worksheet = make_batch_worksheet(row_count)
    test_ids = tuple(f"SBX-T-{index + 1:03d}" for index in range(row_count))
    batch = BatchRecord("SBX-BATCH-001", "SBX_ONLY_TERPENES_BATCH", test_ids, "SBX-BWS-001", batch_worksheet)
    tests = [
        TestRecord(
            test_id,
            batch.batch_id,
            f"SBX-S-{index + 1:03d}",
            "SBX-ASSAY-TERPENES",
            "SBX_ONLY_TERPENES",
            "Terpenes reviewed publish",
            f"SBX-TWS-{index + 1:03d}",
            make_test_worksheet(),
        )
        for index, test_id in enumerate(test_ids)
    ]
    return batch, tests


APPROVED_CONFIG = PublisherConfig(
    "SBX_ONLY_",
    ("SBX-ASSAY-TERPENES",),
    ("SBX_ONLY_TERPENES",),
    ("Terpenes reviewed publish",),
    True,
    "api_patch_atomic",
    "indexed_scalar_named_cells",
)


class FakeClient:
    def __init__(self, batch: BatchRecord, tests: list[TestRecord]):
        self.batch = copy.deepcopy(batch)
        self.tests = {record.test_id: copy.deepcopy(record) for record in tests}
        self.patch_calls: list[tuple[str, dict, str]] = []
        self.patch_behaviors: dict[str, list[str]] = {}
        self.test_errors: dict[str, Exception] = {}
        self.mapped_cells = {spec.destination_named_cell: spec.destination_cell for spec in FIELDS}

    def get_batch(self, batch_id: str) -> BatchRecord:
        if batch_id != self.batch.batch_id:
            raise ApiError("GET Batch", 404)
        return copy.deepcopy(self.batch)

    def get_test(self, test_id: str) -> TestRecord:
        if test_id in self.test_errors:
            raise self.test_errors[test_id]
        if test_id not in self.tests:
            raise ApiError("GET Test", 404)
        return copy.deepcopy(self.tests[test_id])

    def patch_test_worksheet(self, test_id: str, data: dict, reason: str) -> dict:
        self.patch_calls.append((test_id, copy.deepcopy(data), reason))
        behavior = self.patch_behaviors.get(test_id, ["success"])
        current_behavior = behavior.pop(0) if behavior else "success"
        self.patch_behaviors[test_id] = behavior
        if current_behavior == "error":
            raise ApiError("PATCH Test Worksheet", 500)
        if current_behavior == "silent_noop":
            return {"status": "success"}
        record = self.tests[test_id]
        worksheet = copy.deepcopy(record.worksheet_json)
        document = WorksheetDocument(worksheet)
        items = list(data.items())
        if current_behavior == "partial":
            items = items[:1]
        for name, value in items:
            document.set_cell(self.mapped_cells[name], value)
        if current_behavior == "corrupt_unrelated":
            document.set_cell("Data!A40", "CHANGED")
        self.tests[test_id] = replace(record, worksheet_json=worksheet)
        if current_behavior == "timeout_after_apply":
            raise AmbiguousPatchOutcome("PATCH outcome is unknown after submission; no retry was attempted")
        return {"status": "success"}


class PublisherFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.batch, tests = make_records()
        self.client = FakeClient(self.batch, tests)
        self.state = StateStore(Path(self.temp.name) / "publisher_state.json")
        self.publisher = Publisher(self.client, FIELDS, APPROVED_CONFIG, self.state)

    def plan(self):
        return self.publisher.prepare(self.batch.batch_id)


class SecurityAndClientTests(unittest.TestCase):
    def test_only_exact_sandbox_url_is_allowed(self) -> None:
        self.assertEqual(validate_base_url(ALLOWED_BASE_URL + "/"), ALLOWED_BASE_URL)
        for value in (
            "https://ait.qbench.net/",
            "http://ait-sandbox.qbench.net/",
            "https://ait-sandbox.qbench.net.evil.example/",
            "https://ait-sandbox.qbench.net/path",
        ):
            with self.assertRaises(SecurityError):
                validate_base_url(value)

    def test_client_credentials_load_from_file_without_repr_disclosure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            secrets_path = Path(temporary_directory) / ".env.local"
            secrets_path.write_text(
                "QBENCH_BASE_URL=https://ait-sandbox.qbench.net\n"
                "QBENCH_CLIENT_ID=synthetic-client-id\n"
                "QBENCH_CLIENT_SECRET=synthetic-client-secret\n",
                encoding="utf-8",
            )
            self.assertEqual(
                credential_key_status(secrets_path),
                {
                    "QBENCH_BASE_URL": True,
                    "QBENCH_CLIENT_ID": True,
                    "QBENCH_CLIENT_SECRET": True,
                },
            )
            credentials = load_client_credentials(secrets_path)
            self.assertEqual(credentials.base_url, ALLOWED_BASE_URL)
            self.assertNotIn("synthetic-client-id", repr(credentials))
            self.assertNotIn("synthetic-client-secret", repr(credentials))

    def test_missing_or_blank_client_credential_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            secrets_path = Path(temporary_directory) / ".env.local"
            secrets_path.write_text(
                "QBENCH_BASE_URL=https://ait-sandbox.qbench.net\n"
                "QBENCH_CLIENT_ID=\n",
                encoding="utf-8",
            )
            with self.assertRaises(ConfigurationError) as raised:
                load_client_credentials(secrets_path)
            self.assertIn("QBENCH_CLIENT_ID", str(raised.exception))
            self.assertIn("QBENCH_CLIENT_SECRET", str(raised.exception))

    def test_client_credentials_exchange_returns_short_lived_in_memory_token(self) -> None:
        calls = []

        def opener(request, timeout):
            calls.append((request, timeout))
            return HttpResponse(
                200,
                {
                    "access_token": "synthetic-access-token",
                    "token_type": "Bearer",
                    "expires_in": 900,
                },
            )

        credentials = ClientCredentials(ALLOWED_BASE_URL, "synthetic-client-id", "synthetic-client-secret")
        token = QBenchTokenClient(
            credentials,
            "/qbench/api/v1/oauth/token",
            opener=opener,
            clock=lambda: 1000.0,
        ).exchange()
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][0].get_method(), "POST")
        self.assertEqual(token.value, "synthetic-access-token")
        self.assertEqual(token.expires_at_epoch, 1900.0)
        self.assertNotIn("synthetic-access-token", repr(token))
        self.assertNotIn("synthetic-client-secret", repr(credentials))

    def test_invalid_or_long_lived_oauth_token_is_rejected(self) -> None:
        credentials = ClientCredentials(ALLOWED_BASE_URL, "synthetic-client-id", "synthetic-client-secret")
        for expires_in in (7200, float("nan")):
            with self.subTest(expires_in=expires_in):
                client = QBenchTokenClient(
                    credentials,
                    "/qbench/api/v1/oauth/token",
                    opener=lambda *_, lifetime=expires_in: HttpResponse(
                        200,
                        {
                            "access_token": "synthetic-access-token",
                            "token_type": "Bearer",
                            "expires_in": lifetime,
                        },
                    ),
                )
                with self.assertRaises(SecurityError):
                    client.exchange()

    def test_unsafe_oauth_token_path_is_rejected(self) -> None:
        credentials = ClientCredentials(ALLOWED_BASE_URL, "synthetic-client-id", "synthetic-client-secret")
        for token_path in ("https://example.invalid/token", "//example.invalid/token", "token", "/token?redirect=1"):
            with self.assertRaises(ConfigurationError):
                QBenchTokenClient(credentials, token_path)

    def test_sanitizer_removes_token_authorization_and_urls(self) -> None:
        value = "Authorization: Bearer sandbox-secret https://ait-sandbox.qbench.net/path"
        sanitized = sanitize_text(value, "sandbox-secret")
        self.assertNotIn("sandbox-secret", sanitized)
        self.assertNotIn("ait-sandbox", sanitized)
        self.assertIn("REDACTED", sanitized)

    def test_get_retries_are_limited(self) -> None:
        calls = []

        def opener(request, timeout):
            calls.append(request)
            if len(calls) < 3:
                raise URLError("synthetic timeout")
            return HttpResponse(
                200,
                {
                    "id": "B1",
                    "display_name": "Synthetic",
                    "test_ids": [],
                    "worksheet_id": "W1",
                    "worksheet_json": make_batch_worksheet(0),
                },
            )

        client = QBenchClient(ALLOWED_BASE_URL, "sandbox-secret", opener=opener, sleep=lambda _: None)
        record = client.get_batch("B1")
        self.assertEqual(record.batch_id, "B1")
        self.assertEqual(len(calls), 3)

    def test_get_timeout_after_limited_retries_is_sanitized(self) -> None:
        calls = []

        def opener(request, timeout):
            calls.append(request)
            raise URLError("https://ait-sandbox.qbench.net/private?token=sandbox-secret")

        client = QBenchClient(ALLOWED_BASE_URL, "sandbox-secret", opener=opener, sleep=lambda _: None)
        with self.assertRaises(ApiError) as raised:
            client.get_batch("B1")
        self.assertEqual(len(calls), 3)
        self.assertNotIn("sandbox-secret", str(raised.exception))
        self.assertNotIn("://", str(raised.exception))

    def test_patch_timeout_is_never_retried(self) -> None:
        calls = []

        def opener(request, timeout):
            calls.append(request)
            raise URLError("synthetic timeout")

        client = QBenchClient(ALLOWED_BASE_URL, "sandbox-secret", opener=opener, sleep=lambda _: None)
        with self.assertRaises(AmbiguousPatchOutcome):
            client.patch_test_worksheet(
                "T1",
                {"sample_mass_g": 1.25},
                "Reviewed Terpenes Batch publish; source hash abcdef123456",
            )
        self.assertEqual(len(calls), 1)

    def test_http_error_suppresses_body_and_url(self) -> None:
        def opener(request, timeout):
            return HttpResponse(500, {"secret": "do-not-log"})

        client = QBenchClient(ALLOWED_BASE_URL, "sandbox-secret", opener=opener, sleep=lambda _: None)
        with self.assertRaises(ApiError) as raised:
            client.get_batch("B1")
        self.assertNotIn("do-not-log", str(raised.exception))
        self.assertNotIn("://", str(raised.exception))

    def test_patch_payload_rejects_pass_fail_and_formula_input(self) -> None:
        client = QBenchClient(ALLOWED_BASE_URL, "sandbox-secret", opener=lambda *_: HttpResponse(200, {}))
        for payload in ({"pass_fail": "Pass"}, {"sample_mass_g": "=1+1"}):
            with self.assertRaises(SecurityError):
                client.patch_test_worksheet(
                    "T1",
                    payload,
                    "Reviewed Terpenes Batch publish; source hash abcdef123456",
                )
        self.assertTrue(contains_forbidden_field("Terpenes Pass-Fail"))

    def test_response_schema_requires_exact_id(self) -> None:
        client = QBenchClient(
            ALLOWED_BASE_URL,
            "sandbox-secret",
            opener=lambda *_: HttpResponse(
                200,
                {
                    "id": "DIFFERENT",
                    "display_name": "Synthetic",
                    "test_ids": [],
                    "worksheet_id": "W1",
                    "worksheet_json": make_batch_worksheet(0),
                },
            ),
        )
        with self.assertRaises(SchemaError):
            client.get_batch("B1")


class LocalPreTokenProofTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.worksheet_path = self.root / "saved-export.json"
        self.worksheet_path.write_text(json.dumps(make_test_worksheet()), encoding="utf-8")

    def write_valid_provenance(self) -> Path:
        provenance_path = self.root / "saved-export.provenance.json"
        provenance_path.write_text(
            json.dumps(
                {
                    "sandbox_hostname": "ait-sandbox.qbench.net",
                    "export_action": "Export Spreadsheet",
                    "saved": True,
                    "reopened": True,
                    "synthetic_only": True,
                    "export_sha256": hashlib.sha256(self.worksheet_path.read_bytes()).hexdigest(),
                    "worksheet_display_name": "SBX_ONLY_DESTINATION_PROOF",
                }
            ),
            encoding="utf-8",
        )
        return provenance_path

    def test_structural_43_field_candidate_without_saved_provenance_does_not_pass(self) -> None:
        result = prove_destination_contract(self.worksheet_path, MAPPING_PATH)
        self.assertFalse(result.passed)
        self.assertEqual(result.target_count, 43)
        self.assertEqual(result.writable_target_count, 43)
        self.assertEqual(result.structural_issues, ())
        self.assertEqual(result.provenance_issues, ("saved_export_provenance_missing",))

    def test_saved_reopened_synthetic_provenance_allows_43_field_proof(self) -> None:
        result = prove_destination_contract(self.worksheet_path, MAPPING_PATH, self.write_valid_provenance())
        self.assertTrue(result.passed)
        self.assertEqual(result.status, "saved_sandbox_destination_contract_proven")
        self.assertEqual(result.target_count, 43)
        self.assertEqual(result.writable_target_count, 43)

    def test_readonly_destination_blocks_43_field_proof(self) -> None:
        worksheet = make_test_worksheet()
        worksheet["config"]["worksheets"][0]["cells"]["B12"]["readonly"] = True
        self.worksheet_path.write_text(json.dumps(worksheet), encoding="utf-8")
        result = prove_destination_contract(self.worksheet_path, MAPPING_PATH, self.write_valid_provenance())
        self.assertFalse(result.passed)
        self.assertIn("destination_not_writable:sample_mass_g", result.structural_issues)
        self.assertEqual(result.writable_target_count, 42)

    def test_current_configuration_blocks_before_any_token_request(self) -> None:
        config = PublisherConfig.from_path(PACKAGE_ROOT / "config" / "publisher_config.json")
        issues = config.pre_token_issues(PACKAGE_ROOT)
        self.assertIn("saved_destination_contract_not_proven_before_token_request", issues)
        self.assertIn("destination_contract_proof_lock_missing", issues)
        self.assertIn("oauth_token_endpoint_contract_not_proven", issues)

    def test_pre_token_gate_validates_locked_proof_contents_and_mapping_hash(self) -> None:
        package_root = self.root / "package"
        (package_root / "config").mkdir(parents=True)
        (package_root / "config" / "field_mapping.csv").write_bytes(MAPPING_PATH.read_bytes())
        result = prove_destination_contract(self.worksheet_path, MAPPING_PATH, self.write_valid_provenance())
        proof_path = package_root / "destination-proof.json"
        proof_path.write_text(json.dumps(result.as_dict()), encoding="utf-8")
        config = PublisherConfig(
            "SBX_ONLY_",
            ("SBX-ASSAY",),
            ("SBX_ONLY_TERPENES",),
            ("Synthetic workflow",),
            True,
            "api_patch_unresolved",
            "unresolved",
            token_path="/qbench/api/v1/oauth/token",
            token_endpoint_contract_proven=True,
            destination_contract_proof_file="destination-proof.json",
            destination_contract_proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest(),
        )
        self.assertEqual(config.pre_token_issues(package_root), [])

        tampered = result.as_dict()
        tampered["mapping_sha256"] = "0" * 64
        proof_path.write_text(json.dumps(tampered), encoding="utf-8")
        config = replace(
            config,
            destination_contract_proof_sha256=hashlib.sha256(proof_path.read_bytes()).hexdigest(),
        )
        self.assertIn("destination_contract_proof_mapping_hash_mismatch", config.pre_token_issues(package_root))

    def test_credentials_check_prints_status_only_and_does_not_request_token(self) -> None:
        secrets_path = self.root / ".env.local"
        secrets_path.write_text(
            "QBENCH_BASE_URL=https://ait-sandbox.qbench.net\n"
            "QBENCH_CLIENT_ID=synthetic-client-id\n"
            "QBENCH_CLIENT_SECRET=synthetic-client-secret\n",
            encoding="utf-8",
        )
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(io.StringIO()):
            result = main(["--secrets-file", str(secrets_path), "credentials-check"])
        rendered = output.getvalue()
        self.assertEqual(result, 0)
        self.assertIn("QBENCH_CLIENT_SECRET: present_and_nonblank=True", rendered)
        self.assertIn("token_request: not_attempted", rendered)
        self.assertNotIn("synthetic-client-id", rendered)
        self.assertNotIn("synthetic-client-secret", rendered)


class PlanningAndGateTests(PublisherFixture):
    def test_valid_complete_plan_is_publish(self) -> None:
        plan = self.plan()
        self.assertTrue(plan.can_publish)
        self.assertEqual(plan.rows[0].action, Action.PUBLISH)
        self.assertEqual(len(plan.rows[0].proposed_values), 43)

    def test_batch_not_found(self) -> None:
        with self.assertRaises(ApiError):
            self.publisher.prepare("MISSING")

    def test_test_not_found_is_blocked(self) -> None:
        self.client.tests.clear()
        plan = self.plan()
        self.assertEqual(plan.rows[0].action, Action.BLOCKED)
        self.assertIn("destination_test_read_failed:ApiError", plan.rows[0].errors)

    def test_test_not_in_selected_batch_is_blocked(self) -> None:
        test = self.client.tests["SBX-T-001"]
        self.client.tests[test.test_id] = replace(test, batch_id="OTHER-BATCH")
        self.assertIn("returned_test_not_in_selected_batch", self.plan().rows[0].errors)

    def test_duplicate_publish_test_id_is_blocked_without_patch(self) -> None:
        duplicate = copy.deepcopy(self.client.batch.worksheet_json)
        for column in range(1, column_number("BI") + 1):
            value = duplicate["data"]["Publish"][1][column - 1]
            duplicate["data"]["Publish"][2][column - 1] = value
        self.client.batch = replace(self.client.batch, worksheet_json=duplicate)
        plan = self.plan()
        self.assertEqual([row.action for row in plan.rows], [Action.BLOCKED, Action.BLOCKED])
        self.assertTrue(all("duplicate_test_id_in_publish_rows" in row.errors for row in plan.rows))
        with self.assertRaises(VerificationError):
            self.publisher.publish(
                plan,
                execute=True,
                confirmation=f"PUBLISH REVIEWED TERPENES BATCH {plan.batch_display_name}",
            )
        self.assertEqual(self.client.patch_calls, [])

    def test_missing_test_id_row_is_included_and_blocked(self) -> None:
        worksheet = copy.deepcopy(self.client.batch.worksheet_json)
        set_cell(worksheet, "Publish!A2", "")
        self.client.batch = replace(self.client.batch, worksheet_json=worksheet)
        row = self.plan().rows[0]
        self.assertEqual(row.action, Action.BLOCKED)
        self.assertIn("missing_test_id", row.errors)

    def test_missing_source_hash_is_blocked(self) -> None:
        worksheet = copy.deepcopy(self.client.batch.worksheet_json)
        set_cell(worksheet, "Publish!AT2", "")
        self.client.batch = replace(self.client.batch, worksheet_json=worksheet)
        self.assertIn("missing_source_hash", self.plan().rows[0].errors)

    def test_authorization_off_is_blocked(self) -> None:
        worksheet = copy.deepcopy(self.client.batch.worksheet_json)
        set_cell(worksheet, "Publish!BE2", "Not Authorized")
        self.client.batch = replace(self.client.batch, worksheet_json=worksheet)
        self.assertIn("reviewer_authorization_off", self.plan().rows[0].errors)

    def test_import_af_rejected_and_ag_invalid_are_blocked(self) -> None:
        worksheet = copy.deepcopy(self.client.batch.worksheet_json)
        set_cell(worksheet, "Instrument Import!AF2", "Rejected")
        set_cell(worksheet, "Instrument Import!AG2", "Analytical values incomplete")
        self.client.batch = replace(self.client.batch, worksheet_json=worksheet)
        errors = self.plan().rows[0].errors
        self.assertIn("import_af_not_valid", errors)
        self.assertIn("import_ag_not_import_row_valid", errors)

    def test_non_numeric_analyte_is_blocked(self) -> None:
        worksheet = copy.deepcopy(self.client.batch.worksheet_json)
        set_cell(worksheet, "Publish!D2", "not numeric")
        set_cell(worksheet, "Instrument Import!AH2", "not numeric")
        self.client.batch = replace(self.client.batch, worksheet_json=worksheet)
        self.assertIn("reportable_analytes_not_23_native_numeric_values", self.plan().rows[0].errors)

    def test_incorrect_counts_are_blocked(self) -> None:
        worksheet = copy.deepcopy(self.client.batch.worksheet_json)
        set_cell(worksheet, "Instrument Import!Y2", 33)
        self.client.batch = replace(self.client.batch, worksheet_json=worksheet)
        self.assertIn("instrument_import_counts_incorrect", self.plan().rows[0].errors)

    def test_missing_destination_named_cell_is_blocked(self) -> None:
        test = self.client.tests["SBX-T-001"]
        worksheet = copy.deepcopy(test.worksheet_json)
        del worksheet["qb_config"]["named_cells"]["sample_mass_g"]
        self.client.tests[test.test_id] = replace(test, worksheet_json=worksheet)
        self.assertIn("missing_destination_named_cell:sample_mass_g", self.plan().rows[0].errors)

    def test_formula_owned_destination_is_blocked(self) -> None:
        test = self.client.tests["SBX-T-001"]
        worksheet = copy.deepcopy(test.worksheet_json)
        set_cell(worksheet, "Data!B12", "=1+1")
        self.client.tests[test.test_id] = replace(test, worksheet_json=worksheet)
        self.assertIn("formula_owned_destination:sample_mass_g", self.plan().rows[0].errors)

    def test_unresolved_runtime_approval_blocks_dry_run_plan(self) -> None:
        unresolved = PublisherConfig("SBX_ONLY_", (), (), (), False, "api_patch_unresolved", "unresolved")
        publisher = Publisher(self.client, FIELDS, unresolved, self.state)
        errors = publisher.prepare(self.batch.batch_id).rows[0].errors
        self.assertIn("saved_destination_contract_not_proven", errors)
        self.assertIn("direct_publish_not_allowed:api_patch_unresolved", errors)

    def test_non_synthetic_batch_name_is_rejected_before_worksheet_processing(self) -> None:
        self.client.batch = replace(self.client.batch, display_name="Ordinary Batch")
        with self.assertRaises(SecurityError):
            self.plan()

    def test_changed_hash_requires_reauthorization(self) -> None:
        self.state.record("SBX-T-001", "previous-source-hash")
        row = self.plan().rows[0]
        self.assertEqual(row.action, Action.REAUTHORIZATION_REQUIRED)
        self.assertIn("source_hash_changed_after_prior_publish", row.errors)


class PublishingAndVerificationTests(PublisherFixture):
    def confirmation(self, plan) -> str:
        return f"PUBLISH REVIEWED TERPENES BATCH {plan.batch_display_name}"

    def test_publish_requires_execute_and_typed_phrase(self) -> None:
        plan = self.plan()
        with self.assertRaises(SecurityError):
            self.publisher.publish(plan, execute=False, confirmation=self.confirmation(plan))
        with self.assertRaises(SecurityError):
            self.publisher.publish(plan, execute=True, confirmation="yes")
        self.assertEqual(self.client.patch_calls, [])

    def test_single_test_publish_verifies_43_fields_numeric_formulas_and_unrelated(self) -> None:
        plan = self.plan()
        outcomes = self.publisher.publish(plan, execute=True, confirmation=self.confirmation(plan))
        self.assertEqual(outcomes[0]["result"], "published_verified")
        self.assertEqual(len(self.client.patch_calls), 1)
        persisted = WorksheetDocument(self.client.tests["SBX-T-001"].worksheet_json)
        self.assertEqual(DestinationContract.values(persisted, FIELDS), dict(plan.rows[0].proposed_values))
        self.assertTrue(all(isinstance(persisted.get_cell(spec.destination_cell), float) for spec in FIELDS[:23]))
        self.assertEqual(persisted.get_cell("Data!A40"), "UNCHANGED")
        self.assertEqual(persisted.formula_manifest(), dict(plan.rows[0].formula_manifest))

    def test_duplicate_unchanged_publish_is_no_change_without_patch(self) -> None:
        first = self.plan()
        self.publisher.publish(first, execute=True, confirmation=self.confirmation(first))
        self.client.patch_calls.clear()
        second = self.plan()
        self.assertEqual(second.rows[0].action, Action.NO_CHANGE)
        outcomes = self.publisher.publish(second, execute=True, confirmation=self.confirmation(second))
        self.assertEqual(outcomes[0]["result"], "no_change")
        self.assertEqual(self.client.patch_calls, [])

    def test_success_response_with_failed_persistence_rolls_back(self) -> None:
        self.client.patch_behaviors["SBX-T-001"] = ["partial", "success"]
        plan = self.plan()
        outcomes = self.publisher.publish(plan, execute=True, confirmation=self.confirmation(plan))
        self.assertEqual(outcomes[0]["result"], "failed_stop_batch")
        self.assertEqual(len(self.client.patch_calls), 2)
        persisted = WorksheetDocument(self.client.tests["SBX-T-001"].worksheet_json)
        self.assertEqual(DestinationContract.values(persisted, FIELDS), dict(plan.rows[0].old_values))

    def test_timeout_after_patch_submission_is_not_retried_and_rolls_back(self) -> None:
        self.client.patch_behaviors["SBX-T-001"] = ["timeout_after_apply", "success"]
        plan = self.plan()
        outcomes = self.publisher.publish(plan, execute=True, confirmation=self.confirmation(plan))
        self.assertEqual(outcomes[0]["result"], "failed_stop_batch")
        self.assertEqual(len(self.client.patch_calls), 2)
        self.assertEqual(self.client.patch_calls[0][1], dict(plan.rows[0].proposed_values))
        self.assertEqual(self.client.patch_calls[1][1], dict(plan.rows[0].old_values))
        self.assertTrue(self.client.patch_calls[1][2].startswith("Prompt 5B controlled rollback"))

    def test_unrelated_change_is_detected_and_rolled_back_not_claimed_atomic(self) -> None:
        self.client.patch_behaviors["SBX-T-001"] = ["corrupt_unrelated", "success"]
        plan = self.plan()
        outcomes = self.publisher.publish(plan, execute=True, confirmation=self.confirmation(plan))
        self.assertEqual(outcomes[0]["result"], "failed_stop_batch")
        self.assertEqual(self.client.tests["SBX-T-001"].worksheet_json["data"]["Data"][39][0], "CHANGED")

    def test_multi_test_stops_after_first_failed_verification(self) -> None:
        batch, tests = make_records(3)
        client = FakeClient(batch, tests)
        client.patch_behaviors["SBX-T-002"] = ["silent_noop", "success"]
        publisher = Publisher(client, FIELDS, APPROVED_CONFIG, self.state)
        plan = publisher.prepare(batch.batch_id)
        outcomes = publisher.publish(
            plan,
            execute=True,
            confirmation=f"PUBLISH REVIEWED TERPENES BATCH {plan.batch_display_name}",
        )
        self.assertEqual([item["result"] for item in outcomes], ["published_verified", "failed_stop_batch"])
        patched_test_ids = [item[0] for item in client.patch_calls]
        self.assertNotIn("SBX-T-003", patched_test_ids)


class AuditTests(PublisherFixture):
    def test_audit_is_sanitized_and_manifest_hashes_match(self) -> None:
        plan = self.plan()
        directory = Path(self.temp.name) / "audit"
        artifacts = AuditWriter(directory).write("dry-run", plan, final_result="synthetic")
        json_text = Path(artifacts["json"]).read_text(encoding="utf-8")
        report_text = Path(artifacts["report"]).read_text(encoding="utf-8")
        manifest = json.loads(Path(artifacts["manifest"]).read_text(encoding="utf-8"))
        self.assertNotIn("SBX-T-001", json_text)
        self.assertNotIn("SBX-S-001", json_text)
        self.assertNotIn("Authorization: Bearer", json_text)
        self.assertNotIn("https://", json_text)
        self.assertEqual(manifest["files"][Path(artifacts["json"]).name], hashlib.sha256(json_text.encode()).hexdigest())
        self.assertEqual(manifest["files"][Path(artifacts["report"]).name], hashlib.sha256(report_text.encode()).hexdigest())

    def test_preflight_failure_creates_sanitized_audit(self) -> None:
        directory = Path(self.temp.name) / "preflight-audit"
        with (
            patch.dict("os.environ", {}, clear=True),
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()),
        ):
            result = main(
                [
                    "--audit-dir",
                    str(directory),
                    "dry-run",
                    "--batch-id",
                    "SBX-NOT-READ",
                ]
            )
        self.assertEqual(result, 2)
        files = sorted(directory.glob("*"))
        self.assertEqual(len(files), 3)
        json_path = next(path for path in files if path.name.endswith("dry-run.json"))
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["final_result"], "preflight_blocked:ConfigurationError")
        self.assertEqual(payload["rows"], [])
        self.assertEqual(payload["credential"], "not_recorded")


if __name__ == "__main__":
    unittest.main()
