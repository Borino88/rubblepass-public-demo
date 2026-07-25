# ==============================================================================
# Stage 1: Build & Dependency Packaging
# ==============================================================================
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==============================================================================
# Stage 2: Production Runtime
# ==============================================================================
FROM python:3.11-slim-bookworm AS runtime

# OCI Standard Metadata Labels
LABEL org.opencontainers.image.title="RubblePass Public Demo"
LABEL org.opencontainers.image.description="Public architectural demonstration of AI-assisted pre-demolition material assessment, circular recovery routing, and digital material passports."
LABEL org.opencontainers.image.source="https://github.com/Borino88/rubblepass-public-demo"
LABEL org.opencontainers.image.url="https://fattahi.xyz"
LABEL org.opencontainers.image.documentation="https://github.com/Borino88/rubblepass-public-demo#readme"
LABEL org.opencontainers.image.version="1.0.0-demo"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.authors="Mahdi Fattahi <a.borino88@gmail.com>"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/lib/python3.11/site-packages:/app:$PATH" \
    PYTHONPATH="/app"

RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -s /bin/bash -m appuser

WORKDIR /app

COPY --from=builder /install /usr/local
COPY requirements.txt ./
COPY src/ ./src/
COPY data/ ./data/
COPY static/ ./static/

RUN chown -R appuser:appgroup /app

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').getcode() == 200" || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
