from app.quality import feature_completeness, prediction_allowed

def test_quality_gate():
    row = {
        "rolling_vwap_deviation": 0.1,
        "spread_zscore": 1.2,
        "volume_ratio_20d": 2.0,
        "return_momentum": 0.01
    }
    assert feature_completeness(row) == 1.0
    assert prediction_allowed(row)

def test_incomplete_features_block_prediction():
    row = {
        "rolling_vwap_deviation": 0.1,
        "spread_zscore": None,
        "volume_ratio_20d": 2.0,
        "return_momentum": None
    }
    assert not prediction_allowed(row)
