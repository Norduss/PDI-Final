"""
Rutas de la API para el monitoreo de ocupación
"""

import os
import random
from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

from services.occupancy_service import analyze_captures, analyze_uploaded_images
from services.yolo_service import get_model_info
from services.reports_service import save_report, get_all_reports, clear_reports
from config import CAPTURES_FOLDER, PROCESSED_FOLDER, ALLOWED_EXTENSIONS, MONITORED_SITES, DATASET_FOLDER

occupancy_bp = Blueprint("occupancy", __name__)


def _allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------------------------------------------------------------------
# Estado actual (escanea la carpeta captures)
# ---------------------------------------------------------------------------

@occupancy_bp.route("/estado-actual", methods=["GET"])
def get_current_status():
    """Devuelve el último reporte guardado. Si no hay ninguno, retorna estado vacío."""
    try:
        reports = get_all_reports()
        if reports:
            last = reports[0]
            data = {
                "site": last.get("site", "Sótano 1"),
                "people_count": last.get("people_count", 0),
                "status": last.get("status", ""),
                "images_analyzed": last.get("images_analyzed", 0),
                "last_update": last.get("date_display", "--"),
                "next_update": "Al subir nuevas imágenes",
                "image_results": [],
                "message": "Último análisis cargado",
            }
        else:
            data = {
                "site": "Sótano 1",
                "people_count": 0,
                "status": "Sin analizar",
                "images_analyzed": 0,
                "last_update": "--",
                "next_update": "--",
                "image_results": [],
                "message": "No hay imágenes en la carpeta de capturas. Sube imágenes para analizar.",
            }
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ---------------------------------------------------------------------------
# Subida y análisis de imágenes
# ---------------------------------------------------------------------------

@occupancy_bp.route("/analizar", methods=["POST"])
def analyze_images():
    """
    Recibe una o varias imágenes (campo 'images'), las guarda en captures/ y
    las procesa con YOLO. Retorna el conteo agregado y el estado del laboratorio.
    """
    try:
        if "images" not in request.files:
            return jsonify({"status": "error", "message": "No se enviaron imágenes (campo 'images')"}), 400

        files = request.files.getlist("images")
        if not files or all(f.filename == "" for f in files):
            return jsonify({"status": "error", "message": "No se seleccionaron archivos"}), 400

        os.makedirs(CAPTURES_FOLDER, exist_ok=True)
        saved_paths = []

        for file in files:
            if file and _allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(CAPTURES_FOLDER, filename)
                file.save(filepath)
                saved_paths.append(filepath)

        if not saved_paths:
            return jsonify({
                "status": "error",
                "message": "Ningún archivo tenía extensión válida (jpg, png, jpeg, bmp, webp)",
            }), 400

        result = analyze_uploaded_images(saved_paths)
        save_report(result)

        for path in saved_paths:
            try:
                os.remove(path)
            except OSError:
                pass

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ---------------------------------------------------------------------------
# Servir imágenes (procesadas y originales)
# ---------------------------------------------------------------------------

@occupancy_bp.route("/imagen/procesada/<path:filename>", methods=["GET"])
def serve_processed_image(filename):
    return send_from_directory(os.path.abspath(PROCESSED_FOLDER), filename)


@occupancy_bp.route("/imagen/captura/<path:filename>", methods=["GET"])
def serve_capture_image(filename):
    return send_from_directory(os.path.abspath(CAPTURES_FOLDER), filename)


# ---------------------------------------------------------------------------
# Sitios y salud del servicio
# ---------------------------------------------------------------------------

@occupancy_bp.route("/sitios", methods=["GET"])
def get_monitored_sites():
    return jsonify({"status": "success", "data": MONITORED_SITES}), 200


@occupancy_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "occupancy-monitoring",
        "yolo": get_model_info(),
    }), 200


# ---------------------------------------------------------------------------
# Análisis desde dataset
# ---------------------------------------------------------------------------

@occupancy_bp.route("/analizar-dataset", methods=["POST"])
def analyze_dataset():
    """
    Escanea la carpeta 'dataset/' recursivamente, elige 5 imágenes al azar
    (sin repetición), las procesa con YOLO y guarda el reporte.
    """
    try:
        dataset_path = os.path.abspath(DATASET_FOLDER)
        if not os.path.exists(dataset_path):
            return jsonify({"status": "error", "message": f"La carpeta '{DATASET_FOLDER}' no existe. Créala y agrega imágenes."}), 400

        all_images = []
        for root, _, files in os.walk(dataset_path):
            for f in files:
                if "." in f and f.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS:
                    all_images.append(os.path.join(root, f))

        if not all_images:
            return jsonify({"status": "error", "message": "No hay imágenes en la carpeta 'dataset'. Agrega imágenes JPG/PNG/BMP/WEBP."}), 400

        sample_size = min(5, len(all_images))
        selected = random.sample(all_images, sample_size)

        result = analyze_uploaded_images(selected)
        save_report(result)
        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ---------------------------------------------------------------------------
# Reportes históricos
# ---------------------------------------------------------------------------

@occupancy_bp.route("/reportes", methods=["GET"])
def get_reports():
    try:
        return jsonify({"status": "success", "data": get_all_reports()}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@occupancy_bp.route("/reportes", methods=["DELETE"])
def delete_reports():
    try:
        clear_reports()
        return jsonify({"status": "success", "message": "Historial eliminado"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
