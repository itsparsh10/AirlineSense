import json
from pathlib import Path

import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "airlinesense_pipeline.joblib"
MODEL_INFO_PATH = PROJECT_ROOT / "models" / "model_info.json"


def load_model_bundle():
    if not MODEL_PATH.exists() or not MODEL_INFO_PATH.exists():
        raise RuntimeError("Model artifacts are missing. Run `make pipeline` first.")
    pipeline = joblib.load(MODEL_PATH)
    model_info = json.loads(MODEL_INFO_PATH.read_text(encoding="utf-8"))
    return pipeline, model_info

