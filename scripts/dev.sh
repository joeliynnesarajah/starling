#!/usr/bin/env bash
# Set up and start all three services. Ctrl+C stops them all.
# Run from the repo root: ./scripts/dev.sh
# Skip the install step with: SKIP_INSTALL=1 ./scripts/dev.sh
# Use a specific Python with: PYTHON=python3.12 ./scripts/dev.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="${PYTHON:-python3}"

setup_python() {
  local dir="$1"
  echo "==> Setting up $dir"
  cd "$ROOT/$dir"
  [ -d .venv ] || "$PYTHON" -m venv .venv
  source .venv/bin/activate
  pip install -q -r requirements.txt
  if [ -f .env.example ] && [ ! -f .env ]; then
    cp .env.example .env
    echo "    created $dir/.env from .env.example"
  fi
  deactivate
}

if [ -z "${SKIP_INSTALL:-}" ]; then
  setup_python engine-mock
  setup_python backend

  echo "==> Setting up frontend"
  cd "$ROOT/frontend"
  npm install --silent
  if [ -f .env.example ] && [ ! -f .env ]; then
    cp .env.example .env
    echo "    created frontend/.env from .env.example"
  fi
fi

trap 'kill 0' EXIT

(cd "$ROOT/engine-mock" && source .venv/bin/activate && uvicorn app.main:app --reload --reload-dir app --port 8001) &
(cd "$ROOT/backend" && source .venv/bin/activate && uvicorn app.main:app --reload --reload-dir app --port 8000) &
(cd "$ROOT/frontend" && npm run dev) &

wait
