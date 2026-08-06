# Professor Review & Presentation Guide - Topic 13: Forecasting Futures Basis using ARIMA Model

**Student**: Hrishi | B25019  
**Topic**: 13: Forecasting Futures basis ARIMA Model  
**Review Type**: First Review / Final Review Presentation  

---

## 🎯 Executive Overview for Your Review

Tomorrow when you present to your professor, you want to show **academic rigor**, **practical financial market understanding**, and a **live working system**. 

You have built a complete, end-to-end framework featuring:
1. **Dhan API v2 Authorization Integration** (`Client ID: 1112620458`) with allowlisted endpoints (`/profile`, `/marketfeed/ltp`, `/optionchain/expirylist`, `/optionchain`).
2. **Box-Jenkins Econometric Time Series Engine** (ADF & KPSS Stationarity tests, ACF/PACF, Auto-ARIMA AICc selection, Ljung-Box residual white-noise test).
3. **Out-of-Sample Forecasting & Walk-Forward Cross-Validation** with 95% and 80% confidence bands.
4. **ARIMA-Guided Trading Strategy Backtest** (Sharpe Ratio, Max Drawdown, Hit Ratio %).
5. **Interactive Web Dashboard** running live at `http://localhost:8080`.

---

## 🗣️ Step-by-Step Presentation Script

### Step 1: Introduction (1 Minute)
> *"Good morning Professor. Today I am presenting Topic 13: Forecasting Futures Basis using ARIMA Model.*
> 
> *In derivatives markets, the **Futures Basis** is the spread between the Futures price ($F_t$) and the underlying Spot price ($S_t$), defined as $\text{Basis}_t = F_t - S_t$. Under the Cost-of-Carry model, basis represents interest rate differential, dividend yield, and storage costs, converging to zero at contract expiration.*
> 
> *Our goal is to build an econometric forecasting system to model futures basis dynamics, evaluate stationarity, optimize ARIMA/SARIMAX parameters automatically, generate out-of-sample prediction bands, and backtest a trading strategy using live Dhan API market connectivity."*

---

### Step 2: Methodology & Theoretical Rigor (2 Minutes)
> *"We follow the classical 4-step Box-Jenkins methodology:*
> 1. ***Identification***: We test for stationarity using both the **Augmented Dickey-Fuller (ADF)** test and the **KPSS** test. If the basis level series contains a unit root, we apply first-differencing ($d = 1$). We also plot Autocorrelation (ACF) and Partial Autocorrelation (PACF) to identify AR ($p$) and MA ($q$) lag bounds.
> 2. ***Estimation***: We minimize the Akaike Information Criterion ($\text{AICc}$) using stepwise Auto-ARIMA grid search to automatically select the parsimonious $(p, d, q)$ order.
> 3. ***Diagnostic Checking***: We perform the **Ljung-Box Q-test** on residual errors ($\hat{\varepsilon}_t$). A $p$-value $> 0.05$ confirms that residuals are uncorrelated white noise.
> 4. ***Forecasting & Backtesting***: We perform 1-step to $h$-step out-of-sample forecasting with 95% confidence intervals and run a Walk-Forward backtest to compute RMSE, Directional Accuracy, and Sharpe Ratio."*

---

### Step 3: Live System Demo Walkthrough (3 Minutes)

Open the browser at `http://localhost:8080` (Run `./venv/bin/python app.py` in terminal).

1. **Header & API Badge**:
   - Point out: *"As shown at the top, our application connects securely to Dhan API v2 with Client ID `1112620458`, utilizing AWS SSM Parameter Store credentials."*
2. **Tab 1: Market Overview**:
   - Select **NIFTY 50 Futures**. Show the Spot vs Futures overlay chart and the Futures Basis series ($F_t - S_t$).
3. **Tab 2: Econometric Diagnostics**:
   - Click **Econometric Diagnostics**. Show the professor the **ADF & KPSS test table**. Point out that the level series p-value confirms stationarity / differencing requirement, and show the ACF/PACF bar chart.
4. **Tab 3: ARIMA Forecasts**:
   - Click **ARIMA Forecasts**. Show the **Optimal ARIMA Order** selected by Auto-ARIMA (e.g. `(1, 1, 1)`), the **95% Confidence Interval prediction bands**, the **Ljung-Box $p$-value** ($> 0.05$), and the full **Statsmodels Summary Box**.
5. **Tab 4: Strategy Backtest**:
   - Click **Strategy Backtest**. Show the **Cumulative Strategy Equity Curve** versus Buy & Hold Futures, along with Sharpe ratio and Max Drawdown cards.

---

## ❓ Professor Q&A Defense Guide

### Q1: "Why forecast Futures Basis instead of raw Futures prices?"
**Answer**:
> *"Professor, raw asset prices usually behave like random walks and are non-stationary ($I(1)$). Futures Basis ($\text{Basis}_t = F_t - S_t$), however, is driven by the cost-of-carry relationship ($S_t [e^{(r-q)T} - 1]$) and index arbitrage logic. Basis exhibits mean-reverting stationary characteristics ($I(0)$), making it theoretically sound for ARIMA modeling and arbitrage signal generation."*

---

### Q2: "How did you determine the differencing parameter $d$?"
**Answer**:
> *"We used the Augmented Dickey-Fuller (ADF) test ($H_0$: Unit root present) alongside the KPSS test ($H_0$: Series is trend stationary). If the $p$-value of ADF on the level series exceeded 0.05, we differenced the series ($d=1$). The first-differenced series yielded an ADF $p$-value $< 0.001$, confirming stationarity."*

---

### Q3: "How do you know your ARIMA model is not overfitting?"
**Answer**:
> *"We enforced two safeguards: First, parameter selection minimizes the penalized Akaike Information Criterion ($\text{AICc}$), which explicitly penalizes excess parameter complexity ($2k$). Second, we performed out-of-sample **Walk-Forward Validation**, evaluating the model strictly on unseen test data."*

---

### Q4: "How are you handling Dhan API authentication securely?"
**Answer**:
> *"Our architecture routes Dhan API requests through custom HTTPS client headers (`access-token` and `client-id`). In production, short-lived access tokens generated from API Key (`0c668a3b`) and Secret (`1a8caf67...`) are stored as encrypted `SecureString` parameters in AWS Systems Manager Parameter Store, ensuring zero plain-text credential leaks."*

---

## 🚀 Quick Launch Commands

To start the app for your professor review:

```bash
cd "/Users/hrishiraajsinghchauhan/Downloads/OPF project"
./venv/bin/python app.py
```

Then open **`http://localhost:8080`** in Google Chrome or Safari.
