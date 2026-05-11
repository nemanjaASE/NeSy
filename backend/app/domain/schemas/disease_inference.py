from pydantic import BaseModel
from typing import List

class DiseaseInference(BaseModel):
    disease_name:         str
    uri:                  str
    normalized_score:     float
    match_count:          int
    disease_coverage_pct: float
    input_coverage_pct:   float
    matched_symptoms:     List[str]
    missing_symptoms:     List[str]
    blocking_symptoms:    List[str] = []