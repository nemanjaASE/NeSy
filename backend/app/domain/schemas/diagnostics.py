from pydantic import BaseModel, Field
from typing import List

class DiagnosticRequest(BaseModel):
    """
    The initial input from the user/patient.
    """
    text: str = Field(..., example="I have a sharp pain in my lower back.")

class SemanticMatchDetail(BaseModel):
    """
    Details about each symptom match, including the original input, the mapped ontology term, confidence score, and whether it was considered a match based on the threshold.
    """
    input_symptom: str
    mapped_symptom: str
    confidence: float
    is_match: bool

class DiagnosticResult(BaseModel):
    """
    The final output of the diagnostic pipeline, including the original input text, the extracted entities, the ontological matches, and detailed information about each match.
    """
    input_text: str
    extracted_entities: List[str]
    ontological_matches: List[str]
    detailed_results: List[SemanticMatchDetail]