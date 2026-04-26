# backend/models/schemas.py

from pydantic import BaseModel
from typing import List

class SymptomInput(BaseModel):
    fever: int
    cough: int
    travel: int
    animal_exposure: int
    mosquito_index: float
    location: str

class RiskOutput(BaseModel):
    score: float
    category: str
    drivers: List[str]
    explanation: str