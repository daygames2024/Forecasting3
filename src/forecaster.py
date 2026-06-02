
import warnings
import numpy as np
import pandas as pd

from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX


def _clean_series(y: pd.Series) -> pd.Series:
    y = pd.Series(y.copy())
    y = pd.to_numeric(y, errors="coerce")
    y = y.replace([np.inf, -np.inf], np.nan).fillna(0.0).astype(float)
    return y


def _forecast_index_from_global(global_last_q: pd.Period, horizon: int, freq: str = "Q-DEC"):
    return pd.period_range(start=global_last_q + 1, periods=horizon, freq=freq)


def select_and_forecast(series_q: pd.Series,
                        horizon: int,
                        seasonal_periods: int = 4,
                        global_last_q: pd.Period | None = None,
                        pad_to_global: bool = True):
    """
    Robust quarterly forecaster.

    Inputs:
      - series_q: pd.Series with PeriodIndex(freq='Q-DEC' or compatible), float values
      - horizon: number of future quarters
      - seasonal_periods: 4 for quarterly
      - global_last_q: if provided, ALL parts will forecast starting at global_last_q + 1
      - pad_to_global: if True and global_last_q provided, extend series with zeros up to global_last_q

    Returns:
      dict(method, index[List[str]], values[List[float]], score[float or None])
    """
    warnings.filterwarnings("ignore")

    if not isinstance(series_q.index, pd.PeriodIndex):
        raise ValueError("series_q must have a PeriodIndex (quarterly).")

    # Clean values
    y = _clean_series(series_q)
    # Align/pad to the same end quarter for all parts
    if global_last_q is not None:
        # Ensure the series has entries through the global last quarter
        if pad_to_global:
            start = y.index.min()
            full_idx = pd.period_range(start=start, end=global_last_q, freq=series_q.index.freqstr or "Q-DEC")
            y = y.reindex(full_idx, fill_value=0.0)
        # Build a unified forecast index starting at global_last_q + 1
        fc_index = _forecast_index_from_global(global_last_q, horizon, freq=series_q.index.freqstr or "Q-DEC")
    else:
        # Fall back to per-series last period if global not supplied
        last_period = y.index.max()
        fc_index = pd.period_range(start=last_period + 1, periods=horizon, freq=series_q.index.freqstr or "Q-DEC")

    n = len(y)

    def _result(method, values, score=None):
        values = np.asarray(values, dtype=float)
        values = np.clip(values, 0.0, None)  # demand can't be negative
        return {
            "method": method,
            "index": [str(p) for p in fc_index],
            "values": values.tolist(),
            "score": score,
        }

    if n == 0:
        return _result("empty_series", [0.0] * horizon)

    if float(y.sum()) == 0.0:
        return _result("all_zero_naive", [0.0] * horizon)

    # SHORT-SERIES FALLBACKS
    if n < 3:
        return _result("naive_last", [float(y.iloc[-1])] * horizon)

    if n < 6:
        try:
            model = SimpleExpSmoothing(y).fit()
            fc = model.forecast(horizon)
            return _result("SES", fc)
        except Exception:
            m = float(y.tail(min(3, n)).mean())
            return _result("rolling_mean_k3", [m] * horizon)

    if n < 8:
        try:
            model = ExponentialSmoothing(
                y, trend="add", seasonal=None, initialization_method="estimated"
            ).fit(optimized=True)
            fc = model.forecast(horizon)
            return _result("ETS_add_trend", fc)
        except Exception:
            try:
                model = SimpleExpSmoothing(y).fit()
                fc = model.forecast(horizon)
                return _result("SES_fallback", fc)
            except Exception:
                return _result("naive_last", [float(y.iloc[-1])] * horizon)

    # ADEQUATE HISTORY → seasonal ETS first
    try:
        model = ExponentialSmoothing(
            y, trend="add", seasonal="add",
            seasonal_periods=seasonal_periods,
            initialization_method="estimated",
        ).fit(optimized=True)
        fc = model.forecast(horizon)
        return _result("ETS_add_add", fc)
    except Exception:
        # Try a basic SARIMAX if ETS fails
        try:
            sarimax = SARIMAX(
                y,
                order=(0, 1, 1),
                seasonal_order=(0, 1, 1, seasonal_periods),
                enforce_stationarity=False,
                enforce_invertibility=False,
            ).fit(disp=False)
            fc = sarimax.forecast(horizon)
            return _result("SARIMAX_011_011m", fc)
        except Exception:
            m = float(y.tail(min(4, n)).mean())
            return _result("rolling_mean_k4", [m] * horizon)
