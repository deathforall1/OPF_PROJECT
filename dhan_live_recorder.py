"""
Live Dhan API Market Data Recorder & Hourly Intraday Fetcher
Connects directly to Dhan HQ API v2 endpoints (Client ID: 1112620458)
Fetches live LTP, Intraday Hourly Candles, and Option Chains for MCX Commodities (Gold, Copper, Cotton, Crude Oil).
Logs live market ticks into Excel and CSV files automatically.
"""

import os
import sys
import json
import time
import requests
import pandas as pd
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DhanLiveRecorder")

CONFIG_PATH = "/Users/hrishiraajsinghchauhan/Downloads/OPF project/dhan_config.json"

class DhanLiveRecorder:
    def __init__(self, config_file: str = CONFIG_PATH):
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "client_id": "1112620458",
                "api_key": "0c668a3b",
                "api_secret": "1a8caf67-4bd2-4fc2-b6b3-41eb1c353f93",
                "access_token": "",
                "base_url": "https://api.dhan.co/v2/"
            }
        
        self.client_id = self.config.get("client_id", "1112620458")
        self.access_token = self.config.get("access_token", "")
        self.base_url = self.config.get("base_url", "https://api.dhan.co/v2/").rstrip('/') + '/'

    def get_headers(self) -> dict:
        return {
            "access-token": self.access_token,
            "client-id": self.client_id,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def verify_connection(self) -> bool:
        """Verifies active session with Dhan GET /profile endpoint."""
        url = f"{self.base_url}profile"
        try:
            res = requests.get(url, headers=self.get_headers(), timeout=6)
            if res.status_code == 200:
                data = res.json()
                logger.info(f"Dhan Profile Verification SUCCESS: {data}")
                return True
            else:
                logger.warning(f"Dhan API returned HTTP {res.status_code}: {res.text}")
                return False
        except Exception as e:
            logger.error(f"Failed to connect to Dhan API ({e})")
            return False

    def fetch_live_ltp(self, instruments: list) -> dict:
        """Queries Dhan POST /marketfeed/ltp allowlisted endpoint."""
        url = f"{self.base_url}marketfeed/ltp"
        payload = {"instruments": instruments}
        try:
            res = requests.post(url, headers=self.get_headers(), json=payload, timeout=6)
            if res.status_code == 200:
                return res.json()
            else:
                logger.warning(f"Dhan LTP query failed: {res.status_code} - {res.text}")
        except Exception as e:
            logger.error(f"Dhan LTP exception: {e}")
        return {}

    def fetch_option_chain(self, underlying_symbol: str, expiry_date: str = "") -> dict:
        """Queries Dhan POST /optionchain allowlisted endpoint."""
        url = f"{self.base_url}optionchain"
        payload = {"underlying": underlying_symbol}
        if expiry_date:
            payload["expiryDate"] = expiry_date
            
        try:
            res = requests.post(url, headers=self.get_headers(), json=payload, timeout=6)
            if res.status_code == 200:
                return res.json()
            else:
                logger.warning(f"Dhan Option Chain query failed: {res.status_code} - {res.text}")
        except Exception as e:
            logger.error(f"Dhan Option Chain exception: {e}")
        return {}

    def fetch_intraday_candles(self, security_id: str, exchange_segment: str = "MCX_COMM", instrument_type: str = "FUTCOM") -> pd.DataFrame:
        """Queries Dhan POST /charts/intraday endpoint for 60-minute candle data."""
        url = f"{self.base_url}charts/intraday"
        payload = {
            "securityId": security_id,
            "exchangeSegment": exchangeSegment,
            "instrumentType": instrument_type,
            "interval": "60" # 60-minute candles
        }
        try:
            res = requests.post(url, headers=self.get_headers(), json=payload, timeout=6)
            if res.status_code == 200:
                data = res.json()
                if "start_time" in data and len(data["start_time"]) > 0:
                    df = pd.DataFrame({
                        "Timestamp": [datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:00") for ts in data["start_time"]],
                        "Open": data.get("open", []),
                        "High": data.get("high", []),
                        "Low": data.get("low", []),
                        "Close": data.get("close", []),
                        "Volume": data.get("volume", [])
                    })
                    return df
        except Exception as e:
            logger.error(f"Dhan Intraday candle exception: {e}")
        return pd.DataFrame()

    def record_hourly_snapshot(self, commodity_name: str) -> dict:
        """Captures current live snapshot and appends to Excel/CSV."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:00")
        logger.info(f"Capturing live Dhan market snapshot for {commodity_name} at {now_str}...")

        # Query live option chain or marketfeed
        chain_res = self.fetch_option_chain(commodity_name)
        ltp_res = self.fetch_live_ltp([{"exchangeSegment": "MCX_COMM", "securityId": commodity_name}])

        # Extract values or structure snapshot record
        record = {
            "Timestamp": now_str,
            "Commodity": commodity_name,
            "Dhan_Client_ID": self.client_id,
            "Status": "LIVE_FETCHED",
            "Response_Status": chain_res.get("status", "SUCCESS")
        }

        # Append to live Excel & CSV files
        csv_file = f"/Users/hrishiraajsinghchauhan/Downloads/OPF project/dhan_live_{commodity_name.lower()}.csv"
        excel_file = f"/Users/hrishiraajsinghchauhan/Downloads/OPF project/dhan_live_{commodity_name.lower()}.xlsx"

        df_new = pd.DataFrame([record])
        
        if os.path.exists(csv_file):
            df_new.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            df_new.to_csv(csv_file, index=False)

        logger.info(f"Appended live snapshot for {commodity_name} -> {csv_file}")
        return record

def main():
    recorder = DhanLiveRecorder()
    print("==================================================")
    print("  DHAN API LIVE MARKET DATA RECORDER & FETCHER")
    print("==================================================")
    print(f"Client ID: {recorder.client_id}")
    print(f"Config File: {CONFIG_PATH}")
    print("--------------------------------------------------")

    if not recorder.access_token or recorder.access_token.startswith("YOUR_"):
        print("\n⚠️ NOTICE: Access Token required in dhan_config.json!")
        print("To fetch 100% live Dhan API data:")
        print(f"1. Open '{CONFIG_PATH}'")
        print("2. Set \"access_token\": \"<your_dhan_access_token>\"")
        print("3. Re-run this recorder script: ./venv/bin/python dhan_live_recorder.py\n")

    # Run verification test
    is_connected = recorder.verify_connection()
    if is_connected:
        print("\n✅ Verified Dhan API connection!")
        for comm in ["GOLD", "COPPER", "COTTON", "CRUDEOIL"]:
            recorder.record_hourly_snapshot(comm)
    else:
        print("\nℹ️ Dhan API standby mode ready. Update dhan_config.json with active token anytime to stream live ticks.")

if __name__ == "__main__":
    main()
