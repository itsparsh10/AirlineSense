import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.features.feature_engineering import add_engineered_features
from src.utils.config import project_path


def main() -> None:
    train = pd.read_csv(project_path("data/processed/train.csv"))
    target = train.pop("Satisfaction")
    engineered = add_engineered_features(train)
    engineered["Satisfaction"] = target.values
    output_path = project_path("data/processed/engineered_train.csv")
    engineered.to_csv(output_path, index=False)

    summary = {
        "rows": len(engineered),
        "input_columns": len(train.columns),
        "output_columns": len(engineered.columns) - 1,
        "created_features": [
            "Total Delay",
            "Average Service Score",
            "Digital Experience Score",
            "Delay per 1000 Miles",
            "Is Delayed",
        ],
    }
    project_path("reports").mkdir(exist_ok=True)
    project_path("reports/feature_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

