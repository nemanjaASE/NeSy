from typing import List, Dict, Any
from app.domain.interfaces import NLPExtractor
from app.domain.services import SemanticMatcher
from app.domain.interfaces.ml import TextEmbedder
from app.core import logger

class DiagnosticCoordinator:
    """
    Coordinator responsible for the neuro-symbolic diagnostic workflow.
    """

    def __init__(
            self,
            nlp_extractor: NLPExtractor,
            embedder: TextEmbedder,
            matcher: SemanticMatcher
        ):
        self.nlp_extractor = nlp_extractor
        self.embedder = embedder
        self.semantic_matcher = matcher

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
            return {"raw_matches": [], "final_symptoms": []}

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

        final_symptoms = [m["mapped_symptom"] for m in matches if m["is_match"]]

        logger.info(f"Pipeline finished. Found {len(final_symptoms)} valid ontological matches.")

        return {
            "raw_matches": matches,
            "final_symptoms": final_symptoms
        }