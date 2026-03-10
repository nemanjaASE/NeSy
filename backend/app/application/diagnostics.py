from typing import List, Dict, Any
from app.domain import NLPExtractor, SemanticMatcher, TextEmbedder, DiseaseScorer
from app.infrastructure import Neo4jRepository, XAIExplainer
from app.core import logger

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
            repository: Neo4jRepository,
            xai_explainer: XAIExplainer
        ):
        self.nlp_extractor = nlp_extractor
        self.embedder = embedder
        self.semantic_matcher = matcher
        self.scorer = scorer
        self.repository = repository
        self.xai_explainer = xai_explainer

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

        # Step 1: Extract symptoms from text
        extracted_terms = await self.nlp_extractor.extract_entities(text)
        if not extracted_terms:
            logger.warning("No symptoms extracted from text.")
            return self._empty_response(text)
        
        logger.info(f"Extracted {len(extracted_terms)} symptoms: {extracted_terms}")

        # Step 2: Semantic matching to ontology
        # Step 2.1: Generate embeddings and perform semantic matching
        query_embeddings = await self.embedder.generate_embeddings(extracted_terms)

        logger.info("Generated embeddings for extracted symptoms.")

        # Step 2.2: Find best matches in the ontology
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

        # Step 3: Query Neo4j for disease inference and calculate scores
        if len(mapped_symptoms) < 1:
            logger.warning(f"Only {len(mapped_symptoms)} symptoms mapped. Inference might be skipped.")

        # Step 3.1: Query Neo4j for candidate diseases based on mapped symptoms
        raw_diseases = await self.repository.infer_diseases(
            mapped_symptoms=mapped_symptoms,
            min_match=1
        )

        logger.info(f"Inference query returned {len(raw_diseases)} candidate diseases from Neo4j.")

        # Step 3.2: Calculate disease scores and coverage
        inference_result = self.scorer.calculate_scores(
            raw_records=raw_diseases,
            total_input_symptoms=len(mapped_symptoms)
        )

        logger.info(f"Scoring completed. Top disease: {inference_result.diseases[0].disease_name if inference_result.diseases else 'None'} with score {inference_result.diseases[0].normalized_score if inference_result.diseases else 'N/A'}.")
        
        # Step 4: Generate XAI explanations for the inferred diseases
        diseases_for_xai = inference_result.model_dump().get("diseases", [])
        explanation_result = await self.xai_explainer.generate_explanation(diseases_for_xai)

        logger.info("XAI explanation generated.")

        return {
            "input_text": text,
            "raw_matches": matches,
            "mapped_symptoms": mapped_symptoms,
            "inference": inference_result.model_dump(),
            "explanation": explanation_result,
            "debug_details": matches
        }

    def _empty_response(self, text: str, raw_matches=None):
        """Helper method to return an empty response structure when no symptoms are extracted."""
        return {
            "input_text": text,
            "raw_matches": raw_matches or [],
            "mapped_symptoms": [],
            "inference": {"total_input_symptoms": 0, "diseases": []},
            "explanation": {[]}
        }