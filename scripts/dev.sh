#!/usr/bin/env bash
# Start all three services. Ctrl+C stops them all.
# Run from the repo root: ./scripts/dev.sh
# Assumes you've already created each Python venv and run npm install (see README).

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

trap 'kill 0' EXIT

(cd "$ROOT/engine-mock" && source .venv/bin/activate && uvicorn app.main:app --reload --port 8001) &
(cd "$ROOT/backend" && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000) &
(cd "$ROOT/frontend" && npm run dev) &

wait
