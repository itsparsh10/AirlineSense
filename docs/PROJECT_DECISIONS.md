# Project decisions

## Dataset and target

**Problem:** The product needs a credible classification target with enough examples for evaluation.

**Alternatives:** Create synthetic data, use a smaller sample, or use the supplied public dataset.

**Decision:** Use all 129,880 supplied passenger records and predict the supplied `Satisfaction` label.

**Evidence:** The target has two valid classes with a 56.5%/43.5% split. The dataset has no duplicates and only 393 missing arrival-delay values.

## Leakage prevention

**Problem:** Preprocessing on the full dataset would leak test information into model selection.

**Alternatives:** Clean everything before splitting, or place learned preprocessing inside a pipeline.

**Decision:** Split with stratification first. Fit imputation, encoding, and model steps inside sklearn pipelines and cross-validation folds. Drop the unique ID.

**Reason:** This preserves an untouched test set and keeps training and inference behavior identical.

## Encoding and imputation

**Problem:** Four categorical variables require encoding, and arrival delay contains missing values.

**Alternatives:** Ordinal-encode nominal categories, delete incomplete rows, fill a global constant, or learn transformations from training data.

**Decision:** One-hot encode with unknown-category tolerance and median-impute numeric values inside the pipeline.

**Reason:** Categories have no reliable order. Median imputation is robust to the long-tailed delay distribution and preserves all 393 affected records.

## Scaling

**Problem:** Logistic Regression is scale-sensitive while Random Forest is not.

**Decision:** Standardize numeric features only in the Logistic Regression pipeline. Leave Random Forest values unscaled.

**Reason:** Tree splits depend on order and thresholds, so scaling adds no benefit to the forest.

## Feature engineering

**Problem:** The course expects meaningful feature engineering, but extra features should earn their place.

**Decision:** Test total delay, service average, digital experience average, delay per 1,000 miles, and a delay flag in a separate Random Forest experiment.

**Evidence:** Engineered CV F1 was 0.951 versus 0.952 for the baseline forest. The final pipeline therefore uses the simpler baseline. The feature code and DVC stage remain as an auditable experiment.

## Production model

**Alternatives:** Logistic Regression, baseline Random Forest, engineered Random Forest.

**Decision:** Baseline Random Forest with 120 trees, maximum depth 16, and minimum leaf size 2.

**Evidence:** It led cross-validation on F1 and ROC-AUC, then achieved 0.954 F1 and 0.994 ROC-AUC on the untouched test set.

## MLflow

**Decision:** Use a local SQLite backend and local artifacts.

**Reason:** It supports run comparison and the Model Registry without adding cloud credentials or infrastructure to the classroom demo. The selected pipeline is registered as `AirlineSenseClassifier` version 1.

## DVC

**Decision:** Track the raw CSV and the prepare, feature, train, and evaluate stages. Use a local DVC remote for the live demonstration.

**Reason:** This shows data and pipeline versioning while staying reliable offline. A shared remote is the next step for team use.

## API and UI

**Decision:** FastAPI owns prediction and Streamlit calls it over HTTP.

**Reason:** It proves the model runs behind a real service. Streamlit never imports or loads the model, so UI and inference responsibilities stay separate.

## Docker and CI/CD

**Decision:** Package both services in one classroom-friendly container. Use separate GitHub workflows for tests and Docker Hub publishing.

**Reason:** One image keeps the live demo simple. GitHub Actions still proves the image can be built and published independently of the laptop.

## Deployment

**Decision:** Keep cloud deployment as optional work.

**Reason:** The assignment marks cloud as a bonus. A complete local chain, tested Docker image, and correct CI/CD workflow provide more value than an unstable last-minute cloud deployment.

