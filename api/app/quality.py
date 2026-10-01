from .features import FEATURE_COLUMNS

def feature_completeness(row):
    present = sum(row.get(name) is not None for name in FEATURE_COLUMNS)
    return present / len(FEATURE_COLUMNS)

def prediction_allowed(row, threshold=0.90):
    return feature_completeness(row) >= threshold
