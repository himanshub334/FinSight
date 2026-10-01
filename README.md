# FinSight — Financial Intelligence & Anomaly Detection Platform

A production-style financial anomaly detection platform combining statistical detection, machine learning, explainability, model versioning, data-quality gates, and human feedback.

## Architecture

```text
Market Data
    |
    v
Feature Engineering (pandas/numpy)
    |
    +--> Data Quality Gate (>=90% complete)
    |
    v
Isolation Forest + Z-score Ensemble
    |
    +--> SHAP-style feature contribution report
    |
    v
FastAPI
    |
    v
PostgreSQL <---- feedback / model metadata
    |
    v
React Dashboard
```

## Stack
Python, scikit-learn, pandas, NumPy, FastAPI, PostgreSQL, React, Docker, AWS Lambda-ready, GitHub Actions.

## Features
- Rolling VWAP deviation
- Bid/ask spread z-score
- Volume / 20-day average
- Intraday return momentum
- Isolation Forest anomaly model
- Statistical z-score ensemble
- Precision/recall evaluation
- Feedback: confirmed / false-positive
- Model version metadata
- Dataset SHA-256 hash
- Feature completeness gate
- Explainability payload
- Historical alert accuracy
- REST API + Swagger
- React dashboard
- Docker and CI

## Run

```bash
docker compose up --build
```

API: http://localhost:8000/docs  
Dashboard: http://localhost:5173

The included data is synthetic/demo data. Benchmark and model metrics should be regenerated against a real, reproducible dataset before being presented as measured results.
# FinSight
