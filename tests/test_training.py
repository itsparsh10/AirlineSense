import json
from pathlib import Path

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "airlinesense_pipeline.joblib"
INFO_PATH = PROJECT_ROOT / "models" / "model_info.json"


SAMPLE = pd.DataFrame(
    [
        {
            "Gender": "Female",
            "Age": 35,
            "Customer Type": "Returning",
            "Type of Travel": "Business",
            "Class": "Business",
            "Flight Distance": 821,
            "Departure Delay": 26,
            "Arrival Delay": 39,
            "Departure and Arrival Time Convenience": 2,
            "Ease of Online Booking": 2,
            "Check-in Service": 3,
            "Online Boarding": 5,
            "Gate Location": 2,
            "On-board Service": 5,
            "Seat Comfort": 4,
            "Leg Room Service": 5,
            "Cleanliness": 5,
            "Food and Drink": 3,
            "In-flight Service": 5,
            "In-flight Wifi Service": 2,
            "In-flight Entertainment": 5,
            "Baggage Handling": 5,
        }
    ]
)


def test_saved_model_and_metadata_exist():
    assert MODEL_PATH.exists()
    assert INFO_PATH.exists()
    assert json.loads(INFO_PATH.read_text())["positive_label"] == "Satisfied"


def test_saved_model_predicts_probability():
    model = joblib.load(MODEL_PATH)
    probability = float(model.predict_proba(SAMPLE)[0, 1])
    assert 0 <= probability <= 1
    assert model.predict(SAMPLE)[0] in [0, 1]


def test_prediction_is_deterministic():
    model = joblib.load(MODEL_PATH)
    assert model.predict_proba(SAMPLE)[0, 1] == model.predict_proba(SAMPLE)[0, 1]

