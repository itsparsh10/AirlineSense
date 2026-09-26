from dataclasses import dataclass

import pandas as pd


TARGET_COLUMN = "Satisfaction"
EXPECTED_COLUMNS = [
    "ID",
    "Gender",
    "Age",
    "Customer Type",
    "Type of Travel",
    "Class",
    "Flight Distance",
    "Departure Delay",
    "Arrival Delay",
    "Departure and Arrival Time Convenience",
    "Ease of Online Booking",
    "Check-in Service",
    "Online Boarding",
    "Gate Location",
    "On-board Service",
    "Seat Comfort",
    "Leg Room Service",
    "Cleanliness",
    "Food and Drink",
    "In-flight Service",
    "In-flight Wifi Service",
    "In-flight Entertainment",
    "Baggage Handling",
    TARGET_COLUMN,
]

ALLOWED_TARGETS = {"Satisfied", "Neutral or Dissatisfied"}


@dataclass(frozen=True)
class ValidationReport:
    rows: int
    columns: int
    duplicate_rows: int
    missing_arrival_delay: int
    target_distribution: dict[str, int]


def validate_dataframe(data: pd.DataFrame) -> ValidationReport:
    missing_columns = sorted(set(EXPECTED_COLUMNS) - set(data.columns))
    extra_columns = sorted(set(data.columns) - set(EXPECTED_COLUMNS))
    if missing_columns or extra_columns:
        raise ValueError(
            f"Schema mismatch. Missing={missing_columns}; unexpected={extra_columns}"
        )

    if data.empty:
        raise ValueError("The dataset is empty.")

    if data["ID"].isna().any() or not data["ID"].is_unique:
        raise ValueError("ID must be complete and unique.")

    targets = set(data[TARGET_COLUMN].dropna().unique())
    if targets != ALLOWED_TARGETS:
        raise ValueError(f"Unexpected target labels: {sorted(targets)}")

    rating_columns = [
        column
        for column in data.columns
        if column
        not in {
            "ID",
            "Gender",
            "Age",
            "Customer Type",
            "Type of Travel",
            "Class",
            "Flight Distance",
            "Departure Delay",
            "Arrival Delay",
            TARGET_COLUMN,
        }
    ]
    invalid_ratings = [
        column for column in rating_columns if not data[column].between(0, 5).all()
    ]
    if invalid_ratings:
        raise ValueError(f"Service ratings outside 0-5: {invalid_ratings}")

    non_arrival_missing = data.drop(columns=["Arrival Delay"]).isna().sum().sum()
    if non_arrival_missing:
        raise ValueError("Only Arrival Delay may contain missing values in this dataset.")

    return ValidationReport(
        rows=len(data),
        columns=len(data.columns),
        duplicate_rows=int(data.duplicated().sum()),
        missing_arrival_delay=int(data["Arrival Delay"].isna().sum()),
        target_distribution={
            str(key): int(value)
            for key, value in data[TARGET_COLUMN].value_counts().items()
        },
    )

