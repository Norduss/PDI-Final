"""
Sistema Inteligente de Monitoreo de Ocupación de Espacios
Aplicación principal Flask
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from routes.occupancy_routes import occupancy_bp


def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Límite de 50 MB para subida de imágenes
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

    # Crear carpetas necesarias si no existen
    for folder in ("captures", "processed", "models"):
        os.makedirs(folder, exist_ok=True)

    app.register_blueprint(occupancy_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return jsonify({
            "status": "success",
            "message": "Backend del Sistema de Monitoreo de Ocupación funcionando correctamente",
            "version": "2.0.0",
            "endpoints": {
                "estado_actual":    "GET  /api/estado-actual",
                "analizar":         "POST /api/analizar  (campo: images)",
                "health":           "GET  /api/health",
                "imagen_procesada": "GET  /api/imagen/procesada/<filename>",
            },
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
