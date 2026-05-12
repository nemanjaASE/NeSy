import asyncio
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
            extracted = await self.nlp_extractor.extract_symptoms(text)
            if not extracted.present and not extracted.absent:
                logger.warning("No symptoms extracted.")
                return self._empty_response(text)

            logger.debug(
                f"Extracted symptoms | "
                f"present={extracted.present} "
                f"absent={extracted.absent}"
            )

            # Step 2: Semantic matching to ontology
            # Step 2.1: Generate embeddings for present and absent symptoms in parallel
            present_query_embeddings, absent_query_embeddings = await asyncio.gather(
                self.embedder.generate_embeddings(extracted.present, prefix="query: "),
                self.embedder.generate_embeddings(extracted.absent,  prefix="query: ")
            )

            logger.debug(
                f"Generated embeddings | "
                f"present={len(present_query_embeddings)} "
                f"absent={len(absent_query_embeddings)}"
            )

            # Step 2.2: Find best matches in the ontology
            matches = self.semantic_matcher.find_best_matches(
                present_query_embeddings=present_query_embeddings,
                absent_query_embeddings=absent_query_embeddings,
                onto_labels=onto_labels,
                onto_vectors=onto_vectors,
                present_terms=extracted.present,
                absent_terms=extracted.absent
            )

            mapped = self.semantic_matcher.filter_matched_symptoms(matches) 

            logger.debug(
                f"Mapped symptoms | "
                f"present={mapped.present} "
                f"absent={mapped.absent}"
            )
            
            if not mapped.present:
                logger.warning("No ontology symptoms mapped")
                return self._empty_response(text)
            
            # Step 3: Query Neo4j for disease inference and calculate scores

            # Step 3.1: Query Neo4j for candidate diseases based on mapped symptoms
            raw_records = await self.repository.infer_diseases(
                present_symptoms=mapped.present,
                absent_symptoms=mapped.absent,
                min_match=settings.MIN_MATCH
            )
            
            logger.debug(
                f"Neo4j inference returned "
                f"{len(raw_records)} candidate diseases"
            )

            # Step 3.2: Calculate disease scores and coverage
            diagnosis_result = self.scoring_engine.evaluate(
                raw_records=raw_records,
                total_input_symptoms=len(mapped.present)
            )

            logger.debug("Disease scoring completed")
            
            # Step 4: Generate XAI explanations for the inferred diseases
            explanation_result = await self.xai_explainer.generate_explanation(diagnosis_result)

            logger.info("Diagnostic pipeline completed successfully")

            return DiagnosticResponseDTO.from_domain(
                text=text,
                present_symptoms=mapped.present,
                absent_symptoms=mapped.absent,
                xai=explanation_result
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