# AirlineSense: Master Pitch, Live Demo & Test Cases Guide

This document is your complete playbook for **pitching AirlineSense**, **delivering a live 3-minute demo**, and **running all technical test cases**.

---

## 1. What is AirlineSense & Who is it for?

### 📌 Is it for the Company or the User?
- **It is built FOR THE COMPANY (Airline Operations, Customer Experience, & Airport Ground Staff).**
- **Goal:** To proactively protect passenger retention and brand reputation.

```text
[Passenger Touchpoint Ratings] ──► [Airline Agent Console (Streamlit)]
                                                │
                                                ▼
                                [FastAPI + Random Forest Model]
                                                │
                                                ▼
                                [Dissatisfaction Alert & Recovery]
                                (Agent offers lounge access, miles, or upgrade)
```

### 🎯 What Problem Does It Solve?
1. **Traditional surveys are reactive:** Airlines analyze post-flight survey data weeks later—after the passenger has already left a negative review or switched to a competitor.
2. **AirlineSense is real-time & proactive:** Frontline staff input journey details and touchpoint ratings into the system. The ML model instantly outputs a dissatisfaction probability, giving agents a window of opportunity for **proactive service recovery** before a formal complaint is filed.

---

## 2. How to Pitch AirlineSense

### ⚡ Option A: 30-Second Elevator Pitch
> *"Customer complaints cost airlines millions in churn, but most issues are handled reactively after the passenger leaves. **AirlineSense** is a real-time MLOps prediction platform that identifies dissatisfied passengers right at airport touchpoints. Powered by a Random Forest microservice with 96% accuracy, 0.954 F1 score, and 0.994 ROC-AUC, it enables frontline staff to deliver instant service recovery before complaints happen."*

---

### 💼 Option B: 2-Minute Executive & Business Pitch
1. **The Business Problem:**
   - Airlines collect thousands of passenger touchpoint ratings (Wi-Fi, boarding, delays, seat comfort), but traditional analytics process them days later.
2. **The Solution:**
   - A real-time prediction microservice that scores passenger satisfaction instantly.
3. **The Financial Impact:**
   - Retaining a dissatisfied frequent flyer saves thousands of dollars in lifetime value compared to the cost of acquisition.
4. **Production Architecture:**
   - Built on a decoupled microservice architecture: Streamlit frontend, FastAPI backend, DVC data versioning, MLflow experiment tracking, and Dockerized deployment.

---

### 🛠️ Option C: 3-Minute Technical & MLOps Pitch
1. **Data Leakage Control:**
   - All preprocessing (imputation, scaling, encoding) is strictly encapsulated inside an `sklearn.pipeline.Pipeline`, fitted **only on training folds**.
2. **Feature Engineering & Selection Rationale:**
   - Evaluated Domain Feature Engineering vs. Baseline Random Forest. Baseline Random Forest achieved superior cross-validated F1 (**0.952**) over Logistic Regression (**0.850**) and Feature-Engineered RF (**0.951**). We applied **Occam's Razor** and selected the simpler baseline.
3. **MLOps Governance:**
   - **DVC:** Tracks raw data lineage and defines execution DAG (`dvc.yaml`).
   - **MLflow:** Logs experiment metrics, hyperparameters, confusion matrix artifacts, and registers `AirlineSenseClassifier` in `sqlite:///mlflow.db`.
   - **FastAPI:** Enforces Pydantic boundary validation and handles unknown categorical levels gracefully (`handle_unknown="ignore"`).

---

## 3. Step-by-Step Live Demo Script (3-Minute Presentation)

