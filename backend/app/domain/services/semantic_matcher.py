import numpy as np
import logging
from typing import Literal, cast
from sklearn.metrics.pairwise import cosine_similarity
from ..models.symptom import SemanticMatchResult, EmbeddingMatrix, ExtractedSymptoms
from ..models.result import Result

logger = logging.getLogger(__name__)


class SemanticMatcher:
    """
    Domain Service responsible for mapping symptoms using vector similarity.
    """

    def __init__(self, threshold: float = 0.90):
        """
        Args:
            threshold: Minimum cosine similarity score required to consider
                       a match valid. Defaults to 0.90.
        """
        self.threshold = threshold

    def find_best_matches(
        self,
        present_query_embeddings: EmbeddingMatrix,
        absent_query_embeddings: EmbeddingMatrix,
        onto_labels: list[str],
        onto_vectors: EmbeddingMatrix,
        present_terms: list[str],
        absent_terms: list[str],
    ) -> Result[list[SemanticMatchResult]]:
        """
        Map each patient-reported symptom to its closest ontological term
        using cosine similarity between their vector embeddings.

        Processes present and absent symptoms separately to preserve
        their clinical role in the diagnostic pipeline.

        Args:
            present_query_embeddings: Embeddings for symptoms the patient reports having.
            absent_query_embeddings:  Embeddings for symptoms the patient explicitly denies.
            onto_labels:   Symptom labels from the ontology knowledge graph.
            onto_vectors:  Embeddings for the ontology symptom labels.
            present_terms: Original present symptom terms from NLP extraction.
            absent_terms:  Original absent symptom terms from NLP extraction.

        Returns:
            Result[list[SemanticMatchResult]]: Success with one result per symptom,
            or failure if ontology vectors are missing.
        """
        if not onto_vectors:
            logger.error(
                "Ontology vectors are empty — cannot perform semantic matching."
            )
            return Result.failure("Ontology vectors are empty.")

        try:
            o_vecs = np.array(onto_vectors)
            results = []

            for embeddings, terms, kind in [
                (present_query_embeddings, present_terms, cast(Literal["present", "absent"], "present")),
                (absent_query_embeddings,  absent_terms,  cast(Literal["present", "absent"], "absent")),
            ]:
                if not embeddings:
                    continue

                q_vecs = np.array(embeddings)
                matrix = cosine_similarity(q_vecs, o_vecs)

                for i, term in enumerate(terms):
                    best_idx = int(np.argmax(matrix[i]))
                    confidence = float(matrix[i][best_idx])

                    results.append(
                        SemanticMatchResult(
                            input_symptom=term,
                            mapped_symptom=onto_labels[best_idx],
                            confidence=confidence,
                            kind=kind,
                            is_match=confidence >= self.threshold,
                        )
                    )

            logger.info(f"Semantic matching complete. Matched {len(results)} symptoms.")
            return Result.success(results)

        except Exception as e:
            logger.error(f"Semantic matching failed: {str(e)}", exc_info=True)
            return Result.failure(f"Semantic matching failed: {str(e)}")

    def filter_matched_symptoms(
        self, matches: list[SemanticMatchResult]
    ) -> ExtractedSymptoms:
        """
        Filter semantic match results by confidence threshold and clinical role.

        Extracts only the ontological terms that meet the similarity threshold,
        separated into present and absent symptom lists for use in the
        downstream inference query.

        Args:
            matches: List of semantic match results from find_best_matches.

        Returns:
            ExtractedSymptoms: Filtered present and absent ontological symptom terms.
        """
        present = [
            m.mapped_symptom for m in matches if m.is_match and m.kind == "present"
        ]
        absent = [
            m.mapped_symptom for m in matches if m.is_match and m.kind == "absent"
        ]

        logger.debug(f"Filtered matches | present={len(present)}, absent={len(absent)}")
        return ExtractedSymptoms(present=present, absent=absent)
