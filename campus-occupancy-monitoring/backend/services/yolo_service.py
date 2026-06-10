"""
Servicio de deteccion de personas e imagenes procesadas.

Por defecto usa OpenCV HOG para funcionar en Render Free (<512 MB).
Si se configura DETECTION_BACKEND=yolo e instalas ultralytics, intenta usar YOLOv8.
"""

import os
import tempfile
from datetime import datetime

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

from config import (
    CONFIDENCE_THRESHOLD,
    DETECTION_BACKEND,
    MODELS_FOLDER,
    PROCESSED_FOLDER,
    PROCESSED_IMAGE_JPEG_QUALITY,
    PROCESSED_IMAGE_MAX_DIMENSION,
    YOLO_IMAGE_SIZE,
)

_model = None
_face_cascade = None
_hog_detector = None


def load_face_cascade():
    global _face_cascade
    if not CV2_AVAILABLE:
        return None
    if _face_cascade is None:
        cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        _face_cascade = cv2.CascadeClassifier(cascade_path)
        if _face_cascade.empty():
            _face_cascade = None
    return _face_cascade


def load_hog_detector():
    global _hog_detector
    if not CV2_AVAILABLE:
        return None
    if _hog_detector is None:
        _hog_detector = cv2.HOGDescriptor()
        _hog_detector.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    return _hog_detector


def yolo_is_available():
    if not CV2_AVAILABLE or DETECTION_BACKEND != "yolo":
        return False
    try:
        import ultralytics  # noqa: F401
        return True
    except ImportError:
        return False


