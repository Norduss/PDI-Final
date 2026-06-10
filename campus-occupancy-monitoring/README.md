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


## Autores

- Equipo de Desarrollo universitario UAO

  - Alejandro Arias Ramirez
  - Steven Camilo Franco Bocanegra
  - Valentina Ochoa Hernandez
  - Santiago Peña Agudelo

---
