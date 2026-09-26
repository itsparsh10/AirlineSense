import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


SERVICE_COLUMNS = [
    "Check-in Service",
    "On-board Service",
    "Seat Comfort",
    "Leg Room Service",
    "Cleanliness",
    "Food and Drink",
    "In-flight Service",
    "In-flight Entertainment",
    "Baggage Handling",
]

DIGITAL_COLUMNS = [
    "Ease of Online Booking",
    "Online Boarding",
    "In-flight Wifi Service",
]


class AirlineFeatureEngineer(BaseEstimator, TransformerMixin):
    """Create explainable passenger-experience features from raw request fields."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        frame = X.copy()
        if "ID" in frame.columns:
            frame = frame.drop(columns=["ID"])

        if not self.enabled:
            return frame

        frame["Total Delay"] = frame["Departure Delay"].fillna(0) + frame[
            "Arrival Delay"
        ].fillna(frame["Departure Delay"])
        frame["Average Service Score"] = frame[SERVICE_COLUMNS].mean(axis=1)
        frame["Digital Experience Score"] = frame[DIGITAL_COLUMNS].mean(axis=1)
        frame["Delay per 1000 Miles"] = (
            frame["Total Delay"] / frame["Flight Distance"].clip(lower=1) * 1000
        )
        frame["Is Delayed"] = (frame["Total Delay"] > 15).astype(int)
        return frame


def add_engineered_features(frame: pd.DataFrame) -> pd.DataFrame:
    return AirlineFeatureEngineer(enabled=True).transform(frame)

