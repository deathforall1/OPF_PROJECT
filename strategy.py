"""
ARIMA-Guided Trading Strategy Backtesting Engine
Evaluates quantitative signals, portfolio performance, cumulative returns,
Sharpe ratio, and maximum drawdown versus Buy & Hold benchmarks.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any

class TradingStrategyBacktest:
    def __init__(self, risk_free_rate: float = 0.06):
        self.risk_free_rate = risk_free_rate

    def run_backtest(
        self,
        actual_prices: pd.Series,
        forecasted_prices: list
    ) -> Dict[str, Any]:
        """
        Backtests an ARIMA signal strategy:
        Position = +1 if forecasted price > current price else -1
        """
        n = len(forecasted_prices)
        if n == 0 or len(actual_prices) < n + 1:
            return {"error": "Insufficient data for backtesting."}

        price_series = actual_prices.iloc[-n-1:].values
        dates = [str(d) for d in actual_prices.iloc[-n:].index]
        
        returns = np.diff(price_series) / price_series[:-1]
        
        # Signal generation
        signals = []
        for i in range(n):
            current_price = price_series[i]
            predicted_next = forecasted_prices[i]
            if predicted_next > current_price:
                signals.append(1)  # Long
            else:
                signals.append(-1) # Short/Flat

        signals = np.array(signals)
        strategy_returns = signals * returns
        
        cum_benchmark = np.cumprod(1 + returns) - 1.0
        cum_strategy = np.cumprod(1 + strategy_returns) - 1.0

        # Performance Metrics
        total_strategy_return = float(cum_strategy[-1] * 100.0)
        total_benchmark_return = float(cum_benchmark[-1] * 100.0)

        # Sharpe ratio
        daily_rf = self.risk_free_rate / 252.0
        excess_returns = strategy_returns - daily_rf
        sharpe_ratio = float((np.mean(excess_returns) / (np.std(excess_returns) + 1e-8)) * np.sqrt(252))

        # Max Drawdown
        cum_equity = np.cumprod(1 + strategy_returns)
        running_max = np.maximum.accumulate(cum_equity)
        drawdowns = (cum_equity - running_max) / running_max
        max_drawdown_pct = float(np.min(drawdowns) * 100.0)

        # Win Rate
        winning_trades = np.sum(strategy_returns > 0)
        total_trades = np.sum(signals != 0)
        win_rate_pct = float((winning_trades / total_trades) * 100.0) if total_trades > 0 else 0.0

        return {
            "dates": dates,
            "benchmark_returns_pct": (cum_benchmark * 100.0).tolist(),
            "strategy_returns_pct": (cum_strategy * 100.0).tolist(),
            "metrics": {
                "total_strategy_return_pct": total_strategy_return,
                "total_benchmark_return_pct": total_benchmark_return,
                "sharpe_ratio": sharpe_ratio,
                "max_drawdown_pct": max_drawdown_pct,
                "win_rate_pct": win_rate_pct,
                "annualized_alpha_pct": float(total_strategy_return - total_benchmark_return)
            }
        }

if __name__ == "__main__":
    prices = pd.Series(100 + np.cumsum(np.random.randn(50)))
    forecasts = prices.values[1:] + np.random.randn(49)*0.5
    backtester = TradingStrategyBacktest()
    res = backtester.run_backtest(prices, forecasts.tolist())
    print("Strategy Backtest Metrics:", res["metrics"])
