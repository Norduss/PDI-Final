"""
Servicio de Detección con YOLOv8
Gestiona la detección de personas usando el modelo YOLOv8
"""

# ============================================================
# IMPORTACIONES PARA YOLOv8
# Descomentar cuando se integre el modelo real
# ============================================================
# from ultralytics import YOLO
# import cv2
# import numpy as np

from config import CONFIDENCE_THRESHOLD, MODELS_FOLDER

# Variable global para el modelo (se cargará una sola vez)
_model = None


def load_model(model_path=None):
    """
    Carga el modelo YOLOv8 preentrenado.
    
    Args:
        model_path (str, optional): Ruta al modelo .pt
                                    Si no se proporciona, usa yolov8n.pt (nano)
    
    Returns:
        YOLO: Instancia del modelo cargado
    
    TODO: Implementar carga real del modelo
    """
    global _model
    
    # ============================================================
    # IMPLEMENTACIÓN FUTURA DE CARGA DE MODELO
    # ============================================================
    # if _model is None:
    #     if model_path is None:
    #         # Usar modelo preentrenado por defecto (nano - más rápido)
    #         model_path = "yolov8n.pt"
    #     _model = YOLO(model_path)
    # return _model
    
    # Por ahora, retornamos None (modelo no cargado)
    return None


def detect_people(image_path):
    """
    Detecta personas en una imagen usando YOLOv8.
    
    Esta función está preparada para integrar YOLOv8. Por ahora retorna
    un conteo simulado para pruebas del sistema.
    
    Args:
        image_path (str): Ruta a la imagen a procesar
    
    Returns:
        dict: Diccionario con:
            - count (int): Número de personas detectadas
            - detections (list): Lista de detecciones con coordenadas
            - processed_image_path (str): Ruta de la imagen con anotaciones
    
    Ejemplo de uso futuro:
        result = detect_people("captures/camera_001.jpg")
        print(f"Personas detectadas: {result['count']}")
    """
    
    # ============================================================
    # IMPLEMENTACIÓN FUTURA CON YOLOv8
    # ============================================================
    # 
    # Pasos para integrar YOLOv8:
    # 
    # 1. Cargar el modelo:
    #    model = load_model()
    # 
    # 2. Ejecutar inferencia:
    #    results = model(image_path, conf=CONFIDENCE_THRESHOLD)
    # 
    # 3. Filtrar solo detecciones de personas (clase 0 en COCO):
    #    person_detections = []
    #    for result in results:
    #        boxes = result.boxes
    #        for box in boxes:
    #            if int(box.cls) == 0:  # 0 = persona en COCO
    #                person_detections.append({
    #                    "bbox": box.xyxy.tolist()[0],  # [x1, y1, x2, y2]
    #                    "confidence": float(box.conf)
    #                })
    # 
    # 4. Guardar imagen con anotaciones:
    #    annotated_frame = results[0].plot()
    #    output_path = f"processed/result_{timestamp}.jpg"
    #    cv2.imwrite(output_path, annotated_frame)
    # 
    # 5. Retornar resultados:
    #    return {
    #        "count": len(person_detections),
    #        "detections": person_detections,
    #        "processed_image_path": output_path
    #    }
    # ============================================================
    
    # DATOS SIMULADOS PARA PRUEBAS
    # Reemplazar con la implementación real cuando se integre YOLOv8
    simulated_count = 45
    
    return {
        "count": simulated_count,
        "detections": [
            # Ejemplo de formato de detección
            {"bbox": [100, 200, 150, 400], "confidence": 0.92},
            {"bbox": [300, 180, 350, 380], "confidence": 0.88},
            # ... más detecciones simuladas
        ],
        "processed_image_path": "processed/result.jpg"
    }


def detect_people_from_frame(frame):
    """
    Detecta personas directamente desde un frame de OpenCV.
    
    Args:
        frame (numpy.ndarray): Frame de imagen en formato BGR (OpenCV)
    
    Returns:
        dict: Mismo formato que detect_people()
    
    TODO: Implementar cuando se integre YOLOv8
    """
    # ============================================================
    # IMPLEMENTACIÓN FUTURA
    # ============================================================
    # model = load_model()
    # results = model(frame, conf=CONFIDENCE_THRESHOLD)
    # ... procesar resultados similar a detect_people()
    
    # Por ahora, retornar datos simulados
    return {
        "count": 45,
        "detections": [],
        "processed_image_path": None
    }


def get_model_info():
    """
    Obtiene información sobre el modelo cargado.
    
    Returns:
        dict: Información del modelo (nombre, versión, clases, etc.)
    """
    return {
        "model_name": "YOLOv8n (Nano)",
        "model_loaded": _model is not None,
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "target_class": "person (COCO class 0)"
    }
