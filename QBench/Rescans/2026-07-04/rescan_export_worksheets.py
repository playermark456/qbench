#!/usr/bin/env python3
"""Read-only QBench Sandbox worksheet rescan/export helper.

The QBench "Export Spreadsheet" button is client-side for dynamic worksheets:
it loads `/worksheet/version/dynamic/{version_id}/config`, converts those
documents into `{config, qb_config, data}`, and saves the result as JSON. This
script performs the same read-only conversion without clicking any changing UI.

Credentials are read from environment variables and are never written to disk:
`QBENCH_EMAIL` and `QBENCH_PASSWORD`.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, Request, build_opener
import http.cookiejar


BASE_URL = "https://ait.qbench.net"
RESCAN_DATE = "2026-07-04"
USER_AGENT = "Mozilla/5.0"


@dataclass
class VersionInfo:
    version_id: str
    title: str
    status: str
    active: bool
    selected: bool


@dataclass
class WorksheetResult:
    worksheet_id: str
    worksheet_name: str = ""
    worksheet_type: str = ""
    page_found: bool = False
    export_button_found: bool = False
    is_dynamic: bool = False
    active_version_found: bool = False
    draft_version_found: bool = False
    selected_version: VersionInfo | None = None
    versions: list[VersionInfo] = field(default_factory=list)
    downloaded: bool = False
    local_file: str = ""
    previous_file: str = ""
    changed: str = "not downloaded"
    change_summary: str = ""
    error: str = ""


def request(opener: Any, path_or_url: str, *, data: bytes | None = None, accept_json: bool = False, timeout: int = 60) -> tuple[str, str]:
    url = path_or_url if path_or_url.startswith("http") else BASE_URL + path_or_url
    headers = {"User-Agent": USER_AGENT}
    if accept_json:
        headers["Accept"] = "application/json"
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    resp = opener.open(Request(url, data=data, headers=headers), timeout=timeout)
    body = resp.read().decode("utf-8", "replace")
    return body, resp.geturl()


def login(email: str, password: str) -> Any:
    cookie_jar = http.cookiejar.CookieJar()
    opener = build_opener(HTTPCookieProcessor(cookie_jar))
    login_page, _ = request(opener, "/assays")
    csrf_match = re.search(r'name="csrf_token"\s+value="([^"]+)"', login_page)
    if not csrf_match:
        raise RuntimeError("Could not find QBench CSRF token on login page.")
    payload = urlencode(
        {
            "csrf_token": csrf_match.group(1),
            "next_url": f"{BASE_URL}/worksheets",
            "timezone": "America/Chicago",
            "email": email,
            "password": password,
        }
    ).encode("utf-8")
    body, url = request(opener, "/login", data=payload, timeout=60)
    if "qbenchLoginLIMSForm" in body:
        raise RuntimeError("QBench login did not complete; login form was returned.")
    return opener


def slugify(value: str, default: str = "unknown") -> str:
    value = html.unescape(value or "").strip().lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or default


def truncate_slug(value: str, max_len: int = 56) -> str:
    if len(value) <= max_len:
        return value
    return value[:max_len].rstrip("_") or value[:max_len]


def folder_for_worksheet(name: str) -> str:
    n = name.lower()
    if "[logs]" in n or n.startswith("cold storage") or n.startswith("incubator temperature"):
        return "Other"
    if "homogeneity" in n:
        return "Homogeneity"
    if "cannabinoid" in n or "potency" in n:
        return "Cannabinoids"
    if "terpene" in n:
        return "Terpenes"
    if "heavy metal" in n:
        return "Heavy_Metals"
    if "pesticide" in n:
        return "Pesticides"
    if "mycotoxin" in n or "myco" in n:
        return "Mycotoxins"
    if "residual solvent" in n:
        return "Residual_Solvents"
    if "foreign material" in n:
        return "Foreign_Material"
    if "water activity" in n:
        return "Water_Activity"
    if "moisture" in n:
        return "Moisture_Analysis"
    if "stability" in n:
        return "Stability"
    if "aspergillus" in n:
        return "Microbiology/Aspergillus"
    if "enterobacteriaceae" in n:
        return "Microbiology/Enterobacteriaceae"
    if "salmonella" in n:
        return "Microbiology/Salmonella"
    if "stec" in n:
        return "Microbiology/STEC"
    if "listeria" in n:
        return "Microbiology/Listeria"
    if "yeast" in n or "mold" in n or "tymc" in n:
        return "Microbiology/TYMC"
    if "aerobic" in n or "tamc" in n:
        return "Microbiology/TAMC"
    if "microbial" in n or "microbiology" in n:
        return "Microbiology/General_Microbial_Analysis"
    return "Other"


def discover_worksheet_ids(opener: Any) -> list[str]:
    body, _ = request(opener, "/worksheets", timeout=90)
    ids = sorted(set(re.findall(r"/worksheet\?id=(\d+)", body)), key=lambda x: int(x))
    return ids


def parse_versions(page: str) -> list[VersionInfo]:
    versions: list[VersionInfo] = []
    option_re = re.compile(
        r"<option\s+value=\"(?P<id>\d+)\"\s+data-status=\"(?P<status>[^\"]*)\"\s+data-active=\"(?P<active>[^\"]*)\"(?P<attrs>.*?)>(?P<title>.*?)</option>",
        re.I | re.S,
    )
    for match in option_re.finditer(page):
        title = html.unescape(re.sub(r"\s+", " ", match.group("title")).strip())
        versions.append(
            VersionInfo(
                version_id=match.group("id"),
                title=title,
                status=match.group("status"),
                active=match.group("active").lower() == "true",
                selected="selected" in match.group("attrs").lower(),
            )
        )
    return versions


def choose_version(versions: list[VersionInfo]) -> VersionInfo | None:
    active_approved = [v for v in versions if v.active and v.status.upper() == "APPROVED"]
    if active_approved:
        return active_approved[0]
    active = [v for v in versions if v.active]
    if active:
        return active[0]
    selected = [v for v in versions if v.selected]
    if selected:
        return selected[0]
    return versions[0] if versions else None


def parse_worksheet_page(worksheet_id: str, page: str) -> WorksheetResult:
    result = WorksheetResult(worksheet_id=worksheet_id, page_found="qbenchWorksheetForm" in page)
    name_match = re.search(r'data-qbench-attr="name"[^>]*value="([^"]*)"', page, re.I | re.S)
    if name_match:
        result.worksheet_name = html.unescape(name_match.group(1))
    type_block = re.search(r'data-qbench-attr="type".*?</select>', page, re.I | re.S)
    if type_block:
        selected_type = re.search(r'<option[^>]*value="([^"]+)"[^>]*selected', type_block.group(0), re.I | re.S)
        if selected_type:
            result.worksheet_type = selected_type.group(1)
    result.export_button_found = "qbench-export-spreadsheet" in page
    result.is_dynamic = re.search(r"IS_DYNAMIC_SPREADSHEET_WORKSHEET\s*=\s*true", page) is not None
    result.versions = parse_versions(page)
    result.selected_version = choose_version(result.versions)
    result.active_version_found = any(v.active and v.status.upper() == "APPROVED" for v in result.versions)
    result.draft_version_found = any(v.status.upper() in {"DRAFT", "PENDING"} for v in result.versions)
    return result


def excel_to_coords(cell: str) -> tuple[int, int]:
    letters = "".join(ch for ch in cell if ch.isalpha()).upper()
    digits = "".join(ch for ch in cell if ch.isdigit())
    col = 0
    for ch in letters:
        col = col * 26 + (ord(ch) - 64)
    return int(digits) - 1, col - 1


def set_ws_data(worksheets: dict[int, dict[str, Any]], tab_index: int, cell: str, value: Any) -> None:
    row, col = excel_to_coords(cell)
    try:
        worksheets[tab_index]["data"][row][col] = value
    except Exception:
        return


def convert_dynamic_documents(documents: list[dict[str, Any]], version_id: str) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for document in documents:
        grouped[str(document.get("entity_id"))].append(document)
    docs = grouped.get(str(version_id), documents)

    ws_config: dict[str, Any] = {}
    qb_config: dict[str, Any] = {}
    worksheets: dict[int, dict[str, Any]] = {}
    processed_data: dict[str, Any] = {}

    for document in docs:
        doc_type = document.get("type")
        data = document.get("data")
        if doc_type == "CONFIG" and isinstance(data, dict):
            ws_config.update(data)
        elif doc_type == "STYLE":
            ws_config["style"] = data
        elif doc_type == "QB_CONFIG" and isinstance(data, dict):
            qb_config.update(data)
        elif doc_type == "NAMED_CELLS":
            qb_config["named_cells"] = data
        elif doc_type in {"WORKSHEET_CONFIG", "WORKSHEET_DATA", "WORKSHEET_STYLE"}:
            tab_index = int(document.get("tab_index") or 0)
            if tab_index not in worksheets:
                worksheets[tab_index] = {}
            if doc_type == "WORKSHEET_CONFIG" and isinstance(data, dict):
                worksheets[tab_index].update(data)
            elif doc_type == "WORKSHEET_DATA":
                worksheets[tab_index]["data"] = data
                worksheets[tab_index]["worksheetId"] = document.get("tab_id") or worksheets[tab_index].get("worksheetId")
            elif doc_type == "WORKSHEET_STYLE":
                worksheets[tab_index]["style"] = data

    for document in docs:
        tab_index = int(document.get("tab_index") or 0)
        doc_type = document.get("type")
        data = document.get("data")
        if tab_index not in worksheets or not isinstance(data, dict):
            continue
        if doc_type in {"WORKSHEET_FORMULAS", "WORKSHEET_IMAGE_DATA", "WORKSHEET_DOLLAR_REFERENCES"}:
            for excel_cell, value in data.items():
                set_ws_data(worksheets, tab_index, excel_cell, value)
                if doc_type == "WORKSHEET_DOLLAR_REFERENCES":
                    raw_data = document.get("raw_data") or {}
                    if excel_cell in raw_data:
                        worksheets[tab_index].setdefault("cells", {}).setdefault(excel_cell, {})["dollarReference"] = raw_data[excel_cell]

    for document in docs:
        if document.get("type") == "WORKSHEET_DATA_PROCESSED":
            sheet_name = document.get("worksheet_name")
            if not sheet_name:
                tab_index = int(document.get("tab_index") or 0)
                sheet_name = worksheets.get(tab_index, {}).get("worksheetName") or f"Worksheet {tab_index}"
            processed_data[sheet_name] = document.get("data")

    ws_config["worksheets"] = [worksheets[i] for i in sorted(worksheets)]
    return {"config": ws_config, "qb_config": qb_config, "data": processed_data}


def export_dynamic(opener: Any, version_id: str) -> dict[str, Any]:
    path = f"/worksheet/version/dynamic/{version_id}/config?exclude_types=WORKSHEET_DOLLAR_REFERENCES&construct_worksheet_data_array=true"
    body, _ = request(opener, path, accept_json=True, timeout=120)
    payload = json.loads(body)
    return convert_dynamic_documents(payload.get("data") or [], version_id)


def export_legacy(opener: Any, version_id: str) -> dict[str, Any]:
    body, _ = request(opener, f"/worksheet/version/get?id={version_id}", accept_json=True, timeout=120)
    payload = json.loads(body)
    if isinstance(payload, dict):
        return payload
    raise RuntimeError("Legacy worksheet version endpoint did not return a JSON object.")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_hash(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    encoded = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def collect_formulas(obj: Any, prefix: str = "") -> dict[str, str]:
    formulas: dict[str, str] = {}
    if isinstance(obj, str) and obj.startswith("="):
        formulas[prefix] = obj
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            formulas.update(collect_formulas(value, f"{prefix}[{idx}]"))
    elif isinstance(obj, dict):
        for key, value in obj.items():
            formulas.update(collect_formulas(value, f"{prefix}.{key}" if prefix else str(key)))
    return formulas


def get_named_cells(obj: dict[str, Any]) -> dict[str, Any]:
    named = (obj.get("qb_config") or {}).get("named_cells") or {}
    return named if isinstance(named, dict) else {}


def summarize_diff(old_path: Path | None, new_path: Path) -> tuple[str, str]:
    if not old_path or not old_path.exists():
        return "new", "No previous worksheet export found in QBench/Worksheets."
    old_hash = sha256(old_path)
    new_hash = sha256(new_path)
    if old_hash == new_hash:
        return "unchanged", f"Exact SHA-256 match with prior export `{old_path.name}`."
    try:
        old_canon = canonical_json_hash(old_path)
        new_canon = canonical_json_hash(new_path)
        if old_canon == new_canon:
            return "unchanged", f"Canonical JSON match with prior export `{old_path.name}`; file byte order/format differs."
    except Exception:
        pass

    old = json.loads(old_path.read_text(encoding="utf-8"))
    new = json.loads(new_path.read_text(encoding="utf-8"))
    pieces: list[str] = []

    old_tabs = [ws.get("worksheetName") for ws in (old.get("config") or {}).get("worksheets", []) if isinstance(ws, dict)]
    new_tabs = [ws.get("worksheetName") for ws in (new.get("config") or {}).get("worksheets", []) if isinstance(ws, dict)]
    if old_tabs != new_tabs:
        pieces.append(f"Tabs changed from {old_tabs} to {new_tabs}.")

    old_named = get_named_cells(old)
    new_named = get_named_cells(new)
    added_named = sorted(set(new_named) - set(old_named))
    removed_named = sorted(set(old_named) - set(new_named))
    changed_named = sorted(
        name
        for name in set(old_named) & set(new_named)
        if old_named.get(name, {}).get("cell") != new_named.get(name, {}).get("cell")
        or old_named.get(name, {}).get("display_name") != new_named.get(name, {}).get("display_name")
    )
    if added_named:
        pieces.append(f"Named cells added: {', '.join(added_named[:20])}{'...' if len(added_named) > 20 else ''}.")
    if removed_named:
        pieces.append(f"Named cells removed: {', '.join(removed_named[:20])}{'...' if len(removed_named) > 20 else ''}.")
    if changed_named:
        pieces.append(f"Named cells changed: {', '.join(changed_named[:20])}{'...' if len(changed_named) > 20 else ''}.")

    old_formulas = collect_formulas(old.get("config") or {})
    new_formulas = collect_formulas(new.get("config") or {})
    formula_delta = len(set(old_formulas.items()) ^ set(new_formulas.items()))
    if formula_delta:
        pieces.append(f"Formula entries differ ({len(old_formulas)} prior vs {len(new_formulas)} new; delta count {formula_delta}).")

    for named_cell in ["report_results", "pass_fail", "report_header", "report_content"]:
        old_cell = old_named.get(named_cell, {}).get("cell") if isinstance(old_named.get(named_cell), dict) else None
        new_cell = new_named.get(named_cell, {}).get("cell") if isinstance(new_named.get(named_cell), dict) else None
        if old_cell != new_cell:
            pieces.append(f"`{named_cell}` changed from `{old_cell}` to `{new_cell}`.")

    old_styles = json.dumps((old.get("config") or {}).get("style", []), sort_keys=True)
    new_styles = json.dumps((new.get("config") or {}).get("style", []), sort_keys=True)
    if old_styles != new_styles:
        pieces.append("Workbook style list changed.")

    return "changed", " ".join(pieces) if pieces else "JSON differs; no high-level worksheet/name/formula/named-cell summary generated."


def build_baseline_map(repo_root: Path) -> dict[str, Path]:
    candidates: dict[str, list[Path]] = defaultdict(list)
    for path in (repo_root / "QBench" / "Worksheets").rglob("*.json"):
        match = re.search(r"ws_id_(\d+)", path.name)
        if match:
            candidates[match.group(1)].append(path)
    baseline: dict[str, Path] = {}
    for worksheet_id, paths in candidates.items():
        active = [p for p in paths if "__active__" in p.name]
        selected = active or paths
        baseline[worksheet_id] = sorted(selected, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    return baseline


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def export_worksheets(repo_root: Path, ids: list[str], email: str, password: str) -> list[WorksheetResult]:
    opener = login(email, password)
    baseline_map = build_baseline_map(repo_root)
    base = repo_root / "QBench" / "Rescans" / RESCAN_DATE
    results: list[WorksheetResult] = []

    for index, worksheet_id in enumerate(ids, start=1):
        result = WorksheetResult(worksheet_id=worksheet_id)
        try:
            page, _ = request(opener, f"/worksheet?id={worksheet_id}", timeout=90)
            result = parse_worksheet_page(worksheet_id, page)
            if not result.page_found:
                result.error = "Worksheet page did not expose qbenchWorksheetForm."
            elif not result.export_button_found:
                result.error = "Export Spreadsheet control not visible on page."
            elif not result.selected_version:
                result.error = "No worksheet version found."
            else:
                version = result.selected_version
                if result.is_dynamic:
                    exported = export_dynamic(opener, version.version_id)
                else:
                    exported = export_legacy(opener, version.version_id)
                folder = folder_for_worksheet(result.worksheet_name)
                assay_slug = slugify(folder.split("/")[-1], default="other")
                status = "active" if version.active else version.status.lower() or "unknown"
                filename = f"{assay_slug}__id_{worksheet_id}__worksheet_export_spreadsheet__{status}__{RESCAN_DATE}.json"
                new_path = base / "Worksheets" / folder / filename
                write_json(new_path, exported)
                result.downloaded = True
                result.local_file = str(new_path.relative_to(repo_root)).replace("\\", "/")
                previous = baseline_map.get(worksheet_id)
                if previous:
                    result.previous_file = str(previous.relative_to(repo_root)).replace("\\", "/")
                changed, summary = summarize_diff(previous, new_path)
                result.changed = changed
                result.change_summary = summary
        except (HTTPError, URLError, TimeoutError, RuntimeError, json.JSONDecodeError) as exc:
            result.error = f"{type(exc).__name__}: {exc}"
        except Exception as exc:
            result.error = f"Unexpected {type(exc).__name__}: {exc}"
        results.append(result)
        print(f"[{index}/{len(ids)}] worksheet {worksheet_id}: {'downloaded' if result.downloaded else 'failed'} {result.worksheet_name or ''} {result.error or ''}", flush=True)
        time.sleep(0.1)

    return results


def markdown_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def result_to_record(result: WorksheetResult) -> dict[str, Any]:
    version = result.selected_version
    return {
        "worksheet_id": result.worksheet_id,
        "worksheet_name": result.worksheet_name,
        "worksheet_type": result.worksheet_type,
        "page_found": result.page_found,
        "export_button_found": result.export_button_found,
        "dynamic": result.is_dynamic,
        "active_version_found": result.active_version_found,
        "draft_version_found": result.draft_version_found,
        "selected_version_id": version.version_id if version else "",
        "selected_version_title": version.title if version else "",
        "selected_version_status": version.status if version else "",
        "selected_version_active": version.active if version else False,
        "versions": [v.__dict__ for v in result.versions],
        "downloaded": result.downloaded,
        "local_file": result.local_file,
        "previous_file": result.previous_file,
        "changed": result.changed,
        "change_summary": result.change_summary,
        "error": result.error,
    }


def write_rescan_docs(repo_root: Path, results: list[WorksheetResult]) -> None:
    base = repo_root / "QBench" / "Rescans" / RESCAN_DATE
    records = [result_to_record(r) for r in results]
    (base / "worksheet_rescan_metadata.json").write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    downloaded = [r for r in results if r.downloaded]
    changed = [r for r in downloaded if r.changed == "changed"]
    unchanged = [r for r in downloaded if r.changed == "unchanged"]
    new = [r for r in downloaded if r.changed == "new"]
    failed = [r for r in results if not r.downloaded]
    assays = Counter(folder_for_worksheet(r.worksheet_name) for r in results if r.worksheet_name)

    summary_lines = [
        f"# QBench Sandbox Rescan Summary - {RESCAN_DATE}",
        "",
        "## Scope",
        "",
        "Read-only QBench Sandbox rescan of visible worksheet/template pages. Dynamic worksheet JSON files were rebuilt from the same read-only version config endpoint used by QBench's client-side Export Spreadsheet button.",
        "",
        "## Assays Scanned",
        "",
    ]
    for assay, count in sorted(assays.items()):
        summary_lines.append(f"- {assay}: {count} worksheet page(s)")
    summary_lines.extend(
        [
            "",
            "## Totals",
            "",
            f"- Worksheet/template pages scanned: {len(results)}",
            f"- Export Spreadsheet JSON files saved locally: {len(downloaded)}",
            f"- Unchanged worksheets: {len(unchanged)}",
            f"- Changed worksheets: {len(changed)}",
            f"- New worksheets: {len(new)}",
            f"- Failed downloads/exports: {len(failed)}",
            "",
            "## Worksheets Downloaded",
            "",
        ]
    )
    for result in downloaded:
        summary_lines.append(f"- {result.worksheet_id} {result.worksheet_name}: `{result.local_file}` ({result.changed})")
    summary_lines.extend(["", "## Failed Downloads", ""])
    if failed:
        for result in failed:
            summary_lines.append(f"- {result.worksheet_id} {result.worksheet_name or '(unknown)'}: {result.error}")
    else:
        summary_lines.append("None.")
    summary_lines.extend(
        [
            "",
            "## Manual Actions Needed",
            "",
            "- Browser connector and bundled Playwright were unavailable in this Codex session, so no visible UI click/download event could be captured. If strict button-click provenance is required, manually verify representative exports in QBench Sandbox.",
        ]
    )
    (base / "rescan_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    change_lines = [
        f"# Worksheet Change Log - {RESCAN_DATE}",
        "",
        "| Assay | Worksheet/template | Status | Previous file | New file | Changed? | Summary of changes |",
        "|---|---|---|---|---|---|---|",
    ]
    for result in results:
        version = result.selected_version
        status = "not downloaded"
        if version:
            status = "active" if version.active else version.status.lower()
        change_lines.append(
            "| "
            + " | ".join(
                markdown_escape(value)
                for value in [
                    folder_for_worksheet(result.worksheet_name),
                    f"{result.worksheet_name} (ID {result.worksheet_id})",
                    status,
                    result.previous_file or "",
                    result.local_file or "",
                    result.changed,
                    result.change_summary or result.error,
                ]
            )
            + " |"
        )
    (base / "worksheet_change_log.md").write_text("\n".join(change_lines) + "\n", encoding="utf-8")

    status_lines = [
        f"# Download Status - {RESCAN_DATE}",
        "",
        "| Assay | Worksheet page found? | Active version found? | Draft version found? | Export Spreadsheet downloaded? | Local file path | Notes |",
        "|---|---|---|---|---|---|---|",
    ]
    for result in results:
        status_lines.append(
            "| "
            + " | ".join(
                markdown_escape(value)
                for value in [
                    folder_for_worksheet(result.worksheet_name),
                    "Yes" if result.page_found else "No",
                    "Yes" if result.active_version_found else "No",
                    "Yes" if result.draft_version_found else "No",
                    "Yes" if result.downloaded else "No",
                    result.local_file,
                    result.error or result.change_summary,
                ]
            )
            + " |"
        )
    (base / "download_status.md").write_text("\n".join(status_lines) + "\n", encoding="utf-8")

    open_lines = [
        f"# Open Questions - {RESCAN_DATE}",
        "",
        "## Failed Worksheet Downloads",
        "",
    ]
    if failed:
        for result in failed:
            open_lines.append(f"- Worksheet ID {result.worksheet_id} `{result.worksheet_name or '(unknown)'}`: {result.error}")
    else:
        open_lines.append("None recorded.")
    open_lines.extend(["", "## Active vs Draft Status Unclear", ""])
    unclear = [r for r in results if r.page_found and not r.active_version_found]
    if unclear:
        for result in unclear:
            open_lines.append(f"- Worksheet ID {result.worksheet_id} `{result.worksheet_name}` did not expose an active approved version in the parsed selector.")
    else:
        open_lines.append("None recorded.")
    open_lines.extend(
        [
            "",
            "## Screenshots or Named-Cell Captures Only",
            "",
            "None recorded.",
            "",
            "## Parser Internals Not Visible",
            "",
            "Parser pages still need browser/UI inspection or a parser export endpoint. No parser export was performed by this worksheet rescan helper.",
            "",
            "## Automations Not Fully Visible",
            "",
            "Automation pages still need browser/UI inspection or an automation export endpoint. No automation export was performed by this worksheet rescan helper.",
            "",
            "## Assets Not Downloadable",
            "",
            "COA/report assets were not downloaded by this worksheet rescan helper.",
            "",
            "## Pages Requiring Modification To Proceed",
            "",
            "None encountered by the read-only worksheet GET/export process.",
            "",
            "## Tooling Limitation",
            "",
            "The in-app browser connector failed to start and the bundled Playwright package was incomplete. The rescan therefore used authenticated read-only QBench HTTP GET requests and the same client-side dynamic worksheet conversion used by Export Spreadsheet.",
        ]
    )
    (base / "open_questions.md").write_text("\n".join(open_lines) + "\n", encoding="utf-8")


def append_master_export_status(repo_root: Path, results: list[WorksheetResult]) -> None:
    path = repo_root / "QBench" / "Docs" / "qbench_export_status.md"
    marker = f"\n\n## Rescan {RESCAN_DATE}\n"
    existing = path.read_text(encoding="utf-8") if path.exists() else "# QBench Export Status\n"
    if marker.strip() in existing:
        existing = existing.split(marker.strip(), 1)[0].rstrip() + "\n"
    lines = [
        existing.rstrip(),
        "",
        f"## Rescan {RESCAN_DATE}",
        "",
        "| Assay | Worksheet page found? | Active/approved version found? | Export Spreadsheet downloaded? | Local file path | Notes |",
        "|---|---|---|---|---|---|",
    ]
    for result in results:
        lines.append(
            "| "
            + " | ".join(
                markdown_escape(value)
                for value in [
                    folder_for_worksheet(result.worksheet_name),
                    "Yes" if result.page_found else "No",
                    "Yes" if result.active_version_found else "No",
                    "Yes" if result.downloaded else "No",
                    result.local_file,
                    f"{result.changed}; {result.change_summary or result.error}",
                ]
            )
            + " |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_named_cell_index(repo_root: Path, results: list[WorksheetResult]) -> None:
    path = repo_root / "QBench" / "NAMED_CELL_INDEX.md"
    lines = [path.read_text(encoding="utf-8").rstrip() if path.exists() else "# Named Cell Index"]
    lines.extend(["", f"## Rescan {RESCAN_DATE} Named-Cell Changes", ""])
    changed_or_new = [r for r in results if r.downloaded and r.changed in {"changed", "new"}]
    if not changed_or_new:
        lines.append("No changed or new worksheet named cells found during this rescan.")
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return
    lines.extend(["| Assay | Worksheet | Named Cell | Cell/Range | Purpose | Used by COA? | Notes |", "|---|---|---|---|---|---|---|"])
    repo = repo_root
    for result in changed_or_new:
        new_path = repo / result.local_file
        try:
            obj = json.loads(new_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        for system_name, info in sorted(get_named_cells(obj).items()):
            cell = info.get("cell", "") if isinstance(info, dict) else ""
            display = info.get("display_name", "") if isinstance(info, dict) else ""
            used_by_coa = "Yes" if system_name in {"pass_fail", "report_results", "report_header", "report_content", "homogeneity_metrc"} else "Unknown"
            lines.append(
                "| "
                + " | ".join(
                    markdown_escape(value)
                    for value in [
                        folder_for_worksheet(result.worksheet_name),
                        result.worksheet_name,
                        system_name,
                        cell,
                        display,
                        used_by_coa,
                        f"Discovered/verified in {RESCAN_DATE} rescan ({result.changed}).",
                    ]
                )
                + " |"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_system_map(repo_root: Path, results: list[WorksheetResult]) -> None:
    path = repo_root / "QBench" / "SYSTEM_MAP.md"
    existing = path.read_text(encoding="utf-8").rstrip() if path.exists() else "# QBench System Map"
    downloaded = [r for r in results if r.downloaded]
    changed = [r for r in downloaded if r.changed == "changed"]
    new = [r for r in downloaded if r.changed == "new"]
    lines = [
        existing,
        "",
        f"## Rescan {RESCAN_DATE}",
        "",
        f"- Worksheet/template pages scanned: {len(results)}.",
        f"- Export Spreadsheet JSON files saved locally: {len(downloaded)}.",
        f"- Changed worksheets: {len(changed)}.",
        f"- New worksheets: {len(new)}.",
        "- Parser, automation, and COA source inspection remains limited by browser/tooling availability unless separately completed.",
    ]
    if changed:
        lines.append("- Changed worksheet IDs: " + ", ".join(f"{r.worksheet_id} ({r.worksheet_name})" for r in changed[:50]) + ("..." if len(changed) > 50 else ""))
    if new:
        lines.append("- New worksheet IDs: " + ", ".join(f"{r.worksheet_id} ({r.worksheet_name})" for r in new[:50]) + ("..." if len(new) > 50 else ""))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Rescan QBench Sandbox worksheet exports.")
    parser.add_argument("--repo-root", type=Path, default=Path(r"C:\Users\Mark Adams\Documents\GitHub\qbench"))
    parser.add_argument("--ids", nargs="*", default=None, help="Worksheet IDs to export. Defaults to all visible IDs from /worksheets.")
    parser.add_argument("--discover-only", action="store_true")
    args = parser.parse_args()

    email = os.environ.get("QBENCH_EMAIL")
    password = os.environ.get("QBENCH_PASSWORD")
    if not email or not password:
        raise SystemExit("Set QBENCH_EMAIL and QBENCH_PASSWORD environment variables.")

    opener = login(email, password)
    ids = args.ids or discover_worksheet_ids(opener)
    if args.discover_only:
        print("\n".join(ids))
        return 0

    results = export_worksheets(args.repo_root, ids, email, password)
    write_rescan_docs(args.repo_root, results)
    append_master_export_status(args.repo_root, results)
    append_named_cell_index(args.repo_root, results)
    append_system_map(args.repo_root, results)

    downloaded = sum(1 for r in results if r.downloaded)
    failed = sum(1 for r in results if not r.downloaded)
    print(f"Completed worksheet rescan: {len(results)} scanned, {downloaded} saved, {failed} failed.")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
