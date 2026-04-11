#!/usr/bin/env bash

set -euo pipefail

DEPLOY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${DEPLOY_DIR}/.env"
ENV_EXAMPLE_FILE="${DEPLOY_DIR}/.env.example"

cd "${DEPLOY_DIR}"

if [ ! -f "${ENV_FILE}" ]; then
  echo "Creating deploy/.env from deploy/.env.example ..."
  cp "${ENV_EXAMPLE_FILE}" "${ENV_FILE}"
fi

echo "Starting Tender AI stack ..."
docker compose up -d --build

echo "Tender AI is starting."
echo "Health check URL: http://127.0.0.1:8000/v1/health"
