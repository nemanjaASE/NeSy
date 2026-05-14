from pydantic import BaseModel, Field
from typing import List


class XAIReasoning(BaseModel):
    primary_analysis: str
    differential_comparison: str
    exclusion_criteria: str


class XAIExplanationResult(BaseModel):
    most_likely: str
    confidence: str
    differentials: List[str] = Field(default_factory=list)
    excluded_conditions: List[str] = Field(default_factory=list)
    reasoning: XAIReasoning
    recommendation: str

    @classmethod
    def fallback(cls, message: str) -> "XAIExplanationResult":
        return cls(
            most_likely="Unknown",
            confidence="low",
            differentials=[],
            excluded_conditions=[],
            reasoning=XAIReasoning(
                primary_analysis=message,
                differential_comparison="N/A",
                exclusion_criteria="N/A",
            ),
            recommendation="Consult a medical professional.",
        )
