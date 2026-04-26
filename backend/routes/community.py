# backend/routes/community.py

from fastapi import APIRouter

router = APIRouter()

# ZIP code to region mapping for Arizona
ZIP_TO_REGION = {
    # Phoenix
    "850": "Phoenix",
    "851": "Phoenix",
    "852": "Phoenix",
    "853": "Phoenix",
    "854": "Phoenix",
    "855": "Phoenix",
    "856": "Phoenix",
    "857": "Phoenix",
    "858": "Phoenix",
    "859": "Phoenix",

    # Tucson
    "857": "Tucson",
    "858": "Tucson",
    "859": "Tucson",
    "860": "Tucson",

    # Flagstaff
    "860": "Flagstaff",
    "861": "Flagstaff",
    "862": "Flagstaff",

    # Mesa
    "852": "Mesa",
    "853": "Mesa",

    # Scottsdale
    "852": "Scottsdale",
    "853": "Scottsdale",
}

def get_region_from_zip(zip_code: str) -> str:
    """
    Maps Arizona ZIP code to a region name.
    Uses first 3 digits to match region.
    """
    if not zip_code:
        return "Unknown"
    
    prefix = zip_code[:3]
    return ZIP_TO_REGION.get(prefix, "Other Arizona")


@router.get("/api/community")
async def get_community_risk():
    # Mock community data for now
    # Person 3 will replace this with real aggregation
    return {
        "community_risk_score": 0.65,
        "trend": "increasing",
        "total_reports": 142,
        "hotspots": [
            {"region": "Phoenix",   "risk": 0.8, "reports": 58},
            {"region": "Tucson",    "risk": 0.6, "reports": 34},
            {"region": "Mesa",      "risk": 0.7, "reports": 27},
            {"region": "Scottsdale","risk": 0.75,"reports": 15},
            {"region": "Flagstaff", "risk": 0.3, "reports": 8}
        ],
        "insight": "Phoenix and Mesa showing elevated risk this week.",
        "recommended_action": "Avoid crowded areas in high risk regions."
    }


@router.get("/api/region/{zip_code}")
async def get_region_risk(zip_code: str):
    """
    Takes a ZIP code and returns the region and its risk level.
    """
    region = get_region_from_zip(zip_code)

    # Mock risk per region
    region_risk = {
        "Phoenix":       0.8,
        "Tucson":        0.6,
        "Mesa":          0.7,
        "Scottsdale":    0.75,
        "Flagstaff":     0.3,
        "Other Arizona": 0.5
    }

    risk = region_risk.get(region, 0.5)
    category = "High" if risk >= 0.65 else "Moderate" if risk >= 0.35 else "Low"

    return {
        "zip_code": zip_code,
        "region": region,
        "risk": risk,
        "category": category
    }