# backend/routes/risk.py

from fastapi import APIRouter
from backend.models.schemas import SymptomInput, RiskOutput
from ml.risk_engine import get_risk_score

router = APIRouter()

@router.post("/api/risk", response_model=RiskOutput)
async def calculate_risk(input: SymptomInput):
    
    # Convert input to dict and pass to ML
    input_data = {
        "fever": input.fever,
        "cough": input.cough,
        "travel": input.travel,
        "animal_exposure": input.animal_exposure,
        "mosquito_index": input.mosquito_index
    }

    # Call Person 1's ML function
    result = get_risk_score(input_data)

    return result