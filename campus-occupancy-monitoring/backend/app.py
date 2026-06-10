"""
Sistema Inteligente de Monitoreo de Ocupación de Espacios
Aplicación principal Flask
"""

import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from routes.occupancy_routes import occupancy_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))


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
        if os.path.exists(os.path.join(FRONTEND_FOLDER, "index.html")):
            return send_from_directory(FRONTEND_FOLDER, "index.html")

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

    @app.route("/<path:filename>")
    def frontend_files(filename):
        file_path = os.path.join(FRONTEND_FOLDER, filename)
        if os.path.isfile(file_path):
            return send_from_directory(FRONTEND_FOLDER, filename)
        return send_from_directory(FRONTEND_FOLDER, "index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
