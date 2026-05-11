import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
from ..schemas import SemanticMatchResult

class SemanticMatcher:
    """
    Domain Service responsible for mapping symptoms using vector similarity.
    """

    def __init__(self, threshold: float = 0.90):
        self.threshold = threshold

    def find_best_matches(
        self, 
        present_query_embeddings: List[List[float]], 
        absent_query_embeddings: List[List[float]], 
        onto_labels: List[str], 
        onto_vectors: List[List[float]],
        present_terms: List[str],
        absent_terms: List[str]
    ) -> List[SemanticMatchResult]:
        """
        Calculates cosine similarity between query embeddings and ontology vectors to find the best matches.
        Args:
            present_query_embeddings: List of vector embeddings for the present symptoms.
            absent_query_embeddings: List of vector embeddings for the absent symptoms.
            onto_labels: List of symptom labels from the ontology.
            onto_vectors: List of vector embeddings for the ontology symptoms.
            present_terms: List of original symptom terms for the present symptoms.
            absent_terms: List of original symptom terms for the absent symptoms.
        Returns:
            A list of SemanticMatchResult objects containing the input symptom, mapped symptom, confidence score, and match status.
        """
        if not onto_vectors:
            return []

        o_vecs = np.array(onto_vectors)
        results = []

        for embeddings, terms, kind in [
            (present_query_embeddings, present_terms, "present"),
            (absent_query_embeddings,  absent_terms,  "absent"),
        ]:
            if not embeddings:
                continue

            q_vecs = np.array(embeddings)
            matrix = cosine_similarity(q_vecs, o_vecs)

            for i, term in enumerate(terms):
                best_idx   = int(np.argmax(matrix[i]))
                confidence = float(matrix[i][best_idx])

                results.append(SemanticMatchResult(
                    input_symptom=term,
                    mapped_symptom=onto_labels[best_idx],
                    confidence=confidence,
                    kind=kind,
                    is_match=confidence >= self.threshold
                ))

        return results