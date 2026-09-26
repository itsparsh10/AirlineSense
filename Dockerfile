FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    AIRLINESENSE_API_URL=http://127.0.0.1:8000

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
COPY src src
COPY models models
COPY configs configs
COPY scripts/start_services.sh scripts/start_services.sh
RUN chmod +x scripts/start_services.sh

EXPOSE 8000 8501
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)" || exit 1

CMD ["./scripts/start_services.sh"]

