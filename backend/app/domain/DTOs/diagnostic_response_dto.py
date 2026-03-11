from typing import List
from pydantic import BaseModel
from app.domain import XAIExplanationResult

class DiagnosticResponseDTO(BaseModel):
    input_text: str
    top_disease: str
    confidence: str
    mapped_symptoms: List[str]
    missing_symptoms: List[str]
    explanation_text: str
    recommendation: str
    other_potential_diseases: List[str]

    @classmethod
    def from_domain(cls, text: str, symptoms: List[str], missing_symptoms: List[str], xai: XAIExplanationResult):
        return cls(
            input_text=text,
            top_disease=xai.most_likely,
            confidence=xai.confidence,
            missing_symptoms=missing_symptoms,
            explanation_text=xai.reasoning,
            recommendation=xai.recommendation,
            mapped_symptoms=symptoms,
            other_potential_diseases=xai.differentials
        )