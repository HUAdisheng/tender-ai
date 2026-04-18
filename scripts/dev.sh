#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"
ENV_FILE="${ROOT_DIR}/.env"
ENV_EXAMPLE_FILE="${ROOT_DIR}/.env.example"
UV_CACHE_DIR_DEFAULT="/tmp/tender-ai-uv-cache"

cd "${ROOT_DIR}"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed. Please install uv first: https://docs.astral.sh/uv/"
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
UV_CACHE_DIR="${UV_CACHE_DIR:-${UV_CACHE_DIR_DEFAULT}}" uv sync

echo "Starting Tender AI on http://127.0.0.1:8000 ..."
exec uv run uvicorn app.main:app --reload
