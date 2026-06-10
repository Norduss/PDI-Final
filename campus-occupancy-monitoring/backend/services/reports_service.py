"""
Servicio de persistencia de reportes – guarda y lee history.json
"""

import json
import os
from datetime import datetime, timedelta

from config import ALLOWED_EXTENSIONS, PROCESSED_FOLDER, REPORTS_FILE, REPORT_EXPIRATION_HOURS

def _ensure_file():
    os.makedirs(os.path.dirname(REPORTS_FILE), exist_ok=True)
    if not os.path.exists(REPORTS_FILE):
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump({"reports": []}, f, ensure_ascii=False, indent=2)


def _load_data() -> dict:
    _ensure_file()
    with open(REPORTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_data(data: dict) -> None:
    with open(REPORTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _parse_timestamp(value: str):
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def _delete_processed_image(filename: str) -> None:
    if not filename:
        return

    safe_filename = os.path.basename(str(filename))
    image_path = os.path.join(PROCESSED_FOLDER, safe_filename)

    try:
        if os.path.isfile(image_path):
            os.remove(image_path)
    except OSError:
        pass


def _delete_report_images(report: dict) -> None:
    for image in report.get("processed_images", []):
        filename = image.get("filename") if isinstance(image, dict) else image
        _delete_processed_image(filename)


def _delete_expired_orphan_processed_images(cutoff: datetime) -> None:
    if not os.path.isdir(PROCESSED_FOLDER):
        return

    for filename in os.listdir(PROCESSED_FOLDER):
        if "." not in filename:
            continue

        extension = filename.rsplit(".", 1)[-1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            continue

        path = os.path.join(PROCESSED_FOLDER, filename)
        try:
            modified_at = datetime.fromtimestamp(os.path.getmtime(path))
            if modified_at < cutoff:
                os.remove(path)
        except OSError:
            pass


def purge_expired_reports() -> int:
    """Elimina reportes e imagenes procesadas vencidas."""
    data = _load_data()
    reports = data.get("reports", [])
    cutoff = datetime.now() - timedelta(hours=REPORT_EXPIRATION_HOURS)
    active_reports = []
    deleted_count = 0

    for report in reports:
        timestamp = _parse_timestamp(report.get("timestamp"))
        if timestamp and timestamp < cutoff:
            _delete_report_images(report)
            deleted_count += 1
        else:
            active_reports.append(report)

    if deleted_count:
        data["reports"] = active_reports
        _save_data(data)

    _delete_expired_orphan_processed_images(cutoff)
    return deleted_count


def save_report(analysis_result: dict) -> dict:
    purge_expired_reports()
    data = _load_data()

    now = datetime.now()
    report = {
        "id": now.strftime("%Y%m%d%H%M%S%f"),
        "timestamp": now.isoformat(),
        "date_display": now.strftime("%d %b %Y, %I:%M %p"),
        "site": analysis_result.get("site", "Sótano 1"),
        "people_count": analysis_result.get("people_count", 0),
        "status": analysis_result.get("status", ""),
        "images_analyzed": analysis_result.get("images_analyzed", 0),
        "image_names": [
            r.get("source_image", "") for r in analysis_result.get("image_results", [])
        ],
        "processed_images": [
            {
                "filename": r.get("processed_image_filename", ""),
                "count": r.get("count", 0),
            }
            for r in analysis_result.get("image_results", [])
            if r.get("processed_image_filename")
        ],
    }
    data["reports"].insert(0, report)

    _save_data(data)

    return report


def get_all_reports() -> list:
    purge_expired_reports()
    data = _load_data()
    return data.get("reports", [])


def clear_reports() -> None:
    data = _load_data()
    for report in data.get("reports", []):
        _delete_report_images(report)

    if os.path.isdir(PROCESSED_FOLDER):
        for filename in os.listdir(PROCESSED_FOLDER):
            _delete_processed_image(filename)

    _save_data({"reports": []})