def blur_detected_faces(image):
    cascade = load_face_cascade()
    if cascade is None or image is None:
        return image

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(24, 24),
    )

    for x, y, w, h in faces:
        face_roi = image[y:y + h, x:x + w]
        if face_roi.size == 0:
            continue
        kernel_size = max(31, ((min(w, h) // 2) * 2) + 1)
        image[y:y + h, x:x + w] = cv2.GaussianBlur(face_roi, (kernel_size, kernel_size), 0)

    return image


def resize_for_storage(image):
    if image is None:
        return image

    height, width = image.shape[:2]
    longest_side = max(width, height)
    if longest_side <= PROCESSED_IMAGE_MAX_DIMENSION:
        return image

    scale = PROCESSED_IMAGE_MAX_DIMENSION / longest_side
    new_size = (max(1, int(width * scale)), max(1, int(height * scale)))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)


def write_jpeg_image(path: str, image) -> bool:
    if image is None:
        return False
    image = resize_for_storage(image)
    return cv2.imwrite(
        str(path),
        image,
        [int(cv2.IMWRITE_JPEG_QUALITY), PROCESSED_IMAGE_JPEG_QUALITY],
    )


def blur_faces_in_file(image_path: str) -> bool:
    if not CV2_AVAILABLE:
        return False

    image = cv2.imread(str(image_path))
    if image is None:
        return False

    write_jpeg_image(str(image_path), blur_detected_faces(image))
    return True


def save_uploaded_image_with_blurred_faces(uploaded_file, destination: str) -> bool:
    if not CV2_AVAILABLE:
        uploaded_file.save(destination)
        return False

    file_bytes = uploaded_file.read()
    image_array = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        uploaded_file.seek(0)
        uploaded_file.save(destination)
        return False

    write_jpeg_image(destination, blur_detected_faces(image))
    return True


def preprocess_for_detection(image_path: str) -> str | None:
    if not CV2_AVAILABLE:
        return None

    try:
        img = cv2.imread(str(image_path))
        if img is None:
            return None

        img = resize_for_storage(img)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l_eq = clahe.apply(l_channel)
        lab_eq = cv2.merge([l_eq, a_channel, b_channel])
        img_clahe = cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)
        img_bilateral = cv2.bilateralFilter(img_clahe, d=7, sigmaColor=50, sigmaSpace=50)
        blur = cv2.GaussianBlur(img_bilateral, (0, 0), sigmaX=2)
        img_processed = cv2.addWeighted(img_bilateral, 1.35, blur, -0.35, 0)
        img_processed = blur_detected_faces(img_processed)

        ext = os.path.splitext(image_path)[-1] or ".jpg"
        tmp = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
        tmp.close()
        write_jpeg_image(tmp.name, img_processed)
        return tmp.name
    except Exception:
        return None


def load_model(model_path=None):
    global _model
    if not yolo_is_available():
        return None
    if _model is None:
        from ultralytics import YOLO

        if model_path is None:
            candidate = os.path.join(MODELS_FOLDER, "yolov8n.pt")
            model_path = candidate if os.path.exists(candidate) else "yolov8n.pt"
        _model = YOLO(model_path)
    return _model


def _missing_image_result(source_name):
    return {
        "count": 0,
        "detections": [],
        "processed_image_filename": None,
        "simulated": False,
        "source_image": source_name,
        "error": "Imagen no encontrada",
    }


def _build_output_path(source_name):
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(source_name)[0]
    output_filename = f"{base}_result_{ts}.jpg"
    return output_filename, os.path.join(PROCESSED_FOLDER, output_filename)


def detect_people_with_opencv(image_path):
    source_name = os.path.basename(str(image_path))

    if not os.path.exists(str(image_path)):
        return _missing_image_result(source_name)
    if not CV2_AVAILABLE:
        return _simulated_result(source_name)

    image = cv2.imread(str(image_path))
    detector = load_hog_detector()
    if image is None or detector is None:
        return _simulated_result(source_name)

    image = resize_for_storage(image)
    boxes, weights = detector.detectMultiScale(
        image,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05,
    )

    detections = []
    annotated_image = image.copy()
    for (x, y, w, h), weight in zip(boxes, weights):
        confidence = round(float(weight), 3)
        detections.append({
            "bbox": [int(x), int(y), int(x + w), int(y + h)],
            "confidence": confidence,
        })
        cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (46, 204, 113), 2)
        cv2.putText(
            annotated_image,
            f"persona {confidence:.2f}",
            (x, max(20, y - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (46, 204, 113),
            2,
        )

    output_filename, output_path = _build_output_path(source_name)
    write_jpeg_image(output_path, blur_detected_faces(annotated_image))

    return {
        "count": len(detections),
        "detections": detections,
        "processed_image_filename": output_filename,
        "simulated": False,
        "source_image": source_name,
        "detector": "opencv-hog",
    }


def detect_people_with_yolo(image_path):
    source_name = os.path.basename(str(image_path))

    if not os.path.exists(str(image_path)):
        return _missing_image_result(source_name)
    if not yolo_is_available():
        return detect_people_with_opencv(image_path)

    model = load_model()
    if model is None:
        return detect_people_with_opencv(image_path)

    temp_path = preprocess_for_detection(str(image_path))
    inference_path = temp_path if temp_path else str(image_path)

    try:
        results = model(
            inference_path,
            conf=CONFIDENCE_THRESHOLD,
            classes=[0],
            imgsz=YOLO_IMAGE_SIZE,
            iou=0.4,
            augment=False,
            verbose=False,
        )
    finally:
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

    output_filename, output_path = _build_output_path(source_name)
    annotated_image = blur_detected_faces(results[0].plot())
    write_jpeg_image(output_path, annotated_image)

    return {
        "count": len(person_detections),
        "detections": person_detections,
        "processed_image_filename": output_filename,
        "simulated": False,
        "source_image": source_name,
        "detector": "yolo",
    }


def detect_people(image_path):
    if DETECTION_BACKEND == "yolo":
        return detect_people_with_yolo(image_path)
    return detect_people_with_opencv(image_path)


def analyze_multiple_images(image_paths):
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
        "detector": "simulated",
    }


def get_model_info():
    return {
        "detector_backend": DETECTION_BACKEND,
        "model_name": "OpenCV HOG" if DETECTION_BACKEND != "yolo" else "YOLOv8n",
        "opencv_available": CV2_AVAILABLE,
        "yolo_available": yolo_is_available(),
        "model_loaded": _model is not None,
        "confidence_threshold": CONFIDENCE_THRESHOLD,
        "target_class": "person",
    }
