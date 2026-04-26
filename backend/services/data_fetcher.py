# backend/services/data_fetcher.py

import requests

def fetch_cdc_data(state="AZ"):
    try:
        url = "https://data.cdc.gov/resource/9mfq-cb36.json"
        response = requests.get(url, params={"state": state, "$limit": 100})
        return response.json()
    except Exception as e:
        print(f"CDC fetch error: {e}")
        return []

def fetch_mosquito_index(location: str) -> float:
    try:
        # Mock mosquito index by location for now
        mosquito_data = {
            "phoenix": 0.8,
            "tucson": 0.6,
            "flagstaff": 0.3,
            "mesa": 0.7,
            "scottsdale": 0.75
        }
        return mosquito_data.get(location.lower(), 0.5)
    except Exception as e:
        print(f"Mosquito fetch error: {e}")
        return 0.5

def fetch_az_health_data():
    try:
        # Placeholder for AZ Dept of Health data
        return {
            "active_alerts": [],
            "outbreak_regions": [],
            "last_updated": "2026-04-25"
        }
    except Exception as e:
        print(f"AZ health fetch error: {e}")
        return {}