### 📋 Pre-Demo Setup (Open These 3 Tabs)
1. **Tab 1 — Streamlit UI:** [http://localhost:8501](http://localhost:8501)
2. **Tab 2 — FastAPI Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
3. **Tab 3 — MLflow Dashboard:** [http://localhost:5001](http://localhost:5001)

---

### 🎙️ Word-for-Word Script & Actions

#### ⏱️ 0:00 – 0:45 | Streamlit UI & Live Prediction
- **What to say:** *"Welcome! This is AirlineSense. Frontline customer service agents use this console to evaluate passenger satisfaction in real time."*
- **What to show:** Point to the left sidebar badge: **"Prediction API connected"**.
- **What to do:** Keep default high-rating values (Business traveler, high boarding/Wi-Fi scores). Click **`PREDICT PASSENGER SATISFACTION`**.
- **What to say:** *"Notice the output card: Prediction is **Satisfied** with **99.99% probability**, powered by `random_forest_baseline v1.0.0`."*
- **Live Change:** Lower *Online Boarding*, *Wi-Fi*, and *Seat Comfort* to `1` or `2`, and set *Arrival Delay* to `60 min`. Click **`PREDICT PASSENGER SATISFACTION`** again.
- **What to say:** *"Notice how the model instantly flips to **Neutral or Dissatisfied** with high dissatisfaction probability. Frontline agents can now offer an instant lounge pass or upgrade."*

#### ⏱️ 0:45 – 1:30 | FastAPI Microservice & Boundary Validation
- **What to do:** Switch to **Tab 2 (FastAPI Docs: `localhost:8000/docs`)**.
- **What to show:**
  - Expand `GET /health` -> Click **Try it out** -> **Execute**. Show status `ok` and `model_loaded: true`.
  - Expand `POST /predict`.
- **What to say:** *"Streamlit does not load the ML model directly. It communicates over HTTP with our FastAPI microservice. FastAPI enforces strict Pydantic input validation—rejecting invalid ratings outside 0–5 and handling missing delay values via median imputation."*

#### ⏱️ 1:30 – 2:15 | MLflow Experiment Tracking & Model Selection
- **What to do:** Switch to **Tab 3 (MLflow UI: `localhost:5001`)**.
- **What to show:** Point out the 3 experiment runs: **Logistic Regression**, **Random Forest Baseline**, and **Random Forest Feature Engineered**.
- **What to say:** *"In MLflow, we tracked all candidate runs. Logistic Regression scored 0.850 F1. Random Forest achieved 0.952 F1 because it captures non-linear interactions between delays and service quality. Feature engineering did not beat the baseline, so we registered `AirlineSenseClassifier v1.0.0` without unnecessary code complexity."*

#### ⏱️ 2:15 – 3:00 | Reproducibility & Docker Deployment
- **What to say:** *"Finally, the full data pipeline is versioned with DVC (`dvc.yaml`), verified with 9 passing automated pytest unit tests, and packaged into a production Docker container for automated CI/CD deployment."*

---

## 4. Comprehensive Test Cases Matrix

### 🧪 Category A: Automated Unit & Integration Tests (`pytest`)
Run in terminal:
```bash
.venv/bin/python -m pytest -v
```

| Test ID | Test Function | Target Component | Description / Expected Result |
| :--- | :--- | :--- | :--- |
| **TC-01** | `test_health_endpoint` | `FastAPI /health` | Returns HTTP `200 OK`, `status: ok`, `model_loaded: true`. |
| **TC-02** | `test_predict_satisfied` | `FastAPI /predict` | Sends high-rating JSON payload -> Returns HTTP `200 OK`, `prediction: Satisfied`. |
| **TC-03** | `test_predict_dissatisfied` | `FastAPI /predict` | Sends low-rating/high-delay JSON -> Returns HTTP `200 OK`, `prediction: Neutral or Dissatisfied`. |
| **TC-04** | `test_validation_error` | `FastAPI /predict` | Sends invalid rating (`seat_comfort: 99`) -> Returns HTTP `422 Unprocessable Entity`. |
| **TC-05** | `test_feature_transformer` | `AirlineFeatureEngineer` | Verifies pipeline transformer executes without mutating original input DataFrame. |
| **TC-06** | `test_training_pipeline` | `src/models/pipeline.py` | Trains candidate pipeline and verifies output predictions shape and probability bounds [0, 1]. |

---

### 🖐️ Category B: Manual UI & API End-to-End Test Cases

#### Test Case 1: Satisfied Business Traveler
- **Input Payload:**
  - Customer: `Female`, `35 years`, `Returning`, `Business Travel`, `Business Class`
  - Flight Distance: `821 miles`, Departure Delay: `0 min`, Arrival Delay: `0 min`
  - Ratings: Boarding: `5`, Wi-Fi: `5`, Seat Comfort: `5`, Cleanliness: `5`
- **Expected Result:**
  - Label: `Satisfied`
  - Probability: `≥ 95%`
  - HTTP Status: `200 OK`

#### Test Case 2: Dissatisfied Economy Passenger (Heavy Delay)
- **Input Payload:**
  - Customer: `Male`, `42 years`, `First-time`, `Personal Travel`, `Eco`
  - Flight Distance: `1200 miles`, Departure Delay: `75 min`, Arrival Delay: `90 min`
  - Ratings: Boarding: `1`, Wi-Fi: `1`, Service: `1`, Leg Room: `2`
- **Expected Result:**
  - Label: `Neutral or Dissatisfied`
  - Dissatisfaction Probability: `≥ 95%`
  - HTTP Status: `200 OK`

#### Test Case 3: Missing Arrival Delay (Median Imputer Robustness)
- **Input Payload:** Set `"arrival_delay": null` or omit field in request.
- **Expected Result:** API handles missing value automatically using training median (`11.0 min`), returning HTTP `200 OK` without throwing a 500 error.

#### Test Case 4: Invalid Boundary Rejection (Pydantic Defense)
- **Input Payload:** Set `"inflight_wifi_service": 10` or `"age": -5`.
- **Expected Result:** FastAPI rejects payload with HTTP `422 Unprocessable Entity`, displaying exact field validation errors.
