# backend/routes/risk.py

from fastapi import APIRouter
from backend.models.schemas import SymptomInput, RiskOutput
from backend.routes.community import get_region_from_zip
from ml.risk_engine import get_risk_score

router = APIRouter()

# High risk travel destinations based on CDC travel advisories
HIGH_RISK_DESTINATIONS = [
    "mexico", "india", "china", "brazil", "indonesia",
    "nigeria", "ethiopia", "congo", "pakistan", "bangladesh"
]

def get_travel_risk(destination: str) -> float:
    """
    Returns extra risk score based on travel destination.
    Based on CDC travel health advisories.
    """
    if not destination:
        return 0.0
    if destination.lower() in HIGH_RISK_DESTINATIONS:
        return 0.2
    return 0.1


@router.post("/api/risk", response_model=RiskOutput)
async def calculate_risk(input: SymptomInput):

    # Get extra travel risk based on destination
    travel_risk = get_travel_risk(input.travel_destination)

    # Get region from ZIP code
    region = get_region_from_zip(input.arizona_zip) if input.arizona_zip else "Unknown"

    # Convert all input fields to dict and pass to ML
    input_data = {
        # Original symptoms
        "fever": input.fever,
        "cough": input.cough,
        "travel": input.travel,
        "animal_exposure": input.animal_exposure,
        "mosquito_index": input.mosquito_index,
        "location": input.location,

        # New symptoms
        "shortness_of_breath": input.shortness_of_breath,
        "fatigue": input.fatigue,
        "vomiting_diarrhea": input.vomiting_diarrhea,
        "rash": input.rash,
        "body_aches": input.body_aches,
        "mosquito_bite": input.mosquito_bite,

        # Pre existing conditions
        "diabetes": input.diabetes,
        "asthma": input.asthma,
        "immunocompromised": input.immunocompromised,

        # Context
        "age_range": input.age_range,
        "travel_risk": travel_risk
    }

    # Call ML function
    result = get_risk_score(input_data)

    # Add region to result
    result["region"] = region

    return result