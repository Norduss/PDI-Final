# Sistema Inteligente de Monitoreo de Ocupación de Espacios en Campus Universitario mediante Visión Computacional

Sistema web para monitorear la ocupación de espacios dentro de un campus universitario usando visión computacional con YOLOv8.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Objetivo

Crear un sistema que permita:
- Monitorear la ocupación de espacios universitarios en intervalos de 15 minutos
- Detectar personas usando el modelo YOLOv8
- Visualizar resultados en un dashboard web intuitivo
- Generar alertas según niveles de ocupación

## Arquitectura del Sistema

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
## Tecnologías Utilizadas

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **Flask-CORS** - Manejo de CORS
- **OpenCV** - Procesamiento de imágenes
- **Ultralytics YOLOv8** - Detección de objetos
- **NumPy** - Operaciones numéricas
- **Pandas** - Exportación de datos (opcional)

### Frontend
- **HTML5**
- **CSS3** - Diseño responsive
- **JavaScript (Vanilla)** - Lógica del dashboard
- **Fetch API** - Consumo de API REST


## Estructura del Proyecto

```
sistema-monitoreo-ocupacion/
│
├── backend/
│   ├── app.py                 # Aplicación Flask principal
│   ├── config.py              # Configuración y constantes
│   ├── requirements.txt       # Dependencias de Python
│   │
│   ├── routes/
│   │   └── occupancy_routes.py    # Rutas de la API
│   │
│   ├── services/
│   │   ├── camera_service.py      # Captura de imágenes
│   │   ├── yolo_service.py        # Detección con YOLOv8
│   │   └── occupancy_service.py   # Lógica de ocupación
│   │
│   ├── database/
│   │   └── database.py            # Gestión de base de datos
│   │
│   ├── captures/              # Imágenes capturadas
│   ├── processed/             # Imágenes procesadas
│   └── models/                # Modelos YOLOv8 (.pt)
│
├── frontend/
│   ├── index.html             # Dashboard principal
│   ├── css/
│   │   └── styles.css         # Estilos del dashboard
│   ├── js/
│   │   └── dashboard.js       # Lógica del frontend
│   └── assets/                # Recursos estáticos
│
├── dataset/
│   ├── ocupado/               # Imágenes de espacios ocupados
│   └── vacio/                 # Imágenes de espacios vacíos
│
├── docs/
│   └── README_PROYECTO.md     # Documentación técnica
│
├── .gitignore
└── README.md
```


## Requimientos del sistema antes de la instalación

```bash

# Tener instalado Python en el dispositivo minimo V3.10

```
### 1. Configurar el Backend

```bash

# Alojarse en la carpeta backend del proyecto
cd campus-occupancy-monitoring/backend

# Instalar dependencias
pip install -r requirements.txt

# Inicializamos el proyecto
python app.py

```

## Despliegue recomendado: Hugging Face Spaces con Docker

Hugging Face Spaces es una mejor opcion para una demostracion con YOLOv8 porque
su entorno gratuito de CPU ofrece mas memoria que Render Free. El proyecto ya
incluye un `Dockerfile` para ejecutar Flask, servir el frontend y procesar con
YOLO desde el mismo contenedor.

### Configuracion del Space

Crear un Space nuevo en Hugging Face con:

```bash
Space SDK:
Docker

Visibility:
Public
```

El contenedor expone el puerto `7860`, que es el puerto esperado por Hugging
Face Spaces. El comando de arranque usa un solo worker de Gunicorn para evitar
duplicar el modelo YOLO en memoria:

```bash
gunicorn --chdir backend "app:create_app()" --bind 0.0.0.0:7860 --workers 1 --threads 1 --timeout 180
```

Variables opcionales recomendadas en Settings > Variables:

```bash
REPORT_EXPIRATION_HOURS=168
PROCESSED_IMAGE_EXPIRATION_MINUTES=5
MAX_STORED_REPORTS=100
PROCESSED_IMAGE_JPEG_QUALITY=70
PROCESSED_IMAGE_MAX_DIMENSION=1280
YOLO_IMAGE_SIZE=640
```

Con estos valores el sistema conserva los datos historicos, borra rapido las
imagenes temporales y reduce el peso de las imagenes procesadas.

## Despliegue alternativo en Render

### Backend Flask

Crear un **Web Service** en Render conectado al repositorio y usar:

```bash
Build Command:
pip install -r backend/requirements.txt

Start Command:
gunicorn --chdir backend "app:create_app()"
```

El backend usa `gunicorn` para ejecutarse en produccion y `opencv-python-headless`
para evitar dependencias graficas innecesarias del servidor.

### Frontend estatico

Crear un **Static Site** en Render conectado al mismo repositorio y usar:

```bash
Publish Directory:
frontend

Build Command:
# dejar vacio
```

Cuando Render genere la URL del backend, reemplazar este valor en
`frontend/js/config.js`:

```js
https://TU-BACKEND-EN-RENDER.onrender.com/api
```

por la URL real del Web Service, manteniendo el sufijo `/api`.

Nota: Render Free tiene 512 MB de memoria y puede no ser suficiente para YOLOv8,
porque Ultralytics carga PyTorch. Para una demo con YOLO, se recomienda Hugging
Face Spaces con Docker. El almacenamiento de Render en Web Services tambien
puede ser temporal.

Variables opcionales para controlar almacenamiento en Render:

```bash
REPORT_EXPIRATION_HOURS=168
PROCESSED_IMAGE_EXPIRATION_MINUTES=5
MAX_STORED_REPORTS=100
PROCESSED_IMAGE_JPEG_QUALITY=70
PROCESSED_IMAGE_MAX_DIMENSION=1280
YOLO_IMAGE_SIZE=640
```

Con estos valores el sistema mantiene los datos historicos, borra rapido las
imagenes temporales y guarda las imagenes nuevas con menor peso.


## Autores

- Equipo de Desarrollo universitario UAO

  - Alejandro Arias Ramirez
  - Steven Camilo Franco Bocanegra
  - Valentina Ochoa Hernandez
  - Santiago Peña Agudelo

---
