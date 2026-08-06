"""
Time Series Econometrics & Stationarity Diagnostics Component
Performs Augmented Dickey-Fuller (ADF), KPSS, ACF, PACF, and Descriptive Statistical tests.
"""

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from scipy.stats import jarque_bera, skew, kurtosis
from typing import Dict, Any, List

class TimeSeriesAnalytics:
    @staticmethod
    def adf_test(series: pd.Series) -> Dict[str, Any]:
        """
        Augmented Dickey-Fuller test for stationarity.
        H0: The series has a unit root (Non-Stationary).
        H1: The series is Stationary.
        """
        clean_series = series.dropna()
        result = adfuller(clean_series, autolag='AIC')
        p_val = float(result[1])
        is_stationary = p_val < 0.05
        
        return {
            "test_name": "Augmented Dickey-Fuller (ADF)",
            "adf_statistic": float(result[0]),
            "p_value": p_val,
            "used_lags": int(result[2]),
            "n_obs": int(result[3]),
            "critical_values": {k: float(v) for k, v in result[4].items()},
            "is_stationary": is_stationary,
            "conclusion": "Stationary (Reject H0 at 5% alpha)" if is_stationary else "Non-Stationary (Fail to reject H0)"
        }

    @staticmethod
    def kpss_test(series: pd.Series) -> Dict[str, Any]:
        """
        Kwiatkowski-Phillips-Schmidt-Shin test for stationarity.
        H0: The process is trend stationary.
        H1: The series has a unit root.
        """
        clean_series = series.dropna()
        try:
            stat, p_val, lags, crit = kpss(clean_series, regression='c', nlags="auto")
            p_val = float(p_val)
            is_stationary = p_val >= 0.05
            return {
                "test_name": "KPSS Test",
                "kpss_statistic": float(stat),
                "p_value": p_val,
                "used_lags": int(lags),
                "critical_values": {k: float(v) for k, v in crit.items()},
                "is_stationary": is_stationary,
                "conclusion": "Stationary (Fail to reject H0)" if is_stationary else "Non-Stationary (Reject H0)"
            }
        except Exception as e:
            return {"test_name": "KPSS Test", "error": str(e)}

    @staticmethod
    def compute_acf_pacf(series: pd.Series, nlags: int = 20) -> Dict[str, Any]:
        """Computes Autocorrelation (ACF) and Partial Autocorrelation (PACF) up to nlags."""
        clean_series = series.dropna()
        max_lags = min(nlags, len(clean_series) // 2 - 1)
        
        acf_vals, acf_confint = acf(clean_series, nlags=max_lags, alpha=0.05)
        pacf_vals, pacf_confint = pacf(clean_series, nlags=max_lags, alpha=0.05)

        lags = list(range(max_lags + 1))
        
        return {
            "lags": lags,
            "acf": acf_vals.tolist(),
            "acf_ci_lower": (acf_confint[:, 0] - acf_vals).tolist(),
            "acf_ci_upper": (acf_confint[:, 1] - acf_vals).tolist(),
            "pacf": pacf_vals.tolist(),
            "pacf_ci_lower": (pacf_confint[:, 0] - pacf_vals).tolist(),
            "pacf_ci_upper": (pacf_confint[:, 1] - pacf_vals).tolist()
        }

    @staticmethod
    def descriptive_stats(series: pd.Series) -> Dict[str, Any]:
        """Calculates statistical moments and Jarque-Bera normality test."""
        clean_series = series.dropna()
        jb_stat, jb_p = jarque_bera(clean_series)

        return {
            "count": int(clean_series.count()),
            "mean": float(clean_series.mean()),
            "std": float(clean_series.std()),
            "min": float(clean_series.min()),
            "quantile_25": float(clean_series.quantile(0.25)),
            "median": float(clean_series.median()),
            "quantile_75": float(clean_series.quantile(0.75)),
            "max": float(clean_series.max()),
            "skewness": float(skew(clean_series)),
            "kurtosis": float(kurtosis(clean_series)),
            "jarque_bera_stat": float(jb_stat),
            "jarque_bera_p": float(jb_p),
            "is_normal": float(jb_p) > 0.05
        }

if __name__ == "__main__":
    s = pd.Series(np.random.randn(100))
    print("ADF:", TimeSeriesAnalytics.adf_test(s))
    print("Stats:", TimeSeriesAnalytics.descriptive_stats(s))
