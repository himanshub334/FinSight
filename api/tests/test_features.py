import pandas as pd
from app.features import engineer_features, FEATURE_COLUMNS

def test_feature_engineering():
    rows = []
    for i in range(25):
        rows.append({
            "symbol": "AAPL",
            "timestamp": f"2026-01-{1 + i:02d}T10:00:00",
            "bid": 100 + i * 0.1,
            "ask": 100.1 + i * 0.1,
            "volume": 1000 + i * 10
        })
    out = engineer_features(pd.DataFrame(rows))
    assert all(col in out.columns for col in FEATURE_COLUMNS)
    assert len(out) == 25
