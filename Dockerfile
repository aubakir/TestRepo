FROM python:3.11-slim

WORKDIR /app

COPY app.py .
COPY speedtest/ ./speedtest/

ENTRYPOINT ["python", "app.py"]
