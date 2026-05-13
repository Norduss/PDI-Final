"""
Servicio de Ocupación
Gestiona la lógica de negocio para el monitoreo de ocupación
"""

from datetime import datetime
from config import (
    DEFAULT_SITE_NAME,
    DEFAULT_MAX_CAPACITY,
    UPDATE_INTERVAL_MINUTES,
    OCCUPANCY_THRESHOLDS,
    STATUS_LABELS
)


def classify_occupancy_status(occupancy_percentage):
    """
    Clasifica el estado de ocupación basado en el porcentaje.
    
    Args:
        occupancy_percentage (float): Porcentaje de ocupación (0-100)
    
    Returns:
        str: Estado de ocupación (Vacío, Parcialmente ocupado, Ocupado)
    """
    if occupancy_percentage <= OCCUPANCY_THRESHOLDS["empty"]:
        return STATUS_LABELS["empty"]
    elif occupancy_percentage <= OCCUPANCY_THRESHOLDS["partial"]:
        return STATUS_LABELS["partial"]
    else:
        return STATUS_LABELS["full"]


def get_current_occupancy_status(site_name=None, max_capacity=None):
    """
    Obtiene el estado actual de ocupación.
    
    En la versión actual, retorna datos simulados estructurados
    como si vinieran de la detección con YOLOv8.
    
    Args:
        site_name (str, optional): Nombre del sitio. Por defecto usa DEFAULT_SITE_NAME
        max_capacity (int, optional): Capacidad máxima. Por defecto usa DEFAULT_MAX_CAPACITY
    
    Returns:
        dict: Diccionario con los datos de ocupación
    """
    # Usar valores por defecto si no se proporcionan
    site = site_name or DEFAULT_SITE_NAME
    capacity = max_capacity or DEFAULT_MAX_CAPACITY
    
    # ============================================================
    # DATOS SIMULADOS
    # En el futuro, aquí se integrará la detección real con YOLOv8
    # Por ahora, usamos datos de prueba para verificar el sistema
    # ============================================================
    
    # Simulación del conteo de personas (reemplazar con yolo_service.detect_people())
    people_count = 45  # Dato simulado
    
    # Calcular porcentaje de ocupación
    occupancy_percentage = round((people_count / capacity) * 100, 1)
    
    # Clasificar estado de ocupación
    status = classify_occupancy_status(occupancy_percentage)
    
    # Obtener hora actual para last_update
    current_time = datetime.now().strftime("%I:%M %p")
    
    # Construir respuesta
    occupancy_data = {
        "site": site,
        "people_count": people_count,
        "max_capacity": capacity,
        "occupancy_percentage": occupancy_percentage,
        "status": status,
        "next_update": f"{UPDATE_INTERVAL_MINUTES} minutos",
        "last_update": current_time,
        "processed_image": "processed/result.jpg"
    }
    
    return occupancy_data


def get_occupancy_history(site_name=None, limit=10):
    """
    Obtiene el historial de ocupación de un sitio.
    
    Args:
        site_name (str, optional): Nombre del sitio
        limit (int): Número máximo de registros a retornar
    
    Returns:
        list: Lista de registros históricos de ocupación
    
    TODO: Implementar cuando se integre la base de datos
    """
    # Placeholder para historial
    # En el futuro, esto consultará la base de datos
    return []


def export_occupancy_to_csv(site_name=None, start_date=None, end_date=None):
    """
    Exporta los datos de ocupación a formato CSV.
    
    Args:
        site_name (str, optional): Nombre del sitio a exportar
        start_date (datetime, optional): Fecha de inicio del rango
        end_date (datetime, optional): Fecha de fin del rango
    
    Returns:
        str: Contenido CSV o ruta al archivo generado
    
    TODO: Implementar cuando se integre la base de datos y pandas
    """
    # Placeholder para exportación CSV
    pass
