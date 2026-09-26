import json
import sys
import time
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_validate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.models.pipeline import build_logistic_pipeline, build_random_forest_pipeline
from src.utils.config import load_params, project_path


def main() -> None:
    params = load_params()
    train = pd.read_csv(project_path("data/processed/train.csv"))
    engineered = pd.read_csv(project_path("data/processed/engineered_train.csv"))
    if len(train) != len(engineered):
        raise ValueError("Engineered feature output does not match the training rows.")

    target_name = params["data"]["target"]
    X_train = train.drop(columns=[target_name])
    y_train = (train[target_name] == "Satisfied").astype(int)
    training = params["training"]

    experiments = {
        "logistic_baseline": build_logistic_pipeline(
            max_iter=training["logistic_max_iter"], engineered=False
        ),
        "random_forest_baseline": build_random_forest_pipeline(
            n_estimators=training["random_forest_estimators"],
            max_depth=training["random_forest_max_depth"],
            min_samples_leaf=training["random_forest_min_samples_leaf"],
            random_state=training["random_state"],
            engineered=False,
        ),
        "random_forest_engineered": build_random_forest_pipeline(
            n_estimators=training["random_forest_estimators"],
            max_depth=training["random_forest_max_depth"],
            min_samples_leaf=training["random_forest_min_samples_leaf"],
            random_state=training["random_state"],
            engineered=True,
        ),
    }

    mlflow.set_tracking_uri(params["mlflow"]["tracking_uri"])
    mlflow.set_experiment(params["mlflow"]["experiment_name"])
    cv = StratifiedKFold(
        n_splits=training["cv_folds"], shuffle=True, random_state=training["random_state"]
    )
    scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]
    results = []

    for name, pipeline in experiments.items():
        started = time.perf_counter()
        scores = cross_validate(
            pipeline,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
            n_jobs=1,
        )
        elapsed = time.perf_counter() - started
        metrics = {
            metric: float(scores[f"test_{metric}"].mean()) for metric in scoring
        }
        metrics["training_seconds"] = elapsed
        record = {
            "name": name,
            "feature_set": "engineered" if name.endswith("engineered") else "baseline",
            **metrics,
        }
        results.append(record)

        with mlflow.start_run(run_name=name):
            mlflow.log_params(
                {
                    "model": name,
                    "feature_set": record["feature_set"],
                    "cv_folds": training["cv_folds"],
                    "random_state": training["random_state"],
                    "train_rows": len(X_train),
                }
            )
            mlflow.log_metrics(metrics)
            mlflow.set_tag("purpose", "model_selection_cross_validation")

    best = max(results, key=lambda item: (item["f1"], item["roc_auc"]))
    best_pipeline = experiments[best["name"]]
    best_pipeline.fit(X_train, y_train)

    model_dir = project_path("models")
    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / "airlinesense_pipeline.joblib"
    joblib.dump(best_pipeline, model_path, compress=3)

    with mlflow.start_run(run_name="production_candidate") as run:
        mlflow.log_params(
            {
                "selected_experiment": best["name"],
                "selection_metric": "cv_f1",
                "feature_set": best["feature_set"],
            }
        )
        mlflow.log_metrics({f"cv_{key}": value for key, value in best.items() if isinstance(value, float)})
        try:
            model_info = mlflow.sklearn.log_model(
                sk_model=best_pipeline,
                name="model",
                registered_model_name=params["mlflow"]["registered_model_name"],
                input_example=X_train.head(2),
            )
            registry_status = "registered"
            model_uri = model_info.model_uri
        except Exception as exc:
            mlflow.sklearn.log_model(sk_model=best_pipeline, name="model")
            registry_status = f"artifact logged; registry unavailable: {exc}"
            model_uri = f"runs:/{run.info.run_id}/model"

    reports_dir = project_path("reports")
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "experiment_results.json").write_text(
        json.dumps(sorted(results, key=lambda item: item["f1"], reverse=True), indent=2),
        encoding="utf-8",
    )
    metadata = {
        "project": "AirlineSense",
        "model_name": best["name"],
        "model_version": "1.0.0",
        "feature_set": best["feature_set"],
        "selection_metric": "cross-validated F1",
        "cv_f1": best["f1"],
        "cv_roc_auc": best["roc_auc"],
        "mlflow_run_id": run.info.run_id,
        "mlflow_model_uri": model_uri,
        "registry_status": registry_status,
        "positive_label": "Satisfied",
    }
    (model_dir / "model_info.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    print(json.dumps({"selected": metadata, "experiments": results}, indent=2))


if __name__ == "__main__":
    main()

