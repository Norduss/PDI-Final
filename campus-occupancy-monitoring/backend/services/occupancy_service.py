"""
Servicio de Ocupación
Clasifica el estado del laboratorio usando conteo absoluto de personas.
"""

import os
from datetime import datetime

from config import (
    DEFAULT_SITE_NAME,
    DEFAULT_MAX_CAPACITY,
    UPDATE_INTERVAL_MINUTES,
    PEOPLE_THRESHOLDS,
    STATUS_LABELS,
    CAPTURES_FOLDER,
    ALLOWED_EXTENSIONS,
)
from services.yolo_service import analyze_multiple_images


def classify_occupancy_by_count(people_count):
    """
    Clasifica el estado según el conteo absoluto de personas.
      0–4   → Vacío
      5–15  → Parcialmente lleno
      16+   → Lleno
    """
    if people_count <= PEOPLE_THRESHOLDS["empty_max"]:
        return STATUS_LABELS["empty"]
    elif people_count <= PEOPLE_THRESHOLDS["partial_max"]:
        return STATUS_LABELS["partial"]
    else:
        return STATUS_LABELS["full"]


def _list_images_in_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
        return []
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if "." in f and f.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS
    ]


def _build_response(site, capacity, image_results):
    total_people = sum(r["count"] for r in image_results)
    return {
        "site": site,
        "people_count": total_people,
        "max_capacity": capacity,
        "status": classify_occupancy_by_count(total_people),
        "image_results": image_results,
        "images_analyzed": len(image_results),
        "next_update": f"{UPDATE_INTERVAL_MINUTES} minutos",
        "last_update": datetime.now().strftime("%I:%M %p"),
    }


def analyze_captures(site_name=None, max_capacity=None):
    """
    Escanea la carpeta 'captures', procesa cada imagen con YOLO
    y retorna el estado agregado del laboratorio.
    """
    site = site_name or DEFAULT_SITE_NAME
    capacity = max_capacity or DEFAULT_MAX_CAPACITY
    image_paths = _list_images_in_folder(CAPTURES_FOLDER)

    if not image_paths:
        return {
            "site": site,
            "people_count": 0,
            "max_capacity": capacity,
            "status": STATUS_LABELS["empty"],
            "image_results": [],
            "images_analyzed": 0,
            "next_update": f"{UPDATE_INTERVAL_MINUTES} minutos",
            "last_update": datetime.now().strftime("%I:%M %p"),
            "message": "No hay imágenes en la carpeta de capturas. Sube imágenes para analizar.",
        }

    image_results = analyze_multiple_images(image_paths)
    return _build_response(site, capacity, image_results)


def analyze_uploaded_images(image_paths, site_name=None, max_capacity=None):
    """Procesa una lista de rutas (imágenes recién subidas) y retorna el estado agregado."""
    site = site_name or DEFAULT_SITE_NAME
    capacity = max_capacity or DEFAULT_MAX_CAPACITY
    image_results = analyze_multiple_images(image_paths)
    return _build_response(site, capacity, image_results)


def get_occupancy_history(site_name=None, limit=10):
    return []


def export_occupancy_to_csv(site_name=None, start_date=None, end_date=None):
    pass
