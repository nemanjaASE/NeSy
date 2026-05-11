from typing import List
from app.domain import RawDiseaseMatch
from ..schemas import DiagnosisResult
from .disease_scorer import DiseaseScorer
from .disease_filter import DiseaseFilter
from .disease_ranker import DiseaseRanker

class ScoringEngine:
    """
    Domain service that orchestrates scoring, filtering and ranking of disease candidates.
    """

    def __init__(self, top_k: int = 5, top_excluded: int = 3):
        self.scorer = DiseaseScorer()
        self.filter = DiseaseFilter()
        self.ranker = DiseaseRanker(top_k=top_k, top_excluded=top_excluded)

    def evaluate(
        self,
        raw_records: List[RawDiseaseMatch],
        total_input_symptoms: int
    ) -> DiagnosisResult:
        scored             = self.scorer.score_all(raw_records, total_input_symptoms)
        included, excluded = self.filter.split(scored, raw_records)
        return self.ranker.rank(included, excluded)