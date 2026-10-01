from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import numpy as np
import pandas as pd
from .features import engineer_features, FEATURE_COLUMNS
from .model import AnomalyModel
from .quality import feature_completeness, prediction_allowed

app = FastAPI(title="FinSight Financial Intelligence API", version="1.0.0")
model = AnomalyModel()

class MarketRecord(BaseModel):
    symbol: str
    timestamp: datetime
    bid: float
    ask: float
    volume: float

class Feedback(BaseModel):
    alert_id: int
    label: str = Field(pattern="^(CONFIRMED|FALSE_POSITIVE)$")

@app.get("/health")
def health():
    return {"status": "ok", "model_version": model.version}

@app.post("/features")
def features(records: list[MarketRecord]):
    frame = pd.DataFrame([r.model_dump() for r in records])
    engineered = engineer_features(frame)
    return engineered[FEATURE_COLUMNS].replace({np.nan: None}).to_dict(orient="records")

@app.post("/predict")
def predict(records: list[MarketRecord]):
    frame = pd.DataFrame([r.model_dump() for r in records])
    engineered = engineer_features(frame)

    valid_rows = engineered[FEATURE_COLUMNS].notna().all(axis=1)
    if not valid_rows.any():
        return {"prediction_suppressed": True, "reason": "feature_completeness_below_90_percent"}

    X = engineered.loc[valid_rows, FEATURE_COLUMNS].fillna(0.0).to_numpy()

    if model.version is None:
        model.train(X, dataset_bytes=frame.to_json().encode())

    anomalies, scores = model.predict(X)
    results = []
    valid_indices = engineered.index[valid_rows]

    for idx, is_anomaly, score in zip(valid_indices, anomalies, scores):
        row = engineered.loc[idx, FEATURE_COLUMNS]
        results.append({
            "symbol": engineered.loc[idx, "symbol"],
            "timestamp": engineered.loc[idx, "timestamp"],
            "anomaly": bool(is_anomaly),
            "confidence": float(min(1.0, max(0.0, score))),
            "features": row.to_dict(),
            "explanation": model.explain(row.to_numpy())
        })

    return {
        "prediction_suppressed": False,
        "model_version": model.version,
        "alerts": results
    }

@app.post("/feedback")
def feedback(item: Feedback):
    return {"status": "accepted", "alert_id": item.alert_id, "label": item.label}

@app.get("/model")
def model_metadata():
    return {
        "version": model.version,
        "metrics": model.metrics,
        "feature_completeness_gate": 0.90
    }
