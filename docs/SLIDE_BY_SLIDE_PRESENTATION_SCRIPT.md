# AirlineSense: Slide-by-Slide Pitch & Presentation Master Playbook

This master guide provides the exact **Slide-by-Slide script**, **speaker notes**, **data breakdowns**, and **presentation flow** matching your final presentation deck `outputs/AirlineSense_Pitch_Deck_Feature_MLOps_Final.pptx`.

---

## 📽️ Deck Structure Overview

```text
Slide 1 ──► Cover & Product Vision ("Predict before the complaint")
Slide 2 ──► Business Problem & Dataset (129,880 records, 43.5% satisfied)
Slide 3 ──► Data Pipeline & Leakage Control (Stratified 80/20 split, zero leakage)
Slide 4 ──► Feature Engineering Used (Imputation, Encoding, Scaling decisions)
Slide 5 ──► Experiments & Model Selection (Logistic Regression vs RF Baseline vs RF Engineered)
Slide 6 ──► Test Set Performance (96% Accuracy, 95.4% F1, 0.994 ROC-AUC)
Slide 7 ──► MLOps Architecture & Stack (Streamlit -> FastAPI -> DVC -> MLflow -> Docker)
Slide 8 ──► Live Product Demo Script (Real-time Streamlit + FastAPI HTTP interaction)
Slide 9 ──► Production Summary & Business Value
```

---

## Slide 1: Cover — Product Vision
- **Slide Title:** AirlineSense
- **Subtitle:** Predict passenger satisfaction before the complaint
- **Presenter:** Sparsh Sharma | MLOps & Feature Engineering Project
- **Visual:** Streamlit UI Screenshot showing live API connection
- **Exact Speaker Script (30 seconds):**
  > *"Good morning everyone. Today I'm presenting **AirlineSense**, an end-to-end Machine Learning product that predicts passenger satisfaction before a formal complaint is ever filed.*
  >
  > *Instead of waiting weeks for survey reports, AirlineSense allows frontline airline staff to enter journey and service touchpoint details into a web interface and instantly receive a model prediction and dissatisfaction probability score."*

---

## Slide 2: Business Problem & Dataset Breakdown
- **Slide Title:** Business Problem and Data Overview
- **Key Metrics Displayed:**
  - `129,880` Passenger Records
  - `43.5%` Baseline Satisfaction Rate
- **Visual:** Satisfaction rates broken down by Travel Class (Business vs. Eco) and Purpose (Business vs. Personal).
- **Exact Speaker Script (45 seconds):**
  > *"The core business problem is that airlines handle customer dissatisfaction **reactively**. By the time a passenger files a complaint or posts a negative review, they have often already decided to switch to a competing airline.*
  >
  > *Our dataset contains **129,880 passenger records**. Crucially, only **43.5% of passengers are satisfied**. Satisfaction rates drop drastically for personal economy travelers compared to business class travelers. A single overall average isn't enough—airlines need row-level, real-time dissatisfaction warnings at key touchpoints."*

---

## Slide 3: Data Integrity & Leakage Control
- **Slide Title:** Data Integrity & Leakage Prevention
- **4-Step Data Flow Visual:**
  1. `Raw CSV (129,880 rows)` -> 2. `Stratified 80/20 Split` -> 3. `Pipeline Fit (Train Only)` -> 4. `Final Test Set (25,976 rows)`
- **Key Highlights:**
  - `393 missing arrival delays` -> Handled via Median Imputation inside training fold.
  - `Unique Passenger ID` -> Removed to prevent arbitrary memorization.
- **Exact Speaker Script (50 seconds):**
  > *"To guarantee strict ML engineering standards, data split happens **BEFORE** any preprocessing.*
  >
  > *Arrival Delay contained 393 missing values. Rather than dropping these rows or computing global averages, we fit a median imputer exclusively on training folds. The unique passenger ID was stripped out so the model cannot memorize row identifiers. The 25,976 test rows remained untouched until final evaluation."*

---

## Slide 4: Feature Engineering Used (And Evaluated)
- **Slide Title:** Feature Engineering Techniques Used
- **Side-by-Side Comparison:**
  - **Left Box (In Production Pipeline):**
    - `Median Imputation` for right-skewed delays.
    - `Mode Imputation` for categorical fallbacks.
    - `One-Hot Encoding` with `handle_unknown="ignore"` for travel classes/types.
    - `Conditional StandardScaler` (enabled for Logistic Regression, disabled for Random Forest).
  - **Right Box (Evaluated Experiment):**
    - `AirlineFeatureEngineer` (`Total Delay`, `Average Service Score`, `Digital Experience Score`, `Delay / 1k Miles`).
    - *Result:* CV F1 was **0.951**, compared to **0.952** for the baseline Random Forest.
