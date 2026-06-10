"""
Servicio de Detección con YOLOv8
Detecta personas en imágenes usando YOLOv8 preentrenado (COCO clase 0).
Si ultralytics no está instalado, cae en modo simulación para pruebas.

Pre-procesamiento aplicado antes de inferencia (basado en técnicas PDI):
  1. CLAHE sobre canal L del espacio LAB - mejora contraste adaptativo
  2. Filtro bilateral - reduce ruido conservando bordes
Esto mejora la detección de personas sentadas, de espaldas o en condiciones
de iluminación irregular.
"""

import os
import tempfile
from datetime import datetime

try:
    from ultralytics import YOLO
    import cv2
    import numpy as np
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

from config import CONFIDENCE_THRESHOLD, MODELS_FOLDER, PROCESSED_FOLDER

_model = None


def preprocess_for_detection(image_path: str) -> str | None:
    """
    Pipeline híbrido de pre-procesamiento para mejorar detección de personas
    sentadas, de espaldas o en escenas con iluminación irregular:

      1. CLAHE en canal L (LAB) - contraste adaptativo por zonas
      2. Filtro bilateral - reduce ruido preservando siluetas
      3. Unsharp mask (enfoque) - resalta contornos corporales
      4. Corrección gamma - aclara zonas oscuras (bajo mesas, esquinas)

    Retorna la ruta de un archivo temporal o None si falla
    (en ese caso YOLO usa la imagen original como fallback).
    """
    try:
        img = cv2.imread(str(image_path))
        if img is None:
            return None

        # 1. CLAHE sobre canal L (espacio LAB)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l_eq = clahe.apply(l_channel)
        lab_eq = cv2.merge([l_eq, a_channel, b_channel])
        img_clahe = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)

        # 2. Filtro bilateral (preserva bordes, reduce ruido)
        img_bilateral = cv2.bilateralFilter(img_clahe, d=9, sigmaColor=75, sigmaSpace=75)

        # 3. Unsharp mask – enfoca siluetas sin saturar
        #   Fórmula: sharpened = original * 1.5 – gaussian_blur * 0.5
        blur = cv2.GaussianBlur(img_bilateral, (0, 0), sigmaX=3)
        img_sharp = cv2.addWeighted(img_bilateral, 1.5, blur, -0.5, 0)

        # 4. Corrección gamma (γ = 0.85) – levanta sombras sin saturar luces 
        inv_gamma = 1.0 / 0.85
        lut = np.array([
            min(255, int((i / 255.0) ** inv_gamma * 255))
            for i in range(256)
        ], dtype=np.uint8)
        img_processed = cv2.LUT(img_sharp, lut)

        # 5. Guardar en archivo temporal para inferencia (YOLO requiere ruta de archivo)
        ext = os.path.splitext(image_path)[-1] or ".jpg"
        tmp = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
        tmp.close()
        cv2.imwrite(tmp.name, img_processed)
        return tmp.name

    except Exception:
        return None


def load_model(model_path=None):
    """Carga el modelo YOLOv8 una sola vez (singleton)."""
    global _model
    if not YOLO_AVAILABLE:
        return None
    if _model is None:
        if model_path is None:
            candidate = os.path.join(MODELS_FOLDER, "yolov8n.pt")
            model_path = candidate if os.path.exists(candidate) else "yolov8n.pt"
        _model = YOLO(model_path)
    return _model


def detect_people(image_path):
    """
    Detecta personas en una imagen con YOLOv8.

    Returns dict:
        count                    – número de personas detectadas
        detections               – lista de {bbox, confidence}
        processed_image_filename – nombre del archivo anotado en PROCESSED_FOLDER
        simulated                – True si se usaron datos simulados
        source_image             – nombre del archivo fuente
    """
    source_name = os.path.basename(str(image_path))

    if not os.path.exists(str(image_path)):
        return {
            "count": 0,
            "detections": [],
            "processed_image_filename": None,
            "simulated": False,
            "source_image": source_name,
            "error": "Imagen no encontrada",
        }

    if not YOLO_AVAILABLE:
        return _simulated_result(source_name)

    model = load_model()
    if model is None:
        return _simulated_result(source_name)

    # Pre-procesamiento PDI antes de inferencia 
    temp_path = preprocess_for_detection(str(image_path))
    inference_path = temp_path if temp_path else str(image_path)

    try:
        results = model(
            inference_path,
            conf=CONFIDENCE_THRESHOLD, # 0.25 – captura personas parcialmente visibles
            classes=[0], # solo clase "person"
            imgsz=1280, # resolución alta → detecta personas pequeñas/lejanas
            iou=0.4, # NMS más estricto → no fusiona personas adyacentes
            augment=True, # TTA: inferencia multi-escala + flip → mejor recall
            verbose=False,
        )
    finally:
        # Limpiar archivo temporal independientemente del resultado
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass

    person_detections = []
    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                person_detections.append({
                    "bbox": [round(x, 1) for x in box.xyxy[0].tolist()],
                    "confidence": round(float(box.conf[0]), 3),
                })

    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(source_name)[0]
    output_filename = f"{base}_result_{ts}.jpg"
    output_path = os.path.join(PROCESSED_FOLDER, output_filename)
    cv2.imwrite(output_path, results[0].plot())

    return {
        "count": len(person_detections),
        "detections": person_detections,
        "processed_image_filename": output_filename,
        "simulated": False,
        "source_image": source_name,
    }


def analyze_multiple_images(image_paths):
    """Procesa una lista de rutas de imagen y retorna resultados individuales."""
    return [detect_people(path) for path in image_paths]


def _simulated_result(source_name="unknown"):
    import random
    count = random.randint(0, 25)
    return {
        "count": count,
        "detections": [],
        "processed_image_filename": None,
        "simulated": True,
        "source_image": source_name,
    }


def get_model_info():
    return {
        "model_name": "YOLOv8n (Nano)",
        "yolo_available": YOLO_AVAILABLE,
        "model_loaded": _model is not None,
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "target_class": "person (COCO class 0)",
    }
