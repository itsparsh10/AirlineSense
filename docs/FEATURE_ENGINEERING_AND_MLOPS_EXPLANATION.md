# AirlineSense: Humanized Feature Engineering & MLOps Guide

> **"If you can't explain your machine learning system to a human in simple terms, you don't truly control your pipeline."**

This document provides a **humanized, step-by-step audit** of the AirlineSense project. It explains **how data flows through the system**, **what concepts from the 3 Mind Maps were used vs. avoided**, and **why Random Forest was chosen over other models**.

---

## 1. The Humanized Story: How Data Results in a Prediction

Imagine a passenger finishes a flight and submits ratings. Here is what happens under the hood, step-by-step:

```text
[Passenger Survey / Agent Input]
              │
              ▼
    [1. FastAPI Request Boundary]
    Pydantic checks: Is age > 0? Are ratings between 0 and 5? Valid travel class?
              │
              ▼
    [2. ColumnTransformer Split]
    Splits numerical columns (Age, Delays, Ratings) from categorical columns (Gender, Class, Travel Type).
              │
              ▼
    [3. Imputation (Handling Missing Data)]
    • Arrival Delay missing? Replaced with training median (11.0 minutes).
    • Categorical missing? Replaced with training mode (most frequent value).
              │
              ▼
    [4. Categorical Encoding]
    • Turns "Business Class" into binary flags [1, 0, 0].
    • handle_unknown="ignore" ensures new categories in production won't crash the server.
              │
              ▼
    [5. Random Forest Decision Trees (100 Trees)]
    • 100 decision trees evaluate non-linear feature splits (e.g., Delay > 20 MIN AND Wi-Fi < 2).
    • Trees vote to produce a final consensus probability score.
              │
              ▼
    [6. Final Output returned to Streamlit UI]
    • Label: "Satisfied" or "Neutral or Dissatisfied"
    • Probability: 99.99%
    • Interpretation: "Strong satisfaction signal."
```

---

## 2. Audit of the 3 HTML Mind Maps: What Was Used vs. Not Used

Below is a complete phase-by-phase breakdown auditing every concept across `feature_engineering_mindmap_1.html`, `feature_engineering_mindmap_2.html`, and `feature_engineering_mindmap_3.html`.

---

### 🔹 PHASE 1: Foundations
- **Train/Test Split BEFORE Preprocessing (`USED`):** We split 80% train / 20% test before fitting any imputer or encoder. Why? Fitting scalers or imputers on the whole dataset introduces **data leakage** (the model sees future test distribution statistics).
- **Pipeline Automation (`USED`):** Implemented using `sklearn.pipeline.Pipeline`. Chaining preprocessing + model into one object guarantees that training and production inference execute identical code.
- **Raw vs. Engineered Features (`USED`):** Tested raw survey ratings vs. engineered aggregations (`Average Service Score`, `Total Delay`).

---

### 🔹 PHASE 2: Cleaning & Data Prep
- **Median Imputation (`USED`):** Used `SimpleImputer(strategy="median")` for `Arrival Delay`. Why? Delays are heavily right-skewed (most delays are 0–10 min, but a few are 300+ min). The median is unaffected by rare extreme delays.
- **Mean Imputation (`NOT USED`):** Avoided because the mean would be distorted by extreme delay outliers.
- **Mode Imputation (`USED`):** Used `SimpleImputer(strategy="most_frequent")` for categorical columns.
- **One-Hot Encoding (`USED`):** Used `OneHotEncoder(handle_unknown="ignore")` for nominal categoricals (`Gender`, `Customer Type`, `Type of Travel`, `Class`).
- **Standard Scaling (`StandardScaler`) (`CONDITIONAL`):**
  - **Used for Logistic Regression:** Gradient descent optimization requires equal feature scales.
  - **Not Used for Random Forest:** Tree models split based on value ordering, not distance. Monotonic scaling does not change tree splits.
- **Log / Box-Cox / Yeo-Johnson Transformations (`NOT USED`):** Not used in the final model because tree-based models are invariant to monotonic feature transformations.
- **Target / Ordinal Encoding (`NOT USED`):** Avoided because categoricals have low cardinality (2 to 3 levels). One-hot encoding handles them without target leakage risk.

---

### 🔹 PHASE 3: Feature Creation
- **Domain Feature Engineering (`EVALUATED & REJECTED`):** Created `AirlineFeatureEngineer` (`Total Delay`, `Average Service Score`, `Digital Experience Score`, `Delay per 1000 Miles`). Tested in experiments, but baseline Random Forest performed slightly better (**0.952** vs **0.951** F1). We followed **Occam's Razor** and chose the simpler baseline.
- **Time-Series / Lag / Rolling Features (`NOT USED`):** Dataset is tabular survey data per passenger, not continuous time-series.
- **Text Features (TF-IDF / Bag-of-Words / N-grams) (`NOT USED`):** Dataset contains 1–5 numerical ratings rather than unstructured text reviews.

---

