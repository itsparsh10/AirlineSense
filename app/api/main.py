from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException

from app.api.dependencies import load_model_bundle
from app.api.schemas import PassengerInput, PredictionOutput


pipeline = None
model_info = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipeline, model_info
    pipeline, model_info = load_model_bundle()
    yield
    pipeline = None
    model_info = None


app = FastAPI(
    title="AirlineSense Prediction API",
    description="Predict passenger satisfaction from raw passenger, trip, and service inputs.",
    version="1.0.0",
    lifespan=lifespan,
)


def to_model_frame(passenger: PassengerInput) -> pd.DataFrame:
    values = passenger.model_dump()
    row = {
        "Gender": values["gender"],
        "Age": values["age"],
        "Customer Type": values["customer_type"],
        "Type of Travel": values["type_of_travel"],
        "Class": values["travel_class"],
        "Flight Distance": values["flight_distance"],
        "Departure Delay": values["departure_delay"],
        "Arrival Delay": values["arrival_delay"],
        "Departure and Arrival Time Convenience": values[
            "departure_arrival_convenience"
        ],
        "Ease of Online Booking": values["ease_of_online_booking"],
        "Check-in Service": values["checkin_service"],
        "Online Boarding": values["online_boarding"],
        "Gate Location": values["gate_location"],
        "On-board Service": values["onboard_service"],
        "Seat Comfort": values["seat_comfort"],
        "Leg Room Service": values["leg_room_service"],
        "Cleanliness": values["cleanliness"],
        "Food and Drink": values["food_and_drink"],
        "In-flight Service": values["inflight_service"],
        "In-flight Wifi Service": values["inflight_wifi_service"],
        "In-flight Entertainment": values["inflight_entertainment"],
        "Baggage Handling": values["baggage_handling"],
    }
    return pd.DataFrame([row])


@app.get("/health")
def health():
    return {
        "status": "ok" if pipeline is not None else "degraded",
        "model_loaded": pipeline is not None,
        "model_name": model_info.get("model_name") if model_info else None,
        "model_version": model_info.get("model_version") if model_info else None,
    }


@app.get("/model-info")
def get_model_info():
    if model_info is None:
        raise HTTPException(status_code=503, detail="Model metadata is unavailable.")
    return model_info


@app.post("/predict", response_model=PredictionOutput)
def predict(passenger: PassengerInput):
    if pipeline is None or model_info is None:
        raise HTTPException(status_code=503, detail="Model is not loaded.")

    try:
        frame = to_model_frame(passenger)
        probability = float(pipeline.predict_proba(frame)[0, 1])
        predicted = int(probability >= 0.5)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=f"Prediction failed: {exc}") from exc

    label = "Satisfied" if predicted else "Neutral or Dissatisfied"
    if probability >= 0.75:
        interpretation = "Strong satisfaction signal. The service profile resembles satisfied passengers."
    elif probability >= 0.5:
        interpretation = "Moderate satisfaction signal. Small service changes could still matter."
    elif probability >= 0.25:
        interpretation = "Meaningful dissatisfaction risk. Review the weakest service ratings."
    else:
        interpretation = "High dissatisfaction risk. Proactive service recovery is recommended."

    return PredictionOutput(
        prediction=label,
        probability=round(probability, 4),
        model_name=model_info["model_name"],
        model_version=model_info["model_version"],
        interpretation=interpretation,
    )

