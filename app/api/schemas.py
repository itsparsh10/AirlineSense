from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PassengerInput(BaseModel):
    gender: Literal["Female", "Male"]
    age: int = Field(ge=7, le=85)
    customer_type: Literal["First-time", "Returning"]
    type_of_travel: Literal["Business", "Personal"]
    travel_class: Literal["Business", "Economy", "Economy Plus"]
    flight_distance: int = Field(ge=31, le=5000)
    departure_delay: float = Field(ge=0, le=1600)
    arrival_delay: float | None = Field(default=None, ge=0, le=1600)
    departure_arrival_convenience: int = Field(ge=0, le=5)
    ease_of_online_booking: int = Field(ge=0, le=5)
    checkin_service: int = Field(ge=0, le=5)
    online_boarding: int = Field(ge=0, le=5)
    gate_location: int = Field(ge=0, le=5)
    onboard_service: int = Field(ge=0, le=5)
    seat_comfort: int = Field(ge=0, le=5)
    leg_room_service: int = Field(ge=0, le=5)
    cleanliness: int = Field(ge=0, le=5)
    food_and_drink: int = Field(ge=0, le=5)
    inflight_service: int = Field(ge=0, le=5)
    inflight_wifi_service: int = Field(ge=0, le=5)
    inflight_entertainment: int = Field(ge=0, le=5)
    baggage_handling: int = Field(ge=1, le=5)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
        }
    )


class PredictionOutput(BaseModel):
    prediction: Literal["Satisfied", "Neutral or Dissatisfied"]
    probability: float
    model_name: str
    model_version: str
    interpretation: str

