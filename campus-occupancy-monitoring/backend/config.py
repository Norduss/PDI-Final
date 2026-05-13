"""
Configuración del Sistema de Monitoreo de Ocupación
Constantes y parámetros globales del sistema
"""

# Intervalo de actualización en minutos
UPDATE_INTERVAL_MINUTES = 15

# Configuración del sitio por defecto
DEFAULT_SITE_NAME = "Sótano 1"
DEFAULT_MAX_CAPACITY = 90

# Umbral de confianza para detección de YOLOv8
CONFIDENCE_THRESHOLD = 0.5

# Rutas de carpetas
CAPTURES_FOLDER = "captures"
PROCESSED_FOLDER = "processed"
MODELS_FOLDER = "models"

# Configuración de la cámara
CAMERA_INDEX = 0  # Índice de la cámara (0 para cámara por defecto)

# Umbrales de ocupación para clasificación de estado
OCCUPANCY_THRESHOLDS = {
    "empty": 10,           # Porcentaje máximo para considerar vacío
    "partial": 70,         # Porcentaje máximo para considerar parcialmente ocupado
    # Por encima de 70% se considera ocupado
}

# Configuración de estados
STATUS_LABELS = {
    "empty": "Vacío",
    "partial": "Parcialmente ocupado",
    "full": "Ocupado"
}

# Lista de sitios monitoreados (para futuras expansiones)
MONITORED_SITES = [
    {"id": 1, "name": "Sótano 1", "max_capacity": 90},
    {"id": 2, "name": "Sótano 2", "max_capacity": 80},
    {"id": 3, "name": "Biblioteca", "max_capacity": 150},
    {"id": 4, "name": "Cafetería", "max_capacity": 100},
]