- **Exact Speaker Script (50 seconds):**
  > *"We strictly implemented transformers inside an `sklearn.pipeline.Pipeline`.*
  >
  > *We used median imputation for continuous delays and One-Hot Encoding with `handle_unknown="ignore"` for categoricals so unseen levels in production won't crash the API. Standard scaling was applied ONLY to Logistic Regression, as tree models are scale-invariant.*
  >
  > *We also engineered domain features like Total Delay and Average Service Score. However, cross-validation proved the baseline Random Forest achieved 0.952 F1 versus 0.951 for the engineered forest. Following **Occam's Razor**, we selected the simpler baseline model for production."*

---

## Slide 5: Experiments & Model Comparison
- **Slide Title:** Experiment Tracking & Model Selection
- **Comparison Table / Bar Chart:**
  - **Logistic Regression (Scaled):** CV F1 = `0.850` | ROC-AUC = `0.926`
  - **Random Forest (Engineered):** CV F1 = `0.951` | ROC-AUC = `0.993`
  - **Random Forest Baseline (SELECTED):** CV F1 = `0.952` | ROC-AUC = `0.993`
- **Exact Speaker Script (45 seconds):**
  > *"We logged all candidate models in MLflow. Logistic Regression gave us a baseline F1 of 0.850. Because passenger satisfaction depends on complex, non-linear interactions—such as a flight delay being acceptable ONLY if Wi-Fi and seat comfort are high—Random Forest dramatically improved cross-validated F1 to 0.952.*
  >
  > *Since the baseline Random Forest outperformed the feature-engineered variant, it was registered as `AirlineSenseClassifier v1.0.0` in MLflow."*

---

## Slide 6: Verified Test Performance Evidence
- **Slide Title:** Final Performance on Untouched Test Set
- **Metrics Grid:**
  - **Accuracy:** `96.0%`
  - **F1 Score:** `95.4%`
  - **Recall:** `94.7%`
  - **ROC-AUC:** `0.994`
- **Exact Speaker Script (40 seconds):**
  > *"Evaluating our registered model on the untouched test set of 25,976 passengers yielded outstanding results: **96.0% Accuracy**, **95.4% F1 Score**, **94.7% Recall**, and **0.994 ROC-AUC**.*
  >
  > *We prioritized F1 and Recall because in airline operations, failing to identify a dissatisfied passenger leads directly to customer churn."*

---

## Slide 7: MLOps Product Architecture
- **Slide Title:** End-to-End MLOps Architecture
- **Diagram:** `DVC (Data Versioning)` ──► `MLflow (Registry)` ──► `FastAPI (:8000)` ──► `Streamlit (:8501)` ──► `Docker Container`
- **Exact Speaker Script (50 seconds):**
  > *"AirlineSense is built as a modular microservice architecture.*
  >
  > *DVC tracks raw data files and orchestrates our four-stage pipeline (`dvc.yaml`). MLflow tracks parameters and registers candidate models in SQLite. FastAPI hosts the prediction endpoints (`/health` and `/predict`), while Streamlit acts as an independent UI communicating purely over HTTP. The entire system is containerized with Docker and verified via GitHub Actions CI/CD."*

---

## Slide 8: Live Product Demonstration
- **Slide Title:** Live Product Demo
- **Action Sequence:**
  1. Switch to Streamlit ([http://localhost:8501](http://localhost:8501)). Show **"Prediction API connected"**.
  2. Click **Predict Satisfaction** with default high ratings -> Show **Satisfied (99.99%)**.
  3. Lower Wi-Fi, Boarding, and Seat Comfort; add 60-min delay -> Click **Predict** -> Show **Neutral or Dissatisfied**.
- **Exact Speaker Script (75 seconds):**
  > *"Now let's look at the live application. Notice the sidebar badge showing our Streamlit UI is connected to our FastAPI microservice.*
  >
  > *When we submit high ratings for a business traveler, FastAPI evaluates the request through the saved pipeline and returns 'Satisfied' with 99.99% confidence. If we change the passenger's ratings—lowering Wi-Fi and boarding to 1 and adding a 60-minute arrival delay—the model instantly returns 'Neutral or Dissatisfied'. Frontline staff can immediately offer a lounge pass or service recovery."*

---

## Slide 9: Conclusion & Business Value
- **Slide Title:** Production Ready & Business Value
- **Key Takeaways:**
  - Prevents customer churn via real-time touchpoint prediction.
  - Zero training-serving skew with encapsulated `sklearn` pipelines.
  - Fully automated MLOps stack (DVC, MLflow, FastAPI, Streamlit, Docker).
- **Exact Speaker Script (30 seconds):**
  > *"In summary, AirlineSense bridges the gap between machine learning research and real-world operations. It turns raw survey feedback into immediate actionable alerts, allowing airlines to save high-value passenger relationships before complaints occur. Thank you, and I am ready for your questions!"*
