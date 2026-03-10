from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from ..DTOs.DiseaseInferenceDTO import DiseaseInferenceDTO

class DiagnosticRequest(BaseModel):
    """
    The initial input from the user/patient.
    """
    text: str = Field(..., example="Već par dana kašljem i imam baš visoku temperaturu.")

class SemanticMatchDetail(BaseModel):
    """
    Details about each symptom match, including the original input, the mapped ontology term, confidence score, and whether it was considered a match based on the threshold.
    """
    input_symptom: str
    mapped_symptom: str
    confidence: float
    is_match: bool

class DiseaseScore(BaseModel):
    """Represents the scoring and coverage details for a potential disease diagnosis based on the matched symptoms."""
    disease_name: str
    uri: str
    normalized_score: float
    match_count: int
    disease_coverage_pct: float  # D.COV
    input_coverage_pct: float    # I.COV
    matched_symptoms: List[str]
    missing_symptoms: List[str]

class InferenceResult(BaseModel):
    """Represents the final inference results including all potential disease diagnoses."""
    total_input_symptoms: int
    diseases: List[DiseaseInferenceDTO]

class DiagnosticResult(BaseModel):
    """
    The final output of the diagnostic pipeline, including the original input text, the extracted entities, the ontological matches, and detailed information about each match.
    """
    input_text: str
    extracted_entities: List[str]
    ontological_matches: List[str]
    detailed_results: List[SemanticMatchDetail]
    inference: InferenceResult
    explanation: Optional[Dict[str, Any]]