"""
ARIMA, SARIMA, and ARIMAX Modeling & Forecasting Engine
Implements automated parameter selection (Auto-ARIMA), residual diagnostics (Ljung-Box),
multi-step ahead out-of-sample forecasting with confidence intervals, and rolling backtests.
"""

import numpy as np
import pandas as pd
import pmdarima as pm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import logging
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger("ARIMAEngine")

class ARIMAForecaster:
    def __init__(self, p: int = 1, d: int = 1, q: int = 1, auto_select: bool = True):
        self.p = p
        self.d = d
        self.q = q
        self.auto_select = auto_select
        self.fitted_model = None
        self.best_order = (p, d, q)
        self.best_seasonal_order = (0, 0, 0, 0)
        self.model_summary_str = ""

    def fit_auto(
        self,
        train_series: pd.Series,
        exog_train: Optional[pd.DataFrame] = None,
        seasonal: bool = False,
        m: int = 5
    ) -> Dict[str, Any]:
        """Uses Auto-ARIMA (AICc minimization) to find optimal (p, d, q) orders."""
        logger.info("Executing Auto-ARIMA grid search optimization...")
        try:
            auto_model = pm.auto_arima(
                y=train_series,
                X=exog_train,
                start_p=0, max_p=5,
                start_q=0, max_q=5,
                d=None, # auto test ADF for d
                seasonal=seasonal,
                m=m if seasonal else 1,
                trace=False,
                error_action='ignore',
                suppress_warnings=True,
                stepwise=True
            )
            self.best_order = auto_model.order
            self.best_seasonal_order = auto_model.seasonal_order
            self.p, self.d, self.q = self.best_order
            
            # Re-fit statsmodels ARIMA for uniform diagnostics & forecasting interface
            sm_model = ARIMA(
                endog=train_series,
                exog=exog_train,
                order=self.best_order,
                seasonal_order=self.best_seasonal_order if seasonal else (0,0,0,0)
            )
            self.fitted_model = sm_model.fit()
            self.model_summary_str = str(self.fitted_model.summary())
            
        except Exception as e:
            logger.warning(f"Auto-ARIMA failed ({e}). Falling back to manual ARIMA({self.p},{self.d},{self.q}).")
            self.fit_manual(train_series, exog_train)

        return {
            "order": self.best_order,
            "seasonal_order": self.best_seasonal_order,
            "aic": float(self.fitted_model.aic),
            "bic": float(self.fitted_model.bic),
            "hqic": float(getattr(self.fitted_model, 'hqic', 0.0))
        }

    def fit_manual(
        self,
        train_series: pd.Series,
        exog_train: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """Fits exact user-specified ARIMA(p,d,q) model."""
        sm_model = ARIMA(endog=train_series, exog=exog_train, order=(self.p, self.d, self.q))
        self.fitted_model = sm_model.fit()
        self.best_order = (self.p, self.d, self.q)
        self.model_summary_str = str(self.fitted_model.summary())

        return {
            "order": self.best_order,
            "aic": float(self.fitted_model.aic),
            "bic": float(self.fitted_model.bic)
        }

    def predict(
        self,
        steps: int = 15,
        exog_future: Optional[pd.DataFrame] = None
    ) -> Dict[str, Any]:
        """Generates multi-step out-of-sample forecasts with 80% and 95% confidence intervals."""
        if self.fitted_model is None:
            raise ValueError("Model must be fitted before predicting.")

        forecast_res = self.fitted_model.get_forecast(steps=steps, exog=exog_future)
        mean_forecast = forecast_res.predicted_mean
        conf_int_95 = forecast_res.conf_int(alpha=0.05)
        conf_int_80 = forecast_res.conf_int(alpha=0.20)

        # Handle indexing
        if isinstance(mean_forecast, pd.Series):
            forecast_values = mean_forecast.values
            dates = [str(d) for d in mean_forecast.index]
        else:
            forecast_values = np.array(mean_forecast)
            dates = [f"Step_{i+1}" for i in range(steps)]

        return {
            "dates": dates,
            "mean": forecast_values.tolist(),
            "ci_95_lower": conf_int_95.iloc[:, 0].values.tolist(),
            "ci_95_upper": conf_int_95.iloc[:, 1].values.tolist(),
            "ci_80_lower": conf_int_80.iloc[:, 0].values.tolist(),
            "ci_80_upper": conf_int_80.iloc[:, 1].values.tolist(),
        }

    def check_residuals(self) -> Dict[str, Any]:
        """Performs residual white-noise diagnostic checks (Ljung-Box test)."""
        if self.fitted_model is None:
            return {}

        residuals = self.fitted_model.resid
        lb_res = acorr_ljungbox(residuals, lags=[10], return_df=True)
        lb_stat = float(lb_res['lb_stat'].values[0])
        lb_p = float(lb_res['lb_pvalue'].values[0])
        is_white_noise = lb_p > 0.05

        return {
            "ljung_box_stat": lb_stat,
            "ljung_box_pvalue": lb_p,
            "is_white_noise": is_white_noise,
            "conclusion": "Residuals are white noise (No autocorrelation)" if is_white_noise else "Residuals exhibit serial correlation",
            "residual_mean": float(residuals.mean()),
            "residual_std": float(residuals.std())
        }

    def evaluate_forecast(
        self,
        actual: pd.Series,
        predicted: np.ndarray
    ) -> Dict[str, float]:
        """Calculates forecast accuracy metrics (RMSE, MAE, MAPE, Directional Accuracy)."""
        y_true = np.array(actual)
        y_pred = np.array(predicted)
        
        # Avoid division by zero in MAPE
        eps = 1e-8
        mape = float(np.mean(np.abs((y_true - y_pred) / (np.abs(y_true) + eps))) * 100)
        rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
        mae = float(mean_absolute_error(y_true, y_pred))

        # Directional Accuracy (Hit Ratio %)
        if len(y_true) > 1:
            diff_true = np.diff(y_true)
            diff_pred = np.diff(y_pred)
            directional_accuracy = float(np.mean((diff_true * diff_pred) > 0) * 100.0)
        else:
            directional_accuracy = 50.0

        return {
            "rmse": rmse,
            "mae": mae,
            "mape": mape,
            "directional_accuracy_pct": directional_accuracy
        }

    def walk_forward_validation(
        self,
        series: pd.Series,
        train_size_pct: float = 0.85
    ) -> Dict[str, Any]:
        """Executes 1-step ahead rolling Walk-Forward validation across test dataset."""
        n = len(series)
        train_size = int(n * train_size_pct)
        train_data = list(series.iloc[:train_size].values)
        test_data = list(series.iloc[train_size:].values)
        test_dates = list(series.index[train_size:])

        predictions = []

        for t in range(len(test_data)):
            try:
                model = ARIMA(train_data, order=self.best_order)
                model_fit = model.fit()
                yhat = float(model_fit.forecast()[0])
            except Exception:
                yhat = float(train_data[-1])
            
            predictions.append(yhat)
            train_data.append(test_data[t])

        metrics = self.evaluate_forecast(pd.Series(test_data), np.array(predictions))

        return {
            "dates": [str(d) for d in test_dates],
            "actual": test_data,
            "predicted": predictions,
            "metrics": metrics
        }

if __name__ == "__main__":
    series = pd.Series(np.cumsum(np.random.randn(100)) + 100)
    forecaster = ARIMAForecaster(auto_select=True)
    res = forecaster.fit_auto(series[:80])
    print("Auto-ARIMA Result:", res)
    pred = forecaster.predict(10)
    print("Forecast Mean:", pred["mean"])
    print("Residuals Check:", forecaster.check_residuals())
