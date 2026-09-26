import hashlib
import json
import sys
from pathlib import Path

from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.loader import load_and_validate
from src.utils.config import load_params, project_path


def main() -> None:
    params = load_params()
    data_params = params["data"]
    raw_path = project_path(data_params["raw_path"])
    data, report = load_and_validate(raw_path)

    train, test = train_test_split(
        data,
        test_size=data_params["test_size"],
        random_state=data_params["random_state"],
        stratify=data[data_params["target"]],
    )

    output_dir = project_path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)
    train.to_csv(output_dir / "train.csv", index=False)
    test.to_csv(output_dir / "test.csv", index=False)

    fingerprint = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    summary = {
        **report.__dict__,
        "train_rows": len(train),
        "test_rows": len(test),
        "dataset_sha256": fingerprint,
        "status": "READY WITH FIXABLE ISSUES",
        "fix": "Arrival Delay is median-imputed inside the fitted pipeline; ID is excluded.",
    }
    (output_dir / "validation_report.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

