"""
Configuración del Sistema de Monitoreo de Ocupación
"""

UPDATE_INTERVAL_MINUTES = 15
DEFAULT_SITE_NAME = "Sótano 1"
DEFAULT_MAX_CAPACITY = 90
CONFIDENCE_THRESHOLD = 0.25

CAPTURES_FOLDER = "captures"
PROCESSED_FOLDER = "processed"
MODELS_FOLDER = "models"

CAMERA_INDEX = 0

# Umbrales basados en conteo ABSOLUTO de personas
# Vacío: 0 – 30 personas
# Parcialmente lleno: 30 – 60 personas
# Lleno: 60 o más personas

PEOPLE_THRESHOLDS = {
    "empty_max": 30,
    "partial_max": 60,
}

STATUS_LABELS = {
    "empty": "Vacío",
    "partial": "Parcialmente lleno",
    "full": "Lleno",
}

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "webp"}

REPORTS_FOLDER = "reports"
REPORTS_FILE = "reports/history.json"

DATASET_FOLDER = "../dataset"

MONITORED_SITES = [
    {"id": 1, "name": "Sótano 1", "max_capacity": 90}
]
