from typing import List
from pydantic import BaseModel
from app.domain import XAIExplanationResult

class DiagnosticResponseDTO(BaseModel):
    input_text: str
    present_symptoms: List[str]
    absent_symptoms: List[str]
    explanation: XAIExplanationResult

    @classmethod
    def from_domain(cls, text: str, present_symptoms: List[str], absent_symptoms: List[str], xai: XAIExplanationResult):
        return cls(
            input_text=text,
            present_symptoms=present_symptoms,
            absent_symptoms=absent_symptoms,
            explanation=xai,
        )