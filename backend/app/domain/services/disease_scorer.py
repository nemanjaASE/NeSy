from typing import List, Dict, Any

from ..DTOs.DiseaseInferenceDTO import DiseaseInferenceDTO
from ..schemas.diagnostics import DiseaseScore, InferenceResult
from app.core import logger

class DiseaseScorer:
    """
    Domain service for calculating disease probabilities and coverage scores.
    """
    def __init__(self, top_k: int = 5):
        self.top_k = top_k

    def calculate_scores(
        self, 
        raw_records: List[Dict[str, Any]], 
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
            match_count = rec.get('match_count', 0)
            total_symptom_count = rec.get('total_symptom_count', 1) 
            
            disease_cov = round(match_count / total_symptom_count * 100, 1)
            input_cov = round(match_count / total_input_symptoms * 100, 1)

            scored_disease = DiseaseInferenceDTO(
                disease_name=rec.get('disease', 'Unknown'),
                uri=rec.get('uri', ''),
                normalized_score=round(rec.get('normalized_score', 0.0), 2),
                match_count=match_count,
                disease_coverage_pct=disease_cov,
                input_coverage_pct=input_cov,
                matched_symptoms=rec.get('matched_symptoms', []),
                missing_symptoms=rec.get('missing_symptoms', [])
            )
            scored_diseases.append(scored_disease)

        scored_diseases.sort(key=lambda x: x.normalized_score, reverse=True)
        top_diseases = scored_diseases[:self.top_k]

        logger.info(f"Calculated scores for {len(top_diseases)} top diseases.")

        return InferenceResult(
            total_input_symptoms=total_input_symptoms,
            diseases=top_diseases
        )