import pandas as pd

from src.features.feature_engineering import AirlineFeatureEngineer


def sample_frame():
    return pd.DataFrame(
        [
            {
                "ID": 1,
                "Departure Delay": 10,
                "Arrival Delay": 20,
                "Flight Distance": 1000,
                "Check-in Service": 4,
                "On-board Service": 5,
                "Seat Comfort": 4,
                "Leg Room Service": 3,
                "Cleanliness": 5,
                "Food and Drink": 3,
                "In-flight Service": 5,
                "In-flight Entertainment": 4,
                "Baggage Handling": 5,
                "Ease of Online Booking": 3,
                "Online Boarding": 4,
                "In-flight Wifi Service": 2,
            }
        ]
    )


def test_feature_engineer_drops_identifier_and_creates_features():
    result = AirlineFeatureEngineer(enabled=True).fit_transform(sample_frame())
    assert "ID" not in result.columns
    assert result.loc[0, "Total Delay"] == 30
    assert result.loc[0, "Delay per 1000 Miles"] == 30
    assert result.loc[0, "Is Delayed"] == 1
    assert 0 <= result.loc[0, "Average Service Score"] <= 5


def test_baseline_transform_only_drops_identifier():
    result = AirlineFeatureEngineer(enabled=False).fit_transform(sample_frame())
    assert "ID" not in result.columns
    assert "Total Delay" not in result.columns

