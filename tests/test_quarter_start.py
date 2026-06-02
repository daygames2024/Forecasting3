
import pandas as pd
from forecaster import select_and_forecast

def test_forecast_starts_next_quarter():
    # Build a tiny quarterly series ending at 2025Q4
    idx = pd.period_range("2025Q1", "2025Q4", freq="Q")
    series_q = pd.Series([10, 12, 9, 11], index=idx)

    fc = select_and_forecast(series_q, horizon=6, seasonal_periods=4)
    # First forecast quarter must be 2026Q1
    assert fc["index"][0] == "2026Q1"
    assert len(fc["index"]) == 6
    assert len(fc["values"]) == 6

