from pathlib import Path

import pandas as pd

from src.data.validation import ValidationReport, validate_dataframe


def load_and_validate(path: str | Path) -> tuple[pd.DataFrame, ValidationReport]:
    data = pd.read_csv(path)
    report = validate_dataframe(data)
    return data, report

