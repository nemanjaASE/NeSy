from typing import List
from ..models.disease import RawDiseaseMatch, DiseaseInference


class DiseaseScorer:
    def score(
        self, rec: RawDiseaseMatch, total_input_symptoms: int
    ) -> DiseaseInference:
        total = rec.total_symptom_count if rec.total_symptom_count > 0 else 1

        return DiseaseInference(
            disease_name=rec.disease,
            uri=rec.uri,
            normalized_score=round(rec.normalized_score, 2),
            match_count=rec.match_count,
            total_symptoms=rec.total_symptom_count,
            disease_coverage_pct=round(rec.match_count / total * 100, 1),
            input_coverage_pct=round(rec.match_count / total_input_symptoms * 100, 1),
            matched_symptoms=rec.matched_symptoms,
            missing_symptoms=rec.missing_symptoms,
            blocking_symptoms=rec.blocking_symptoms if not rec.passed_filter else [],
        )

    def score_all(
        self, raw_records: List[RawDiseaseMatch], total_input_symptoms: int
    ) -> List[DiseaseInference]:
        if not raw_records or total_input_symptoms == 0:
            return []

        return [self.score(rec, total_input_symptoms) for rec in raw_records]
