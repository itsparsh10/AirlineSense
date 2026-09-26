# Likely instructor questions

## Why Random Forest?

It captured nonlinear interactions between service ratings and journey context. It improved cross-validated F1 from 0.850 for Logistic Regression to 0.952 while remaining fast enough for the API.

## Why did you avoid scaling for Random Forest?

Tree splits depend on ordering and thresholds, not distance. Scaling would change units without improving those splits. Logistic Regression uses scaling because its optimization and coefficients are scale-sensitive.

## How did you prevent leakage?

I created the train/test split before fitting transformations. Imputation and one-hot encoding live inside the sklearn pipeline, so each cross-validation fold learns them only from its training portion. I also removed the unique passenger ID.

## Why median imputation?

Arrival delays are strongly right-skewed. The median is less affected by rare extreme delays than the mean, and it keeps the 393 incomplete rows.

## Why did the engineered model lose?

Random Forest already learns interactions from the original service and delay variables. The grouped averages compressed some useful detail and produced a slightly lower CV F1. I kept the experiment but did not promote it.

## What does 0.994 ROC-AUC mean?

Across decision thresholds, the model ranks satisfied passengers above dissatisfied passengers very reliably. It does not mean every probability is perfectly calibrated.

## Why use both DVC and MLflow?

DVC versions the dataset and execution stages. MLflow records model runs, parameters, metrics, artifacts, and the selected registered model. They answer different reproducibility questions.

## Does Streamlit load the model?

No. Streamlit sends JSON to FastAPI. FastAPI owns the saved pipeline, validation, prediction, and response contract.

## What would you improve next?

I would tune the classification threshold using the cost of missed dissatisfied passengers, monitor drift by route and cabin, add probability calibration, and deploy the verified image to a small cloud service.

