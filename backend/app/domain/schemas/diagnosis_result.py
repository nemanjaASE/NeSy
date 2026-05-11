from pydantic import BaseModel
from typing import List
from .disease_inference import DiseaseInference

class DiagnosisResult(BaseModel):
    included: List[DiseaseInference]
    excluded: List[DiseaseInference]