"""
Rutas de la API para el monitoreo de ocupación
"""

from flask import Blueprint, jsonify
from services.occupancy_service import get_current_occupancy_status

# Crear blueprint para las rutas de ocupación
occupancy_bp = Blueprint('occupancy', __name__)


@occupancy_bp.route('/estado-actual', methods=['GET'])
def get_current_status():
    """
    Obtiene el estado actual de ocupación del sitio monitoreado.
    
    Returns:
        JSON con los datos de ocupación:
        - site: Nombre del sitio
        - people_count: Número de personas detectadas
        - max_capacity: Capacidad máxima del espacio
        - occupancy_percentage: Porcentaje de ocupación
        - status: Estado de ocupación (Vacío, Parcialmente ocupado, Ocupado)
        - next_update: Tiempo para la próxima actualización
        - last_update: Hora de la última actualización
        - processed_image: Ruta de la imagen procesada
    """
    try:
        occupancy_data = get_current_occupancy_status()
        return jsonify({
            "status": "success",
            "data": occupancy_data
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@occupancy_bp.route('/sitios', methods=['GET'])
def get_monitored_sites():
    """
    Obtiene la lista de sitios monitoreados.
    
    Returns:
        JSON con la lista de sitios disponibles
    """
    from config import MONITORED_SITES
    return jsonify({
        "status": "success",
        "data": MONITORED_SITES
    }), 200


@occupancy_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificación de salud del servicio.
    
    Returns:
        JSON indicando que el servicio está activo
    """
    return jsonify({
        "status": "healthy",
        "service": "occupancy-monitoring"
    }), 200
