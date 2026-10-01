import pandas as pd
import numpy as np

FEATURE_COLUMNS = [
    "rolling_vwap_deviation",
    "spread_zscore",
    "volume_ratio_20d",
    "return_momentum",
]

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy().sort_values(["symbol", "timestamp"])
    grouped = out.groupby("symbol", group_keys=False)

    out["typical_price"] = (out["bid"] + out["ask"]) / 2
    out["dollar_volume"] = out["typical_price"] * out["volume"]

    out["rolling_vwap"] = grouped["dollar_volume"].transform(
        lambda s: s.rolling(20, min_periods=1).sum()
    ) / grouped["volume"].transform(
        lambda s: s.rolling(20, min_periods=1).sum()
    )

    out["rolling_vwap_deviation"] = (
        out["typical_price"] - out["rolling_vwap"]
    ) / out["rolling_vwap"].replace(0, np.nan)

    spread = out["ask"] - out["bid"]
    spread_mean = grouped[spread.name if hasattr(spread, "name") else "ask"].transform("mean")
    spread_std = grouped[spread.name if hasattr(spread, "name") else "ask"].transform("std")

    # Direct spread statistics are used to avoid depending on a temporary Series name.
    out["spread"] = spread
    out["spread_mean"] = grouped["spread"].transform("mean")
    out["spread_std"] = grouped["spread"].transform("std").replace(0, np.nan)
    out["spread_zscore"] = (out["spread"] - out["spread_mean"]) / out["spread_std"]

    out["volume_avg_20d"] = grouped["volume"].transform(
        lambda s: s.rolling(20, min_periods=1).mean()
    )
    out["volume_ratio_20d"] = out["volume"] / out["volume_avg_20d"].replace(0, np.nan)

    out["return"] = grouped["typical_price"].pct_change()
    out["return_momentum"] = grouped["return"].transform(
        lambda s: s.rolling(5, min_periods=1).mean()
    )

    return out.replace([np.inf, -np.inf], np.nan)
