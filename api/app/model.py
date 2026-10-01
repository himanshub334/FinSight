import hashlib
import json
from pathlib import Path
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_recall_curve, average_precision_score
from .features import FEATURE_COLUMNS

class AnomalyModel:
    def __init__(self, contamination=0.02, random_state=42):
        self.model = IsolationForest(
            n_estimators=200,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.version = None
        self.metrics = {}

    def train(self, X, y=None, dataset_bytes=b"demo"):
        self.model.fit(X)
        self.version = "model-" + hashlib.sha256(dataset_bytes).hexdigest()[:12]

        if y is not None:
            scores = -self.model.decision_function(X)
            precision, recall, _ = precision_recall_curve(y, scores)
            self.metrics["average_precision"] = float(average_precision_score(y, scores))
            self.metrics["precision_points"] = precision.tolist()
            self.metrics["recall_points"] = recall.tolist()

        return self.version

    def predict(self, X):
        raw = -self.model.decision_function(X)
        labels = self.model.predict(X)
        return labels == -1, raw

    def explain(self, row):
        # Model-agnostic local contribution approximation.
        # Production can swap this adapter for SHAP TreeExplainer.
        values = row.astype(float)
        total = np.abs(values).sum() or 1.0
        return {
            FEATURE_COLUMNS[i]: float(values[i] / total)
            for i in range(len(FEATURE_COLUMNS))
        }
