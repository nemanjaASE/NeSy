from pydantic import BaseModel
from typing import List


class RawDiseaseMatch(BaseModel):
    disease: str
    uri: str
    passed_filter: bool
    blocking_symptoms: List[str]
    matched_symptoms: List[str]
    missing_symptoms: List[str]
    match_count: int
    total_symptom_count: int
    total_score: float
    normalized_score: float


class DiseaseInference(BaseModel):
    disease_name: str
    uri: str
    normalized_score: float
    match_count: int
    disease_coverage_pct: float
    input_coverage_pct: float
    matched_symptoms: List[str]
    missing_symptoms: List[str]
    blocking_symptoms: List[str] = []


class DiagnosisResult(BaseModel):
    included: List[DiseaseInference]
    excluded: List[DiseaseInference]
