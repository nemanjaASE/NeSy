from typing import List
from app.domain import RawDiseaseMatch
from ..schemas import InferenceResult, DiseaseInference
from app.core import logger

class DiseaseScorer:
    """
    Domain service for calculating disease probabilities and coverage scores.
    """
    def __init__(self, top_k: int = 5):
        self.top_k = top_k

    def calculate_scores(
        self, 
        raw_records: List[RawDiseaseMatch], 
        total_input_symptoms: int
    ) -> InferenceResult:
        """
        Calculates disease coverage and input coverage based on Neo4j raw data.
        """
        if total_input_symptoms == 0 or not raw_records:
            logger.warning("No symptoms or records to score.")
            return InferenceResult(total_input_symptoms=total_input_symptoms, diseases=[])

        scored_diseases = []

        for rec in raw_records:
            match_count = rec.match_count
            total_symptom_count = rec.total_symptom_count if rec.total_symptom_count > 0 else 1
            
            disease_cov = round(match_count / total_symptom_count * 100, 1)
            input_cov = round(match_count / total_input_symptoms * 100, 1)

            scored_disease = DiseaseInference(
                disease_name=rec.disease,
                uri=rec.uri,
                normalized_score=round(rec.normalized_score, 2),
                match_count=match_count,
                disease_coverage_pct=disease_cov,
                input_coverage_pct=input_cov,
                matched_symptoms=rec.matched_symptoms,
                missing_symptoms=rec.missing_symptoms
            )
            scored_diseases.append(scored_disease)

        scored_diseases.sort(key=lambda x: x.normalized_score, reverse=True)
        top_diseases = scored_diseases[:self.top_k]

        logger.info(f"Scoring completed. Top candidate: {top_diseases[0].disease_name if top_diseases else 'None'}")

        return InferenceResult(
            total_input_symptoms=total_input_symptoms,
            diseases=top_diseases
        )