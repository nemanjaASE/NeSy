from pydantic import BaseModel, Field
from typing import List

class XAIExplanationResult(BaseModel):
    most_likely: str = Field(..., description="Most commont disease")
    confidence: str = Field(..., description="Confidence level of the diagnosis (e.g., visoka, srednja, niska)")
    differentials: List[str] = Field(default_factory=list)
    reasoning: str
    recommendation: str

    @classmethod
    def fallback(cls, message: str):
        return cls(
            most_likely="Unknown",
            confidence="low",
            differentials=[],
            reasoning=message,
            recommendation="Consult a medical professional."
        )