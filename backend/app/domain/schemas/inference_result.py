from pydantic import BaseModel
from typing import List
from .disease_inference import DiseaseInference

class InferenceResult(BaseModel):
    """Represents the final inference results including all potential disease diagnoses."""
    total_input_symptoms: int
    diseases: List[DiseaseInference]