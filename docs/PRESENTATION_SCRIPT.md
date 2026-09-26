# AirlineSense presentation script

Target length: 5–7 minutes. Speak naturally. Do not read every label on the slides.

## Slide 1 — AirlineSense (30 seconds)

“Good morning. My project is AirlineSense. It predicts whether an airline passenger is likely to be satisfied using passenger details, journey information, and service ratings.

The purpose is simple: identify dissatisfaction risk before it becomes a complaint, so a service team can respond sooner. I built it as a working product, with a Streamlit interface, a FastAPI backend, a trained model, experiment tracking, data versioning, tests, and Docker.”

## Slide 2 — The problem (40 seconds)

“The dataset contains 129,880 passenger records. Each row combines the passenger profile, flight information, delays, and ratings across the airport and on-board experience.

Only 43.5 percent of passengers are satisfied. Satisfaction also changes sharply by cabin class and travel purpose. That means one overall average does not tell an operations team which individual passenger may need attention. This is the decision my model supports.”

## Slide 3 — Data and leakage control (50 seconds)

“Before training, I checked the schema, target balance, missing values, duplicates, identifier columns, and leakage risk.

The dataset has no duplicate rows. Arrival Delay has 393 missing values, which I handle with median imputation inside the fitted pipeline. I removed the unique passenger ID because it has no general predictive meaning.

I used a stratified 80/20 split. Imputation and one-hot encoding are fitted only on training data and inside each cross-validation fold. The final 25,976 test rows remained untouched until model selection was complete.”

## Slide 4 — Experiments (55 seconds)

“I compared three real experiments in MLflow.

Logistic Regression gave an interpretable baseline with an F1 of about 0.85. The baseline Random Forest improved cross-validated F1 to 0.952. I also tested an engineered Random Forest using total delay, average service quality, digital experience, delay per thousand miles, and a delay flag.

The engineered version scored slightly lower at 0.951. I therefore selected the simpler baseline Random Forest. I kept the feature experiment in the project because it demonstrates an important point: a feature should improve evidence, not just increase complexity.”

## Slide 5 — Final performance (45 seconds)

“On the untouched test set, the selected model achieved 96.0 percent accuracy, 95.4 percent F1, 94.7 percent recall, and 0.994 ROC-AUC.

I focused on F1 because both false alarms and missed satisfied or dissatisfied passengers matter. The default probability threshold is 0.50. In a real airline, I would tune that threshold using the cost of missing a dissatisfied passenger and the available service-recovery capacity.”

## Slide 6 — MLOps architecture (55 seconds)

“The user works in Streamlit, but Streamlit never loads the model. It sends an HTTP request to FastAPI. FastAPI validates the request, calls the saved sklearn pipeline, and returns the label, probability, model name, version, and a short interpretation.

DVC tracks the raw dataset and the prepare, feature, train, and evaluate stages. MLflow stores the model runs, parameters, metrics, artifacts, and the registered AirlineSenseClassifier. Docker packages the API and UI. GitHub Actions contains one workflow for tests and one for building and publishing the Docker image.”

## Slide 7 — Live demo (about 90 seconds)

“Now I will show the product running.”

1. Point to `Prediction API connected` in the sidebar.
2. Say: “These are raw passenger and service inputs. No manual preprocessing happens in this interface.”
3. Click `PREDICT SATISFACTION`.
4. Say: “The UI sent JSON to FastAPI. FastAPI used the saved pipeline and returned this probability and model version.”
5. Reduce Online Boarding, Wi-Fi, Cabin Service, Seat Comfort, Cleanliness, and Entertainment to low values.
6. Click the button again.
7. Say: “The result changes because the request reached the real model. This is not a static or fabricated response.”

If time allows, open `http://localhost:8000/docs` and show the three endpoints: `/health`, `/model-info`, and `/predict`.

## Slide 8 — Close (35 seconds)

“The completed local evidence chain runs from a DVC-versioned dataset, through MLflow experiments and a registered model, into a tested API, a browser interface, and a healthy Docker container.

All nine automated tests pass, and the final model has a 95.4 percent test F1. The repository also contains the GitHub Actions workflow required to publish the image to Docker Hub. Cloud hosting is optional and would be the next deployment step.

Thank you. I am ready for questions.”

# Exact live-demo commands

## Recommended Docker demo

Run this before presenting:

```bash
cd airlinesense-mlops
docker run --rm --name airlinesense-demo \
  -p 8000:8000 \
  -p 8501:8501 \
  airlinesense-mlops:local
```

Open:

- Product: `http://localhost:8501`
- API documentation: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

## MLflow demo

In a second terminal:

```bash
cd airlinesense-mlops
source .venv/bin/activate
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 127.0.0.1 \
  --port 5000
```

Open `http://localhost:5000`, then show:

1. Experiment `airlinesense-classification`
2. The three candidate runs
3. F1 and ROC-AUC columns
4. The registered model `AirlineSenseClassifier`

## DVC proof

```bash
export DVC_SITE_CACHE_DIR=/tmp/airlinesense-dvc-site-cache
dvc dag
dvc status
dvc metrics show
```

## Test proof

```bash
pytest -q
```

Expected result: `9 passed`.

# Demo backup

If a live tab fails, do not debug in front of the class. Continue with:

- Slide 7 in the deck
- `presentation/ui-demo.png`
- `reports/figures/confusion_matrix.png`
- `reports/experiment_results.json`

Say: “I verified this flow locally in Chromium and captured the result as backup evidence.”

