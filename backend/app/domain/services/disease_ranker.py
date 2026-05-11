from typing import List
from app.domain import DiseaseInference
from ..schemas.diagnosis_result import DiagnosisResult

class DiseaseRanker:
    def __init__(self, top_k: int = 5, top_excluded: int = 3):
        self.top_k = top_k
        self.top_excluded = top_excluded

    def rank(
        self,
        included: List[DiseaseInference],
        excluded: List[DiseaseInference]
    ) -> DiagnosisResult:
        return DiagnosisResult(
            included=sorted(included, key=lambda x: x.normalized_score, reverse=True)[:self.top_k],
            excluded=sorted(excluded, key=lambda x: x.normalized_score, reverse=True)[:self.top_excluded],
        )