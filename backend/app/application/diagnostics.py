from typing import List, Dict, Any
from app.domain import NLPExtractor, SemanticMatcher, TextEmbedder, DiseaseScorer
from app.core import logger
from app.infrastructure import Neo4jRepository

class DiagnosticCoordinator:
    """
    Coordinator responsible for the neuro-symbolic diagnostic workflow.
    """

    def __init__(
            self,
            nlp_extractor: NLPExtractor,
            embedder: TextEmbedder,
            matcher: SemanticMatcher,
            scorer: DiseaseScorer,
            repository: Neo4jRepository
        ):
        self.nlp_extractor = nlp_extractor
        self.embedder = embedder
        self.semantic_matcher = matcher
        self.scorer = scorer
        self.repository = repository

    async def run_full_diagnostic_pipeline(
            self,
            text: str,
            onto_labels: List[str],
            onto_vectors: List[List[float]]
        ) -> Dict[str, Any]:
        """
        Runs the full neuro-symbolic diagnostic pipeline.
        """
        logger.info("Starting neuro-symbolic extraction and mapping pipeline.")

        extracted_terms = await self.nlp_extractor.extract_entities(text)
        
        if not extracted_terms:
            logger.warning("No symptoms extracted from text.")
            return self._empty_response(text)

        logger.info(f"Extracted {len(extracted_terms)} symptoms: {extracted_terms}")

        logger.info("Generating embeddings for extracted symptoms.")

        query_embeddings = await self.embedder.generate_embeddings(extracted_terms)

        logger.info("Finding best matches against ontology.")

        matches = self.semantic_matcher.find_best_matches(
            query_embeddings=query_embeddings,
            onto_labels=onto_labels,
            onto_vectors=onto_vectors,
            original_terms=extracted_terms
        )

        mapped_symptoms = [m["mapped_symptom"] for m in matches if m["is_match"]]

        if not mapped_symptoms:
            return self._empty_response(text, raw_matches=matches)

        logger.info(f"Pipeline finished. Found {len(mapped_symptoms)} valid ontological matches.")

        if len(mapped_symptoms) < 1:
            logger.warning(f"Only {len(mapped_symptoms)} symptoms mapped. Inference might be skipped.")

        raw_diseases = await self.repository.infer_diseases(
            mapped_symptoms=mapped_symptoms,
            min_match=1
        )

        inference_result = self.scorer.calculate_scores(
            raw_records=raw_diseases,
            total_input_symptoms=len(mapped_symptoms)
        )

        return {
            "input_text": text,
            "raw_matches": matches,
            "mapped_symptoms": mapped_symptoms,
            "inference": inference_result.model_dump(),
            "debug_details": matches
        }

    def _empty_response(self, text: str, raw_matches=None):
        """Helper method to return an empty response structure when no symptoms are extracted."""
        return {
            "input_text": text,
            "raw_matches": raw_matches or [],
            "mapped_symptoms": [],
            "inference": {"total_input_symptoms": 0, "diseases": []}
        }