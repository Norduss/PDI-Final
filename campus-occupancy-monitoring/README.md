# Sistema Inteligente de Monitoreo de Ocupación de Espacios en Campus Universitario mediante Visión Computacional

Sistema web para monitorear la ocupación de espacios dentro de un campus universitario usando visión computacional con YOLOv8.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Objetivo

Crear un sistema que permita:
- Monitorear la ocupación de espacios universitarios en tiempo real
- Detectar personas usando el modelo YOLOv8
- Visualizar resultados en un dashboard web intuitivo
- Generar alertas según niveles de ocupación

## 🛠️ Tecnologías Utilizadas

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

## 📁 Estructura del Proyecto

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

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/sistema-monitoreo-ocupacion.git
cd sistema-monitoreo-ocupacion
```

### 2. Configurar el Backend

```bash
# Ir a la carpeta del backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Descargar modelo YOLOv8 (opcional para desarrollo inicial)

```bash
# El modelo se descargará automáticamente la primera vez que se use
# O puedes descargarlo manualmente:
pip install ultralytics
yolo export model=yolov8n.pt format=pt
# Mover a la carpeta models/
```

## ▶️ Ejecución

### Ejecutar el Backend

```bash
cd backend

# Activar entorno virtual (si no está activo)
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Ejecutar servidor Flask
python app.py
```

El backend estará disponible en: `http://localhost:5000`

### Abrir el Frontend

Simplemente abre el archivo `frontend/index.html` en tu navegador:

```bash
# Opción 1: Abrir directamente
open frontend/index.html  # macOS
start frontend/index.html # Windows

# Opción 2: Usar un servidor local
cd frontend
python -m http.server 8080
# Luego visita: http://localhost:8080
```

## 🔌 Probar la API

### Verificar que el backend funciona

```bash
curl http://localhost:5000/
```

Respuesta esperada:
```json
{
  "status": "success",
  "message": "Backend del Sistema de Monitoreo de Ocupación funcionando correctamente",
  "version": "1.0.0"
}
```

### Obtener estado actual de ocupación

```bash
curl http://localhost:5000/api/estado-actual
```

Respuesta esperada:
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

## 👥 Flujo de Trabajo con GitHub

### Para colaboradores

1. **Fork** del repositorio
2. **Clonar** tu fork localmente
3. Crear una **rama** para tu feature:
   ```bash
   git checkout -b feature/nombre-feature
   ```
4. **Commits** con mensajes descriptivos:
   ```bash
   git add .
   git commit -m "feat: agregar detección de personas con YOLOv8"
   ```
5. **Push** a tu fork:
   ```bash
   git push origin feature/nombre-feature
   ```
6. Crear **Pull Request** hacia el repositorio principal

### Convención de commits

- `feat:` Nueva funcionalidad
- `fix:` Corrección de errores
- `docs:` Cambios en documentación
- `style:` Cambios de formato (no afectan lógica)
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests

## 📋 Próximos Pasos

- [ ] Integrar captura real con OpenCV
- [ ] Implementar detección con YOLOv8
- [ ] Conectar base de datos para historial
- [ ] Agregar sistema de alertas por email
- [ ] Implementar autenticación de usuarios
- [ ] Dashboard multi-sitio

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autores

- Equipo de Desarrollo - Universidad

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub.
