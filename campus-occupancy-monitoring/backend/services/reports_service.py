"""
Servicio de persistencia de reportes – guarda y lee history.json
"""

import json
import os
from datetime import datetime

from config import REPORTS_FILE

def _ensure_file():
    os.makedirs(os.path.dirname(REPORTS_FILE), exist_ok=True)
    if not os.path.exists(REPORTS_FILE):
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump({"reports": []}, f, ensure_ascii=False, indent=2)


def save_report(analysis_result: dict) -> dict:
    _ensure_file()
    with open(REPORTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

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

    with open(REPORTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return report


def get_all_reports() -> list:
    _ensure_file()
    with open(REPORTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("reports", [])


def clear_reports() -> None:
    with open(REPORTS_FILE, "w", encoding="utf-8") as f:
        json.dump({"reports": []}, f, ensure_ascii=False, indent=2)
