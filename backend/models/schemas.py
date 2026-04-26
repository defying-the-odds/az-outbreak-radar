# backend/models/schemas.py

from pydantic import BaseModel
from typing import List, Optional

class SymptomInput(BaseModel):
    # Original symptoms
    fever: int
    cough: int
    travel: int
    animal_exposure: int
    mosquito_index: float
    location: str

    # New symptoms from UI
    shortness_of_breath: int = 0
    fatigue: int = 0
    vomiting_diarrhea: int = 0
    rash: int = 0
    body_aches: int = 0

    # New context fields
    age_range: Optional[str] = None
    mosquito_bite: int = 0

    # Pre existing conditions
    diabetes: int = 0
    asthma: int = 0
    immunocompromised: int = 0

    # New location fields
    arizona_zip: Optional[str] = None
    travel_destination: Optional[str] = None

class RiskOutput(BaseModel):
    score: float
    category: str
    drivers: List[str]
    explanation: str
    region: Optional[str] = None