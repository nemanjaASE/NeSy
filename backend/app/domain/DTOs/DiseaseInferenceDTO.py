from pydantic import BaseModel, Field
from typing import List, Union

class DiseaseInferenceDTO(BaseModel):
    """
    Data Transfer Object for disease inference results.
    """
    disease_name: str
    uri: str
    normalized_score: float
    match_count: int
    disease_coverage_pct: Union[float, str]
    input_coverage_pct: Union[float, str]
    matched_symptoms: List[str]
    missing_symptoms: List[str] = Field(default_factory=list)