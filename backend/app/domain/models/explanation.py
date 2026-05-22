from pydantic import BaseModel, Field
from typing import List


class DifferentialComparison(BaseModel):
    disease: str
    reasoning: str


class ExclusionCriteria(BaseModel):
    excluded_disease: str
    reasoning: str


class XAIReasoning(BaseModel):
    primary_analysis: str
    differential_comparison: List[DifferentialComparison]
    exclusion_criteria: List[ExclusionCriteria]


class Recommendation(BaseModel):
    specialist_consultations: List[str] = Field(default_factory=list)
    lab_tests: List[str] = Field(default_factory=list)
    symptoms_to_verify: List[str] = Field(default_factory=list)


class XAIExplanationResult(BaseModel):
    most_likely: str
    confidence: str
    differentials: List[str] = Field(default_factory=list)
    excluded_conditions: List[str] = Field(default_factory=list)
    reasoning: XAIReasoning
    recommendation: Recommendation

    @classmethod
    def fallback(cls, message: str) -> "XAIExplanationResult":
        return cls(
            most_likely="Unknown",
            confidence="low",
            differentials=[],
            excluded_conditions=[],
            reasoning=XAIReasoning(
                primary_analysis=message,
                differential_comparison=[],
                exclusion_criteria=[],
            ),
            recommendation=Recommendation(),
        )
