FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV YOLO_CONFIG_DIR=/tmp/ultralytics
ENV MPLCONFIGDIR=/tmp/matplotlib
ENV REPORT_EXPIRATION_HOURS=168
ENV PROCESSED_IMAGE_EXPIRATION_MINUTES=5
ENV MAX_STORED_REPORTS=100
ENV PROCESSED_IMAGE_JPEG_QUALITY=70
ENV PROCESSED_IMAGE_MAX_DIMENSION=1280
ENV YOLO_IMAGE_SIZE=640

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libglib2.0-0 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/backend/requirements.txt

COPY . /app

EXPOSE 7860

CMD ["gunicorn", "--chdir", "backend", "app:create_app()", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "1", "--timeout", "180"]
