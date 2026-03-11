from pydantic import BaseModel, Field
from typing import List

class RawDiseaseMatch(BaseModel):
    disease: str = Field(..., alias="disease")
    uri: str
    matched_symptoms: List[str]
    missing_symptoms: List[str]
    match_count: int
    total_symptom_count: int
    total_score: float
    normalized_score: float