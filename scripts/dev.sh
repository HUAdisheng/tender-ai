#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
ENV_FILE="${ROOT_DIR}/.env"
ENV_EXAMPLE_FILE="${ROOT_DIR}/.env.example"

cd "${ROOT_DIR}"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed. Please run: pip install uv"
  exit 1
fi

if [ ! -d "${VENV_DIR}" ]; then
  echo "Creating virtual environment..."
  uv venv "${VENV_DIR}"
fi

if [ ! -f "${ENV_FILE}" ]; then
  echo "Creating .env from .env.example..."
  cp "${ENV_EXAMPLE_FILE}" "${ENV_FILE}"
fi

echo "Installing project dependencies..."
uv pip install --python "${VENV_DIR}/bin/python" -e . --no-build-isolation

echo "Starting Tender AI on http://127.0.0.1:8000 ..."
exec "${VENV_DIR}/bin/python" -m uvicorn app.main:app --reload
