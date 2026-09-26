import json
import os
import sys
from pathlib import Path

import joblib
os.environ.setdefault("MPLCONFIGDIR", "/tmp/airlinesense-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.config import load_params, project_path


def main() -> None:
    params = load_params()
    target_name = params["data"]["target"]
    test = pd.read_csv(project_path("data/processed/test.csv"))
    X_test = test.drop(columns=[target_name])
    y_test = (test[target_name] == "Satisfied").astype(int)
    pipeline = joblib.load(project_path("models/airlinesense_pipeline.joblib"))

    predictions = pipeline.predict(X_test)
    probabilities = pipeline.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "precision": float(precision_score(y_test, predictions)),
        "recall": float(recall_score(y_test, predictions)),
        "f1": float(f1_score(y_test, predictions)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)),
        "test_rows": len(test),
    }
    project_path("reports").mkdir(exist_ok=True)
    project_path("reports/test_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )

    figures_dir = project_path("reports/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    fig, axis = plt.subplots(figsize=(6.5, 5))
    ConfusionMatrixDisplay.from_predictions(
        y_test,
        predictions,
        display_labels=["Neutral / Dissatisfied", "Satisfied"],
        cmap="Blues",
        colorbar=False,
        ax=axis,
    )
    axis.set_title("AirlineSense test-set confusion matrix")
    fig.tight_layout()
    fig.savefig(figures_dir / "confusion_matrix.png", dpi=180)
    plt.close(fig)

    false_positive_rate, true_positive_rate, _ = roc_curve(y_test, probabilities)
    fig, axis = plt.subplots(figsize=(6.5, 5))
    axis.plot(false_positive_rate, true_positive_rate, color="#0C7C86", linewidth=3)
    axis.plot([0, 1], [0, 1], linestyle="--", color="#8A98A5")
    axis.set(
        title=f"ROC curve (AUC {metrics['roc_auc']:.3f})",
        xlabel="False positive rate",
        ylabel="True positive rate",
    )
    fig.tight_layout()
    fig.savefig(figures_dir / "roc_curve.png", dpi=180)
    plt.close(fig)

    satisfaction_by_class = (
        test.assign(Satisfied=y_test)
        .groupby(["Class", "Type of Travel"], as_index=False)["Satisfied"]
        .mean()
    )
    satisfaction_by_class.to_csv(
        project_path("reports/satisfaction_by_segment.csv"), index=False
    )
    fig, axis = plt.subplots(figsize=(8, 4.8))
    sns.barplot(
        data=satisfaction_by_class,
        x="Class",
        y="Satisfied",
        hue="Type of Travel",
        palette=["#0C7C86", "#F28E5B"],
        ax=axis,
    )
    axis.set_title("Satisfaction varies sharply by cabin and travel purpose")
    axis.set_ylabel("Satisfied passengers")
    axis.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    axis.set_xlabel("")
    fig.tight_layout()
    fig.savefig(figures_dir / "segment_satisfaction.png", dpi=180)
    plt.close(fig)

    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
