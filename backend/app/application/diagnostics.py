from typing import List
from app.domain import NLPExtractor, SemanticMatcher, TextEmbedder, ScoringEngine
from app.infrastructure import Neo4jRepository, OllamaExplainer
from app.core import logger
from app.domain import DiagnosticResponseDTO, XAIExplanationResult

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
            present, absent = await self.nlp_extractor.extract_entities(text)
            if not present and not absent:
                logger.warning("No symptoms extracted from text.")
                return self._empty_response(text)
        
            logger.info(f"Extracted {len(present)} present symptoms: {present}")
            logger.info(f"Extracted {len(absent)} absent symptoms: {absent}")
            
            # Step 2: Semantic matching to ontology
            # Step 2.1: Generate embeddings and perform semantic matching
            present_query_embeddings = await self.embedder.generate_embeddings(present)
            logger.info(f"Generated embeddings for present symptoms.")

            absent_query_embeddings = await self.embedder.generate_embeddings(absent)
            logger.info(f"Generated embeddings for absent symptoms.")

            # Step 2.2: Find best matches in the ontology
            matches = self.semantic_matcher.find_best_matches(
                present_query_embeddings=present_query_embeddings,
                absent_query_embeddings=absent_query_embeddings,
                onto_labels=onto_labels,
                onto_vectors=onto_vectors,
                present_terms=present,
                absent_terms=absent
            )

            present_symptoms = [m.mapped_symptom for m in matches if m.is_match and m.kind == "present"]
            absent_symptoms = [m.mapped_symptom for m in matches if m.is_match and m.kind == "absent"]
            if not present_symptoms:
                return self._empty_response(text)
        
            logger.info(f"Pipeline finished. Found {len(present_symptoms)} valid ontological matches.")
            logger.info(f"Mapped symptoms: {present_symptoms}")

            # Step 3: Query Neo4j for disease inference and calculate scores
            if len(present_symptoms) < 1:
                logger.warning(f"Only {len(present_symptoms)} symptoms mapped. Inference might be skipped.")

            # Step 3.1: Query Neo4j for candidate diseases based on mapped symptoms
            raw_records = await self.repository.infer_diseases(
                present_symptoms=present_symptoms,
                absent_symptoms=absent_symptoms,
                min_match=2
            )
            
            logger.info(f"Inference query returned {len(raw_records)} candidate diseases from Neo4j.")

            # Step 3.2: Calculate disease scores and coverage
            diagnosis_result = self.scoring_engine.evaluate(
                raw_records=raw_records,
                total_input_symptoms=len(present_symptoms)
            )

            # Step 4: Generate XAI explanations for the inferred diseases
            explanation_result = await self.xai_explainer.generate_explanation(diagnosis_result)

            logger.info("XAI explanation generated.")

            return DiagnosticResponseDTO.from_domain(
                text=text,
                present_symptoms=present_symptoms,
                absent_symptoms=absent_symptoms,
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
            explanation=XAIExplanationResult.fallback("Došlo je do interne greške pri obradi podataka."),
        )