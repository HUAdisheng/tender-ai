FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/pyproject.toml
COPY app /app/app

# Prefer installing from requirements.txt if present (faster reproducible builds),
# otherwise fall back to installing the package via pyproject.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && if [ -f /app/requirements.txt ]; then \
        pip install --no-cache-dir -r /app/requirements.txt; \
    else \
        pip install --no-cache-dir .; \
    fi

# Create a dedicated (non-root) user for running the app and a directory for rustfs
RUN useradd --create-home appuser || true
RUN mkdir -p /data/rustfs_bucket && chown -R appuser:appuser /data/rustfs_bucket /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
