"""
Sistema Inteligente de Monitoreo de Ocupación de Espacios
Aplicación principal Flask
"""

from flask import Flask, jsonify
from flask_cors import CORS
from routes.occupancy_routes import occupancy_bp

def create_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__)
    
    # Habilitar CORS para permitir peticiones desde el frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Registrar blueprints (rutas)
    app.register_blueprint(occupancy_bp, url_prefix='/api')
    
    # Ruta principal para verificar que el backend funciona
    @app.route('/')
    def index():
        return jsonify({
            "status": "success",
            "message": "Backend del Sistema de Monitoreo de Ocupación funcionando correctamente",
            "version": "1.0.0",
            "endpoints": {
                "estado_actual": "/api/estado-actual",
                "health": "/"
            }
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
