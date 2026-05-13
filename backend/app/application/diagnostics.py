import logging
from typing import List
from app.domain import NLPExtractor, SemanticMatcher, TextEmbedder, ScoringEngine, DiagnosticResponseDTO, XAIExplanationResult
from app.infrastructure import Neo4jRepository, OllamaExplainer
from app.core import settings

logger = logging.getLogger(__name__)

class DiagnosticCoordinator:
    """
    Coordinator responsible for the neuro-symbolic diagnostic workflow.
    """

    def __init__(
            self,
            nlp_extractor: NLPExtractor,
            embedder: TextEmbedder,
            matcher: SemanticMatcher,
            scoring_engine: ScoringEngine,
            repository: Neo4jRepository,
            xai_explainer: OllamaExplainer
        ):
        self.nlp_extractor = nlp_extractor
        self.embedder = embedder
        self.semantic_matcher = matcher
        self.scoring_engine = scoring_engine
        self.repository = repository
        self.xai_explainer = xai_explainer

    async def run_full_diagnostic_pipeline(
            self,
            text: str,
            onto_labels: List[str],
            onto_vectors: List[List[float]]
        ) -> DiagnosticResponseDTO:
        """
        Runs the full neuro-symbolic diagnostic pipeline.
        """
        logger.info("Starting neuro-symbolic extraction and mapping pipeline.")

        try:
            # Step 1: Extract symptoms from text
            extraction_result = await self.nlp_extractor.extract_symptoms(text)
            
            if extraction_result.is_failure:
                logger.error(f"Symptom extraction failed: {extraction_result.error}")
                return self._empty_response(text)
            
            extracted = extraction_result.value

            if not extracted.present and not extracted.absent:
                logger.warning("No symptoms extracted from input.")
                return self._empty_response(text)

            logger.debug(
                f"Extracted symptoms | "
                f"present={extracted.present} "
                f"absent={extracted.absent}"
            )

            # Step 2: Semantic matching to ontology
            # Step 2.1: Generate embeddings for all symptoms in a single call
            embeddings_result = await self.embedder.generate_embeddings_split(
                present_terms=extracted.present,
                absent_terms=extracted.absent,
                prefix=""
            )

            if embeddings_result.is_failure:
                logger.error(f"Failed to generate embeddings: {embeddings_result.error}")
                return self._empty_response(text)

            present_query_embeddings, absent_query_embeddings = embeddings_result.value

            logger.debug(
                f"Generated embeddings | "
                f"present={len(present_query_embeddings)} "
                f"absent={len(absent_query_embeddings)}"
            )

            # Step 2.2: Find best matches in the ontology
            matching_result = self.semantic_matcher.find_best_matches(
                present_query_embeddings=present_query_embeddings,
                absent_query_embeddings=absent_query_embeddings,
                onto_labels=onto_labels,
                onto_vectors=onto_vectors,
                present_terms=extracted.present,
                absent_terms=extracted.absent
            )

            if matching_result.is_failure:
                logger.error(f"Semantic matching failed: {matching_result.error}")
                return self._empty_response(text)

            mapped = self.semantic_matcher.filter_matched_symptoms(matching_result.value)

            logger.debug(
                f"Mapped symptoms | "
                f"present={mapped.present} "
                f"absent={mapped.absent}"
            )

            if not mapped.present:
                logger.warning("No ontology symptoms mapped above confidence threshold.")
                return self._empty_response(text)
            
            # Step 3: Query Neo4j for disease inference and calculate scores

            # Step 3.1: Query Neo4j for candidate diseases based on mapped symptoms
            inference_result = await self.repository.infer_diseases(
                present_symptoms=mapped.present,
                absent_symptoms=mapped.absent,
                min_match=settings.MIN_MATCH
            )
            
            if inference_result.is_failure:
                logger.error(f"Disease inference failed: {inference_result.error}")
                return self._empty_response(text)
            
            raw_records = inference_result.value

            if not raw_records:
                logger.warning("No disease candidates returned from inference query.")
                return self._empty_response(text)

            logger.debug(f"Neo4j inference returned {len(raw_records)} candidate diseases.")

            # Step 3.2: Calculate disease scores and coverage
            scoring_result = self.scoring_engine.evaluate(
                raw_records=raw_records,
                total_input_symptoms=len(mapped.present)
            )

            if scoring_result.is_failure:
                logger.error(f"Disease scoring failed: {scoring_result.error}")
                return self._empty_response(text)

            diagnosis_result = scoring_result.value

            logger.info(
                f"Scoring complete | "
                f"included={len(diagnosis_result.included)}, "
                f"excluded={len(diagnosis_result.excluded)}"
            )
            
            # Step 4: Generate XAI explanations for the inferred diseases
            explanation_result = await self.xai_explainer.generate_explanation(diagnosis_result)

            if explanation_result.is_failure:
                logger.warning(f"XAI explanation failed: {explanation_result.error}. Returning fallback.")
                explanation = XAIExplanationResult.fallback("Explanation could not be generated.")
            else:
                explanation = explanation_result.value

            logger.info("Diagnostic pipeline completed successfully.")

            return DiagnosticResponseDTO.from_domain(
                text=text,
                present_symptoms=mapped.present,
                absent_symptoms=mapped.absent,
                xai=explanation
            )
        except Exception as e:
            logger.error(f"Critical pipeline failure: {str(e)}", exc_info=True)
            return self._error_response(text, "Došlo je do interne greške pri obradi podataka.")
    
    def _empty_response(self, text: str) -> DiagnosticResponseDTO:
        """
        Helper method to return an empty/default response structure 
        when no symptoms are extracted or mapped.
        """
        logger.warning(f"Returning empty diagnostic response for text: '{text}'")
        
        return DiagnosticResponseDTO(
            input_text=text,
            present_symptoms=[],
            absent_symptoms=[],
            explanation=XAIExplanationResult.fallback("Nijedan simptom nije prepoznat u tekstu. Molimo unesite detaljniji opis simptoma."),
        )
    
    def _error_response(self, text: str, message: str) -> DiagnosticResponseDTO:
        """When an error occurs during processing, return a response with the error message."""
        return DiagnosticResponseDTO(
            input_text=text,
            present_symptoms=[],
            absent_symptoms=[],
            explanation=XAIExplanationResult.fallback(message),
        )