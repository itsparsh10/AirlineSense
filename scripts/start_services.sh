#!/bin/sh
set -eu

python -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!

cleanup() {
  kill "$API_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

python -m streamlit run app/streamlit/app.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.headless true

