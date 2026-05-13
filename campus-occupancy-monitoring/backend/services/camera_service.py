"""
Servicio de Cámara
Gestiona la captura de imágenes con OpenCV
"""

# ============================================================
# IMPORTACIONES PARA OPENCV
# Descomentar cuando se implemente la captura real
# ============================================================
# import cv2
# import os
# from datetime import datetime

from config import CAPTURES_FOLDER, CAMERA_INDEX


def capture_image(camera_index=None, output_path=None):
    """
    Captura una imagen desde la cámara usando OpenCV.
    
    Esta función está preparada para capturar imágenes reales.
    Por ahora contiene la implementación comentada para referencia.
    
    Args:
        camera_index (int, optional): Índice de la cámara. Por defecto usa CAMERA_INDEX
        output_path (str, optional): Ruta donde guardar la imagen.
                                     Si no se proporciona, genera una automática
    
    Returns:
        dict: Diccionario con:
            - success (bool): Si la captura fue exitosa
            - image_path (str): Ruta de la imagen guardada
            - timestamp (str): Marca de tiempo de la captura
            - error (str, optional): Mensaje de error si falló
    
    Ejemplo de uso:
        result = capture_image()
        if result['success']:
            print(f"Imagen guardada en: {result['image_path']}")
    """
    
    # ============================================================
    # IMPLEMENTACIÓN PARA CAPTURA REAL CON OPENCV
    # ============================================================
    # 
    # import cv2
    # import os
    # from datetime import datetime
    # 
    # cam_idx = camera_index or CAMERA_INDEX
    # 
    # try:
    #     # Abrir conexión con la cámara
    #     cap = cv2.VideoCapture(cam_idx)
    #     
    #     if not cap.isOpened():
    #         return {
    #             "success": False,
    #             "image_path": None,
    #             "timestamp": None,
    #             "error": f"No se pudo abrir la cámara {cam_idx}"
    #         }
    #     
    #     # Capturar frame
    #     ret, frame = cap.read()
    #     
    #     # Liberar cámara
    #     cap.release()
    #     
    #     if not ret:
    #         return {
    #             "success": False,
    #             "image_path": None,
    #             "timestamp": None,
    #             "error": "No se pudo capturar el frame"
    #         }
    #     
    #     # Generar nombre de archivo con timestamp
    #     timestamp = datetime.now()
    #     timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
    #     
    #     if output_path is None:
    #         # Crear carpeta si no existe
    #         os.makedirs(CAPTURES_FOLDER, exist_ok=True)
    #         output_path = f"{CAPTURES_FOLDER}/capture_{timestamp_str}.jpg"
    #     
    #     # Guardar imagen
    #     cv2.imwrite(output_path, frame)
    #     
    #     return {
    #         "success": True,
    #         "image_path": output_path,
    #         "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
    #         "error": None
    #     }
    #     
    # except Exception as e:
    #     return {
    #         "success": False,
    #         "image_path": None,
    #         "timestamp": None,
    #         "error": str(e)
    #     }
    # ============================================================
    
    # RESPUESTA SIMULADA PARA PRUEBAS
    # Reemplazar con la implementación real cuando se configure la cámara
    from datetime import datetime
    
    timestamp = datetime.now()
    
    return {
        "success": True,
        "image_path": f"{CAPTURES_FOLDER}/capture_simulated.jpg",
        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "error": None,
        "note": "Captura simulada - Implementar OpenCV para captura real"
    }


def capture_from_url(url, output_path=None):
    """
    Captura una imagen desde una cámara IP o URL de stream.
    
    Args:
        url (str): URL de la cámara IP o stream RTSP
        output_path (str, optional): Ruta donde guardar la imagen
    
    Returns:
        dict: Mismo formato que capture_image()
    
    TODO: Implementar para cámaras IP del campus
    """
    # ============================================================
    # IMPLEMENTACIÓN FUTURA PARA CÁMARAS IP
    # ============================================================
    # 
    # import cv2
    # 
    # try:
    #     cap = cv2.VideoCapture(url)
    #     ret, frame = cap.read()
    #     cap.release()
    #     
    #     if ret:
    #         cv2.imwrite(output_path, frame)
    #         return {"success": True, "image_path": output_path, ...}
    #     else:
    #         return {"success": False, "error": "No se pudo conectar", ...}
    # 
    # except Exception as e:
    #     return {"success": False, "error": str(e), ...}
    # ============================================================
    
    return {
        "success": False,
        "image_path": None,
        "timestamp": None,
        "error": "Función no implementada - Pendiente integración de cámaras IP"
    }


def get_available_cameras():
    """
    Detecta las cámaras disponibles en el sistema.
    
    Returns:
        list: Lista de índices de cámaras disponibles
    
    TODO: Implementar detección de cámaras
    """
    # ============================================================
    # IMPLEMENTACIÓN FUTURA
    # ============================================================
    # 
    # import cv2
    # 
    # available = []
    # for i in range(10):  # Probar índices del 0 al 9
    #     cap = cv2.VideoCapture(i)
    #     if cap.isOpened():
    #         available.append(i)
    #         cap.release()
    # return available
    # ============================================================
    
    return [0]  # Por defecto, asumir que hay una cámara en índice 0


def test_camera_connection(camera_index=None):
    """
    Prueba la conexión con una cámara específica.
    
    Args:
        camera_index (int, optional): Índice de la cámara a probar
    
    Returns:
        dict: Estado de la conexión
    """
    cam_idx = camera_index or CAMERA_INDEX
    
    return {
        "camera_index": cam_idx,
        "connected": True,  # Simulado
        "resolution": "1920x1080",  # Simulado
        "note": "Prueba simulada - Implementar OpenCV para prueba real"
    }
