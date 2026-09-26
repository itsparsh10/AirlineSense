from fastapi.testclient import TestClient

from app.api.main import app


VALID_PAYLOAD = {
    "gender": "Female",
    "age": 35,
    "customer_type": "Returning",
    "type_of_travel": "Business",
    "travel_class": "Business",
    "flight_distance": 821,
    "departure_delay": 26,
    "arrival_delay": 39,
    "departure_arrival_convenience": 2,
    "ease_of_online_booking": 2,
    "checkin_service": 3,
    "online_boarding": 5,
    "gate_location": 2,
    "onboard_service": 5,
    "seat_comfort": 4,
    "leg_room_service": 5,
    "cleanliness": 5,
    "food_and_drink": 3,
    "inflight_service": 5,
    "inflight_wifi_service": 2,
    "inflight_entertainment": 5,
    "baggage_handling": 5,
}


def test_health_reports_loaded_model():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["model_loaded"] is True


def test_predict_returns_real_model_response():
    with TestClient(app) as client:
        response = client.post("/predict", json=VALID_PAYLOAD)
        assert response.status_code == 200
        body = response.json()
        assert body["prediction"] in ["Satisfied", "Neutral or Dissatisfied"]
        assert 0 <= body["probability"] <= 1
        assert body["model_name"]


def test_predict_rejects_invalid_rating():
    with TestClient(app) as client:
        response = client.post(
            "/predict", json={**VALID_PAYLOAD, "seat_comfort": 8}
        )
        assert response.status_code == 422


def test_predict_rejects_missing_field():
    payload = {key: value for key, value in VALID_PAYLOAD.items() if key != "age"}
    with TestClient(app) as client:
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

