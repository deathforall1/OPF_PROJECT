"""
Flask Web Application Backend
Exposes REST API endpoints for Dhan API Integration, Econometrics Diagnostics,
ARIMA Forecasting, and Strategy Backtesting. Serves the interactive Web Dashboard UI.
"""

import os
from flask import Flask, jsonify, render_template, request
import pandas as pd
import numpy as np

from dhan_client import DhanClient
from data_loader import DataLoader
from analytics import TimeSeriesAnalytics
from arima_model import ARIMAForecaster
from strategy import TradingStrategyBacktest

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize Dhan Client with user credentials
dhan_client = DhanClient()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dhan_status', methods=['GET'])
def dhan_status():
    profile = dhan_client.get_profile()
    return jsonify(profile)

@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    asset = request.args.get('asset', 'NIFTY50')
    period = request.args.get('period', '1y')
    
    loader = DataLoader(asset_key=asset, period=period)
    df = loader.fetch_data()
    
    stats = {
        "spot": TimeSeriesAnalytics.descriptive_stats(df['Spot']),
        "futures": TimeSeriesAnalytics.descriptive_stats(df['Futures']),
        "basis": TimeSeriesAnalytics.descriptive_stats(df['Basis'])
    }
    
    dates = [str(d.date()) if hasattr(d, 'date') else str(d) for d in df.index]

    return jsonify({
        "asset": asset,
        "dates": dates,
        "spot": df['Spot'].tolist(),
        "futures": df['Futures'].tolist(),
        "basis": df['Basis'].tolist(),
        "basis_pct": df['Basis_Pct'].tolist(),
        "volume": df['Volume'].tolist(),
        "open_interest": df['Open_Interest'].tolist(),
        "stats": stats
    })

@app.route('/api/diagnostics', methods=['GET'])
def get_diagnostics():
    asset = request.args.get('asset', 'NIFTY50')
    target_col = request.args.get('target', 'Basis') # 'Futures', 'Basis', or 'Basis_Pct'
    
    loader = DataLoader(asset_key=asset, period='1y')
    df = loader.fetch_data()
    series = df[target_col].dropna()
    diff_series = series.diff().dropna()
    
    adf_level = TimeSeriesAnalytics.adf_test(series)
    adf_diff = TimeSeriesAnalytics.adf_test(diff_series)
    
    kpss_level = TimeSeriesAnalytics.kpss_test(series)
    kpss_diff = TimeSeriesAnalytics.kpss_test(diff_series)

    acf_pacf_level = TimeSeriesAnalytics.compute_acf_pacf(series, nlags=20)
    acf_pacf_diff = TimeSeriesAnalytics.compute_acf_pacf(diff_series, nlags=20)

    return jsonify({
        "target": target_col,
        "adf_level": adf_level,
        "adf_diff": adf_diff,
        "kpss_level": kpss_level,
        "kpss_diff": kpss_diff,
        "acf_pacf_level": acf_pacf_level,
        "acf_pacf_diff": acf_pacf_diff
    })

@app.route('/api/forecast', methods=['POST'])
def run_forecast():
    data = request.json or {}
    asset = data.get('asset', 'NIFTY50')
    target_col = data.get('target', 'Basis')
    auto_select = data.get('auto_select', True)
    p = int(data.get('p', 1))
    d = int(data.get('d', 1))
    q = int(data.get('q', 1))
    forecast_horizon = int(data.get('forecast_horizon', 15))

    loader = DataLoader(asset_key=asset, period='1y')
    df = loader.fetch_data()
    series = df[target_col].dropna()

    train_df, test_df = loader.get_train_test_split(df, test_ratio=0.15)
    train_series = train_df[target_col]
    test_series = test_df[target_col]

    forecaster = ARIMAForecaster(p=p, d=d, q=q, auto_select=auto_select)
    
    if auto_select:
        fit_info = forecaster.fit_auto(train_series)
    else:
        fit_info = forecaster.fit_manual(train_series)

    out_forecast = forecaster.predict(steps=forecast_horizon)
    residuals_info = forecaster.check_residuals()
    
    # Run Walk-Forward validation over test set
    wf_res = forecaster.walk_forward_validation(series, train_size_pct=0.85)

    return jsonify({
        "fit_info": fit_info,
        "summary": forecaster.model_summary_str,
        "out_forecast": out_forecast,
        "residuals": residuals_info,
        "walk_forward": wf_res,
        "train_dates": [str(x.date()) if hasattr(x, 'date') else str(x) for x in train_series.index],
        "train_values": train_series.tolist()
    })

@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    data = request.json or {}
    asset = data.get('asset', 'NIFTY50')
    
    loader = DataLoader(asset_key=asset, period='1y')
    df = loader.fetch_data()
    futures_series = df['Futures']
    
    forecaster = ARIMAForecaster(p=1, d=1, q=1, auto_select=True)
    wf_res = forecaster.walk_forward_validation(futures_series, train_size_pct=0.80)

    backtester = TradingStrategyBacktest()
    backtest_results = backtester.run_backtest(futures_series, wf_res['predicted'])

    return jsonify(backtest_results)

if __name__ == '__main__':
    os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
    app.run(host='127.0.0.1', port=8080, debug=True)
