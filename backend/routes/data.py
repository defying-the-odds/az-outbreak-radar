# backend/routes/data.py

from fastapi import APIRouter
from backend.services.data_fetcher import fetch_cdc_data, fetch_mosquito_index, fetch_az_health_data

router = APIRouter()

@router.get("/api/realdata")
async def get_real_data():
    
    # Fetch from real sources
    cdc_data = fetch_cdc_data("AZ")
    az_health = fetch_az_health_data()

    return {
        "cdc_cases": cdc_data,
        "az_health": az_health,
        "status": "live"
    }

@router.get("/api/mosquito/{location}")
async def get_mosquito_index(location: str):
    
    # Get mosquito index for a specific location
    index = fetch_mosquito_index(location)
    
    return {
        "location": location,
        "mosquito_index": index
    }