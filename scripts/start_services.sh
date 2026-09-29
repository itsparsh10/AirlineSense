#!/bin/sh
set -eu

PYTHON_BIN="${PYTHON_BIN:-python}"

"$PYTHON_BIN" -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!

cleanup() {
  kill "$API_PID" 2>/dev/null || true
  wait "$API_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

"$PYTHON_BIN" -m streamlit run app/streamlit/app.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.headless true &
UI_PID=$!

while kill -0 "$API_PID" 2>/dev/null && kill -0 "$UI_PID" 2>/dev/null; do
  sleep 2
done

kill "$UI_PID" 2>/dev/null || true
wait "$UI_PID" 2>/dev/null || true
exit 1
