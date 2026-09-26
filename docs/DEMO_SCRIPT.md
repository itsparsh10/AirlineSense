# Three-minute live demo

## Before class

```bash
docker run --rm -p 8000:8000 -p 8501:8501 airlinesense-mlops:local
```

Open these tabs before presenting:

1. Streamlit at `http://localhost:8501`
2. FastAPI docs at `http://localhost:8000/docs`
3. MLflow at `http://localhost:5000`
4. GitHub Actions and Docker Hub, once the account setup is complete

## Demo sequence

**0:00–0:20 — Product**

“This is AirlineSense. An agent enters the passenger and service profile, then the UI asks the FastAPI service for a real model prediction.”

**0:20–1:10 — Live prediction**

- Show the API-connected status.
- Keep the strong business-travel example and click `PREDICT SATISFACTION`.
- Point to the label, probability, model name, and interpretation.
- Reduce Online Boarding, Wi-Fi, seat comfort, and cabin service, then predict again to show that the result responds to changed inputs.

**1:10–1:35 — API boundary**

- Open `/docs`.
- Show the request validation ranges and `/health`, `/model-info`, and `/predict` endpoints.
- Explain that Streamlit does not load the model.

**1:35–2:10 — Evidence**

- Open MLflow.
- Compare the three runs.
- Say: “The engineered model did not beat the baseline forest, so I did not force it into production.”
- Show the registered `AirlineSenseClassifier`.

**2:10–2:35 — Reproducibility**

- Run `dvc dag` or show `dvc.yaml`.
- Explain the four stages: prepare, features, train, evaluate.
- Mention the raw CSV pointer and local remote.

**2:35–3:00 — Shipping**

- Show the passing tests and Docker image.
- Show the CI and Docker publishing workflows.
- Close with the test metrics: 95.4% F1 and 0.994 ROC-AUC.

## Backup plan

If Docker or the network fails, use:

- `presentation/ui-demo.png`
- `reports/figures/confusion_matrix.png`
- `reports/experiment_results.json`
- the final PowerPoint deck

