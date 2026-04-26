# backend/routes/community.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/api/community")
async def get_community_risk():
    
    # Mock community data for now
    # Person 3 will replace this later
    return {
        "community_risk_score": 0.65,
        "trend": "increasing",
        "total_reports": 142,
        "hotspots": [
            {"region": "Phoenix", "risk": 0.8},
            {"region": "Tucson", "risk": 0.6},
            {"region": "Mesa", "risk": 0.7},
            {"region": "Scottsdale", "risk": 0.75},
            {"region": "Flagstaff", "risk": 0.3}
        ],
        "insight": "Phoenix and Mesa showing elevated risk this week.",
        "recommended_action": "Avoid crowded areas in high risk regions."
    }