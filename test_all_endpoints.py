import json
from app import app

def test_system():
    client = app.test_client()
    
    print("--- 1. Testing Dhan Status Endpoint ---")
    r1 = client.get('/api/dhan_status')
    print("Status:", r1.status_code, "Response:", r1.get_json())
    
    print("\n--- 2. Testing Dataset Endpoint ---")
    r2 = client.get('/api/dataset?asset=NIFTY50')
    data2 = r2.get_json()
    print("Status:", r2.status_code, "Asset:", data2.get("asset"), "Dates count:", len(data2.get("dates", [])))
    
    print("\n--- 3. Testing Diagnostics Endpoint ---")
    r3 = client.get('/api/diagnostics?asset=NIFTY50&target=Basis')
    data3 = r3.get_json()
    print("Status:", r3.status_code, "ADF level p-value:", data3["adf_level"]["p_value"])
    
    print("\n--- 4. Testing Forecast Endpoint ---")
    r4 = client.post('/api/forecast', json={"asset": "NIFTY50", "target": "Basis", "auto_select": True, "forecast_horizon": 10})
    data4 = r4.get_json()
    print("Status:", r4.status_code, "Fitted ARIMA Order:", data4["fit_info"]["order"], "Forecast Mean:", data4["out_forecast"]["mean"][:3])
    
    print("\n--- 5. Testing Strategy Backtest Endpoint ---")
    r5 = client.post('/api/backtest', json={"asset": "NIFTY50"})
    data5 = r5.get_json()
    print("Status:", r5.status_code, "Metrics:", data5["metrics"])

if __name__ == "__main__":
    test_system()
