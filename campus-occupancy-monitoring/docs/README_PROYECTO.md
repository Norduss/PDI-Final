# Documentación Técnica del Proyecto

## Sistema Inteligente de Monitoreo de Ocupación de Espacios en Campus Universitario mediante Visión Computacional

### Descripción General

Este documento contiene la documentación técnica detallada del sistema de monitoreo de ocupación. El sistema está diseñado para analizar imágenes capturadas periódicamente y detectar el número de personas presentes en espacios del campus universitario.

---

### Arquitectura del Sistema

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Cámaras      │────▶│    Backend      │────▶│    Frontend     │
│   (Capturas)    │     │  (Flask + YOLO) │     │   (Dashboard)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
   Cada 15 min           Procesamiento            Visualización
                         con YOLOv8               en tiempo real
```

---

### Flujo de Datos

1. **Captura de Imagen**
   - El servicio de cámara (`camera_service.py`) captura una imagen cada 15 minutos
   - La imagen se guarda en la carpeta `captures/`

2. **Procesamiento con YOLOv8**
   - El servicio YOLO (`yolo_service.py`) procesa la imagen
   - Detecta personas usando el modelo preentrenado
   - Genera una imagen con las detecciones marcadas en `processed/`

3. **Cálculo de Ocupación**
   - El servicio de ocupación (`occupancy_service.py`) calcula el porcentaje
   - Clasifica el estado: Vacío, Parcialmente ocupado, Ocupado

4. **Exposición via API**
   - Las rutas (`occupancy_routes.py`) exponen los datos
   - Endpoint principal: `GET /api/estado-actual`

5. **Consumo en Frontend**
   - El dashboard (`dashboard.js`) consume la API
   - Actualiza la interfaz en tiempo real

---

### Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Verificación de salud del backend |
| GET | `/api/estado-actual` | Datos actuales de ocupación |
| GET | `/api/sitios` | Lista de sitios monitoreados |
| GET | `/api/health` | Estado del servicio |

---

### Estructura de Respuesta

```json
{
  "status": "success",
  "data": {
    "site": "Sótano 1",
    "people_count": 45,
    "max_capacity": 90,
    "occupancy_percentage": 50.0,
    "status": "Parcialmente ocupado",
    "next_update": "15 minutos",
    "last_update": "10:25 AM",
    "processed_image": "processed/result.jpg"
  }
}
```

---

### Clasificación de Estados

| Porcentaje | Estado |
|------------|--------|
| 0% - 10% | Vacío |
| 11% - 70% | Parcialmente ocupado |
| 71% - 100% | Ocupado |

---

### Configuración

Las constantes se definen en `config.py`:

- `UPDATE_INTERVAL_MINUTES`: Intervalo de actualización (15 min)
- `CONFIDENCE_THRESHOLD`: Umbral de confianza para YOLO (0.5)
- `DEFAULT_MAX_CAPACITY`: Capacidad máxima por defecto (90)

---

### Integración de YOLOv8

Para integrar YOLOv8 de forma real:

1. Descargar modelo: `yolov8n.pt` (nano, más rápido)
2. Colocar en carpeta `models/`
3. Descomentar código en `yolo_service.py`
4. Ajustar `CONFIDENCE_THRESHOLD` según necesidad

```python
from ultralytics import YOLO
model = YOLO('models/yolov8n.pt')
results = model(image_path, conf=0.5)
```

---

### Notas de Desarrollo

- El sistema usa datos simulados inicialmente
- Cada servicio tiene comentarios explicando la integración real
- El frontend está preparado para recibir imágenes procesadas
- Se recomienda SQLite para desarrollo y PostgreSQL para producción
