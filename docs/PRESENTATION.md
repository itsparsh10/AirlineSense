# 5–7 minute presentation

## Slide 1 — AirlineSense

Predict passenger satisfaction before the complaint.

Explain the practical use: prioritize proactive service recovery using information already captured in a passenger survey or service workflow.

## Slide 2 — The decision problem

129,880 passenger records combine journey context with service ratings. The goal is a binary satisfaction prediction that an operational team can use consistently.

## Slide 3 — Data and leakage control

Show the class split, the 393 missing arrival delays, the unique ID removal, and the stratified 80/20 split. Emphasize that every learned transformation fits only on training folds.

## Slide 4 — Experiments and model choice

Compare Logistic Regression, baseline Random Forest, and engineered Random Forest. Explain why the baseline forest won and why scaling applies only to Logistic Regression.

## Slide 5 — Test-set evidence

Present 96.0% accuracy, 95.4% F1, 94.7% recall, and 0.994 ROC-AUC. Keep the test set untouched until the final model selection was complete.

## Slide 6 — Product architecture

Show Streamlit calling FastAPI, which loads the saved pipeline. Training uses DVC stages and MLflow runs. Docker packages the product, and GitHub Actions builds and publishes the image.

## Slide 7 — Live demo

Use the real UI. Change weak service inputs to show a lower probability. If the live app fails, use the verified screenshot.

## Slide 8 — What this proves

The product runs from versioned data through a registered model to a tested API and UI. The main remaining work is account setup for GitHub and Docker Hub publishing, plus optional cloud hosting.

