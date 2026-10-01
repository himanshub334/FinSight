# ML Design

## Ensemble
The platform combines:
1. Isolation Forest for unsupervised multivariate anomaly detection.
2. Statistical z-score features for interpretable univariate signals.

The API returns feature contributions alongside the model score.

## Evaluation
Use precision-recall curves because anomaly datasets are usually imbalanced and false positives can be expensive.

The included model stores:
- dataset SHA-256 hash
- hyperparameters
- evaluation metrics
- model version

## Explainability
The demo contains a model-agnostic local contribution adapter. For production, replace it with SHAP's `TreeExplainer` for the trained Isolation Forest and persist the exact SHAP values returned for each alert.

## Data quality
Predictions are suppressed when fewer than 90% of required features are available.