### 🔹 PHASE 4: Feature Selection & Evaluation
- **Tree-Based Feature Importance (`USED`):** Random Forest naturally ranks feature importance (e.g. `Online Boarding` and `In-flight Wifi Service` emerge as top satisfaction drivers).
- **Filter / Wrapper Methods (RFE / Variance Threshold) (`NOT USED`):** With only 22 tabular features, Random Forest natively selects splits without needing a pre-filter or RFE wrapper.
- **SHAP / Local Interpretability (`RECOMMENDED NEXT STEP`):** Useful for explaining individual predictions to support agents.

---

### 🔹 PHASE 5: Dimensionality Reduction
- **PCA (Principal Component Analysis) / SVD (`NOT USED`):**
  - **Why NOT used?** PCA compresses 22 meaningful columns into uninterpretable linear components (`PC1`, `PC2`). An airline agent cannot act on `"PC1 = 1.8"`, but they CAN act on `"In-flight Wifi = 1"`.
  - Furthermore, 22 features is small enough that dimensionality reduction is unnecessary.

---

### 🔹 PHASE 6: Feature Ops & Governance (MLOps)
- **Data Leakage Prevention (`USED`):** Strict separation of train/test transformations inside `sklearn.pipeline.Pipeline`.
- **DVC Data Versioning (`USED`):** Tracks raw CSV (`data/raw/`) and defines pipeline DAG (`dvc.yaml`).
- **MLflow Experiment Tracking & Registry (`USED`):** Logs metrics, hyperparameter runs, artifacts, and registers production model `AirlineSenseClassifier` in `sqlite:///mlflow.db`.
- **Feature Stores (`NOT USED`):** Feature stores (like Feast) are designed for large enterprise teams sharing features across hundreds of models. For a single focused service, an `sklearn` pipeline is more lightweight and maintainable.

---

## 3. Why Random Forest? (Model Selection Justification)

```text
+-----------------------------------+----------+------------+------------------------------------------+
| Model Candidate                   |  CV F1   | CV ROC-AUC | Why Selected or Rejected?                |
+-----------------------------------+----------+------------+------------------------------------------+
| Logistic Regression (Scaled)      |  0.850   |   0.926    | Rejected: Cannot capture non-linear links|
| Random Forest Baseline            |  0.952   |   0.993    | SELECTED: Highest F1 & ROC-AUC           |
| Random Forest (Feature Engineered)|  0.951   |   0.993    | Rejected: Extra complexity, no accuracy gain|
+-----------------------------------+----------+------------+------------------------------------------+
```

### 1. Why Random Forest over Logistic Regression?
Logistic Regression assumes linear decision boundaries. In passenger satisfaction, features interact **non-linearly**:
- A 30-minute delay is acceptable if seat comfort and Wi-Fi are rated `5/5`.
- That same 30-minute delay causes dissatisfaction if Wi-Fi and boarding are rated `1/5`.
Logistic Regression missed these interactions (F1: 0.850), whereas Random Forest captured them natively (F1: 0.952).

### 2. Why Random Forest over XGBoost / Gradient Boosting?
Random Forest uses **Bagging** (parallel independent trees). It is highly robust to hyperparameter settings, less prone to overfitting out-of-the-box, and fast to evaluate during live API serving.

### 3. Why Baseline RF over Engineered RF?
Adding grouped averages (`Average Service Score`) compressed fine-grained details, yielding a slightly lower F1 (0.951). In production MLOps, we **never add pipeline complexity unless empirical metrics prove a benefit**.

---

## 4. Summary Table: Used vs. Not Used

| Concept | Used? | Humanized Explanation |
| :--- | :---: | :--- |
| **Train/Test Split First** | ✅ YES | Prevents data leakage. Imputers and encoders learn ONLY from training rows. |
| **Median Imputation** | ✅ YES | Fills missing `Arrival Delay` values safely without outlier corruption. |
| **One-Hot Encoding** | ✅ YES | Converts categorical strings to numbers; `handle_unknown="ignore"` prevents API crashes. |
| **Random Forest Baseline** | ✅ YES | Best model (96% accuracy, 0.952 F1, 0.994 ROC-AUC). Captures non-linear ratings. |
| **DVC & MLflow** | ✅ YES | DVC versions raw data and pipeline DAG; MLflow tracks metrics and registers models. |
| **Decoupled FastAPI + Streamlit** | ✅ YES | Streamlit UI does not load the ML model; it calls FastAPI over HTTP. |
| **Standard Scaling for RF** | ❌ NO | Decision trees split on ordering thresholds; scaling adds zero accuracy value. |
| **PCA Dimensionality Reduction**| ❌ NO | Destroys feature interpretability; 22 features is already small enough. |
| **Text Processing (TF-IDF)** | ❌ NO | Data contains numerical 1–5 ratings, not free text feedback. |
| **Feature Store (Feast)** | ❌ NO | Overkill for a single microservice; sklearn pipeline provides clean encapsulation. |
